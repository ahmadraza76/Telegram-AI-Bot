# main.py
# Developer: G A RAZA
# Premium ChatGPT-like Telegram Bot - Main Application

import logging
import asyncio
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

class PremiumAIBot:
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
        # Command handlers
        self.application.add_handler(CommandHandler("start", self.handlers.start_command))
        self.application.add_handler(CommandHandler("new", self.handlers.new_chat_command))
        self.application.add_handler(CommandHandler("export", self.handlers.export_command))
        
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
            logger.info(f"🚀 Starting Premium AI Bot (@{Config.BOT_USERNAME})")
            logger.info(f"🤖 Using OpenAI model: {Config.DEFAULT_MODEL}")
            
            # Start polling
            await self.application.run_polling(
                drop_pending_updates=True,
                allowed_updates=['message', 'callback_query']
            )
            
        except Exception as e:
            logger.error(f"Failed to start bot: {e}")
            raise
    
    def run(self):
        """Run the bot"""
        try:
            asyncio.run(self.start_bot())
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
        except Exception as e:
            logger.error(f"Bot crashed: {e}")
            raise

def main():
    """Main function"""
    try:
        bot = PremiumAIBot()
        bot.run()
    except Exception as e:
        logger.error(f"Failed to start application: {e}")
        exit(1)

if __name__ == '__main__':
    main()