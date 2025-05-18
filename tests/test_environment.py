import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.config.config import load_config, validate_config
from src.api.youtube_client import initialize_youtube
import openai

def check_env_var(var_name, value):
    """Check if an environment variable is set."""
    if value:
        print(f"✅ {var_name} is set.")
    else:
        print(f"❌ {var_name} is MISSING!")

def test_openai_api(api_key):
    """Test the OpenAI API connection."""
    try:
        client = openai.OpenAI(api_key=api_key)
        models = client.models.list()
        if models.data:
            print(f"✅ OpenAI API call succeeded. Example model: {models.data[0].id}")
        else:
            print("❌ OpenAI API call returned no models.")
    except Exception as e:
        print(f"❌ OpenAI API call failed: {e}")

def test_youtube_api(api_key):
    """Test the YouTube API connection."""
    try:
        service = initialize_youtube(api_key)
        request = service.search().list(q="relaxing nature", part="snippet", maxResults=1)
        response = request.execute()
        print("✅ YouTube API call succeeded.")
    except Exception as e:
        print(f"❌ YouTube API call failed: {e}")

def main():
    """Run the environment test."""
    print("🔍 Running environment test for Inner Mirror Agent...\n")
    
    # Load configuration
    config = load_config()
    
    # Check environment variables
    check_env_var("OPENAI_API_KEY", config["openai_api_key"])
    check_env_var("YOUTUBE_API_KEY", config["youtube_api_key"])
    
    print("\n📡 Testing API connectivity...\n")
    
    # Test API connections
    test_openai_api(config["openai_api_key"])
    test_youtube_api(config["youtube_api_key"])

if __name__ == "__main__":
    main() 