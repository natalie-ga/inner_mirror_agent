from src.config.config import load_config, validate_config
from src.config.logging_config import setup_logging
from src.config.prompts import (
    INTRO_MESSAGE, NAME_REQUEST, GREETING_RESPONSE,
    ERROR_MISSING_ENV, MAX_HISTORY_LENGTH
)
from src.api.openai_client import initialize_openai, generate_reflection
from src.api.youtube_client import initialize_youtube, detect_video_request, extract_tool_request
from src.utils.mood_analyzer import infer_mood
from src.utils.text_processing import format_tool_response
from src.data.journal_db import JournalDatabase
from src.ui.gradio_interface import JournalUI
import sys
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

def main():
    """Main entry point for the Inner Mirror Agent."""
    # Setup logging
    setup_logging()
    logger.info("🌿 Starting Inner Mirror Agent...")
    
    # Load configuration
    config = load_config()
    
    # Validate configuration
    missing_keys = validate_config(config)
    if missing_keys:
        error_msg = ERROR_MISSING_ENV.format(', '.join(missing_keys))
        logger.error(error_msg)
        print(error_msg)
        print("Please set these variables in your .env file and try again.")
        sys.exit(1)
    
    try:
        # Initialize components
        initialize_openai(config["openai_api_key"])
        youtube_tool = initialize_youtube(config["youtube_api_key"])
        journal_db = JournalDatabase(config["db_path"])
        
        # Define chat handler
        def chat(message: str, history: list) -> tuple[str, list]:
            try:
                if len(history) == 0:
                    history.append({"role": "assistant", "content": INTRO_MESSAGE})
                    history.append({"role": "assistant", "content": NAME_REQUEST})
                
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
                    if any(phrase in message.lower() for phrase in ["video of", "video about", "video showing"]):
                        agent_response = tool_response
                        history.append({"role": "user", "content": message})
                        history.append({"role": "assistant", "content": agent_response})
                        journal_db.save_entry(message, mood)
                        return "", history
                
                # Handle greeting specially
                if mood == 'greeting':
                    history.append({"role": "user", "content": message})
                    history.append({"role": "assistant", "content": GREETING_RESPONSE})
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
                logger.error(f"Chat error: {e}", exc_info=True)
                history.append({"role": "user", "content": message})
                history.append({"role": "assistant", "content": error_msg})
                return "", history
        
        # Create and launch UI
        journal_ui = JournalUI(chat)
        demo = journal_ui.create_interface()
        demo.launch(share=True)
        
    except Exception as e:
        logger.error(f"Application error: {e}", exc_info=True)
        sys.exit(1)

if __name__ == "__main__":
    main()