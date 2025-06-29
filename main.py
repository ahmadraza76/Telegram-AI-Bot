# main.py
# Developer: Mr @Mrnick66
# USTAAD-AI Premium Telegram Bot - Main Application

import logging
import asyncio
import sys
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from config import Config
from handlers import BotHandlers
from utils import Utils

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('logs/bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class UstaadAIBot:
    def __init__(self):
        # Validate configuration
        Config.validate()
        
        # Setup directories
        Utils.setup_directories()
        
        # Initialize handlers
        self.handlers = BotHandlers()
        
        # Create application
        self.application = Application.builder().token(Config.TELEGRAM_BOT_TOKEN).build()
        
        # Setup handlers
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup all bot handlers"""
        # Command handlers - Only 3 commands total
        self.application.add_handler(CommandHandler("start", self.handlers.start_command))
        self.application.add_handler(CommandHandler("help", self.handlers.help_command))
        self.application.add_handler(CommandHandler("info", self.handlers.info_command))
        
        # Callback query handler for inline buttons
        self.application.add_handler(CallbackQueryHandler(self.handlers.button_callback))
        
        # Message handler for all text messages (must be last)
        self.application.add_handler(
            MessageHandler(filters.TEXT & ~filters.COMMAND, self.handlers.handle_message)
        )
        
        logger.info("All handlers have been set up successfully")
    
    async def start_bot(self):
        """Start the bot"""
        try:
            logger.info(f"🎯 Starting {Config.BOT_NAME} {Config.VERSION}")
            logger.info(f"🧠 {Config.POWERED_BY}")
            logger.info(f"👨‍💻 Developer: {Config.DEVELOPER}")
            logger.info(f"🤖 Using OpenAI model: {Config.DEFAULT_MODEL}")
            
            # Initialize application
            await self.application.initialize()
            
            # Start polling
            await self.application.start()
            await self.application.updater.start_polling(
                drop_pending_updates=True,
                allowed_updates=['message', 'callback_query']
            )
            
            # Keep the bot running
            logger.info("🚀 Bot is now running! Press Ctrl+C to stop.")
            
            # Run until interrupted
            try:
                await asyncio.Event().wait()
            except KeyboardInterrupt:
                logger.info("🛑 Received stop signal")
            
        except Exception as e:
            logger.error(f"Failed to start bot: {e}")
            raise
        finally:
            # Cleanup
            try:
                await self.application.updater.stop()
                await self.application.stop()
                await self.application.shutdown()
            except Exception as e:
                logger.error(f"Error during cleanup: {e}")
    
    def run(self):
        """Run the bot"""
        try:
            # Check if event loop is already running
            try:
                loop = asyncio.get_running_loop()
                logger.info("Event loop is already running, creating task")
                # If we're in an already running loop, create a task
                task = loop.create_task(self.start_bot())
                return task
            except RuntimeError:
                # No event loop running, create new one
                logger.info("Creating new event loop")
                if sys.platform == 'win32':
                    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())
                asyncio.run(self.start_bot())
                
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
        except Exception as e:
            logger.error(f"Bot crashed: {e}")
            raise

def main():
    """Main function"""
    try:
        bot = UstaadAIBot()
        bot.run()
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()