# ai.py
# Developer: G A RAZA
# AI model interactions for the Telegram bot

import requests
from textblob import TextBlob

# AI API configuration
AI_API_URL = "https://api.example.com/v1/completions"
AI_API_KEY = "YOUR_AI_API_KEY"

def humanize_text(text, lang="en"):
    """Humanize AI-generated text."""
    prompt = f"Make this text sound more natural and human-like in {'English' if lang == 'en' else 'Hindi'}: {text}"
    try:
        response = requests.post(
            AI_API_URL,
            headers={"Authorization": f"Bearer {AI_API_KEY}"},
            json={"prompt": prompt, "max_tokens": 500}
        )
        response.raise_for_status()
        return response.json().get("choices", [{}])[0].get("text", "Error")
    except Exception as e:
        return f"{'Error' if lang == 'en' else 'तृटि'}: {e}"

def generate_seo_article(topic, lang="en"):
    """Generate an SEO-optimized article."""
    prompt = f"Write a 500-word SEO-optimized article in {'English' if lang == 'en' else 'Hindi'} on {topic}. Include keywords and headings."
    try:
        response = requests.post(
            AI_API_URL,
            headers={"Authorization": f"Bearer {AI_API_KEY}"},
            json={"prompt": prompt, "max_tokens": 1000}
        )
        response.raise_for_status()
        return response.json().get("choices", [{}])[0].get("text", "Error")
    except Exception as e:
        return f"{'Error' if lang == 'en' else 'तृटि'}: {e}"

def check_grammar(text):
    """Check grammar using TextBlob (English only)."""
    blob = TextBlob(text)
    corrections = []
    for sentence in blob.sentences:
        if sentence.correct() != sentence:
            corrections.append(f"Original: {sentence}\nCorrected: {sentence.correct()}")
    return "\n".join(corrections) if corrections else "No grammar issues found."

def assist_writing(text, lang="en"):
    """Provide writing suggestions."""
    prompt = f"Improve the clarity and style of this text in {'English' if lang == 'en' else 'Hindi'}: {text}"
    try:
        response = requests.post(
            AI_API_URL,
            headers={"Authorization": f"Bearer {AI_API_KEY}"},
            json={"prompt": prompt, "max_tokens": 500}
        )
        response.raise_for_status()
        return response.json().get("choices", [{}])[0].get("text", "Error")
    except Exception as e:
        return f"{'Error' if lang == 'en' else 'तृटि'}: {e}"
