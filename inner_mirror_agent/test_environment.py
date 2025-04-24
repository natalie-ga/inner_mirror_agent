# test_environment.py

import os
from dotenv import load_dotenv
from openai import OpenAI
from googleapiclient.discovery import build

# === Load environment variables ===
load_dotenv()

# === Initialize OpenAI Client ===
client = OpenAI()

def check_env_var(var_name):
    value = os.getenv(var_name)
    if value:
        print(f"✅ {var_name} is set.")
    else:
        print(f"❌ {var_name} is MISSING!")

def test_openai_api():
    try:
        models = client.models.list()
        if models.data:
            print(f"✅ OpenAI API call succeeded. Example model: {models.data[0].id}")
        else:
            print("❌ OpenAI API call returned no models.")
    except Exception as e:
        print(f"❌ OpenAI API call failed: {e}")

def test_youtube_api():
    try:
        service = build("youtube", "v3", developerKey=os.getenv("YOUTUBE_API_KEY"))
        request = service.search().list(q="relaxing nature", part="snippet", maxResults=1)
        response = request.execute()
        print("✅ YouTube API call succeeded.")
    except Exception as e:
        print(f"❌ YouTube API call failed: {e}")

if __name__ == "__main__":
    print("🔍 Running environment test for Inner Mirror Agent...\n")

    check_env_var("OPENAI_API_KEY")
    check_env_var("YOUTUBE_API_KEY")

    print("\n📡 Testing API connectivity...\n")

    test_openai_api()
    test_youtube_api()
