# handlers.py
# Developer: Mr @Mrnick66
# USTAAD-AI Premium Telegram bot handlers

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from ai_service import AIService
from language_detector import LanguageDetector
from user_preferences import UserPreferences
from utils import Utils
from config import Config

logger = logging.getLogger(__name__)

class BotHandlers:
    def __init__(self):
        self.ai_service = AIService()
        self.language_detector = LanguageDetector()
        self.user_preferences = UserPreferences()
        self.utils = Utils()
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        try:
            user_info = self.utils.get_user_info(update)
            
            # Get user's preferred language or detect from message
            preferred_lang = self.user_preferences.get_user_language(user_info['id'])
            if not preferred_lang:
                preferred_lang = self.language_detector.detect_language(
                    update.message.text or user_info.get('language_code', 'en')
                )
            
            # Simulate typing
            await self.utils.simulate_typing(update.effective_chat.id, context)
            
            # Get localized welcome message
            welcome_data = self.language_detector.get_welcome_message(preferred_lang)
            
            # Create inline keyboard with HELP, INFO, SETTINGS, and MENU
            keyboard = [
                [
                    InlineKeyboardButton("🆘 HELP", callback_data="help"),
                    InlineKeyboardButton("ℹ️ INFO", callback_data="info")
                ],
                [
                    InlineKeyboardButton("🌍 Language", callback_data="language_settings"),
                    InlineKeyboardButton("🏠 MENU", callback_data="main_menu")
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
            
            # Get user's preferred language
            preferred_lang = self.user_preferences.get_user_language(user_info['id'])
            if not preferred_lang:
                preferred_lang = self.language_detector.detect_language(
                    update.message.text or user_info.get('language_code', 'en')
                )
            
            await self.utils.simulate_typing(update.effective_chat.id, context)
            
            help_message = self.language_detector.get_help_message(preferred_lang)
            
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
            
            # Get user's preferred language
            preferred_lang = self.user_preferences.get_user_language(user_info['id'])
            if not preferred_lang:
                preferred_lang = self.language_detector.detect_language(
                    update.message.text or user_info.get('language_code', 'en')
                )
            
            await self.utils.simulate_typing(update.effective_chat.id, context)
            
            info_message = self.language_detector.get_info_message(preferred_lang)
            
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
            
            # Get user's preferred language or detect from message
            preferred_lang = self.user_preferences.get_user_language(user_info['id'])
            if not preferred_lang:
                detected_lang = self.language_detector.detect_language(user_message)
                # Save detected language as preference
                self.user_preferences.set_user_language(user_info['id'], detected_lang)
                preferred_lang = detected_lang
            
            # Simulate typing
            await self.utils.simulate_typing(update.effective_chat.id, context, duration=3)
            
            # Get AI response
            ai_response = await self.ai_service.get_ai_response(
                user_info['id'], 
                user_message, 
                preferred_lang
            )
            
            # Format response with emojis
            formatted_response = self.utils.format_response_with_emojis(ai_response, preferred_lang)
            
            # Split long messages
            message_chunks = self.utils.split_long_message(formatted_response)
            
            # Add menu button to last message
            keyboard = [
                [
                    InlineKeyboardButton("🏠 Menu", callback_data="main_menu"),
                    InlineKeyboardButton("🌍 Language", callback_data="language_settings")
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
            
            # Get user's preferred language for error message
            user_info = self.utils.get_user_info(update)
            preferred_lang = self.user_preferences.get_user_language(user_info['id']) or 'en'
            
            error_messages = {
                'hi': "माफ़ करें, कुछ गलत हुआ है। कृपया दोबारा कोशिश करें। 🙏",
                'ur': "معذرت، کچھ غلط ہوا ہے۔ براہ کرم دوبارہ کوشش کریں۔ 🙏",
                'ar': "عذراً، حدث خطأ ما. يرجى المحاولة مرة أخرى. 🙏",
                'default': "Sorry, something went wrong. Please try again. 🙏"
            }
            
            error_msg = error_messages.get(preferred_lang, error_messages['default'])
            
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
            
            # Get user's preferred language
            preferred_lang = self.user_preferences.get_user_language(user_info['id'])
            if not preferred_lang:
                preferred_lang = self.language_detector.detect_language(
                    query.message.text or user_info.get('language_code', 'en')
                )
            
            if callback_data == "main_menu":
                # Show main menu
                welcome_data = self.language_detector.get_welcome_message(preferred_lang)
                
                keyboard = [
                    [
                        InlineKeyboardButton("🆘 HELP", callback_data="help"),
                        InlineKeyboardButton("ℹ️ INFO", callback_data="info")
                    ],
                    [
                        InlineKeyboardButton("🌍 Language", callback_data="language_settings"),
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
            
            elif callback_data == "language_settings":
                # Show language selection
                settings_message = self.language_detector.get_language_settings_message(preferred_lang)
                
                # Create language selection buttons
                popular_langs = self.language_detector.get_popular_languages()
                keyboard = []
                
                # Add popular languages in pairs
                lang_items = list(popular_langs.items())
                for i in range(0, len(lang_items), 2):
                    row = []
                    for j in range(2):
                        if i + j < len(lang_items):
                            lang_code, lang_name = lang_items[i + j]
                            # Mark current language
                            if lang_code == preferred_lang:
                                lang_name += " ✅"
                            row.append(InlineKeyboardButton(lang_name, callback_data=f"set_lang_{lang_code}"))
                    keyboard.append(row)
                
                # Add back button
                keyboard.append([InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu")])
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await query.edit_message_text(
                    settings_message,
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
            
            elif callback_data.startswith("set_lang_"):
                # Set user's language preference
                new_lang = callback_data.replace("set_lang_", "")
                self.user_preferences.set_user_language(user_info['id'], new_lang)
                
                # Show confirmation message
                confirmations = {
                    'en': f"✅ **Language Updated!**\n\nYour language has been set to **English**.\n\nAll future conversations will be in English.",
                    'hi': f"✅ **भाषा अपडेट हो गई!**\n\nआपकी भाषा **हिंदी** में सेट कर दी गई है।\n\nभविष्य की सभी बातचीत हिंदी में होगी।",
                    'ur': f"✅ **زبان اپڈیٹ ہو گئی!**\n\nآپ کی زبان **اردو** میں سیٹ کر دی گئی ہے۔\n\nمستقبل کی تمام گفتگو اردو میں ہوگی۔",
                    'ar': f"✅ **تم تحديث اللغة!**\n\nتم تعيين لغتك إلى **العربية**.\n\nجميع المحادثات المستقبلية ستكون بالعربية.",
                    'es': f"✅ **¡Idioma Actualizado!**\n\nTu idioma ha sido configurado a **Español**.\n\nTodas las conversaciones futuras serán en español.",
                    'fr': f"✅ **Langue Mise à Jour!**\n\nVotre langue a été définie sur **Français**.\n\nToutes les conversations futures seront en français.",
                    'de': f"✅ **Sprache Aktualisiert!**\n\nIhre Sprache wurde auf **Deutsch** eingestellt.\n\nAlle zukünftigen Gespräche werden auf Deutsch sein.",
                    'ru': f"✅ **Язык Обновлен!**\n\nВаш язык установлен на **Русский**.\n\nВсе будущие разговоры будут на русском языке.",
                    'ja': f"✅ **言語が更新されました！**\n\nあなたの言語は**日本語**に設定されました。\n\n今後のすべての会話は日本語で行われます。",
                    'zh': f"✅ **语言已更新！**\n\n您的语言已设置为**中文**。\n\n未来的所有对话都将使用中文。"
                }
                
                confirmation_msg = confirmations.get(new_lang, confirmations['en'])
                
                keyboard = [
                    [
                        InlineKeyboardButton("🔙 Back to Settings", callback_data="language_settings"),
                        InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")
                    ]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await query.edit_message_text(
                    confirmation_msg,
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
            
            elif callback_data == "help":
                help_message = self.language_detector.get_help_message(preferred_lang)
                
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
                info_message = self.language_detector.get_info_message(preferred_lang)
                
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
                
                chat_msg = chat_messages.get(preferred_lang, chat_messages['default'])
                
                await query.edit_message_text(
                    chat_msg,
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
            
        except Exception as e:
            logger.error(f"Error in button_callback: {e}")
            await query.edit_message_text("Sorry, something went wrong with that action.")