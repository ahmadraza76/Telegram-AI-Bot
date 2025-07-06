# config.py
# Developer: Ahmad Raza
# Enhanced Ostaad AI Premium Telegram Bot Configuration

import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # ==============================================
    # 🔧 Bot Core Configuration
    # ==============================================
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    GROQ_API_KEY = os.getenv('GROQ_API_KEY')
    BOT_USERNAME = os.getenv('BOT_USERNAME', 'OstaadAIBot')
    ADMIN_USER_ID = int(os.getenv('ADMIN_USER_ID', '0'))
    
    # ==============================================
    # 🤖 Enhanced AI Model Configuration
    # ==============================================
    DEFAULT_MODEL = "llama3-70b-8192"      # Powerful model for better responses
    FALLBACK_MODEL = "llama3-8b-8192"      # Fallback for high load
    MAX_TOKENS = 4000                      # Increased for comprehensive responses
    TEMPERATURE = 0.8                      # Higher creativity for human-like responses
    TOP_P = 0.9                           # Nucleus sampling
    FREQUENCY_PENALTY = 0.1               # Reduce repetition
    PRESENCE_PENALTY = 0.1                # Encourage topic diversity
    
    # ==============================================
    # ⚙️ Enhanced Bot Technical Settings
    # ==============================================
    MAX_MESSAGE_LENGTH = 4096              # Telegram message limit
    TYPING_DELAY = 3                       # Typing simulation delay
    MAX_RETRIES = 3                        # API call retry attempts
    REQUEST_TIMEOUT = 45                   # Timeout for complex queries
    CONVERSATION_MEMORY = 40               # Conversation history limit
    
    # ==============================================
    # 🧠 Ostaad AI Knowledge Configuration
    # ==============================================
    KNOWLEDGE_CATEGORIES = [
        "padhai_education", "career_job", "programming_tech", "online_earning",
        "love_relationships", "language_learning", "entertainment", "motivation",
        "health_fitness", "general_knowledge", "religion_culture", "jokes_fun"
    ]
    
    EXPERTISE_LEVELS = ["beginner", "intermediate", "advanced", "expert"]
    
    SUPPORTED_TOPICS = [
        # Academic
        "mathematics", "physics", "chemistry", "biology", "computer_science",
        "economics", "history", "geography", "political_science", "psychology",
        
        # Competitive Exams
        "upsc", "jee", "neet", "cat", "gate", "ssc", "banking", "railway",
        
        # Technology
        "programming", "ai_ml", "cybersecurity", "web_development", "mobile_development",
        "data_science", "cloud_computing", "blockchain", "telegram_bots",
        
        # Career & Business
        "job_search", "interview_prep", "resume_writing", "startup", "business_plan",
        "digital_marketing", "freelancing", "online_earning", "cryptocurrency",
        
        # Personal & Social
        "relationships", "love_advice", "friendship", "family", "communication",
        "motivation", "goal_setting", "habit_formation", "stress_management",
        
        # Language & Culture
        "english_learning", "hindi_grammar", "translation", "indian_culture",
        "festivals", "religion", "philosophy", "current_affairs",
        
        # Entertainment & Fun
        "movies", "music", "memes", "jokes", "shayari", "poetry", "storytelling",
        "riddles", "games", "timepass"
    ]
    
    # ==============================================
    # 📁 File System Configuration
    # ==============================================
    LOGS_DIR = "logs"
    TEMP_DIR = "temp"
    USER_DATA_DIR = "user_data"
    
    # ==============================================
    # 🎨 Enhanced Branding & UI Configuration
    # ==============================================
    BOT_NAME = "Ostaad AI"
    VERSION = "v3.0.0"
    DEVELOPER = "Ahmad Raza"
    POWERED_BY = "⚡ Powered by Ostaad AI Engine"
    SUPPORT_CHAT = "https://t.me/OstaadAISupport"
    TAGLINE = "Your Digital Ustad - Har Sawal Ka Jawab! 🎯"
    
    # ==============================================
    # ✨ Enhanced Emoji Configuration for Desi Style
    # ==============================================
    BRAND_EMOJI = "🎯"
    SUCCESS_EMOJI = "✅"
    ERROR_EMOJI = "❌"
    WARNING_EMOJI = "⚠️"
    THINKING_EMOJI = "🤔"
    AI_EMOJI = "🧠"
    FIRE_EMOJI = "🔥"
    STAR_EMOJI = "⭐"
    LOADING_EMOJI = "⏳"
    
    # Mood-based emojis
    MOOD_EMOJIS = {
        "happy": ["😄", "😊", "🔥", "💪", "✨"],
        "sad": ["😞", "💔", "🥺", "🙏", "❤️"],
        "angry": ["😤", "😌", "🙏", "💆‍♂️", "🧘‍♂️"],
        "confused": ["🤔", "💡", "📚", "🎯", "👨‍🏫"],
        "neutral": ["👋", "💬", "👍", "👌", "🤝"]
    }
    
    # Category-specific emojis
    CATEGORY_EMOJIS = {
        "padhai_education": ["🎓", "📚", "✏️", "🧠"],
        "career_job": ["💼", "📄", "📈", "🧑‍💼"],
        "programming_tech": ["💻", "🛠️", "⚙️", "🧑‍💻"],
        "online_earning": ["💰", "💸", "📊", "💳"],
        "love_relationships": ["❤️", "💕", "🤗", "🥰"],
        "language_learning": ["📖", "🗣️", "🔤", "📚"],
        "entertainment": ["🎬", "🎵", "😂", "🤣"],
        "motivation": ["💪", "🔥", "🧠", "✨"],
        "health_fitness": ["🩺", "🍎", "🏃‍♂️", "😷"],
        "general_knowledge": ["🌍", "📰", "🧭", "📊"],
        "religion_culture": ["🕉️", "🙏", "🎭", "🏛️"],
        "jokes_fun": ["😜", "😎", "🤣", "🔥"]
    }
    
    # ==============================================
    # 🌐 Enhanced Language & Localization
    # ==============================================
    DEFAULT_LANGUAGE = "hi"
    SUPPORTED_LANGUAGES = [
        "en", "hi", "ur", "ar", "bn", "mr", 
        "te", "ta", "gu", "kn", "or", "pa",
        "ml", "as", "ne", "si"
    ]
    
    # Hinglish phrases for natural conversation
    HINGLISH_PHRASES = {
        "greetings": ["Are bhai", "Kya haal", "Suno yaar", "Dekho bhai"],
        "agreement": ["Bilkul sahi", "Haan yaar", "Exactly", "Sahi pakde"],
        "explanation": ["Chalo samjhaata hoon", "Dekho aise hai", "Simple hai bhai"],
        "encouragement": ["Tension mat lo", "Ho jaayega", "Koi baat nahi", "Sab theek hai"],
        "excitement": ["Waah bhai", "Bahut badhiya", "Sahi hai", "Mast hai"]
    }
    
    # ==============================================
    # 🔒 Enhanced Security & Rate Limiting
    # ==============================================
    RATE_LIMIT = 60                        # Messages per minute
    BAN_DURATION = 3600                    # 1 hour in seconds
    ADMIN_COMMANDS = [
        "broadcast", "stats", "maintenance", 
        "banuser", "analytics", "user_management"
    ]
    
    # ==============================================
    # 📊 Analytics & Performance
    # ==============================================
    ENABLE_ANALYTICS = True
    PERFORMANCE_MONITORING = True
    USER_MOOD_TRACKING = True              # Track user emotional states
    CONVERSATION_ANALYTICS = True          # Analyze conversation patterns
    
    # ==============================================
    # 🎯 Response Quality Configuration
    # ==============================================
    MIN_RESPONSE_LENGTH = 50
    MAX_RESPONSE_LENGTH = 3500
    QUALITY_THRESHOLD = 0.8
    ACCURACY_TARGET = 0.95
    HUMAN_LIKE_SCORE = 0.9                 # Target for human-like responses
    
    # Desi context keywords
    INDIAN_CULTURAL_KEYWORDS = [
        "bollywood", "cricket", "festival", "tradition", "mythology",
        "spirituality", "yoga", "ayurveda", "classical_music", "dance",
        "chai", "samosa", "diwali", "holi", "eid", "ganesh", "durga"
    ]
    
    @classmethod
    def validate(cls):
        """Enhanced validation of configuration parameters"""
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
        """Get enhanced bot information string"""
        return f"""
{cls.BRAND_EMOJI} {cls.BOT_NAME} {cls.VERSION}
{cls.TAGLINE}

{cls.POWERED_BY}
👨‍💻 Developer: {cls.DEVELOPER}
🧠 Model: {cls.DEFAULT_MODEL}
🌍 Languages: {len(cls.SUPPORTED_LANGUAGES)}
📚 Categories: {len(cls.KNOWLEDGE_CATEGORIES)}

🎯 Pure Desi AI Excellence - Har Sawal Ka Jawab! 💪
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