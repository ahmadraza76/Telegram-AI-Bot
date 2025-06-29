# config.py
# Developer: G A RAZA
# Configuration settings for the premium Telegram AI bot

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Bot Configuration
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    BOT_USERNAME = os.getenv('BOT_USERNAME', 'YourAIBot')
    ADMIN_USER_ID = int(os.getenv('ADMIN_USER_ID', '0'))
    
    # AI Configuration
    DEFAULT_MODEL = "gpt-3.5-turbo"
    MAX_TOKENS = 4000
    TEMPERATURE = 0.7
    
    # Bot Settings
    MAX_MESSAGE_LENGTH = 4096
    TYPING_DELAY = 2
    
    # File Paths
    LOGS_DIR = "logs"
    TEMP_DIR = "temp"
    
    # UI Configuration
    BRAND_COLOR = "🌟"
    SUCCESS_EMOJI = "✅"
    ERROR_EMOJI = "❌"
    THINKING_EMOJI = "🤔"
    AI_EMOJI = "🤖"
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN is required")
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required")
        return True