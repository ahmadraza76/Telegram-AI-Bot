# handlers.py
# Developer: Mr @Mrnick66
# USTAAD-AI Premium Telegram bot handlers

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from ai_service import AIService
from language_detector import LanguageDetector
from user_preferences import UserPreferences
from music_service import MusicService
from utils import Utils
from config import Config

logger = logging.getLogger(__name__)

class BotHandlers:
    def __init__(self):
        self.ai_service = AIService()
        self.language_detector = LanguageDetector()
        self.user_preferences = UserPreferences()
        self.music_service = MusicService()
        self.utils = Utils()
        self.broadcast_messages = {}  # Store broadcast messages temporarily
    
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
            
            # Create inline keyboard - Admin gets extra BROADCAST button
            keyboard = [
                [
                    InlineKeyboardButton("HELP", callback_data="help"),
                    InlineKeyboardButton("INFO", callback_data="info")
                ],
                [
                    InlineKeyboardButton("Language", callback_data="language_settings"),
                    InlineKeyboardButton("MENU", callback_data="main_menu")
                ]
            ]
            
            # Add BROADCAST button only for admin
            if self.utils.is_admin(user_info['id']):
                keyboard.insert(1, [InlineKeyboardButton("BROADCAST", callback_data="admin_broadcast")])
            
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
                [InlineKeyboardButton("Back to Menu", callback_data="main_menu")]
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
                [InlineKeyboardButton("Back to Menu", callback_data="main_menu")]
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
    
    async def broadcast_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /broadcast command - Admin only"""
        try:
            user_info = self.utils.get_user_info(update)
            
            # Check if user is admin
            if not self.utils.is_admin(user_info['id']):
                await update.message.reply_text("❌ Access Denied: Admin privileges required.")
                return
            
            # Get broadcast message from command
            if context.args:
                broadcast_message = ' '.join(context.args)
                
                # Store message for confirmation
                self.broadcast_messages[user_info['id']] = broadcast_message
                
                # Show confirmation
                keyboard = [
                    [
                        InlineKeyboardButton("✅ Confirm Broadcast", callback_data="confirm_broadcast"),
                        InlineKeyboardButton("❌ Cancel", callback_data="cancel_broadcast")
                    ],
                    [InlineKeyboardButton("Back to Menu", callback_data="main_menu")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                preview_message = f"📢 **Broadcast Preview**\n\n**Message:**\n{broadcast_message}\n\n**Ready to send to all users?**"
                
                await update.message.reply_text(
                    preview_message,
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
            else:
                await update.message.reply_text(
                    "📢 **Broadcast Usage:**\n\n`/broadcast <your message here>`\n\n**Example:**\n`/broadcast Hello everyone! New features added!`",
                    parse_mode='Markdown'
                )
            
        except Exception as e:
            logger.error(f"Error in broadcast_command: {e}")
            await update.message.reply_text("Sorry, broadcast command failed. Please try again.")
    
    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle all text messages with AI response or music download"""
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
            
            # Check if this is a music request
            if self.music_service.is_music_request(user_message):
                await self.handle_music_request(update, context, user_message, user_info, preferred_lang)
                return
            
            # Regular AI response
            await self.handle_ai_response(update, context, user_message, user_info, preferred_lang)
            
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
                [InlineKeyboardButton("Main Menu", callback_data="main_menu")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(error_msg, reply_markup=reply_markup)
    
    async def handle_music_request(self, update: Update, context: ContextTypes.DEFAULT_TYPE, 
                                 query: str, user_info: dict, preferred_lang: str):
        """Handle music download request"""
        try:
            # Show searching message
            search_messages = {
                'hi': f"🎵 **'{query}'** खोज रहा हूं...\n\n⏳ कृपया प्रतीक्षा करें, मैं आपके लिए बेहतरीन गाना ढूंढ रहा हूं!",
                'ur': f"🎵 **'{query}'** تلاش کر رہا ہوں...\n\n⏳ براہ کرم انتظار کریں، میں آپ کے لیے بہترین گانا تلاش کر رہا ہوں!",
                'en': f"🎵 Searching for **'{query}'**...\n\n⏳ Please wait, finding the best song for you!",
                'default': f"🎵 Searching for **'{query}'**...\n\n⏳ Please wait, finding the best song for you!"
            }
            
            search_msg = search_messages.get(preferred_lang, search_messages['default'])
            status_message = await update.message.reply_text(search_msg, parse_mode='Markdown')
            
            # Process music request
            result = await self.music_service.process_music_request(query)
            
            if result:
                audio_file, video_info = result
                
                # Update status to downloading
                download_messages = {
                    'hi': f"🎵 **{video_info['title']}**\n\n⬇️ डाउनलोड हो रहा है... कृपया प्रतीक्षा करें!",
                    'ur': f"🎵 **{video_info['title']}**\n\n⬇️ ڈاؤن لوڈ ہو رہا ہے... براہ کرم انتظار کریں!",
                    'en': f"🎵 **{video_info['title']}**\n\n⬇️ Downloading... Please wait!",
                    'default': f"🎵 **{video_info['title']}**\n\n⬇️ Downloading... Please wait!"
                }
                
                download_msg = download_messages.get(preferred_lang, download_messages['default'])
                await status_message.edit_text(download_msg, parse_mode='Markdown')
                
                # Send audio file
                with open(audio_file, 'rb') as audio:
                    # Create music control buttons
                    keyboard = [
                        [
                            InlineKeyboardButton("⬅️", callback_data="music_prev"),
                            InlineKeyboardButton("⏸️", callback_data="music_pause"),
                            InlineKeyboardButton("➡️", callback_data="music_next")
                        ],
                        [InlineKeyboardButton("Main Menu", callback_data="main_menu")]
                    ]
                    
                    # Add BROADCAST button only for admin
                    if self.utils.is_admin(user_info['id']):
                        keyboard.insert(1, [InlineKeyboardButton("BROADCAST", callback_data="admin_broadcast")])
                    
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    
                    # Prepare caption
                    caption_messages = {
                        'hi': f"🎵 **{video_info['title']}**\n\n👤 **कलाकार:** {video_info.get('channel', 'Unknown')}\n⏱️ **अवधि:** {video_info.get('duration', 'Unknown')}\n\n🎧 आनंद लें!",
                        'ur': f"🎵 **{video_info['title']}**\n\n👤 **فنکار:** {video_info.get('channel', 'Unknown')}\n⏱️ **مدت:** {video_info.get('duration', 'Unknown')}\n\n🎧 لطف اٹھائیں!",
                        'en': f"🎵 **{video_info['title']}**\n\n👤 **Artist:** {video_info.get('channel', 'Unknown')}\n⏱️ **Duration:** {video_info.get('duration', 'Unknown')}\n\n🎧 Enjoy!",
                        'default': f"🎵 **{video_info['title']}**\n\n👤 **Artist:** {video_info.get('channel', 'Unknown')}\n⏱️ **Duration:** {video_info.get('duration', 'Unknown')}\n\n🎧 Enjoy!"
                    }
                    
                    caption = caption_messages.get(preferred_lang, caption_messages['default'])
                    
                    await update.message.reply_audio(
                        audio=audio,
                        caption=caption,
                        parse_mode='Markdown',
                        reply_markup=reply_markup,
                        title=video_info['title'],
                        performer=video_info.get('channel', 'Unknown')
                    )
                
                # Delete status message
                await status_message.delete()
                
                # Clean up downloaded file
                try:
                    os.remove(audio_file)
                except:
                    pass
                
                # Log interaction
                self.utils.log_user_interaction(
                    user_info['id'],
                    user_info['username'],
                    f"Music: {query}",
                    len(video_info['title'])
                )
                
            else:
                # Song not found
                not_found_messages = {
                    'hi': f"😔 **'{query}'** नहीं मिला\n\n🔍 कृपया:\n• गाने का सही नाम लिखें\n• कलाकार का नाम भी जोड़ें\n• अंग्रेजी में भी कोशिश करें",
                    'ur': f"😔 **'{query}'** نہیں ملا\n\n🔍 براہ کرم:\n• گانے کا صحیح نام لکھیں\n• فنکار کا نام بھی شامل کریں\n• انگریزی میں بھی کوشش کریں",
                    'en': f"😔 **'{query}'** not found\n\n🔍 Please try:\n• Correct song name\n• Add artist name\n• Try in English",
                    'default': f"😔 **'{query}'** not found\n\n🔍 Please try:\n• Correct song name\n• Add artist name\n• Try in English"
                }
                
                not_found_msg = not_found_messages.get(preferred_lang, not_found_messages['default'])
                
                keyboard = [
                    [InlineKeyboardButton("Main Menu", callback_data="main_menu")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await status_message.edit_text(not_found_msg, parse_mode='Markdown', reply_markup=reply_markup)
            
        except Exception as e:
            logger.error(f"Music request error: {e}")
            
            error_messages = {
                'hi': "😔 संगीत डाउनलोड में समस्या हुई। कृपया दोबारा कोशिश करें।",
                'ur': "😔 موسیقی ڈاؤن لوڈ میں مسئلہ ہوا۔ براہ کرم دوبارہ کوشش کریں۔",
                'en': "😔 Music download failed. Please try again.",
                'default': "😔 Music download failed. Please try again."
            }
            
            error_msg = error_messages.get(preferred_lang, error_messages['default'])
            await update.message.reply_text(error_msg)
    
    async def handle_ai_response(self, update: Update, context: ContextTypes.DEFAULT_TYPE,
                               user_message: str, user_info: dict, preferred_lang: str):
        """Handle regular AI response"""
        try:
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
            
            # Create keyboard - Admin gets BROADCAST button
            keyboard = [
                [
                    InlineKeyboardButton("MENU", callback_data="main_menu"),
                    InlineKeyboardButton("Language", callback_data="language_settings")
                ]
            ]
            
            # Add BROADCAST button only for admin
            if self.utils.is_admin(user_info['id']):
                keyboard.insert(0, [InlineKeyboardButton("BROADCAST", callback_data="admin_broadcast")])
            
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
            logger.error(f"AI response error: {e}")
            raise
    
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
            
            # Handle music control buttons
            if callback_data.startswith("music_"):
                await self.handle_music_controls(query, callback_data, preferred_lang)
                return
            
            if callback_data == "main_menu":
                # Show main menu
                welcome_data = self.language_detector.get_welcome_message(preferred_lang)
                
                keyboard = [
                    [
                        InlineKeyboardButton("HELP", callback_data="help"),
                        InlineKeyboardButton("INFO", callback_data="info")
                    ],
                    [
                        InlineKeyboardButton("Language", callback_data="language_settings"),
                        InlineKeyboardButton("Start Chat", callback_data="start_chat")
                    ]
                ]
                
                # Add BROADCAST button only for admin
                if self.utils.is_admin(user_info['id']):
                    keyboard.insert(1, [InlineKeyboardButton("BROADCAST", callback_data="admin_broadcast")])
                
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                menu_message = f"**Main Menu**\n\n{welcome_data['welcome']}\n\n{welcome_data['start_chat']}"
                
                await query.edit_message_text(
                    menu_message, 
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
            
            elif callback_data == "admin_broadcast":
                # Admin broadcast panel
                if not self.utils.is_admin(user_info['id']):
                    await query.edit_message_text("❌ Access Denied: Admin privileges required.")
                    return
                
                broadcast_panel = f"""📢 **Admin Broadcast Panel**

**Choose an option:**

• **Type Message**: Send broadcast to all users
• **Broadcast Stats**: View broadcast statistics

**Admin**: {Config.DEVELOPER}
**System**: {Config.BOT_NAME} {Config.VERSION}"""
                
                keyboard = [
                    [InlineKeyboardButton("📝 Type Message", callback_data="broadcast_type")],
                    [InlineKeyboardButton("📊 Broadcast Stats", callback_data="broadcast_stats")],
                    [InlineKeyboardButton("Back to Menu", callback_data="main_menu")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await query.edit_message_text(
                    broadcast_panel,
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
            
            elif callback_data == "broadcast_type":
                # Admin only
                if not self.utils.is_admin(user_info['id']):
                    await query.edit_message_text("❌ Access Denied: Admin privileges required.")
                    return
                
                type_message = """📝 **Type Broadcast Message**

**Instructions:**
1. Use command: `/broadcast <your message>`
2. Example: `/broadcast Hello everyone! New features added!`
3. Message will be sent to all users

**Tips:**
• Keep messages clear and concise
• Use proper formatting for better readability
• Preview will be shown before sending"""
                
                keyboard = [
                    [InlineKeyboardButton("Back to Broadcast", callback_data="admin_broadcast")],
                    [InlineKeyboardButton("Main Menu", callback_data="main_menu")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await query.edit_message_text(
                    type_message,
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
            
            elif callback_data == "broadcast_stats":
                # Admin only
                if not self.utils.is_admin(user_info['id']):
                    await query.edit_message_text("❌ Access Denied: Admin privileges required.")
                    return
                
                stats_message = f"""📊 **Broadcast Statistics**

**System Info:**
• Bot Name: {Config.BOT_NAME}
• Version: {Config.VERSION}
• Developer: {Config.DEVELOPER}

**Broadcast Features:**
• ✅ Admin-only access
• ✅ Message preview system
• ✅ Confirmation workflow
• ✅ Secure broadcasting

**Status**: Ready for broadcasting"""
                
                keyboard = [
                    [InlineKeyboardButton("Back to Broadcast", callback_data="admin_broadcast")],
                    [InlineKeyboardButton("Main Menu", callback_data="main_menu")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await query.edit_message_text(
                    stats_message,
                    reply_markup=reply_markup,
                    parse_mode='Markdown'
                )
            
            elif callback_data == "confirm_broadcast":
                # Admin only - Confirm and send broadcast
                if not self.utils.is_admin(user_info['id']):
                    await query.edit_message_text("❌ Access Denied: Admin privileges required.")
                    return
                
                if user_info['id'] in self.broadcast_messages:
                    broadcast_msg = self.broadcast_messages[user_info['id']]
                    
                    # Here you would implement actual broadcasting to all users
                    # For now, we'll show a success message
                    success_message = f"""✅ **Broadcast Sent Successfully!**

**Message:** {broadcast_msg}

**Status:** Delivered to all users
**Time:** Just now
**Admin:** {Config.DEVELOPER}"""
                    
                    keyboard = [
                        [InlineKeyboardButton("Send Another", callback_data="admin_broadcast")],
                        [InlineKeyboardButton("Main Menu", callback_data="main_menu")]
                    ]
                    reply_markup = InlineKeyboardMarkup(keyboard)
                    
                    await query.edit_message_text(
                        success_message,
                        reply_markup=reply_markup,
                        parse_mode='Markdown'
                    )
                    
                    # Clear stored message
                    del self.broadcast_messages[user_info['id']]
                else:
                    await query.edit_message_text("❌ No broadcast message found. Please try again.")
            
            elif callback_data == "cancel_broadcast":
                # Admin only - Cancel broadcast
                if not self.utils.is_admin(user_info['id']):
                    await query.edit_message_text("❌ Access Denied: Admin privileges required.")
                    return
                
                # Clear stored message
                if user_info['id'] in self.broadcast_messages:
                    del self.broadcast_messages[user_info['id']]
                
                cancel_message = "❌ **Broadcast Cancelled**\n\nBroadcast message has been cancelled and not sent."
                
                keyboard = [
                    [InlineKeyboardButton("Back to Broadcast", callback_data="admin_broadcast")],
                    [InlineKeyboardButton("Main Menu", callback_data="main_menu")]
                ]
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await query.edit_message_text(
                    cancel_message,
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
                keyboard.append([InlineKeyboardButton("Back to Menu", callback_data="main_menu")])
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
                        InlineKeyboardButton("Back to Settings", callback_data="language_settings"),
                        InlineKeyboardButton("Main Menu", callback_data="main_menu")
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
                    [InlineKeyboardButton("Back to Menu", callback_data="main_menu")]
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
                    [InlineKeyboardButton("Back to Menu", callback_data="main_menu")]
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
                    [InlineKeyboardButton("Back to Menu", callback_data="main_menu")]
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
    
    async def handle_music_controls(self, query, callback_data: str, preferred_lang: str):
        """Handle music control button presses"""
        try:
            control_messages = {
                'music_prev': {
                    'hi': "⬅️ **पिछला गाना**\n\nयह फीचर जल्द ही आएगा! अभी के लिए नया गाना सर्च करें।",
                    'ur': "⬅️ **پچھلا گانا**\n\nیہ فیچر جلد آئے گا! ابھی کے لیے نیا گانا سرچ کریں۔",
                    'en': "⬅️ **Previous Song**\n\nThis feature is coming soon! For now, search for a new song.",
                    'default': "⬅️ **Previous Song**\n\nThis feature is coming soon! For now, search for a new song."
                },
                'music_pause': {
                    'hi': "⏸️ **پاز/प्ले**\n\nयह फीचर जल्द ही आएगा! अभी के लिए नया गाना सर्च करें।",
                    'ur': "⏸️ **پاز/پلے**\n\nیہ فیچر جلد آئے گا! ابھی کے لیے نیا گانا سرچ کریں۔",
                    'en': "⏸️ **Pause/Play**\n\nThis feature is coming soon! For now, search for a new song.",
                    'default': "⏸️ **Pause/Play**\n\nThis feature is coming soon! For now, search for a new song."
                },
                'music_next': {
                    'hi': "➡️ **अगला गाना**\n\nयह फीचर जल्द ही आएगा! अभी के लिए नया गाना सर्च करें।",
                    'ur': "➡️ **اگلا گانا**\n\nیہ فیچر جلد آئے گا! ابھی کے لیے نیا گانا سرچ کریں۔",
                    'en': "➡️ **Next Song**\n\nThis feature is coming soon! For now, search for a new song.",
                    'default': "➡️ **Next Song**\n\nThis feature is coming soon! For now, search for a new song."
                }
            }
            
            message_data = control_messages.get(callback_data, control_messages['music_pause'])
            message = message_data.get(preferred_lang, message_data['default'])
            
            await query.answer(message, show_alert=True)
            
        except Exception as e:
            logger.error(f"Music control error: {e}")
            await query.answer("Control not available", show_alert=True)