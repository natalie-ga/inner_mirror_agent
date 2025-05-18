def format_tool_response(tool_result, tool_name):
    """Format the response from a tool call."""
    if not tool_result.get("success", False):
        return f"I tried to use the {tool_name} tool, but encountered an error: {tool_result.get('error', 'Unknown error')}"
    
    results = tool_result.get("results", [])
    if not results:
        return f"I used the {tool_name} tool, but didn't find any results."
    
    if tool_name == "search_video":
        return f"I found a video that might interest you: '{results[0]['title']}'\n{results[0]['url']}"
    elif tool_name == "get_trending_videos":
        response = "Here are some trending videos you might enjoy:\n"
        for i, video in enumerate(results, 1):
            response += f"{i}. '{video['title']}'\n{video['url']}\n"
        return response
    elif tool_name == "get_mood_based_recommendation":
        return f"Based on your mood, you might enjoy this video: '{results[0]['title']}'\n{results[0]['url']}"
    else:
        return f"Here are the results from the {tool_name} tool:\n" + "\n".join([f"- {result}" for result in results]) 