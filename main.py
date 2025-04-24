import os
from dotenv import load_dotenv
import openai
import sqlite3
import gradio as gr
from googleapiclient.discovery import build
from textblob import TextBlob
import re 

# === Load environment variables ===
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")
youtube_api_key = os.getenv("YOUTUBE_API_KEY")

# === Mood Inference Function ===
def infer_mood(user_entry):
    blob = TextBlob(user_entry)
    sentiment = blob.sentiment.polarity

    if sentiment > 0.2:
        return 'joy'
    elif sentiment < -0.2:
        return 'stress'
    else:
        return 'reflection'

# === OpenAI Function ===
def generate_reflection(user_entry, mood, previous_mood=None):
    system_prompt = {
        "role": "system",
        "content": """
        You are "Mirror," a thoughtful and empathetic conversational agent. Your purpose is to help the user reflect on their emotions, decisions, and experiences, like a friend or a psychologist. You should always approach each conversation with warmth, curiosity, and an open heart.
        
        Your main focus is to create a safe, reflective space for the user to express themselves. Ask open-ended, empathetic questions, reflect thoughtfully on their responses, and always remember previous conversations. Do not push for answers; let the user open up when they're ready.
        
        Avoid giving labels or categorizing the user's emotions. Your tone should be kind, non-judgmental, and supportive. Be patient, ask questions gently, and encourage the user to reflect on their feelings or experiences.
        """
    }

    user_message = {
        "role": "user",
        "content": f"Journal entry: {user_entry}\nMood: {mood}\nReflect on this entry thoughtfully and suggest a helpful insight."
    }

    response = openai.chat.completions.create(
        model="gpt-4",
        messages=[system_prompt, user_message]
    )

    return response.choices[0].message.content.strip()

# === YouTube API ===
def get_video_recommendation(specific_request=None):
    youtube = build('youtube', 'v3', developerKey=youtube_api_key)
    
    if specific_request:
        search_query = specific_request
    else:
        return None

    request = youtube.search().list(q=search_query, part='snippet', maxResults=1)
    response = request.execute()

    if response['items']:
        return f"https://www.youtube.com/watch?v={response['items'][0]['id']['videoId']}"
    else:
        return None

# === SQLite ===
def init_db():
    conn = sqlite3.connect('journal.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS entries (
            id INTEGER PRIMARY KEY,
            entry TEXT,
            mood TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_entry(entry, mood):
    conn = sqlite3.connect('journal.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO entries (entry, mood) VALUES (?, ?)', (entry, mood))
    conn.commit()
    conn.close()

# === Detecting Video Requests ===
def detect_video_request(message):
    video_keywords = r'\b(watch|look|see|show|gaze|glance|stare|peek|scan|view|notice|spot|glimpse|behold|catch)\b.*\b(video|play|film|clip|movie|watch)\b'
    if re.search(video_keywords, message, re.IGNORECASE):
        return True
    return False

# === Extracting Specific Video Requests ===
def extract_specific_video_request(message):
    return message.strip()

# === Chat logic ===
def chat(message, history):
    try:
        if len(history) == 0:
            intro_message = "Hello there!😊 I'm Mirror, here to reflect on your thoughts and provide insights."
            history.append({"role": "assistant", "content": intro_message})
            history.append({"role": "assistant", "content": "Can I ask how you'd like me to address you?"})
        
        mood = infer_mood(message)
        reflection = "How are you feeling today? Is there something on your mind that you'd like to share?"
        
        if history:
            last_entry = history[-1]["content"]
            reflection += f" Last time, we talked about {last_entry}. Has anything changed since then?"

        reflection_text = generate_reflection(message, mood)
        wants_video = detect_video_request(message)
        specific_request = extract_specific_video_request(message)
        
        if wants_video and specific_request:
            video_url = get_video_recommendation(specific_request)
            if video_url:
                agent_response = f"{reflection_text}\n\nIt seems like you'd like to watch something specific. Here's the video you requested: {video_url}"
            else:
                agent_response = f"{reflection_text}\n\nSorry, I couldn't find a video matching your request."
        else:
            agent_response = f"{reflection_text}"

        save_entry(message, mood)
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": agent_response})

        return "", history

    except Exception as e:
        error_msg = f"⚠️ Error: {str(e)}"
        history.append({"role": "user", "content": message})
        history.append({"role": "assistant", "content": error_msg})
        return "", history
    
# === Gradio UI ===
with gr.Blocks() as demo:
    gr.Markdown("### 🌿 Journaling Agent Chat")
    chatbot = gr.Chatbot(
        height=400, 
        type="messages", 
        value=[
            {"role": "assistant", "content": "Hello there! 😊 I'm Mirror, here to reflect on your thoughts and provide insights."}
        ]
    )
    msg = gr.Textbox(show_label=False, placeholder="Write your thoughts and press Enter…")
    send_button = gr.Button("Send")
    state = gr.State([])

    msg.submit(chat, [msg, state], [msg, chatbot])
    send_button.click(chat, [msg, state], [msg, chatbot])

if __name__ == "__main__":
    init_db()
    demo.launch(share=True)
