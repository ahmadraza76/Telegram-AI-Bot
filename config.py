# config.py
# Developer: Mr AHMAD
# USTAAD-AI Premium Telegram Bot Configuration

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # ==============================================
    # 🔧 Bot Core Configuration
    # ==============================================
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    BOT_USERNAME = os.getenv('BOT_USERNAME', 'UstaadAIBot')
    ADMIN_USER_ID = int(os.getenv('ADMIN_USER_ID', '0'))
    
    # ==============================================
    # 🤖 AI Model Configuration
    # ==============================================
    DEFAULT_MODEL = "llama3-8b-8192"  # Groq's fast model
    MAX_TOKENS = 4000                  # Max tokens per response
    TEMPERATURE = 0.7                  # Creativity level (0-1)
    TOP_P = 0.9                        # Nucleus sampling
    FREQUENCY_PENALTY = 0.0            # Reduce repetition
    
    # ==============================================
    # ⚙️ Bot Technical Settings
    # ==============================================
    MAX_MESSAGE_LENGTH = 4096          # Telegram message limit
    TYPING_DELAY = 2                   # Seconds to show "typing" status
    MAX_RETRIES = 3                    # API call retry attempts
    REQUEST_TIMEOUT = 30               # API timeout in seconds
    
    # ==============================================
    # 📁 File System Configuration
    # ==============================================
    LOGS_DIR = "logs"                  # Directory for log files
    TEMP_DIR = "temp"                  # Temporary files directory
    USER_DATA_DIR = "user_data"        # User preferences storage
    
    # ==============================================
    # 🎨 Branding & UI Configuration
    # ==============================================
    BOT_NAME = "USTAAD-AI"
    VERSION = "v2.5.0"
    DEVELOPER = "Mr AHMAD"
    POWERED_BY = "⚡ Powered by USTAAD-AI"
    SUPPORT_CHAT = "https://t.me/UstaadAISupport"
    
    # ==============================================
    # ✨ UI Emoji Configuration
    # ==============================================
    BRAND_EMOJI = "🎯"                # Primary brand emoji
    SUCCESS_EMOJI = "✅"              # Success indicators
    ERROR_EMOJI = "❌"                # Error indicators
    WARNING_EMOJI = "⚠️"              # Warning messages
    THINKING_EMOJI = "🤔"             # AI processing
    AI_EMOJI = "🧠"                   # AI responses
    FIRE_EMOJI = "🔥"                 # Special highlights
    STAR_EMOJI = "⭐"                  # Premium features
    LOADING_EMOJI = "⏳"              # Loading states
    
    # ==============================================
    # 🌐 Language & Localization
    # ==============================================
    DEFAULT_LANGUAGE = "en"            # Fallback language
    SUPPORTED_LANGUAGES = [            # Available languages
        "en", "hi", "ur", "ar", 
        "bn", "mr", "te", "ta",
        "gu", "kn", "or", "pa"
    ]
    
    # ==============================================
    # 🔒 Security & Rate Limiting
    # ==============================================
    RATE_LIMIT = 30                    # Messages per minute
    BAN_DURATION = 3600                # 1 hour in seconds
    ADMIN_COMMANDS = [                 # Restricted commands
        "broadcast", "stats", 
        "maintenance", "banuser"
    ]
    
    @classmethod
    def validate(cls):
        """
        🔍 Validate essential configuration parameters
        Raises:
            ValueError: If required configurations are missing
        """
        if not cls.TELEGRAM_BOT_TOKEN:
            raise ValueError("🚫 TELEGRAM_BOT_TOKEN is required in .env file")
        if not cls.GROQ_API_KEY:
            raise ValueError("🚫 GROQ_API_KEY is required in .env file")
        if cls.ADMIN_USER_ID == 0:
            print("⚠️ Warning: ADMIN_USER_ID not set - admin features disabled")
        return True
    
    @classmethod
    def get_bot_info(cls):
        """📊 Get formatted bot information string"""
        return f"""
{cls.BRAND_EMOJI} {cls.BOT_NAME} {cls.VERSION}
{cls.POWERED_BY}
👨‍💻 Developer: {cls.DEVELOPER}
📩 Support: {cls.SUPPORT_CHAT}
"""
