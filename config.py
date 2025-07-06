# config.py
# Developer: Mr AHMAD
# Enhanced USTAAD-AI Premium Telegram Bot Configuration

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
    # 🤖 Enhanced AI Model Configuration
    # ==============================================
    DEFAULT_MODEL = "llama3-70b-8192"      # Upgraded to more powerful model
    FALLBACK_MODEL = "llama3-8b-8192"      # Fallback for high load
    MAX_TOKENS = 4000                      # Increased for comprehensive responses
    TEMPERATURE = 0.7                      # Optimal creativity balance
    TOP_P = 0.9                           # Nucleus sampling
    FREQUENCY_PENALTY = 0.1               # Reduce repetition
    PRESENCE_PENALTY = 0.1                # Encourage topic diversity
    
    # ==============================================
    # ⚙️ Enhanced Bot Technical Settings
    # ==============================================
    MAX_MESSAGE_LENGTH = 4096              # Telegram message limit
    TYPING_DELAY = 3                       # Increased for complex responses
    MAX_RETRIES = 3                        # API call retry attempts
    REQUEST_TIMEOUT = 45                   # Increased timeout for complex queries
    CONVERSATION_MEMORY = 40               # Increased conversation history
    
    # ==============================================
    # 🧠 Knowledge & Learning Configuration
    # ==============================================
    KNOWLEDGE_DOMAINS = [
        "academic", "technology", "creative", "cultural", 
        "business", "science", "philosophy", "current_affairs"
    ]
    
    EXPERTISE_LEVELS = ["beginner", "intermediate", "advanced", "expert"]
    
    SUPPORTED_SUBJECTS = [
        # Academic
        "mathematics", "physics", "chemistry", "biology", "computer_science",
        "economics", "history", "geography", "political_science", "psychology",
        
        # Technology
        "programming", "ai_ml", "cybersecurity", "cloud_computing", "blockchain",
        "web_development", "mobile_development", "data_science", "devops",
        
        # Competitive Exams
        "upsc", "jee", "neet", "cat", "gate", "ssc", "banking", "railway",
        
        # Creative
        "writing", "poetry", "storytelling", "design", "music", "art",
        
        # Life Skills
        "career", "relationships", "productivity", "motivation", "health"
    ]
    
    # ==============================================
    # 📁 File System Configuration
    # ==============================================
    LOGS_DIR = "logs"                      # Directory for log files
    TEMP_DIR = "temp"                      # Temporary files directory
    USER_DATA_DIR = "user_data"            # User preferences storage
    KNOWLEDGE_BASE_DIR = "knowledge_base"  # Knowledge base storage
    
    # ==============================================
    # 🎨 Enhanced Branding & UI Configuration
    # ==============================================
    BOT_NAME = "USTAAD-AI"
    VERSION = "v3.0.0"                     # Updated version
    DEVELOPER = "Mr AHMAD"
    POWERED_BY = "⚡ Powered by USTAAD-AI Engine"
    SUPPORT_CHAT = "https://t.me/UstaadAISupport"
    TAGLINE = "Your Omni-Domain AI Mentor"
    
    # ==============================================
    # ✨ Enhanced UI Emoji Configuration
    # ==============================================
    BRAND_EMOJI = "🎯"                     # Primary brand emoji
    SUCCESS_EMOJI = "✅"                   # Success indicators
    ERROR_EMOJI = "❌"                     # Error indicators
    WARNING_EMOJI = "⚠️"                   # Warning messages
    THINKING_EMOJI = "🤔"                  # AI processing
    AI_EMOJI = "🧠"                        # AI responses
    FIRE_EMOJI = "🔥"                      # Special highlights
    STAR_EMOJI = "⭐"                       # Premium features
    LOADING_EMOJI = "⏳"                   # Loading states
    GURU_EMOJI = "🎓"                      # Academic responses
    TECH_EMOJI = "💻"                      # Technology responses
    CREATIVE_EMOJI = "🎨"                  # Creative responses
    CULTURE_EMOJI = "🌍"                   # Cultural responses
    
    # ==============================================
    # 🌐 Enhanced Language & Localization
    # ==============================================
    DEFAULT_LANGUAGE = "hi"                # Default to Hindi
    SUPPORTED_LANGUAGES = [                # Available languages
        "en", "hi", "ur", "ar", "bn", "mr", 
        "te", "ta", "gu", "kn", "or", "pa",
        "ml", "as", "ne", "si"             # Added more languages
    ]
    
    # Language preferences for different domains
    DOMAIN_LANGUAGE_PREFERENCES = {
        "academic": ["hi", "en"],           # Hindi + English for academics
        "technology": ["en", "hi"],         # English primary for tech
        "creative": ["hi", "ur", "en"],     # Hindi/Urdu for creativity
        "cultural": ["hi", "ur", "bn"]      # Local languages for culture
    }
    
    # ==============================================
    # 🔒 Enhanced Security & Rate Limiting
    # ==============================================
    RATE_LIMIT = 60                        # Increased to 60 messages per minute
    BAN_DURATION = 3600                    # 1 hour in seconds
    ADMIN_COMMANDS = [                     # Restricted commands
        "broadcast", "stats", "maintenance", 
        "banuser", "analytics", "knowledge_update"
    ]
    
    # ==============================================
    # 📊 Analytics & Performance
    # ==============================================
    ENABLE_ANALYTICS = True                # Track user interactions
    PERFORMANCE_MONITORING = True          # Monitor response times
    KNOWLEDGE_TRACKING = True              # Track knowledge domain usage
    USER_FEEDBACK_COLLECTION = True        # Collect user feedback
    
    # ==============================================
    # 🎯 Response Quality Configuration
    # ==============================================
    MIN_RESPONSE_LENGTH = 50               # Minimum response length
    MAX_RESPONSE_LENGTH = 3500             # Maximum response length
    QUALITY_THRESHOLD = 0.8                # Response quality threshold
    ACCURACY_TARGET = 0.95                 # Target accuracy rate
    
    # Cultural context keywords
    INDIAN_CULTURAL_KEYWORDS = [
        "bollywood", "cricket", "festival", "tradition", "mythology",
        "spirituality", "yoga", "ayurveda", "classical_music", "dance"
    ]
    
    @classmethod
    def validate(cls):
        """
        🔍 Enhanced validation of configuration parameters
        """
        if not cls.TELEGRAM_BOT_TOKEN:
            raise ValueError("🚫 TELEGRAM_BOT_TOKEN is required in .env file")
        if not cls.GROQ_API_KEY:
            raise ValueError("🚫 GROQ_API_KEY is required in .env file")
        if cls.ADMIN_USER_ID == 0:
            print("⚠️ Warning: ADMIN_USER_ID not set - admin features disabled")
        
        # Validate model configuration
        if cls.MAX_TOKENS > 8192:
            print("⚠️ Warning: MAX_TOKENS exceeds model limit, adjusting to 8192")
            cls.MAX_TOKENS = 8192
        
        return True
    
    @classmethod
    def get_bot_info(cls):
        """📊 Get enhanced bot information string"""
        return f"""
{cls.BRAND_EMOJI} {cls.BOT_NAME} {cls.VERSION}
{cls.TAGLINE}

{cls.POWERED_BY}
👨‍💻 Developer: {cls.DEVELOPER}
🧠 Model: {cls.DEFAULT_MODEL}
🌍 Languages: {len(cls.SUPPORTED_LANGUAGES)}
📚 Domains: {len(cls.KNOWLEDGE_DOMAINS)}
📩 Support: {cls.SUPPORT_CHAT}

🎯 Omni-Domain AI Excellence
"""
    
    @classmethod
    def get_performance_config(cls):
        """Get performance configuration"""
        return {
            "model": cls.DEFAULT_MODEL,
            "max_tokens": cls.MAX_TOKENS,
            "temperature": cls.TEMPERATURE,
            "top_p": cls.TOP_P,
            "frequency_penalty": cls.FREQUENCY_PENALTY,
            "presence_penalty": cls.PRESENCE_PENALTY,
            "timeout": cls.REQUEST_TIMEOUT
        }