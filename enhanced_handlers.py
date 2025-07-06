# enhanced_handlers.py
# Developer: Mr AHMAD 
# Enhanced USTAAD-AI Premium Telegram bot handlers with omni-domain expertise

import logging
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from ai_service import AIService
from language_detector import LanguageDetector
from user_preferences import UserPreferences
from utils import Utils
from config import Config
from knowledge_domains import KnowledgeDomainClassifier

logger = logging.getLogger(__name__)

class EnhancedBotHandlers:
    def __init__(self):
        self.ai_service = AIService()
        self.language_detector = LanguageDetector()
        self.user_preferences = UserPreferences()
        self.utils = Utils()
        self.domain_classifier = KnowledgeDomainClassifier()
        self.broadcast_messages = {}
        self.user_sessions = {}  # Track user sessions and context
        
        logger.info("🎯 Enhanced Bot handlers initialized with omni-domain expertise")
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Enhanced /start command with comprehensive introduction"""
        try:
            user_info = self.utils.get_user_info(update)
            
            # Initialize user session
            self.user_sessions[user_info['id']] = {
                'start_time': update.message.date,
                'query_count': 0,
                'domains_explored': set(),
                'knowledge_level': 'intermediate'
            }
            
            # Get user's preferred language or detect
            preferred_lang = self.user_preferences.get_user_language(user_info['id'])
            if not preferred_lang:
                preferred_lang = self.language_detector.detect_language(
                    update.message.text or user_info.get('language_code', 'hi')
                )
            
            # Simulate typing
            await self.utils.simulate_typing(update.effective_chat.id, context, duration=2)
            
            # Get enhanced welcome message
            welcome_data = self._get_enhanced_welcome_message(preferred_lang)
            
            # Create enhanced inline keyboard
            keyboard = [
                [
                    InlineKeyboardButton("🎓 Academic Help", callback_data="domain_academic"),
                    InlineKeyboardButton("💻 Tech Support", callback_data="domain_technology")
                ],
                [
                    InlineKeyboardButton("🎨 Creative Zone", callback_data="domain_creative"),
                    InlineKeyboardButton("💼 Business Guide", callback_data="domain_business")
                ],
                [
                    InlineKeyboardButton("💪 Life Coach", callback_data="domain_life"),
                    InlineKeyboardButton("🌍 Cultural Guide", callback_data="domain_culture")
                ],
                [
                    InlineKeyboardButton("🆘 Help & Commands", callback_data="help"),
                    InlineKeyboardButton("ℹ️ About USTAAD-AI", callback_data="info")
                ],
                [
                    InlineKeyboardButton("🌐 Language Settings", callback_data="language_settings"),
                    InlineKeyboardButton("📊 My Stats", callback_data="user_stats")
                ]
            ]
            
            # Add admin broadcast button
            if self.utils.is_admin(user_info['id']):
                keyboard.insert(-1, [InlineKeyboardButton("📢 Admin Broadcast", callback_data="admin_broadcast")])
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Send enhanced welcome message
            await update.message.reply_text(
                welcome_data,
                reply_markup=reply_markup,
                parse_mode='Markdown'
            )
            
            # Log interaction
            self.utils.log_user_interaction(
                user_info['id'], 
                user_info['username'], 
                "/start", 
                len(welcome_data)
            )
            
        except Exception as e:
            logger.error(f"❌ Error in enhanced start_command: {e}")
            await update.message.reply_text("⚠️ Sorry, something went wrong. Please try again.")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Enhanced message handler with domain classification and expertise"""
        try:
            user_info = self.utils.get_user_info(update)
            user_message = update.message.text
            
            logger.info(f"📨 Processing query from user {user_info['id']}: '{user_message[:100]}...'")
            
            # Update user session
            if user_info['id'] in self.user_sessions:
                self.user_sessions[user_info['id']]['query_count'] += 1
            
            # Get user's preferred language
            preferred_lang = self.user_preferences.get_user_language(user_info['id'])
            if not preferred_lang:
                detected_lang = self.language_detector.detect_language(user_message)
                self.user_preferences.set_user_language(user_info['id'], detected_lang)
                preferred_lang = detected_lang
            
            # Classify query into knowledge domain
            domain, confidence = self.domain_classifier.classify_query(user_message, preferred_lang)
            
            # Update user's explored domains
            if user_info['id'] in self.user_sessions:
                self.user_sessions[user_info['id']]['domains_explored'].add(domain)
            
            logger.info(f"🎯 Classified query as '{domain}' with confidence {confidence:.2f}")
            
            # Process enhanced AI response
            await self.handle_enhanced_ai_response(
                update, context, user_message, user_info, preferred_lang, domain, confidence
            )
            
        except Exception as e:
            logger.error(f"❌ Error in enhanced handle_message: {e}")
            await self._send_error_response(update, user_info, preferred_lang)

    async def handle_enhanced_ai_response(self, update: Update, context: ContextTypes.DEFAULT_TYPE,
                                        user_message: str, user_info: dict, preferred_lang: str,
                                        domain: str, confidence: float):
        """Enhanced AI response with domain expertise"""
        try:
            # Show domain-specific typing indicator
            typing_duration = 4 if confidence > 0.5 else 3
            await self.utils.simulate_typing(update.effective_chat.id, context, duration=typing_duration)
            
            # Get enhanced AI response
            ai_response = await self.ai_service.get_ai_response(
                user_info['id'], 
                user_message, 
                preferred_lang
            )
            
            # Enhance response with domain-specific context
            if confidence > 0.3:
                ai_response = self.domain_classifier.enhance_response_with_domain_context(
                    ai_response, domain, preferred_lang
                )
            
            # Format response with enhanced emojis and structure
            formatted_response = self._format_enhanced_response(ai_response, domain, preferred_lang)
            
            # Split long messages intelligently
            message_chunks = self.utils.split_long_message(formatted_response)
            
            # Create enhanced keyboard with domain-specific options
            keyboard = self._create_enhanced_keyboard(domain, user_info['id'], preferred_lang)
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            # Send response(s) with enhanced formatting
            for i, chunk in enumerate(message_chunks):
                if i > 0:
                    await self.utils.simulate_typing(update.effective_chat.id, context, duration=1)
                
                # Add enhanced menu buttons only to the last chunk
                current_markup = reply_markup if i == len(message_chunks) - 1 else None
                
                await update.message.reply_text(
                    chunk,
                    reply_markup=current_markup,
                    parse_mode='Markdown'
                )
            
            # Log enhanced interaction
            self.utils.log_user_interaction(
                user_info['id'],
                user_info['username'],
                f"[{domain}] {user_message}",
                len(ai_response)
            )
            
        except Exception as e:
            logger.error(f"❌ Enhanced AI response error: {e}")
            await self._send_error_response(update, user_info, preferred_lang)

    def _get_enhanced_welcome_message(self, language: str) -> str:
        """Get enhanced welcome message with comprehensive capabilities"""
        messages = {
            'hi': f"""🎯 **{Config.BOT_NAME} {Config.VERSION} में आपका स्वागत है!** 🎯

🚀 **मैं आपका Omni-Domain AI Mentor हूं!**

{Config.GURU_EMOJI} **Academic Excellence**: UPSC, JEE, NEET से PhD तक
{Config.TECH_EMOJI} **Technology Mastery**: Programming, AI/ML, Cybersecurity
{Config.CREATIVE_EMOJI} **Creative Powerhouse**: Writing, Shayari, Content Creation
{Config.CULTURE_EMOJI} **Cultural Guide**: 12+ भारतीय भाषाओं में expertise
💼 **Business Mentor**: Startup से Corporate strategy तक
💪 **Life Coach**: Career, Relationships, Personal Growth

🔥 **ChatGPT-Level Intelligence + Indian Context**

💬 **कुछ भी पूछें - मैं हर domain का expert हूं!**
📚 Academic problems से लेकर life advice तक, सब कुछ!

{Config.POWERED_BY} | Developer: {Config.DEVELOPER}""",
            
            'ur': f"""🎯 **{Config.BOT_NAME} {Config.VERSION} میں خوش آمدید!** 🎯

🚀 **میں آپ کا Omni-Domain AI Mentor ہوں!**

{Config.GURU_EMOJI} **Academic Excellence**: UPSC, JEE, NEET سے PhD تک
{Config.TECH_EMOJI} **Technology Mastery**: Programming, AI/ML, Cybersecurity
{Config.CREATIVE_EMOJI} **Creative Powerhouse**: Writing, شاعری, Content Creation
{Config.CULTURE_EMOJI} **Cultural Guide**: 12+ ہندوستانی زبانوں میں expertise
💼 **Business Mentor**: Startup سے Corporate strategy تک
💪 **Life Coach**: Career, Relationships, Personal Growth

🔥 **ChatGPT-Level Intelligence + Indian Context**

💬 **کچھ بھی پوچھیں - میں ہر domain کا expert ہوں!**
📚 Academic problems سے لے کر life advice تک، سب کچھ!

{Config.POWERED_BY} | Developer: {Config.DEVELOPER}""",
            
            'default': f"""🎯 **Welcome to {Config.BOT_NAME} {Config.VERSION}!** 🎯

🚀 **I'm your Omni-Domain AI Mentor!**

{Config.GURU_EMOJI} **Academic Excellence**: From UPSC, JEE, NEET to PhD level
{Config.TECH_EMOJI} **Technology Mastery**: Programming, AI/ML, Cybersecurity
{Config.CREATIVE_EMOJI} **Creative Powerhouse**: Writing, Poetry, Content Creation
{Config.CULTURE_EMOJI} **Cultural Guide**: Expertise in 12+ Indian languages
💼 **Business Mentor**: From Startups to Corporate strategy
💪 **Life Coach**: Career, Relationships, Personal Growth

🔥 **ChatGPT-Level Intelligence + Indian Context**

💬 **Ask me anything - I'm an expert in every domain!**
📚 From academic problems to life advice, everything!

{Config.POWERED_BY} | Developer: {Config.DEVELOPER}"""
        }
        return messages.get(language, messages['default'])

    def _format_enhanced_response(self, response: str, domain: str, language: str) -> str:
        """Format response with enhanced structure and emojis"""
        
        # Add domain-specific emoji if not already present
        domain_emojis = {
            "academic_stem": Config.GURU_EMOJI,
            "competitive_exams": "📚",
            "technology": Config.TECH_EMOJI,
            "creative_arts": Config.CREATIVE_EMOJI,
            "business_finance": "💼",
            "life_skills": "💪",
            "cultural_social": Config.CULTURE_EMOJI,
            "current_affairs": "📰",
            "health_wellness": "🏥"
        }
        
        # Enhance formatting based on content
        if domain in domain_emojis and not response.startswith(domain_emojis[domain]):
            response = f"{domain_emojis[domain]} {response}"
        
        # Add motivational footer for learning-related queries
        learning_keywords = ['learn', 'study', 'understand', 'सीखना', 'समझना', 'سیکھنا']
        if any(keyword in response.lower() for keyword in learning_keywords):
            if language == 'hi':
                response += f"\n\n🌟 **{Config.BOT_NAME} Motivation**: सफलता का रास्ता knowledge से होकर जाता है! 💪"
            elif language == 'ur':
                response += f"\n\n🌟 **{Config.BOT_NAME} Motivation**: کامیابی کا راستہ علم سے ہوکر جاتا ہے! 💪"
            else:
                response += f"\n\n🌟 **{Config.BOT_NAME} Motivation**: The path to success goes through knowledge! 💪"
        
        return response

    def _create_enhanced_keyboard(self, domain: str, user_id: int, language: str) -> list:
        """Create enhanced keyboard with domain-specific options"""
        
        # Base keyboard
        keyboard = [
            [
                InlineKeyboardButton("📋 Main Menu", callback_data="main_menu"),
                InlineKeyboardButton("🔄 New Topic", callback_data="new_topic")
            ]
        ]
        
        # Add domain-specific quick actions
        domain_actions = {
            "academic_stem": [
                InlineKeyboardButton("📚 More Examples", callback_data="more_examples"),
                InlineKeyboardButton("🧮 Practice Problems", callback_data="practice_problems")
            ],
            "competitive_exams": [
                InlineKeyboardButton("📅 Study Plan", callback_data="study_plan"),
                InlineKeyboardButton("🎯 Exam Tips", callback_data="exam_tips")
            ],
            "technology": [
                InlineKeyboardButton("💻 Code Examples", callback_data="code_examples"),
                InlineKeyboardButton("🔗 Resources", callback_data="tech_resources")
            ],
            "creative_arts": [
                InlineKeyboardButton("🎨 Creative Exercise", callback_data="creative_exercise"),
                InlineKeyboardButton("✍️ Writing Tips", callback_data="writing_tips")
            ],
            "business_finance": [
                InlineKeyboardButton("📊 Case Study", callback_data="case_study"),
                InlineKeyboardButton("💡 Business Ideas", callback_data="business_ideas")
            ],
            "life_skills": [
                InlineKeyboardButton("🎯 Action Plan", callback_data="action_plan"),
                InlineKeyboardButton("💪 Motivation", callback_data="motivation_boost")
            ]
        }
        
        if domain in domain_actions:
            keyboard.insert(0, domain_actions[domain])
        
        # Add language and stats options
        keyboard.append([
            InlineKeyboardButton("🌐 Language", callback_data="language_settings"),
            InlineKeyboardButton("📊 My Progress", callback_data="user_stats")
        ])
        
        # Add admin broadcast button for admin users
        if self.utils.is_admin(user_id):
            keyboard.append([InlineKeyboardButton("📢 Admin Panel", callback_data="admin_broadcast")])
        
        return keyboard

    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Enhanced button callback handler with domain-specific actions"""
        try:
            query = update.callback_query
            await query.answer()
            
            user_info = self.utils.get_user_info(update)
            callback_data = query.data
            
            # Get user's preferred language
            preferred_lang = self.user_preferences.get_user_language(user_info['id']) or 'hi'
            
            # Handle domain-specific callbacks
            if callback_data.startswith("domain_"):
                await self._handle_domain_selection(query, callback_data, user_info, preferred_lang)
            
            elif callback_data == "user_stats":
                await self._show_user_stats(query, user_info, preferred_lang)
            
            elif callback_data == "new_topic":
                await self._handle_new_topic(query, user_info, preferred_lang)
            
            elif callback_data in ["more_examples", "practice_problems", "study_plan", "exam_tips",
                                 "code_examples", "tech_resources", "creative_exercise", "writing_tips",
                                 "case_study", "business_ideas", "action_plan", "motivation_boost"]:
                await self._handle_quick_actions(query, callback_data, user_info, preferred_lang)
            
            # Handle existing callbacks (main_menu, help, info, etc.)
            else:
                await self._handle_standard_callbacks(query, callback_data, user_info, preferred_lang)
                
        except Exception as e:
            logger.error(f"❌ Error in enhanced button_callback: {e}")
            await query.edit_message_text("⚠️ Sorry, something went wrong with that action.")

    async def _handle_domain_selection(self, query, callback_data: str, user_info: dict, language: str):
        """Handle domain selection callbacks"""
        domain = callback_data.replace("domain_", "")
        
        domain_info = {
            "academic": {
                "title": "🎓 Academic Excellence Zone",
                "description": "UPSC, JEE, NEET, School/College subjects, Research help",
                "examples": ["Solve calculus problems", "UPSC preparation strategy", "Physics concepts"]
            },
            "technology": {
                "title": "💻 Technology Mastery Hub",
                "description": "Programming, AI/ML, Cybersecurity, Web development",
                "examples": ["Python coding help", "Machine learning concepts", "Web development guide"]
            },
            "creative": {
                "title": "🎨 Creative Powerhouse",
                "description": "Writing, Poetry, Content creation, Storytelling",
                "examples": ["Write a shayari", "Content strategy", "Creative writing tips"]
            },
            "business": {
                "title": "💼 Business Strategy Center",
                "description": "Startup guidance, Marketing, Finance, Management",
                "examples": ["Business plan help", "Marketing strategies", "Investment advice"]
            },
            "life": {
                "title": "💪 Life Coaching Zone",
                "description": "Career guidance, Relationships, Personal development",
                "examples": ["Career planning", "Interview preparation", "Goal setting"]
            },
            "culture": {
                "title": "🌍 Cultural Wisdom Hub",
                "description": "Indian culture, Traditions, Languages, Philosophy",
                "examples": ["Festival significance", "Cultural traditions", "Philosophy concepts"]
            }
        }
        
        info = domain_info.get(domain, domain_info["academic"])
        
        message = f"""**{info['title']}**

