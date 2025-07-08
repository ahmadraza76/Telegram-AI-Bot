# enhanced_handlers.py
# Developer: Ahmad Raza
# Enhanced Ostaad AI Premium Telegram bot handlers with pure desi expertise

import logging
import os
import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from ai_service import OstaadAIService
from language_detector import LanguageDetector
from user_preferences import UserPreferences
from utils import Utils
from config import Config

logger = logging.getLogger(__name__)

class EnhancedOstaadHandlers:
    def __init__(self):
        self.ai_service = OstaadAIService()
        self.language_detector = LanguageDetector()
        self.user_preferences = UserPreferences()
        self.utils = Utils()
        self.broadcast_messages = {}
        self.user_sessions = {}
        
        logger.info("🎯 Enhanced Ostaad AI handlers initialized with pure desi expertise")
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Enhanced /start command with desi welcome"""
        try:
            user_info = self.utils.get_user_info(update)
            
            # Initialize user session
            self.user_sessions[user_info['id']] = {
                'start_time': update.message.date,
                'query_count': 0,
                'categories_explored': set(),
                'mood_history': []
            }
            
            # Get user's preferred language
            preferred_lang = self.user_preferences.get_user_language(user_info['id'])
            if not preferred_lang:
                preferred_lang = self.language_detector.detect_language(
                    update.message.text or user_info.get('language_code', 'hi')
                )
            
            # Simulate typing
            await self.utils.simulate_typing(update.effective_chat.id, context, duration=2)
            
            # Get enhanced welcome message
            welcome_data = self._get_desi_welcome_message(preferred_lang, user_info['first_name'])
            
            # Create clean inline keyboard without emojis
            keyboard = [
                [
                    InlineKeyboardButton("Padhai Help", callback_data="category_education"),
                    InlineKeyboardButton("Career Guide", callback_data="category_career")
                ],
                [
                    InlineKeyboardButton("Tech Support", callback_data="category_tech"),
                    InlineKeyboardButton("Earning Tips", callback_data="category_earning")
                ],
                [
                    InlineKeyboardButton("Love Advice", callback_data="category_love"),
                    InlineKeyboardButton("Language Help", callback_data="category_language")
                ],
                [
                    InlineKeyboardButton("Entertainment", callback_data="category_fun"),
                    InlineKeyboardButton("Motivation", callback_data="category_motivation")
                ],
                [
                    InlineKeyboardButton("Help & Commands", callback_data="help"),
                    InlineKeyboardButton("About Ostaad AI", callback_data="info")
                ],
                [
                    InlineKeyboardButton("Language Settings", callback_data="language_settings"),
                    InlineKeyboardButton("My Journey", callback_data="user_stats")
                ]
            ]
            
            # Add admin panel for admin users only
            if self.utils.is_admin(user_info['id']):
                keyboard.append([InlineKeyboardButton("Admin Panel", callback_data="admin_panel")])
            
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
            await update.message.reply_text("⚠️ Arre yaar, kuch gadbad ho gayi! Phir se try karo 🙏")

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Enhanced message handler with desi expertise"""
        try:
            user_info = self.utils.get_user_info(update)
            user_message = update.message.text
            
            logger.info(f"📨 Processing desi query from user {user_info['id']}: '{user_message[:100]}...'")
            
            # Update user session
            if user_info['id'] in self.user_sessions:
                self.user_sessions[user_info['id']]['query_count'] += 1
            
            # Get user's preferred language
            preferred_lang = self.user_preferences.get_user_language(user_info['id'])
            if not preferred_lang:
                detected_lang = self.language_detector.detect_language(user_message)
                self.user_preferences.set_user_language(user_info['id'], detected_lang)
                preferred_lang = detected_lang
            
            # Classify query category
            category = self._classify_query_category(user_message)
            
            # Update user's explored categories
            if user_info['id'] in self.user_sessions:
                self.user_sessions[user_info['id']]['categories_explored'].add(category)
            
            logger.info(f"🎯 Classified query as '{category}' category")
            
            # Process enhanced AI response
            await self.handle_enhanced_ai_response(
                update, context, user_message, user_info, preferred_lang, category
            )
            
        except Exception as e:
            logger.error(f"❌ Error in enhanced handle_message: {e}")
            await self._send_desi_error_response(update, user_info, preferred_lang)

    async def handle_enhanced_ai_response(self, update: Update, context: ContextTypes.DEFAULT_TYPE,
                                        user_message: str, user_info: dict, preferred_lang: str,
                                        category: str):
        """Enhanced AI response with desi expertise"""
        try:
            # Show category-specific typing indicator
            typing_duration = 4 if len(user_message) > 100 else 3
            await self.utils.simulate_typing(update.effective_chat.id, context, duration=typing_duration)
            
            # Get enhanced AI response from Ostaad AI
            ai_response = await self.ai_service.get_ai_response(
                user_info['id'], 
                user_message, 
                preferred_lang
            )
            
            # Format response with enhanced desi style
            formatted_response = self._format_desi_response(ai_response, category, preferred_lang)
            
            # Split long messages intelligently
            message_chunks = self.utils.split_long_message(formatted_response)
            
            # Create enhanced keyboard with category-specific options
            keyboard = self._create_clean_keyboard(category, user_info['id'], preferred_lang)
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
                f"[{category}] {user_message}",
                len(ai_response)
            )
            
        except Exception as e:
            logger.error(f"❌ Enhanced AI response error: {e}")
            await self._send_desi_error_response(update, user_info, preferred_lang)

    def _get_desi_welcome_message(self, language: str, first_name: str) -> str:
        """Get enhanced welcome message with pure desi style"""
        name = first_name or "bhai"
        
        messages = {
            'hi': f"""🎯 **Namaste {name}! Ustad AI {Config.VERSION} mein aapka swagat hai!** 🎯

🚀 **Main tumhara Digital Ustad hoon!**

Are bhai 😎 Main har sawal ka jawab de sakta hoon!

🧠 **Meri expertise:**
🎓 **Padhai Master**: School se PhD tak - sab subjects covered!
💼 **Career Guru**: Job, interview, resume - sab guidance ready!
💻 **Tech Expert**: Programming, AI, bots - technical sab kuch!
💰 **Earning Guide**: Online paise kamane ke sab tareeke!
❤️ **Love Advisor**: Relationships, dosti - dil ki baat samjhta hoon!
🗣️ **Language Teacher**: English, Hindi - fluency improve karo!
🎬 **Entertainment**: Movies, memes, jokes - timepass bhi hai!
💪 **Motivator**: Life coach, success mindset - confidence boost!

🔥 **Bilkul human jaisa conversation - emotions, jokes, sab samjhta hoon!**

💬 **Kuch bhi poocho - main tumhara digital dost hoon!**
📚 Padhai se lekar life advice tak, har field mein expert!

{Config.POWERED_BY} | Developer: {Config.DEVELOPER}""",
            
            'default': f"""🎯 **Hello {name}! Welcome to Ostaad AI {Config.VERSION}!** 🎯

🚀 **I'm your Digital Ustad!**

Hey bhai 😎 I can answer any question!

🧠 **My expertise:**
🎓 **Study Master**: From school to PhD - all subjects covered!
💼 **Career Guru**: Jobs, interviews, resume - complete guidance!
💻 **Tech Expert**: Programming, AI, bots - all technical stuff!
💰 **Earning Guide**: All ways to earn money online!
❤️ **Love Advisor**: Relationships, friendship - understand emotions!
🗣️ **Language Teacher**: English, Hindi - improve fluency!
🎬 **Entertainment**: Movies, memes, jokes - fun time too!
💪 **Motivator**: Life coach, success mindset - confidence boost!

🔥 **Completely human-like conversation - emotions, jokes, everything!**

💬 **Ask anything - I'm your digital friend!**
📚 From studies to life advice, expert in every field!

{Config.POWERED_BY} | Developer: {Config.DEVELOPER}"""
        }
        return messages.get(language, messages['default'])

    def _classify_query_category(self, message: str) -> str:
        """Classify user query into categories"""
        message_lower = message.lower()
        
        category_keywords = {
            "padhai_education": ["study", "exam", "school", "college", "padhai", "homework", "assignment", 
                               "upsc", "jee", "neet", "mathematics", "physics", "chemistry"],
            "career_job": ["job", "career", "interview", "resume", "cv", "naukri", "salary", "promotion"],
            "programming_tech": ["code", "programming", "python", "javascript", "website", "app", "bot", 
                               "algorithm", "software", "tech", "computer"],
            "online_earning": ["earn", "money", "income", "freelance", "business", "startup", "investment", 
                             "crypto", "trading", "paise"],
            "love_relationships": ["love", "girlfriend", "boyfriend", "relationship", "breakup", "marriage", 
                                 "dating", "crush", "propose"],
            "language_learning": ["english", "hindi", "grammar", "speaking", "writing", "translation", 
                                "language", "vocabulary"],
            "entertainment": ["movie", "song", "meme", "joke", "funny", "entertainment", "timepass", 
                            "bollywood", "music"],
            "motivation": ["motivation", "confidence", "success", "goal", "depression", "stress", 
                         "inspiration", "life"],
            "health_fitness": ["health", "fitness", "exercise", "diet", "weight", "gym", "yoga", "medicine"],
            "general_knowledge": ["news", "current", "gk", "general", "world", "india", "politics", "history"],
            "religion_culture": ["religion", "god", "festival", "culture", "tradition", "spiritual", 
                               "hindu", "muslim", "christian"],
            "jokes_fun": ["joke", "funny", "meme", "roast", "comedy", "laugh", "fun", "riddle", "puzzle"]
        }
        
        # Count matches for each category
        category_scores = {}
        for category, keywords in category_keywords.items():
            score = sum(1 for keyword in keywords if keyword in message_lower)
            if score > 0:
                category_scores[category] = score
        
        # Return category with highest score, or general if no matches
        if category_scores:
            return max(category_scores, key=category_scores.get)
        else:
            return "general_knowledge"

    def _format_desi_response(self, response: str, category: str, language: str) -> str:
        """Format response with enhanced desi style and emojis"""
        
        # Add category-specific emoji if not already present
        category_emojis = Config.CATEGORY_EMOJIS.get(category, ["💬"])
        if not any(emoji in response[:10] for emoji in category_emojis):
            response = f"{category_emojis[0]} {response}"
        
        # Add category-specific tips and context
        category_tips = {
            "padhai_education": "\n\n📚 **Padhai Tip**: Regular practice aur revision karte raho bhai! 💪",
            "career_job": "\n\n💼 **Career Advice**: Confidence rakho aur preparation solid karo! 📈",
            "programming_tech": "\n\n💻 **Tech Tip**: Daily coding practice karo - consistency is key! 🔥",
            "online_earning": "\n\n💰 **Earning Tip**: Patience rakho aur skills develop karte raho! ✨",
            "love_relationships": "\n\n❤️ **Love Advice**: Dil ki suno lekin dimag bhi use karo! 🤗",
            "language_learning": "\n\n📖 **Language Tip**: Daily practice aur confidence building important hai! 🗣️",
            "entertainment": "\n\n🎬 **Fun Fact**: Entertainment bhi learning ka part hai! 😄",
            "motivation": "\n\n💪 **Motivation**: Har din ek step aage badhte raho! 🔥",
            "health_fitness": "\n\n🏃‍♂️ **Health Tip**: Consistency aur balance maintain karo! 🍎",
            "religion_culture": "\n\n🕉️ **Cultural Wisdom**: Traditions mein bahut gyaan chupa hai! 🙏"
        }
        
        if category in category_tips:
            response += category_tips[category]
        
        # Add signature for longer responses
        if len(response) > 300:
            response += f"\n\n🎯 **Ostaad AI** | Hamesha tumhare saath! 🤝"
        
        return response

    def _create_clean_keyboard(self, category: str, user_id: int, language: str) -> list:
        """Create clean keyboard without emojis - glass-type buttons"""
        
        # Base keyboard with back button
        keyboard = [
            [
                InlineKeyboardButton("◀️ Main Menu", callback_data="main_menu"),
                InlineKeyboardButton("🔄 New Question", callback_data="new_question")
            ]
        ]
        
        # Add category-specific quick actions
        category_actions = {
            "padhai_education": [
                InlineKeyboardButton("More Examples", callback_data="more_examples"),
                InlineKeyboardButton("Practice Questions", callback_data="practice_questions")
            ],
            "career_job": [
                InlineKeyboardButton("Interview Tips", callback_data="interview_tips"),
                InlineKeyboardButton("Resume Help", callback_data="resume_help")
            ],
            "programming_tech": [
                InlineKeyboardButton("Code Examples", callback_data="code_examples"),
                InlineKeyboardButton("Tech Resources", callback_data="tech_resources")
            ],
            "online_earning": [
                InlineKeyboardButton("Earning Ideas", callback_data="earning_ideas"),
                InlineKeyboardButton("Business Tips", callback_data="business_tips")
            ],
            "love_relationships": [
                InlineKeyboardButton("Love Tips", callback_data="love_tips"),
                InlineKeyboardButton("Relationship Advice", callback_data="relationship_advice")
            ],
            "entertainment": [
                InlineKeyboardButton("More Fun", callback_data="more_fun"),
                InlineKeyboardButton("Jokes", callback_data="jokes")
            ],
            "motivation": [
                InlineKeyboardButton("Motivation Boost", callback_data="motivation_boost"),
                InlineKeyboardButton("Goal Setting", callback_data="goal_setting")
            ]
        }
        
        if category in category_actions:
            keyboard.insert(0, category_actions[category])
        
        return keyboard

    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Enhanced button callback handler with desi actions"""
        try:
            query = update.callback_query
            await query.answer()
            
            user_info = self.utils.get_user_info(update)
            callback_data = query.data
            
            # Get user's preferred language
            preferred_lang = self.user_preferences.get_user_language(user_info['id']) or 'hi'
            
            # Handle category-specific callbacks
            if callback_data.startswith("category_"):
                await self._handle_category_selection(query, callback_data, user_info, preferred_lang)
            
            elif callback_data == "user_stats":
                await self._show_user_journey(query, user_info, preferred_lang)
            
            elif callback_data == "new_question":
                await self._handle_new_question(query, user_info, preferred_lang)
            
            elif callback_data == "admin_panel":
                await self._handle_admin_panel(query, user_info, preferred_lang)
            
            elif callback_data == "broadcast":
                await self._handle_broadcast_menu(query, user_info, preferred_lang)
            
            elif callback_data in ["more_examples", "practice_questions", "interview_tips", "resume_help",
                                 "code_examples", "tech_resources", "earning_ideas", "business_tips",
                                 "love_tips", "relationship_advice", "more_fun", "jokes",
                                 "motivation_boost", "goal_setting"]:
                await self._handle_quick_actions(query, callback_data, user_info, preferred_lang)
            
            # Handle existing callbacks (main_menu, help, info, etc.)
            else:
                await self._handle_standard_callbacks(query, callback_data, user_info, preferred_lang)
                
        except Exception as e:
            logger.error(f"❌ Error in enhanced button_callback: {e}")
            await query.edit_message_text("⚠️ Arre yaar, kuch gadbad ho gayi! 🙏")

    async def _handle_category_selection(self, query, callback_data: str, user_info: dict, language: str):
        """Handle category selection callbacks with desi style"""
        category = callback_data.replace("category_", "")
        
        category_info = {
            "education": {
                "title": "🎓 Padhai & Education Zone",
                "description": "School, college, competitive exams, homework - sab help milegi!",
                "examples": ["Math problems solve karo", "UPSC strategy batao", "Physics concepts explain karo"]
            },
            "career": {
                "title": "💼 Career & Job Guidance",
                "description": "Job search, interview prep, resume writing, career planning",
                "examples": ["Interview tips do", "Resume improve karo", "Career change advice do"]
            },
            "tech": {
                "title": "💻 Technology & Programming Hub",
                "description": "Coding, web development, AI/ML, tech troubleshooting",
                "examples": ["Python code sikhao", "Website banane ka tareeka", "Bot development guide"]
            },
            "earning": {
                "title": "💰 Online Earning & Business",
                "description": "Freelancing, business ideas, investment, money making tips",
                "examples": ["Online paise kaise kamaye", "Business plan banao", "Investment advice do"]
            },
            "love": {
                "title": "❤️ Love & Relationships",
                "description": "Dating advice, relationship problems, love guidance",
                "examples": ["Propose kaise kare", "Breakup se kaise deal kare", "Relationship tips do"]
            },
            "language": {
                "title": "🗣️ Language Learning Center",
                "description": "English speaking, Hindi grammar, translation help",
                "examples": ["English fluency improve karo", "Grammar mistakes correct karo", "Translation help karo"]
            },
            "fun": {
                "title": "🎬 Entertainment & Fun Zone",
                "description": "Movies, music, memes, jokes, timepass content",
                "examples": ["Funny jokes sunao", "Movie recommend karo", "Memes banao"]
            },
            "motivation": {
                "title": "💪 Motivation & Life Coaching",
                "description": "Success mindset, goal setting, confidence building",
                "examples": ["Motivation boost karo", "Goals set karne help karo", "Confidence badhao"]
            }
        }
        
        info = category_info.get(category, category_info["education"])
        
        message = f"""**{info['title']}**

