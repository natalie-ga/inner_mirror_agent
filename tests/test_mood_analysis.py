import sys
import os
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent.parent
sys.path.append(str(project_root))

from src.utils.mood_analyzer import infer_mood

def test_mood_analyzer():
    """Test the mood analyzer with different inputs."""
    # Test greeting detection
    greeting_entry = "Hi there!"
    greeting_mood = infer_mood(greeting_entry)
    print(f"Greeting entry mood: {greeting_mood}")
    assert greeting_mood == "greeting", f"Expected 'greeting', got '{greeting_mood}'"
    
    # Test positive sentiment
    positive_entry = "I'm feeling really happy today! Everything is going well."
    positive_mood = infer_mood(positive_entry)
    print(f"Positive entry mood: {positive_mood}")
    assert positive_mood == "joy", f"Expected 'joy', got '{positive_mood}'"
    
    # Test negative sentiment with explicit sadness
    sad_entry = "I'm feeling very sad today. Nothing is going right."
    sad_mood = infer_mood(sad_entry)
    print(f"Sad entry mood: {sad_mood}")
    assert sad_mood == "sadness", f"Expected 'sadness', got '{sad_mood}'"
    
    # Test negative sentiment with explicit stress
    stress_entry = "I'm feeling very stressed today. Everything is overwhelming."
    stress_mood = infer_mood(stress_entry)
    print(f"Stress entry mood: {stress_mood}")
    assert stress_mood == "stress", f"Expected 'stress', got '{stress_mood}'"
    
    # Test neutral sentiment
    neutral_entry = "Today was an ordinary day. I went to work and came back home."
    neutral_mood = infer_mood(neutral_entry)
    print(f"Neutral entry mood: {neutral_mood}")
    # Allow for various interpretations of a neutral statement
    acceptable_moods = ["neutral", "reflection", "negative", "positive"]
    assert neutral_mood in acceptable_moods, f"Expected one of {acceptable_moods}, got '{neutral_mood}'"
    
    # Test more clearly neutral sentiment
    more_neutral_entry = "The sky is blue. The grass is green."
    more_neutral_mood = infer_mood(more_neutral_entry)
    print(f"More neutral entry mood: {more_neutral_mood}")
    assert more_neutral_mood in ["neutral", "positive"], f"Expected 'neutral' or 'positive', got '{more_neutral_mood}'"
    
    # Test specific emotions
    anger_entry = "I'm so angry about what happened at work today!"
    anger_mood = infer_mood(anger_entry)
    print(f"Anger entry mood: {anger_mood}")
    assert anger_mood == "anger", f"Expected 'anger', got '{anger_mood}'"
    
    gratitude_entry = "I'm so grateful for all the support I've received."
    gratitude_mood = infer_mood(gratitude_entry)
    print(f"Gratitude entry mood: {gratitude_mood}")
    assert gratitude_mood == "gratitude", f"Expected 'gratitude', got '{gratitude_mood}'"
    
    print("✅ All mood analyzer tests passed!")

if __name__ == "__main__":
    print("🔍 Testing mood analyzer...\n")
    test_mood_analyzer() 