from googleapiclient.discovery import build
import re
import json

class YouTubeToolHandler:
    """A tool handler for YouTube video recommendations and searches."""
    
    def __init__(self, api_key):
        """Initialize the YouTube tool handler with the given API key."""
        self.youtube_client = build('youtube', 'v3', developerKey=api_key)
        self.tools = {
            "search_video": self.search_video,
            "get_trending_videos": self.get_trending_videos,
            "get_mood_based_recommendation": self.get_mood_based_recommendation
        }
    
    def handle_tool_call(self, tool_name, **kwargs):
        """Handle a tool call with the given name and arguments."""
        if tool_name in self.tools:
            return self.tools[tool_name](**kwargs)
        else:
            return {"error": f"Unknown tool: {tool_name}"}
    
    def search_video(self, query, max_results=1):
        """Search for videos matching the given query."""
        try:
            request = self.youtube_client.search().list(
                q=query,
                part="snippet",
                maxResults=max_results,
                type="video"
            )
            response = request.execute()
            
            results = []
            for item in response.get("items", []):
                video_id = item["id"]["videoId"]
                title = item["snippet"]["title"]
                url = f"https://www.youtube.com/watch?v={video_id}"
                results.append({
                    "title": title,
                    "url": url
                })
            
            return {
                "success": True,
                "results": results
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_trending_videos(self, category="music", max_results=3):
        """Get trending videos in the specified category."""
        try:
            request = self.youtube_client.videos().list(
                part="snippet",
                chart="mostPopular",
                videoCategoryId=self._get_category_id(category),
                maxResults=max_results
            )
            response = request.execute()
            
            results = []
            for item in response.get("items", []):
                video_id = item["id"]
                title = item["snippet"]["title"]
                url = f"https://www.youtube.com/watch?v={video_id}"
                results.append({
                    "title": title,
                    "url": url
                })
            
            return {
                "success": True,
                "results": results
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_mood_based_recommendation(self, mood, max_results=1):
        """Get video recommendations based on the user's mood."""
        mood_queries = {
            'joy': "uplifting motivational videos",
            'positive': "inspiring videos",
            'stress': "relaxing meditation music",
            'negative': "calming nature videos",
            'sadness': "uplifting music videos",
            'anger': "calming meditation videos",
            'surprise': "amazing nature videos",
            'gratitude': "gratitude meditation videos",
            'confusion': "explanatory videos",
            'curious': "educational videos",
            'greeting': "positive morning videos",
            'reflection': "mindfulness reflection videos",
            'neutral': "relaxing videos"
        }
        
        query = mood_queries.get(mood, "relaxing videos")
        return self.search_video(query, max_results)
    
    def _get_category_id(self, category_name):
        """Get the YouTube category ID for the given category name."""
        category_map = {
            "music": "10",
            "comedy": "23",
            "education": "27",
            "science": "28",
            "meditation": "26"
        }
        return category_map.get(category_name, "10")  # Default to music

def initialize_youtube(api_key):
    """Initialize the YouTube API client with the provided API key."""
    return YouTubeToolHandler(api_key)

def detect_video_request(message):
    """Detect if the user's message contains a video request."""
    # Direct video request patterns
    direct_request_patterns = [
        r'(show|provide|give|send|get|find)(\s+me)?\s+a\s+video',
        r'(can|could)\s+you\s+(show|provide|give|send|get|find)(\s+me)?\s+a\s+video',
        r'(i\s+want|i\'d\s+like|please\s+show)\s+(to\s+see\s+)?(a\s+)?video',
        r'video\s+of',
        r'videos?\s+(about|on|showing|featuring)',
        r'(watch|see)\s+(a\s+)?videos?'
    ]
    
    # Check for direct video requests
    for pattern in direct_request_patterns:
        if re.search(pattern, message.lower(), re.IGNORECASE):
            return True
    
    # Original patterns
    video_keywords = r'\b(watch|look|see|show|gaze|glance|stare|peek|scan|view|notice|spot|glimpse|behold|catch)\b.*\b(video|play|film|clip|movie|watch)\b'
    tool_keywords = r'\b(search|find|get|recommend|suggest)\b.*\b(video|youtube|clip|music)\b'
    
    if re.search(video_keywords, message, re.IGNORECASE) or re.search(tool_keywords, message, re.IGNORECASE):
        return True
    
    return False

def extract_tool_request(message):
    """Extract the tool request from the user's message."""
    # Check for specific tool patterns
    search_pattern = r'\b(search|find|look for)\b.*\b(video|videos)\b.*\b(about|on|for|of)\b\s+(.+)'
    trending_pattern = r'\b(trending|popular)\b.*\b(videos|music)\b.*\b(in|on|about)\b\s+(.+)'
    
    # Direct video request pattern
    direct_video_pattern = r'(video|videos)(\s+of|\s+about|\s+on|\s+showing|\s+featuring)?\s+(.+)'
    
    search_match = re.search(search_pattern, message, re.IGNORECASE)
    trending_match = re.search(trending_pattern, message, re.IGNORECASE)
    direct_match = re.search(direct_video_pattern, message, re.IGNORECASE)
    
    if search_match:
        query = search_match.group(4).strip()
        return {
            "tool": "search_video",
            "query": query
        }
    elif trending_match:
        category = trending_match.group(4).strip()
        return {
            "tool": "get_trending_videos",
            "category": category
        }
    elif direct_match:
        query = direct_match.group(3).strip()
        return {
            "tool": "search_video",
            "query": query
        }
    else:
        # Default to a simple search with the entire message
        return {
            "tool": "search_video",
            "query": message.strip()
        } 