📋 **Main kya help kar sakta hoon:**
{info['description']}

💡 **Example questions:**
• {info['examples'][0]}
• {info['examples'][1]}
• {info['examples'][2]}

💬 **Bas apna sawal type karo aur main expert guidance dunga! 🎯**"""
        
        keyboard = [
            [InlineKeyboardButton("💬 Ask Question", callback_data="new_question")],
            [InlineKeyboardButton("◀️ Back to Main Menu", callback_data="main_menu")]
        ]
        
        await query.edit_message_text(
            message,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )

    async def _handle_admin_panel(self, query, user_info: dict, language: str):
        """Handle admin panel - only for admin users"""
        if not self.utils.is_admin(user_info['id']):
            await query.edit_message_text("🚫 Admin access required bhai! 😅")
            return
        
        admin_message = f"""👨‍💻 **Admin Panel - Ostaad AI**

🎯 **System Status**: Online & Active
📊 **Bot Version**: {Config.VERSION}
🧠 **AI Model**: {Config.DEFAULT_MODEL}

**Available Admin Functions:**"""
        
        keyboard = [
            [
                InlineKeyboardButton("📢 Broadcast Message", callback_data="broadcast"),
                InlineKeyboardButton("📊 Bot Statistics", callback_data="admin_stats")
            ],
            [
                InlineKeyboardButton("👥 User Management", callback_data="user_management"),
                InlineKeyboardButton("⚙️ System Settings", callback_data="system_settings")
            ],
            [InlineKeyboardButton("◀️ Back to Main Menu", callback_data="main_menu")]
        ]
        
        await query.edit_message_text(
            admin_message,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )

    async def _handle_broadcast_menu(self, query, user_info: dict, language: str):
        """Handle broadcast menu - only for admin"""
        if not self.utils.is_admin(user_info['id']):
            await query.edit_message_text("🚫 Admin access required! 😅")
            return
        
        broadcast_message = """📢 **Broadcast Message System**