📋 **What I can help with:**
{info['description']}

💡 **Example queries:**
• {info['examples'][0]}
• {info['examples'][1]}
• {info['examples'][2]}

💬 **Just type your question and I'll provide expert guidance!**"""
        
        keyboard = [
            [InlineKeyboardButton("💬 Ask Question", callback_data="new_topic")],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu")]
        ]
        
        await query.edit_message_text(
            message,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )

    async def _show_user_stats(self, query, user_info: dict, language: str):
        """Show user statistics and progress"""
        user_id = user_info['id']
        session = self.user_sessions.get(user_id, {})
        ai_stats = self.ai_service.get_user_stats(user_id)
        
        stats_message = f"""📊 **Your USTAAD-AI Journey**

👤 **User**: {user_info['first_name']} (@{user_info['username']})

📈 **Session Stats:**
• Queries Asked: {session.get('query_count', 0)}
• Domains Explored: {len(session.get('domains_explored', set()))}
• Knowledge Level: {ai_stats.get('knowledge_level', 'Intermediate')}

🎯 **Domains You've Explored:**
{', '.join(session.get('domains_explored', {'General'})) or 'None yet'}

💬 **Total Conversations**: {ai_stats.get('conversation_count', 0)}

🌟 **Your Learning Journey**: Keep exploring different domains to become a well-rounded learner!

{Config.POWERED_BY}"""
        
        keyboard = [
            [InlineKeyboardButton("🔄 Reset Stats", callback_data="reset_stats")],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu")]
        ]
        
        await query.edit_message_text(
            stats_message,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )

    async def _handle_quick_actions(self, query, action: str, user_info: dict, language: str):
        """Handle quick action buttons"""
        
        action_responses = {
            "more_examples": "📚 I'll provide more detailed examples in our next conversation. Just ask for specific examples!",
            "practice_problems": "🧮 Ready to practice? Ask me for practice problems in any subject!",
            "study_plan": "📅 I can create a personalized study plan. Tell me your exam and timeline!",
            "exam_tips": "🎯 Ask me for specific exam strategies and I'll share proven tips!",
            "code_examples": "💻 Need code examples? Just specify the programming language and problem!",
            "tech_resources": "🔗 Ask me for resources on any technology topic!",
            "creative_exercise": "🎨 Ready for a creative challenge? Ask me for writing prompts or exercises!",
            "writing_tips": "✍️ I'll share writing tips based on your specific needs. Just ask!",
            "case_study": "📊 Want a business case study? Tell me the industry or topic!",
            "business_ideas": "💡 Looking for business ideas? Share your interests and I'll suggest opportunities!",
            "action_plan": "🎯 I'll help create an action plan. Tell me your goal!",
            "motivation_boost": "💪 Need motivation? Ask me for inspirational guidance!"
        }
        
        response = action_responses.get(action, "💬 Just ask me anything and I'll help!")
        
        keyboard = [
            [InlineKeyboardButton("💬 Ask Now", callback_data="new_topic")],
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu")]
        ]
        
        await query.edit_message_text(
            response,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )

    async def _handle_new_topic(self, query, user_info: dict, language: str):
        """Handle new topic selection"""
        message = f"""💬 **Ready for a New Question!**

🎯 **I'm your expert in ALL domains:**
• 📚 Academic & Competitive Exams
• 💻 Technology & Programming  
• 🎨 Creative Arts & Writing
• 💼 Business & Finance
• 💪 Life Skills & Career
• 🌍 Culture & Current Affairs

**Just type your question and I'll provide expert guidance!**

{Config.TAGLINE}"""
        
        keyboard = [
            [InlineKeyboardButton("🔙 Back to Menu", callback_data="main_menu")]
        ]
        
        await query.edit_message_text(
            message,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )

    async def _handle_standard_callbacks(self, query, callback_data: str, user_info: dict, language: str):
        """Handle standard callback queries (existing functionality)"""
        # This would include all the existing callback handling logic
        # from the original handlers.py file
        pass

    async def _send_error_response(self, update: Update, user_info: dict, language: str):
        """Send enhanced error response"""
        error_messages = {
            'hi': f"""🙏 माफ़ करें, मुझे कुछ technical difficulty हो रही है।

🔧 **समाधान:**
• कुछ seconds wait करें और फिर try करें
• अगर problem persist करे तो @Mrnick66 को contact करें

💡 **Meanwhile**: मैं जल्दी ही आपकी service में वापस आऊंगा!

{Config.POWERED_BY} | Always Learning, Always Improving""",
            
            'default': f"""🙏 Sorry, I'm experiencing some technical difficulties.

🔧 **Solutions:**
• Wait a few seconds and try again
• If problem persists, contact @Mrnick66

💡 **Meanwhile**: I'll be back to serve you shortly!

{Config.POWERED_BY} | Always Learning, Always Improving"""
        }
        
        error_msg = error_messages.get(language, error_messages['default'])
        
        keyboard = [
            [InlineKeyboardButton("🔄 Try Again", callback_data="new_topic")],
            [InlineKeyboardButton("📋 Main Menu", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(error_msg, reply_markup=reply_markup, parse_mode='Markdown')