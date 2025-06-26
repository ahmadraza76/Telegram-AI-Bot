# utilities.py
# Developer: G A RAZA
# Utility functions for the Telegram bot

import os
from langdetect import detect
import subprocess
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def detect_language(text):
    """Detect the language of input text."""
    try:
        lang = detect(text)
        logger.info(f"Detected language: {lang}")
        return lang
    except Exception as e:
        logger.error(f"Failed to detect language: {e}")
        return "en"  # Default to English

def validate_text(text):
    """Validate input text."""
    if not text or len(text.strip()) < 5:
        logger.warning("Input text is too short or empty")
        return False, "Text is too short or empty."
    logger.info("Text validated successfully")
    return True, ""

def log_interaction(user_id, command, action):
    """Log user interactions."""
    try:
        with open(os.path.join("bot_log", "interactions.log"), "a") as f:
            log_message = f"User {user_id} used {command}: {action}\n"
            f.write(log_message)
            logger.info(f"Logged interaction: {log_message.strip()}")
    except Exception as e:
        logger.error(f"Failed to log interaction: {e}")

def generate_pdf(content, lang="en"):
    """Generate a PDF using LaTeX."""
    try:
        with open("latex_template.tex", "r") as f:
            template = f.read()
        title = "AI-Powered Bot Output" if lang == "en" else "AI-पावर्ड बॉट आउटपुट"
        content = content.replace('\n', '\\\\\n').replace('"', '\\"')
        latex_content = template.format(title=title, content=content, developer="G A RAZA")
        with open("output.tex", "w") as f:
            f.write(latex_content)
        subprocess.run(["latexmk", "-pdf", "output.tex"], check=True)
        logger.info("PDF generated successfully")
        return "output.pdf"
    except Exception as e:
        logger.error(f"Failed to generate PDF: {e}")
        raise