🎯 **Instructions:**
1. Use `/broadcast <your_message>` command to send message to all users
2. Message will be sent to all active users
3. Use responsibly - avoid spam

**Example:**
`/broadcast 🎉 Ostaad AI has new features! Check them out!`

⚠️ **Note**: This feature is under development"""
        
        keyboard = [
            [InlineKeyboardButton("◀️ Back to Admin Panel", callback_data="admin_panel")],
            [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
        ]
        
        await query.edit_message_text(
            broadcast_message,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )

    async def _show_user_journey(self, query, user_info: dict, language: str):
        """Show user journey and statistics with desi style"""
        user_id = user_info['id']
        session = self.user_sessions.get(user_id, {})
        ai_stats = self.ai_service.get_user_stats(user_id)
        
        stats_message = f"""📊 **Tumhara Ostaad AI Journey**

👤 **User**: {user_info['first_name']} (@{user_info['username']})

📈 **Session Stats:**
• Sawal Pooche: {session.get('query_count', 0)} 🤔
• Categories Explore Kiye: {len(session.get('categories_explored', set()))} 🎯
• Current Mood: {ai_stats.get('current_mood', 'Neutral').title()} 😊

🎯 **Explore Kiye Categories:**
{', '.join(session.get('categories_explored', {'General'})) or 'Abhi koi nahi'}

