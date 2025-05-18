import os
from dotenv import load_dotenv
import pathlib

# Get the project root directory
PROJECT_ROOT = pathlib.Path(__file__).parent.parent.parent

# Load environment variables from .env file
def load_config():
    dotenv_path = PROJECT_ROOT / ".env"
    load_dotenv(dotenv_path=dotenv_path)
    
    config = {
        "openai_api_key": os.getenv("OPENAI_API_KEY"),
        "youtube_api_key": os.getenv("YOUTUBE_API_KEY"),
        "db_path": PROJECT_ROOT / "journal.db"
    }
    
    return config

# Validate that required environment variables are set
def validate_config(config):
    missing_keys = []
    
    if not config["openai_api_key"]:
        missing_keys.append("OPENAI_API_KEY")
    
    if not config["youtube_api_key"]:
        missing_keys.append("YOUTUBE_API_KEY")
    
    return missing_keys 