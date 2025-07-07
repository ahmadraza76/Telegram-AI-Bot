# main.py
# Developer: Ahmad Raza
# Enhanced Ostaad AI Premium Telegram Bot - Main Application

import logging
import asyncio
import sys
import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from telegram.ext.filters import BaseFilter
from config import Config
from enhanced_handlers import EnhancedOstaadHandlers
from utils import Utils

import random
from ahmad_intro import get_creator_intro, get_ahmad_vision
import re

# Custom filter class for intro queries
class IntroFilter(BaseFilter):
    def filter(self, message):
        if not message.text:
            return False
        text = message.text.lower()
        return bool(re.search(r'\b(ahmad|creator|vision|founder|developer|banaya|malik)\b', text))

# Create instance of the custom filter
intro_filter = filters.TEXT & IntroFilter()

async def reply_intro_vision(update, context):
    if random.random() < 0.5:
        reply = get_creator_intro()
    else:
        reply = get_ahmad_vision()
    await update.message.reply_text(reply, parse_mode="Markdown")

# Configure enhanced logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('logs/ostaad_ai.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class EnhancedOstaadAIBot:
    def __init__(self):
        # Validate configuration
        Config.validate()
        
        # Setup directories
        Utils.setup_directories()
        
        # Initialize enhanced handlers
        self.handlers = EnhancedOstaadHandlers()
        
        # Create application with enhanced settings
        self.application = Application.builder().token(Config.TELEGRAM_BOT_TOKEN).build()
        
        # Setup handlers
        self._setup_handlers()
        
        logger.info(f"🎯 {Config.BOT_NAME} {Config.VERSION} initialized successfully")
        logger.info(f"🧠 {Config.TAGLINE}")
    
    def _setup_handlers(self):
        """Setup all enhanced bot handlers"""
        
        # Command handlers - Core commands
        self.application.add_handler(CommandHandler("start", self.handlers.start_command))
        self.application.add_handler(CommandHandler("help", self.handlers.help_command))
        self.application.add_handler(CommandHandler("info", self.handlers.info_command))
        self.application.add_handler(CommandHandler("broadcast", self.handlers.broadcast_command))
        
        # Enhanced command handlers
        self.application.add_handler(CommandHandler("stats", self._stats_command))
        self.application.add_handler(CommandHandler("categories", self._categories_command))
        self.application.add_handler(CommandHandler("reset", self._reset_command))
        
        # Callback query handler for enhanced inline buttons
        self.application.add_handler(CallbackQueryHandler(self.handlers.button_callback))
        
        # Ahmad/creator/vision custom handler (only for keywords, should come before generic handler)
        self.application.add_handler(MessageHandler(intro_filter, reply_intro_vision))

        # Enhanced message handler for all text messages (must be last)
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handlers.handle_message)
        )
        
        logger.info("✅ All enhanced Ostaad AI handlers have been set up successfully")
    
    async def _stats_command(self, update, context):
        """Show bot statistics with desi style"""
        user_info = Utils.get_user_info(update)
        
        if not Utils.is_admin(user_info['id']):
            await update.message.reply_text("🚫 Admin access chahiye bhai statistics ke liye! 😅")
            return
        
        stats_message = f"""📊 **{Config.BOT_NAME} Statistics**

🤖 **System Info:**
• Version: {Config.VERSION}
• Model: {Config.DEFAULT_MODEL}
• Categories: {len(Config.KNOWLEDGE_CATEGORIES)}
• Languages: {len(Config.SUPPORTED_LANGUAGES)}

🎯 **Performance:**
• Max Tokens: {Config.MAX_TOKENS}
• Temperature: {Config.TEMPERATURE}
• Response Timeout: {Config.REQUEST_TIMEOUT}s
• Human-like Score: {Config.HUMAN_LIKE_SCORE}

👨‍💻 **Developer**: {Config.DEVELOPER}
⚡ **Engine**: Pure Desi AI Excellence

🟢 **Status**: Fully Operational aur Ready! 🔥"""
        
        await update.message.reply_text(stats_message, parse_mode='Markdown')
    
    async def _categories_command(self, update, context):
        """Show available knowledge categories with desi style"""
        categories_message = f"""🎯 **{Config.BOT_NAME} Knowledge Categories**

🎓 **Padhai & Education**
• School/College subjects (All levels)
• Competitive Exams (UPSC, JEE, NEET, CAT)
• Homework aur assignment help

💼 **Career & Job Guidance**
• Job search strategies
• Interview preparation
• Resume writing aur improvement

💻 **Technology & Programming**
• Coding aur development
• AI/ML concepts
• Tech troubleshooting

💰 **Online Earning & Business**
• Freelancing tips
• Business ideas aur planning
• Investment guidance

❤️ **Love & Relationships**
• Dating advice
• Relationship problems
• Communication tips

🗣️ **Language Learning**
• English speaking improvement
• Grammar aur vocabulary
• Translation help

🎬 **Entertainment & Fun**
• Movies aur music recommendations
• Jokes aur memes
• Timepass content

💪 **Motivation & Life Coaching**
• Success mindset
• Goal setting
• Confidence building

💬 **Kuch bhi poocho - main har category mein expert hoon! 🔥**"""
        
        await update.message.reply_text(categories_message, parse_mode='Markdown')
    
    async def _reset_command(self, update, context):
        """Reset user conversation history with desi style"""
        user_info = Utils.get_user_info(update)
        
        # Clear user's conversation history
        self.handlers.ai_service.clear_conversation(user_info['id'])
        
        # Reset user session if exists
        if user_info['id'] in self.handlers.user_sessions:
            del self.handlers.user_sessions[user_info['id']]
        
        await update.message.reply_text(
            "🔄 **Conversation Reset Ho Gaya!**\n\n"
            "Tumhara conversation history clear ho gaya hai bhai! "
            "Ab fresh start kar sakte ho kisi bhi topic ke saath! 🚀\n\n"
            "💬 Aaj kya explore karna chahte ho? 🎯"
        )
    
    async def start_bot(self):
        """Start the enhanced Ostaad AI bot"""
        try:
            # Display enhanced startup information
            startup_info = f"""
╔══════════════════════════════════════════════════════════════╗
║                    🎯 OSTAAD AI ENHANCED                     ║
╠══════════════════════════════════════════════════════════════╣
║  Version: {Config.VERSION:<47} ║
║  Developer: {Config.DEVELOPER:<45} ║
║  Model: {Config.DEFAULT_MODEL:<49} ║
║  Categories: {len(Config.KNOWLEDGE_CATEGORIES):<45} ║
║  Languages: {len(Config.SUPPORTED_LANGUAGES):<45} ║
╠══════════════════════════════════════════════════════════════╣
║  🧠 Pure Desi AI Excellence                                 ║
║  🚀 Human-like Intelligence + Indian Context                ║
║  ⚡ Powered by Ostaad AI Engine                             ║
║  💬 Har Sawal Ka Jawab - Bilkul Human Jaisa!               ║
╚══════════════════════════════════════════════════════════════╝
"""
            
            print(startup_info)
            logger.info(f"🎯 Starting {Config.BOT_NAME} {Config.VERSION}")
            logger.info(f"🧠 {Config.TAGLINE}")
            logger.info(f"👨‍💻 Developer: {Config.DEVELOPER}")
            logger.info(f"🤖 AI Model: {Config.DEFAULT_MODEL}")
            logger.info(f"🌍 Supported Languages: {len(Config.SUPPORTED_LANGUAGES)}")
            logger.info(f"📚 Knowledge Categories: {len(Config.KNOWLEDGE_CATEGORIES)}")
            
            # Initialize application
            await self.application.initialize()
            
            # Start polling with enhanced settings
            await self.application.start()
            await self.application.updater.start_polling(
                drop_pending_updates=True,
                allowed_updates=['message', 'callback_query'],
                timeout=30,
                read_timeout=30,
                write_timeout=30,
                connect_timeout=30
            )
            
            # Enhanced startup message
            logger.info("🚀 Ostaad AI is now LIVE and ready to serve!")
            logger.info("🎯 Pure desi expertise activated")
            logger.info("💬 Ready to handle any question with human-like intelligence")
            logger.info("🌟 Press Ctrl+C to stop the bot")
            
            # Run until interrupted
            try:
                await asyncio.Event().wait()
            except KeyboardInterrupt:
                logger.info("🛑 Received stop signal - Shutting down gracefully")
            
        except Exception as e:
            logger.error(f"❌ Failed to start enhanced Ostaad AI bot: {e}")
            raise
        finally:
            # Enhanced cleanup
            try:
                logger.info("🔄 Performing cleanup operations...")
                await self.application.updater.stop()
                await self.application.stop()
                await self.application.shutdown()
                logger.info("✅ Cleanup completed successfully")
            except Exception as e:
                logger.error(f"❌ Error during cleanup: {e}")
    
    def run(self):
        """Run the enhanced Ostaad AI bot"""
        try:
            # Check if event loop is already running
            try:
                loop = asyncio.get_running_loop()
                logger.info("📡 Event loop detected, creating task")
                task = loop.create_task(self.start_bot())
                return task
            except RuntimeError:
                # No event loop running, create new one
                logger.info("🔄 Creating new event loop")
                if sys.platform == 'win32':
                    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
                asyncio.run(self.start_bot())
                
        except KeyboardInterrupt:
            logger.info("👋 Ostaad AI stopped by user")
        except Exception as e:
            logger.error(f"💥 Ostaad AI crashed: {e}")
            raise

def main():
    """Enhanced main function"""
    try:
        print("🎯 Initializing Ostaad AI Enhanced...")
        bot = EnhancedOstaadAIBot()
        bot.run()
    except Exception as e:
        logger.error(f"💥 Failed to start Ostaad AI: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()