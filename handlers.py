# handlers.py
# Developer: Mr @Mrnick66
# USTAAD-AI Premium Telegram bot handlers

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from ai_service import AIService
from language_detector import LanguageDetector
from utils import Utils
from config import Config

logger = logging.getLogger(__name__)

class BotHandlers:
    def __init__(self):
        self.ai_service = AIService()
        self.language_detector = LanguageDetector()
        self.utils = Utils()
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        try:
            user_info = self.utils.get_user_info(update)
            user_lang = self.language_detector.detect_language(
                update.message.text or user_info.get('language_code', 'en')
            )
            
            # Simulate typing
            await self.utils.simulate_typing(update.effective_chat.id, context)
            
            # Get localized welcome message
            welcome_data = self.language_detector.get_welcome_message(user_lang)
            
            # Create inline keyboard with only HELP and INFO
            keyboard = [
                [
                    InlineKeyboardButton("🆘 HELP", callback_data="help"),
                    InlineKeyboardButton("ℹ️ INFO", callback_data="info")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Send welcome message
            full_message = f"{welcome_data['welcome']}\n\n{welcome_data['description']}\n\n{welcome_data['start_chat']}"
            
            await update.message.reply_text(
                full_message,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
            
            # Log interaction
            self.utils.log_user_interaction(
                user_info['id'], 
                user_info['username'], 
                "/start", 
                len(full_message)
            )
            
        except Exception as e:
            logger.error(f"Error in start_command: {e}")
            await update.message.reply_text("Sorry, something went wrong. Please try again.")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        try:
            user_info = self.utils.get_user_info(update)
            user_lang = self.language_detector.detect_language(
                update.message.text or user_info.get('language_code', 'en')
            )
            
            await self.utils.simulate_typing(update.effective_chat.id, context)
            
            help_message = self.language_detector.get_help_message(user_lang)
            
            await update.message.reply_text(
                help_message,
                parse_mode='Markdown'
            )
            
            self.utils.log_user_interaction(
                user_info['id'],
                user_info['username'],
                "/help",
                len(help_message)
            )
            
        except Exception as e:
            logger.error(f"Error in help_command: {e}")
            await update.message.reply_text("Sorry, couldn't load help. Please try again.")
    
    async def info_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /info command"""
        try:
            user_info = self.utils.get_user_info(update)
            user_lang = self.language_detector.detect_language(
                update.message.text or user_info.get('language_code', 'en')
            )
            
            await self.utils.simulate_typing(update.effective_chat.id, context)
            
            info_message = self.language_detector.get_info_message(user_lang)
            
            await update.message.reply_text(
                info_message,
                parse_mode='Markdown'
            )
            
            self.utils.log_user_interaction(
                user_info['id'],
                user_info['username'],
                "/info",
                len(info_message)
            )
            
        except Exception as e:
            logger.error(f"Error in info_command: {e}")
            await update.message.reply_text("Sorry, couldn't load info. Please try again.")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle all text messages with AI response"""
        try:
            user_info = self.utils.get_user_info(update)
            user_message = update.message.text
            
            # Detect language
            detected_lang = self.language_detector.detect_language(user_message)
            
            # Simulate typing
            await self.utils.simulate_typing(update.effective_chat.id, context, duration=3)
            
            # Get AI response
            ai_response = await self.ai_service.get_ai_response(
                user_info['id'], 
                user_message, 
                detected_lang
            )
            
            # Format response with emojis
            formatted_response = self.utils.format_response_with_emojis(ai_response, detected_lang)
            
            # Split long messages
            message_chunks = self.utils.split_long_message(formatted_response)
            
            # Send response(s)
            for i, chunk in enumerate(message_chunks):
                if i > 0:  # Add small delay between chunks
                    await self.utils.simulate_typing(update.effective_chat.id, context, duration=1)
                
                await update.message.reply_text(
                    chunk,
                    parse_mode='Markdown' if '*' in chunk or '_' in chunk else None
                )
            
            # Log interaction
            self.utils.log_user_interaction(
                user_info['id'],
                user_info['username'],
                user_message,
                len(ai_response)
            )
            
        except Exception as e:
            logger.error(f"Error in handle_message: {e}")
            error_messages = {
                'hi': "माफ़ करें, कुछ गलत हुआ है। कृपया दोबारा कोशिश करें। 🙏",
                'ur': "معذرت، کچھ غلط ہوا ہے۔ براہ کرم دوبارہ کوشش کریں۔ 🙏",
                'ar': "عذراً، حدث خطأ ما. يرجى المحاولة مرة أخرى. 🙏",
                'default': "Sorry, something went wrong. Please try again. 🙏"
            }
            
            detected_lang = self.language_detector.detect_language(update.message.text or "")
            error_msg = error_messages.get(detected_lang, error_messages['default'])
            
            await update.message.reply_text(error_msg)
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline button callbacks"""
        try:
            query = update.callback_query
            await query.answer()
            
            user_info = self.utils.get_user_info(update)
            callback_data = query.data
            
            user_lang = self.language_detector.detect_language(
                query.message.text or user_info.get('language_code', 'en')
            )
            
            if callback_data == "help":
                help_message = self.language_detector.get_help_message(user_lang)
                await query.edit_message_text(help_message, parse_mode='Markdown')
            
            elif callback_data == "info":
                info_message = self.language_detector.get_info_message(user_lang)
                await query.edit_message_text(info_message, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error in button_callback: {e}")
            await query.edit_message_text("Sorry, something went wrong with that action.")