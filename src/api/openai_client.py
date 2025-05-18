import openai

def initialize_openai(api_key):
    """Initialize the OpenAI client with the provided API key."""
    openai.api_key = api_key

def generate_reflection(user_entry, mood, previous_mood=None):
    """Generate a reflective response based on the user's journal entry and mood."""
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