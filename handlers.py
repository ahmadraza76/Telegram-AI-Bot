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
            
            # Create inline keyboard with HELP, INFO, and MENU
            keyboard = [
                [
                    InlineKeyboardButton("🆘 HELP", callback_data="help"),
                    InlineKeyboardButton("ℹ️ INFO", callback_data="info")
                ],
                [
                    InlineKeyboardButton("🏠 MAIN MENU", callback_data="main_menu")
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
            
            # Add back button
            keyboard = [
                [InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                help_message,
                reply_markup=reply_markup,
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
            
            # Add back button
            keyboard = [
                [InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                info_message,
                reply_markup=reply_markup,
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
            
            # Add menu button to last message
            keyboard = [
                [
                    InlineKeyboardButton("🏠 Menu", callback_data="main_menu"),
                    InlineKeyboardButton("🆘 Help", callback_data="help")
                ]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Send response(s)
            for i, chunk in enumerate(message_chunks):
                if i > 0:  # Add small delay between chunks
                    await self.utils.simulate_typing(update.effective_chat.id, context, duration=1)
                
                # Add menu buttons only to the last chunk
                current_markup = reply_markup if i == len(message_chunks) - 1 else None
                
                await update.message.reply_text(
                    chunk,
                    reply_markup=current_markup,
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
            
            # Add menu button even for error messages
            keyboard = [
                [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(error_msg, reply_markup=reply_markup)
    
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
            
            if callback_data == "main_menu":
                # Show main menu
                welcome_data = self.language_detector.get_welcome_message(user_lang)
                
                keyboard = [
                    [
                        InlineKeyboardButton("🆘 HELP", callback_data="help"),
                        InlineKeyboardButton("ℹ️ INFO", callback_data="info")
                    ],
                    [
                        InlineKeyboardButton("💬 Start Chat", callback_data="start_chat")
                    ]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                menu_message = f"🏠 **Main Menu**\n\n{welcome_data['welcome']}\n\n{welcome_data['start_chat']}"
                
                await query.edit_message_text(
                    menu_message, 
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
            
            elif callback_data == "help":
                help_message = self.language_detector.get_help_message(user_lang)
                
                keyboard = [
                    [InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await query.edit_message_text(
                    help_message, 
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
            
            elif callback_data == "info":
                info_message = self.language_detector.get_info_message(user_lang)
                
                keyboard = [
                    [InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await query.edit_message_text(
                    info_message, 
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
            
            elif callback_data == "start_chat":
                # Encourage user to start chatting
                chat_messages = {
                    'hi': "💬 **चैट शुरू करें!**\n\nअब आप मुझसे कुछ भी पूछ सकते हैं। बस अपना सवाल टाइप करें और भेजें!\n\n🎯 मैं आपकी हर मदद के लिए तैयार हूं।",
                    'ur': "💬 **چیٹ شروع کریں!**\n\nاب آپ مجھ سے کچھ بھی پوچھ سکتے ہیں۔ بس اپنا سوال ٹائپ کریں اور بھیجیں!\n\n🎯 میں آپ کی ہر مدد کے لیے تیار ہوں۔",
                    'ar': "💬 **ابدأ المحادثة!**\n\nيمكنك الآن أن تسألني أي شيء. فقط اكتب سؤالك وأرسله!\n\n🎯 أنا مستعد لمساعدتك في كل شيء.",
                    'default': "💬 **Start Chatting!**\n\nYou can now ask me anything. Just type your question and send it!\n\n🎯 I'm ready to help you with everything."
                }
                
                keyboard = [
                    [InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                chat_msg = chat_messages.get(user_lang, chat_messages['default'])
                
                await query.edit_message_text(
                    chat_msg,
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
            
        except Exception as e:
            logger.error(f"Error in button_callback: {e}")
            await query.edit_message_text("Sorry, something went wrong with that action.")