💬 **Total Conversations**: {ai_stats.get('conversation_count', 0)}

🌟 **Tumhara Learning Journey**: Different categories explore karte raho aur expert bano! 💪

🔥 **Ostaad AI Tip**: Curiosity rakho aur har din kuch naya seekho! ✨

{Config.POWERED_BY}"""
        
        keyboard = [
            [InlineKeyboardButton("🔄 Reset Stats", callback_data="reset_stats")],
            [InlineKeyboardButton("◀️ Back to Main Menu", callback_data="main_menu")]
        ]
        
        await query.edit_message_text(
            stats_message,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )

    async def _handle_new_question(self, query, user_info: dict, language: str):
        """Handle new question selection with desi style"""
        message = f"""💬 **Naya Sawal Poochne Ke Liye Ready!**

🎯 **Main har category mein expert hoon:**
• 🎓 Padhai & Competitive Exams
• 💼 Career & Job Guidance  
• 💻 Technology & Programming
• 💰 Online Earning & Business
• ❤️ Love & Relationships
• 🗣️ Language Learning
• 🎬 Entertainment & Fun
• 💪 Motivation & Life Coaching

**Bas apna sawal type karo aur main expert guidance dunga! 🔥**

Tension mat lo - Main tumhara digital ustad hoon! 🧑‍🏫"""
        
        keyboard = [
            [InlineKeyboardButton("◀️ Back to Main Menu", callback_data="main_menu")]
        ]
        
        await query.edit_message_text(
            message,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )

    async def _handle_quick_actions(self, query, action: str, user_info: dict, language: str):
        """Handle quick action buttons with desi responses"""
        
        action_responses = {
            "more_examples": "📚 Bilkul bhai! More detailed examples chahiye? Bas specific topic batao! 🎯",
            "practice_questions": "🧮 Practice time! Koi bhi subject ka practice questions chahiye? Batao! 💪",
            "interview_tips": "💼 Interview tips ready hain! Kaunsa type ka interview hai? Technical ya HR? 🎯",
            "resume_help": "📄 Resume improve karna hai? Current resume share karo ya format chahiye? ✨",
            "code_examples": "💻 Code examples ready! Kaunsi language aur kya problem solve karni hai? 🛠️",
            "tech_resources": "🔗 Best tech resources batata hoon! Kaunsa technology seekhna hai? 🚀",
            "earning_ideas": "💰 Paisa kamane ke ideas! Skills kya hain aur kitna time de sakte ho? 📊",
            "business_tips": "📈 Business tips ready! Startup idea hai ya existing business improve karna hai? 💡",
            "love_tips": "❤️ Love advice ready! Kya situation hai? Propose karna hai ya relationship improve? 🥰",
            "relationship_advice": "🤗 Relationship guidance! Problem kya hai? Communication ya trust issues? 💕",
            "more_fun": "🎬 More entertainment! Movies, music, ya jokes chahiye? Mood kya hai? 😄",
            "jokes": "😂 Jokes ready hain! Kaunse type ke - funny, witty, ya roast style? 🤣",
            "motivation_boost": "💪 Motivation boost time! Kya problem hai? Confidence low hai ya goals unclear? 🔥",
            "goal_setting": "🎯 Goal setting expert! Short-term ya long-term goals set karne hain? ✨"
        }
        
        response = action_responses.get(action, "💬 Bas poocho bhai, main help karunga! 🤝")
        
        keyboard = [
            [InlineKeyboardButton("💬 Ask Now", callback_data="new_question")],
            [InlineKeyboardButton("◀️ Back to Main Menu", callback_data="main_menu")]
        ]
        
        await query.edit_message_text(
            response,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )

    async def _handle_standard_callbacks(self, query, callback_data: str, user_info: dict, language: str):
        """Handle standard callback queries with desi style"""
        
        if callback_data == "main_menu":
            # Redirect to start command functionality
            welcome_data = self._get_desi_welcome_message(language, user_info['first_name'])
            
            keyboard = [
                [
                    InlineKeyboardButton("Padhai Help", callback_data="category_education"),
                    InlineKeyboardButton("Career Guide", callback_data="category_career")
                ],
                [
                    InlineKeyboardButton("Tech Support", callback_data="category_tech"),
                    InlineKeyboardButton("Earning Tips", callback_data="category_earning")
                ],
                [
                    InlineKeyboardButton("Love Advice", callback_data="category_love"),
                    InlineKeyboardButton("Language Help", callback_data="category_language")
                ],
                [
                    InlineKeyboardButton("Entertainment", callback_data="category_fun"),
                    InlineKeyboardButton("Motivation", callback_data="category_motivation")
                ],
                [
                    InlineKeyboardButton("Help & Commands", callback_data="help"),
                    InlineKeyboardButton("About Ostaad AI", callback_data="info")
                ],
                [
                    InlineKeyboardButton("Language Settings", callback_data="language_settings"),
                    InlineKeyboardButton("My Journey", callback_data="user_stats")
                ]
            ]
            
            # Add admin panel for admin users only
            if self.utils.is_admin(user_info['id']):
                keyboard.append([InlineKeyboardButton("Admin Panel", callback_data="admin_panel")])
            
            await query.edit_message_text(
                welcome_data,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
        
        elif callback_data == "help":
            await self._show_help_message(query, language)
        
        elif callback_data == "info":
            await self._show_info_message(query, language)
        
        elif callback_data == "language_settings":
            await self._show_language_settings(query, language)

    async def _show_help_message(self, query, language: str):
        """Show help message with desi style"""
        help_message = f"""🆘 **Ostaad AI Help Guide** 🆘

