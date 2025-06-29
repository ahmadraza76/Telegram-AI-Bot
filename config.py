# config.py
# Developer: Mr @Mrnick66
# USTAAD-AI Premium Telegram Bot Configuration

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Bot Configuration
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    BOT_USERNAME = os.getenv('BOT_USERNAME', 'UstaadAIBot')
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
    
    # Branding
    BOT_NAME = "USTAAD-AI"
    VERSION = "v2.5.0"
    DEVELOPER = "Mr @Mrnick66"
    POWERED_BY = "Powered by USTAAD-AI"
    
    # UI Configuration
    BRAND_COLOR = "🎯"
    SUCCESS_EMOJI = "✅"
    ERROR_EMOJI = "❌"
    THINKING_EMOJI = "🤔"
    AI_EMOJI = "🧠"
    FIRE_EMOJI = "🔥"
    STAR_EMOJI = "⭐"
    
    @classmethod
    def validate(cls):
        """Validate required configuration"""
        if not cls.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN is required")
        if not cls.OPENAI_API_KEY:
            raise ValueError("OPENAI_API_KEY is required")
        return True