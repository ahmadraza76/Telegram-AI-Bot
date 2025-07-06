# main.py
# Developer: Mr Ahmad 
# Enhanced USTAAD-AI Premium Telegram Bot - Main Application

import logging
import asyncio
import sys
import os
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from config import Config
from enhanced_handlers import EnhancedBotHandlers
from utils import Utils

# Configure enhanced logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('logs/ustaad_ai.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class EnhancedUstaadAIBot:
    def __init__(self):
        # Validate configuration
        Config.validate()
        
        # Setup directories
        Utils.setup_directories()
        
        # Initialize enhanced handlers
        self.handlers = EnhancedBotHandlers()
        
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
        self.application.add_handler(CommandHandler("domains", self._domains_command))
        self.application.add_handler(CommandHandler("reset", self._reset_command))
        
        # Callback query handler for enhanced inline buttons
        self.application.add_handler(CallbackQueryHandler(self.handlers.button_callback))
        
        # Enhanced message handler for all text messages (must be last)
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handlers.handle_message)
        )
        
        logger.info("✅ All enhanced handlers have been set up successfully")
    
    async def _stats_command(self, update, context):
        """Show bot statistics"""
        user_info = Utils.get_user_info(update)
        
        if not Utils.is_admin(user_info['id']):
            await update.message.reply_text("🚫 Admin access required for statistics.")
            return
        
        stats_message = f"""📊 **{Config.BOT_NAME} Statistics**

🤖 **System Info:**
• Version: {Config.VERSION}
• Model: {Config.DEFAULT_MODEL}
• Domains: {len(Config.KNOWLEDGE_DOMAINS)}
• Languages: {len(Config.SUPPORTED_LANGUAGES)}

🎯 **Performance:**
• Max Tokens: {Config.MAX_TOKENS}
• Temperature: {Config.TEMPERATURE}
• Response Timeout: {Config.REQUEST_TIMEOUT}s

👨‍💻 **Developer**: {Config.DEVELOPER}
⚡ **Engine**: USTAAD-AI Enhanced

🟢 **Status**: Fully Operational"""
        
        await update.message.reply_text(stats_message, parse_mode='Markdown')
    
    async def _domains_command(self, update, context):
        """Show available knowledge domains"""
        domains_message = f"""🎯 **{Config.BOT_NAME} Knowledge Domains**

🎓 **Academic Excellence**
• Competitive Exams (UPSC, JEE, NEET, CAT)
• School/College subjects (All levels)
• Research methodology & papers

💻 **Technology Mastery**
• Programming & Development
• AI/ML & Data Science
• Cybersecurity & Cloud

🎨 **Creative Powerhouse**
• Content Writing & Blogging
• Poetry & Shayari
• Storytelling & Scripts

💼 **Business Intelligence**
• Startup guidance
• Marketing strategies
• Financial planning

💪 **Life Coaching**
• Career development
• Relationship advice
• Personal growth

🌍 **Cultural Wisdom**
• Indian traditions & festivals
• Philosophy & spirituality
• Current affairs analysis

💬 **Just ask anything - I'm your omni-domain expert!**"""
        
        await update.message.reply_text(domains_message, parse_mode='Markdown')
    
    async def _reset_command(self, update, context):
        """Reset user conversation history"""
        user_info = Utils.get_user_info(update)
        
        # Clear user's conversation history
        self.handlers.ai_service.clear_conversation(user_info['id'])
        
        # Reset user session if exists
        if user_info['id'] in self.handlers.user_sessions:
            del self.handlers.user_sessions[user_info['id']]
        
        await update.message.reply_text(
            "🔄 **Conversation Reset Complete!**\n\n"
            "Your conversation history has been cleared. "
            "You can start fresh with any new topic!\n\n"
            "💬 What would you like to explore today?"
        )
    
    async def start_bot(self):
        """Start the enhanced bot"""
        try:
            # Display enhanced startup information
            startup_info = f"""
╔══════════════════════════════════════════════════════════════╗
║                    🎯 USTAAD-AI ENHANCED                     ║
╠══════════════════════════════════════════════════════════════╣
║  Version: {Config.VERSION:<47} ║
║  Developer: {Config.DEVELOPER:<45} ║
║  Model: {Config.DEFAULT_MODEL:<49} ║
║  Domains: {len(Config.KNOWLEDGE_DOMAINS):<47} ║
║  Languages: {len(Config.SUPPORTED_LANGUAGES):<45} ║
╠══════════════════════════════════════════════════════════════╣
║  🧠 Omni-Domain AI Excellence                               ║
║  🚀 ChatGPT-Level Intelligence + Indian Context             ║
║  ⚡ Powered by USTAAD-AI Engine                             ║
╚══════════════════════════════════════════════════════════════╝
"""
            
            print(startup_info)
            logger.info(f"🎯 Starting {Config.BOT_NAME} {Config.VERSION}")
            logger.info(f"🧠 {Config.TAGLINE}")
            logger.info(f"👨‍💻 Developer: {Config.DEVELOPER}")
            logger.info(f"🤖 AI Model: {Config.DEFAULT_MODEL}")
            logger.info(f"🌍 Supported Languages: {len(Config.SUPPORTED_LANGUAGES)}")
            logger.info(f"📚 Knowledge Domains: {len(Config.KNOWLEDGE_DOMAINS)}")
            
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
            logger.info("🚀 USTAAD-AI is now LIVE and ready to serve!")
            logger.info("🎯 Omni-Domain expertise activated")
            logger.info("💬 Ready to handle any question in any domain")
            logger.info("🌟 Press Ctrl+C to stop the bot")
            
            # Run until interrupted
            try:
                await asyncio.Event().wait()
            except KeyboardInterrupt:
                logger.info("🛑 Received stop signal - Shutting down gracefully")
            
        except Exception as e:
            logger.error(f"❌ Failed to start enhanced bot: {e}")
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
        """Run the enhanced bot"""
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
            logger.info("👋 USTAAD-AI stopped by user")
        except Exception as e:
            logger.error(f"💥 USTAAD-AI crashed: {e}")
            raise

def main():
    """Enhanced main function"""
    try:
        print("🎯 Initializing USTAAD-AI Enhanced...")
        bot = EnhancedUstaadAIBot()
        bot.run()
    except Exception as e:
        logger.error(f"💥 Failed to start USTAAD-AI: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()