📚 **Kaise use kare:**
• Koi bhi sawal type karo - main samjhaunga! 💬
• Categories select kar sakte ho quick help ke liye 🎯
• Main Hinglish mein baat karta hoon - natural feel! 😊

🔧 **Available Commands:**
/start - Welcome message aur main menu
/help - Ye help guide
/info - Ostaad AI ke baare mein details
/reset - Conversation history clear karo

💡 **Best Tips:**
1. Clear aur specific questions poocho 🎯
2. Context do agar complex topic hai 📚
3. Feedback do - main improve karta rehta hoon! ✨

⚙️ **Technical Details:**
• AI Model: {Config.DEFAULT_MODEL}
• Developer: {Config.DEVELOPER}
• Version: {Config.VERSION}

🟢 **Status**: Fully Active aur Ready! 🔥

{Config.POWERED_BY}"""
        
        keyboard = [
            [InlineKeyboardButton("◀️ Back to Main Menu", callback_data="main_menu")]
        ]
        
        await query.edit_message_text(
            help_message,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )

    async def _show_info_message(self, query, language: str):
        """Show info message with desi style"""
        info_message = f"""🤖 **Ostaad AI System Information** 🤖

⚙️ **Core Architecture:**
├─ AI Model: {Config.DEFAULT_MODEL}
├─ Framework: Ostaad AI Engine
├─ Language: Python 3.11
└─ Security: Enterprise-Grade

