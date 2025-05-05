
# Inner Mirror Agent

**Inner Mirror** is a calm, reflective journaling agent designed to support emotional well-being through guided conversations. It helps users process thoughts, track moods, and gently reflect on their experiences — just like talking to a wise, empathetic friend.

---

## Features

- **Mood Analysis** – Understands your emotional tone using sentiment analysis.
- **Reflection Engine** – Generates thoughtful responses based on your mood and journal entry.
- **YouTube Integration** – Recommends relevant calming or motivational videos (only when requested).
- **Journal Memory** – Saves emotional insights and responses to a local SQLite database (journal.db).
- **Test Environment** – Includes a controlled testing setup for development and debugging.

---

## How to Run

1. **Clone this repository** and navigate into the agent directory:
   ```bash
   cd inner_mirror_agent
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your environment variables** in a `.env` file:
   ```
   OPENAI_API_KEY=your-openai-api-key
   YOUTUBE_API_KEY=your-youtube-api-key
   ```
   ***How to get your YouTube API Key***
   1. Go to the [Google Cloud Console – Credentials](https://console.cloud.google.com/apis/credentials)
   2. Make sure you’re in the project where you enabled the YouTube Data API v3
   3. Click on the "+ Create Credentials" button
   4. Select "API key"
   5. The key will be created immediately – copy it
   6. Add it to your .env file like this:
   ```
   YOUTUBE_API_KEY=AIzaSyB...your-key-here
   ```

5. **Launch the app**:
   ```bash
   python main.py
   ```

---

## 🛠 Tech Stack

- Python
- OpenAI API
- YouTube Data API
- Gradio (for future web UI)
- SQLite (for local journal database)
- TextBlob (for sentiment analysis)

---

## Future Improvements

- Add user authentication and encrypted journal storage
- Implement emotion trends visualization
- Integrate voice input/output (optional)
- Improve contextual memory over multiple sessions

---
