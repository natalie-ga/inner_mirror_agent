from src.config.config import load_config, validate_config
from src.api.openai_client import initialize_openai, generate_reflection
from src.api.youtube_client import initialize_youtube, detect_video_request, extract_tool_request
from src.utils.mood_analyzer import infer_mood
from src.utils.text_processing import format_tool_response
from src.data.journal_db import JournalDatabase
from src.ui.gradio_interface import JournalUI
import sys
import json

def main():
    """Main entry point for the Inner Mirror Agent."""
    print("🌿 Starting Inner Mirror Agent...")
    
    # Load configuration
    config = load_config()
    
    # Validate configuration
    missing_keys = validate_config(config)
    if missing_keys:
        print(f"❌ Error: Missing required environment variables: {', '.join(missing_keys)}")
        print("Please set these variables in your .env file and try again.")
        sys.exit(1)
    
    # Initialize components
    initialize_openai(config["openai_api_key"])
    youtube_tool = initialize_youtube(config["youtube_api_key"])
    journal_db = JournalDatabase(config["db_path"])
    
    # Define chat handler
    def chat(message, history):
        try:
            if len(history) == 0:
                intro_message = "Hello there!😊 I'm Mirror, here to reflect on your thoughts and provide insights."
                history.append({"role": "assistant", "content": intro_message})
                history.append({"role": "assistant", "content": "Can I ask how you'd like me to address you?"})
            
            # Analyze mood
            mood = infer_mood(message)
            
            # Check for video requests first
            tool_response = None
            wants_video = detect_video_request(message)
            
            if wants_video:
                # Extract tool request and call the appropriate tool
                tool_request = extract_tool_request(message)
                tool_name = tool_request.pop("tool")
                
                # Call the tool
                tool_result = youtube_tool.handle_tool_call(tool_name, **tool_request)
                
                # Format the tool response
                tool_response = format_tool_response(tool_result, tool_name)
                
                # For direct video requests, we might want to prioritize the video response
                if "video of" in message.lower() or "video about" in message.lower() or "video showing" in message.lower():
                    agent_response = tool_response
                    history.append({"role": "user", "content": message})
                    history.append({"role": "assistant", "content": agent_response})
                    journal_db.save_entry(message, mood)
                    return "", history
            
            # Handle greeting specially
            if mood == 'greeting':
                greeting_response = "Hello! It's nice to chat with you. How are you feeling today?"
                history.append({"role": "user", "content": message})
                history.append({"role": "assistant", "content": greeting_response})
                journal_db.save_entry(message, mood)
                return "", history
            
            # Generate reflection for non-greeting, non-direct video requests
            reflection_text = generate_reflection(message, mood)
            
            # Format response with tool output if available
            if tool_response:
                agent_response = f"{reflection_text}\n\n{tool_response}"
            else:
                # Check if the user might be stressed and needs help
                if mood in ['stress', 'negative', 'sadness'] and any(word in message.lower() for word in ['help', 'bad', 'sad', 'anxious', 'worried']):
                    # Get a mood-based video recommendation
                    tool_result = youtube_tool.handle_tool_call("get_mood_based_recommendation", mood=mood)
                    mood_tool_response = format_tool_response(tool_result, "get_mood_based_recommendation")
                    agent_response = f"{reflection_text}\n\n{mood_tool_response}"
                else:
                    agent_response = reflection_text
            
            # Save entry to database
            journal_db.save_entry(message, mood)
            
            # Update history
            history.append({"role": "user", "content": message})
            history.append({"role": "assistant", "content": agent_response})
            
            return "", history
            
        except Exception as e:
            error_msg = f"⚠️ Error: {str(e)}"
            history.append({"role": "user", "content": message})
            history.append({"role": "assistant", "content": error_msg})
            return "", history
    
    # Create and launch UI
    journal_ui = JournalUI(chat)
    demo = journal_ui.create_interface()
    demo.launch(share=True)

if __name__ == "__main__":
    main()