🌟 **Key Capabilities:**
├─ 12+ Categories mein expertise 🎯
├─ Human-like conversation style 😊
├─ Emotional intelligence 💝
├─ Desi context understanding 🇮🇳

📋 **System Details:**
├─ Developer: {Config.DEVELOPER}
├─ Specialization: Pure Desi AI Assistant
├─ Platform: Telegram Messenger
├─ Version: {Config.VERSION}
└─ Last Updated: December 2024

💡 **Getting Started:**
1. /start se shuru karo
2. Category select karo ya direct question poocho
3. Enjoy human-like conversation! 🔥

🟢 **System Status**: Fully Operational! 💪

{Config.POWERED_BY}"""
        
        keyboard = [
            [InlineKeyboardButton("◀️ Back to Main Menu", callback_data="main_menu")]
        ]
        
        await query.edit_message_text(
            info_message,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )

    async def _show_language_settings(self, query, language: str):
        """Show language settings with desi style"""
        lang_message = f"""🌐 **Language Settings** 🌐

🔹 **Current Language**: {language.upper()}

Choose your preferred language:

**Indian Languages:**
• Hindi (हिंदी) - Default
• English - International
• Urdu (اردو) - Supported
• Bengali (বাংলা) - Supported

📌 **Note**: Main mainly Hinglish mein baat karta hoon - best of both worlds! 😎

