# main.py
# Developer: G A RAZA
# Telegram Bot with AI Humanizer, SEO Article Generator, Grammar Checker, Writing Assistant, and PDF Download

import logging
from telegram.ext import Application, CommandHandler, MessageHandler, filters, CallbackQueryHandler
from handlers import start, help_command, humanize, seo_article, grammar_check, writing_assist, menu, download, button_callback

# Enable logging
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Bot token from BotFather
TOKEN = "YOUR_BOT_TOKEN_HERE"

def main():
    """Main function to run the bot."""
    application = Application.builder().token(TOKEN).build()

    # Add command handlers
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))
    application.add_handler(CommandHandler("humanize", humanize))
    application.add_handler(CommandHandler("seoarticle", seo_article))
    application.add_handler(CommandHandler("grammar", grammar_check))
    application.add_handler(CommandHandler("assist", writing_assist))
    application.add_handler(CommandHandler("menu", menu))
    application.add_handler(CommandHandler("download", download))
    application.add_handler(CallbackQueryHandler(button_callback))

    # Add message handler for non-command text
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, humanize))

    # Start the bot
    logger.info("Bot is starting...")
    application.run_polling()

if __name__ == '__main__':
    main()
