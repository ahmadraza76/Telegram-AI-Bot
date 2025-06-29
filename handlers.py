# handlers.py
# Developer: G A RAZA
# Premium Telegram bot handlers with advanced AI integration

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
            
            # Create inline keyboard
            keyboard = [
                [InlineKeyboardButton("🆕 New Chat", callback_data="new_chat")],
                [InlineKeyboardButton("📊 Chat Stats", callback_data="stats")],
                [InlineKeyboardButton("🌐 Language", callback_data="language")],
                [InlineKeyboardButton("ℹ️ Help", callback_data="help")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Send welcome message
            full_message = f"{welcome_data['welcome']}\n\n{welcome_data['features']}\n\n{welcome_data['start_chat']}"
            
            await update.message.reply_text(
                full_message,
                reply_markup=reply_markup,
                parse_mode='HTML'
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
            
            if callback_data == "new_chat":
                # Clear conversation history
                self.ai_service.clear_conversation(user_info['id'])
                await query.edit_message_text(
                    f"{Config.SUCCESS_EMOJI} New chat started! Your conversation history has been cleared.\n\n"
                    "💬 Send me any message to begin our conversation!"
                )
            
            elif callback_data == "stats":
                # Show chat statistics
                msg_count = self.ai_service.get_conversation_count(user_info['id'])
                stats_text = (
                    f"📊 **Your Chat Statistics**\n\n"
                    f"💬 Messages in current session: {msg_count}\n"
                    f"🆔 User ID: {user_info['id']}\n"
                    f"👤 Username: @{user_info['username']}\n"
                    f"🌐 Detected Language: {self.language_detector.get_language_name('en')}"
                )
                await query.edit_message_text(stats_text, parse_mode='Markdown')
            
            elif callback_data == "language":
                # Show language information
                lang_text = (
                    "🌐 **Language Support**\n\n"
                    "I automatically detect and respond in your language!\n\n"
                    "Supported languages:\n"
                    "🇺🇸 English\n"
                    "🇮🇳 हिंदी (Hindi)\n"
                    "🇵🇰 اردو (Urdu)\n"
                    "🇸🇦 العربية (Arabic)\n"
                    "🇧🇩 বাংলা (Bengali)\n"
                    "🇮🇳 தமிழ் (Tamil)\n"
                    "And many more...\n\n"
                    "Just type in your preferred language!"
                )
                await query.edit_message_text(lang_text, parse_mode='Markdown')
            
            elif callback_data == "help":
                # Show help information
                help_text = (
                    "ℹ️ **How to use this bot:**\n\n"
                    "1. Just send me any message in any language\n"
                    "2. I'll respond intelligently in the same language\n"
                    "3. I remember our conversation context\n"
                    "4. Use /new to start a fresh conversation\n"
                    "5. Use /export to download our chat as PDF\n\n"
                    "**Features:**\n"
                    "• Multi-language support\n"
                    "• Context-aware responses\n"
                    "• Natural conversation flow\n"
                    "• Smart typing indicators\n"
                    "• PDF export functionality\n\n"
                    "💡 **Tip:** I work best with clear, specific questions!"
                )
                await query.edit_message_text(help_text, parse_mode='Markdown')
            
        except Exception as e:
            logger.error(f"Error in button_callback: {e}")
            await query.edit_message_text("Sorry, something went wrong with that action.")
    
    async def new_chat_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /new command to start fresh conversation"""
        try:
            user_info = self.utils.get_user_info(update)
            self.ai_service.clear_conversation(user_info['id'])
            
            detected_lang = self.language_detector.detect_language(
                update.message.text or user_info.get('language_code', 'en')
            )
            
            messages = {
                'hi': f"{Config.SUCCESS_EMOJI} नई चैट शुरू हो गई! अब आप मुझसे कुछ भी पूछ सकते हैं।",
                'ur': f"{Config.SUCCESS_EMOJI} نئی چیٹ شروع ہو گئی! اب آپ مجھ سے کچھ بھی پوچھ سکتے ہیں۔",
                'ar': f"{Config.SUCCESS_EMOJI} بدأت محادثة جديدة! يمكنك الآن أن تسألني أي شيء.",
                'default': f"{Config.SUCCESS_EMOJI} New chat started! You can now ask me anything."
            }
            
            message = messages.get(detected_lang, messages['default'])
            await update.message.reply_text(message)
            
        except Exception as e:
            logger.error(f"Error in new_chat_command: {e}")
            await update.message.reply_text("Sorry, couldn't start new chat. Please try again.")
    
    async def export_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /export command to export chat as PDF"""
        try:
            user_info = self.utils.get_user_info(update)
            
            # Check if there's conversation history
            if user_info['id'] not in self.ai_service.conversation_history:
                await update.message.reply_text(
                    "No conversation history found. Start chatting first!"
                )
                return
            
            await self.utils.simulate_typing(update.effective_chat.id, context)
            
            # Get conversation history
            history = self.ai_service.conversation_history[user_info['id']]
            
            # Format conversation for PDF
            conversation_text = ""
            for msg in history:
                role = "You" if msg['role'] == 'user' else "AI Assistant"
                conversation_text += f"{role}: {msg['content']}\n\n"
            
            # Generate PDF
            pdf_path = await self.utils.generate_pdf(
                conversation_text, 
                f"Chat with AI Assistant - {user_info['username']}"
            )
            
            # Send PDF
            with open(pdf_path, 'rb') as pdf_file:
                await update.message.reply_document(
                    document=pdf_file,
                    filename=f"ai_chat_{user_info['username']}.pdf",
                    caption=f"{Config.SUCCESS_EMOJI} Your chat has been exported as PDF!"
                )
            
            # Clean up temporary file
            import os
            os.remove(pdf_path)
            
        except Exception as e:
            logger.error(f"Error in export_command: {e}")
            await update.message.reply_text("Sorry, couldn't export chat. Please try again.")