Aur languages bhi support karta hoon basic level pe.

{Config.POWERED_BY}"""
        
        keyboard = [
            [
                InlineKeyboardButton("🇮🇳 Hindi", callback_data="set_lang_hi"),
                InlineKeyboardButton("🇬🇧 English", callback_data="set_lang_en")
            ],
            [
                InlineKeyboardButton("🇵🇰 Urdu", callback_data="set_lang_ur"),
                InlineKeyboardButton("🇧🇩 Bengali", callback_data="set_lang_bn")
            ],
            [InlineKeyboardButton("◀️ Back to Main Menu", callback_data="main_menu")]
        ]
        
        await query.edit_message_text(
            lang_message,
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode='Markdown'
        )

    async def _send_desi_error_response(self, update: Update, user_info: dict, language: str):
        """Send enhanced error response with desi style"""
        error_messages = [
            "🙏 Arre yaar, mujhe thoda technical problem ho raha hai!",
            "😅 Oops! Kuch gadbad ho gayi, phir se try karo bhai!",
            "🔧 Technical issue aa gaya, 2 minute wait karo!",
            "⚠️ Server mein thoda issue hai, jaldi theek kar deta hoon!"
        ]
        
        error_msg = f"""{random.choice(error_messages)}

🔧 **Kya karna hai:**
• Thoda wait karo aur phir try karo 
• Agar problem continue kare to developer ko batao

💡 **Meanwhile**: Main jaldi wapas aa jaunga tumhari help ke liye! 💪

{Config.POWERED_BY} | Hamesha seekhta rehta hoon! 🧠"""
        
        keyboard = [
            [InlineKeyboardButton("🔄 Try Again", callback_data="new_question")],
            [InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(error_msg, reply_markup=reply_markup, parse_mode='Markdown')

    # Additional command handlers
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Help command handler"""
        await self._show_help_message(update, 'hi')

    async def info_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Info command handler"""
        await self._show_info_message(update, 'hi')

    async def broadcast_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Broadcast command for admin"""
        user_info = self.utils.get_user_info(update)
        
        if not self.utils.is_admin(user_info['id']):
            await update.message.reply_text("🚫 Admin access required bhai! 😅")
            return
        
        if not context.args:
            await update.message.reply_text("📢 Broadcast message provide karo!\nExample: /broadcast Hello everyone!")
            return
        
        message = ' '.join(context.args)
        await update.message.reply_text(f"📢 Broadcast ready: {message}\n\n(Feature coming soon! 🚀)")