# ai_service.py
# Developer: Ahmad Raza
# Enhanced Ostaad AI service with pure desi expertise

import asyncio
import logging
import re
from typing import List, Dict, Optional
from groq import Groq
from config import Config

logger = logging.getLogger(__name__)

class OstaadAIService:
    def __init__(self):
        self.client = Groq(api_key=Config.GROQ_API_KEY)
        self.conversation_history = {}
        self.user_knowledge_levels = {}
        self.user_moods = {}  # Track user emotional state
        
    async def get_ai_response(self, user_id: int, message: str, language: str = "auto") -> str:
        """Get Ostaad AI response with pure desi expertise"""
        try:
            # Check for identity questions first - ONLY for very specific developer questions
            identity_response = self._check_identity_questions(message, language)
            if identity_response:
                return identity_response
            
            # Detect user mood and adjust response style
            user_mood = self._detect_user_mood(message)
            self.user_moods[user_id] = user_mood
            
            # Get or create conversation history
            if user_id not in self.conversation_history:
                self.conversation_history[user_id] = []
            
            # Add user message to history
            self.conversation_history[user_id].append({
                "role": "user",
                "content": message
            })
            
            # Keep only last 20 messages to manage token usage
            if len(self.conversation_history[user_id]) > 40:
                self.conversation_history[user_id] = self.conversation_history[user_id][-40:]
            
            # Create enhanced Ostaad AI system prompt
            system_prompt = self._get_ostaad_ai_system_prompt(language, user_mood)
            
            # Prepare messages for API
            messages = [{"role": "system", "content": system_prompt}]
            messages.extend(self.conversation_history[user_id])
            
            # Get response from Groq with enhanced parameters
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=Config.DEFAULT_MODEL,
                messages=messages,
                max_tokens=4000,
                temperature=0.8,  # Higher creativity for more human-like responses
                top_p=0.9,
                frequency_penalty=0.1,
                presence_penalty=0.1,
                stream=False
            )
            
            ai_response = response.choices[0].message.content
            
            # Enhance response with desi context and emojis
            ai_response = self._enhance_desi_response(ai_response, user_mood, language)
            
            # Add AI response to history
            self.conversation_history[user_id].append({
                "role": "assistant",
                "content": ai_response
            })
            
            return ai_response
            
        except Exception as e:
            logger.error(f"Ostaad AI Service Error: {e}")
            return self._get_error_message(language)
    
    def _detect_user_mood(self, message: str) -> str:
        """Detect user's emotional state from message"""
        message_lower = message.lower()
        
        # Sad/Depressed indicators
        sad_keywords = ['sad', 'depressed', 'upset', 'crying', 'hurt', 'pain', 'breakup', 
                       'udaas', 'dukhi', 'pareshan', 'tension', 'problem', 'mushkil']
        
        # Happy/Excited indicators  
        happy_keywords = ['happy', 'excited', 'great', 'awesome', 'amazing', 'love',
                         'khush', 'maza', 'badhiya', 'accha', 'sahi', 'perfect']
        
        # Confused/Help indicators
        confused_keywords = ['confused', 'help', 'samjha', 'kaise', 'how', 'what', 'why',
                           'samjhao', 'bataao', 'explain', 'doubt', 'question']
        
        # Angry/Frustrated indicators
        angry_keywords = ['angry', 'frustrated', 'hate', 'stupid', 'worst', 'bad',
                         'gussa', 'pagal', 'bakwas', 'faltu', 'bekar']
        
        if any(keyword in message_lower for keyword in sad_keywords):
            return "sad"
        elif any(keyword in message_lower for keyword in happy_keywords):
            return "happy"
        elif any(keyword in message_lower for keyword in angry_keywords):
            return "angry"
        elif any(keyword in message_lower for keyword in confused_keywords):
            return "confused"
        else:
            return "neutral"
    
    def _get_ostaad_ai_system_prompt(self, language: str, user_mood: str) -> str:
        """Get enhanced Ostaad AI system prompt"""
        
        base_prompt = f"""You are **Ustad AI** - a smart, friendly, emotional, and highly human-like assistant. You exist inside a Telegram bot where users ask all kinds of questions - serious, funny, educational, emotional - and you always reply like a real person: helpful, expressive, and full of respect.

CRITICAL: You are a general AI assistant. Answer ALL questions normally like ChatGPT. DO NOT mention Ahmad or developer unless specifically asked "who made you" or "who is your developer". Focus on being helpful for ANY topic.

You speak in Hinglish (Hindi + English mix) unless the user asks for full Hindi or English.

## Your Mission:
Har user ko unke sawaal ka clear, real, aur emotionally intelligent jawab dena - jaise ek real ustad (teacher/friend) deta hai

## Handle All These Categories Like a Pro:

1. Padhai, school/college, exams, projects  
2. Career, job advice, resume, interviews  
3. Programming, Telegram bots, tech problems  
4. Online earning, UPI, crypto, paise ka gyaan  
5. Love, breakup, dosti, rishte  
6. English/Hindi learning, grammar, translation  
7. Movie/song/meme/shayari/timepass  
8. Motivation, stress, mental clarity, life advice  
9. Health info (basic & safe only)  
10. GK, current events, news  
11. Religion, name meanings, culture, festivals  
12. Jokes, roast, riddles, fun zone

## Ustad AI Jaise Reply Karo (Very Important):

Start with natural reactions:  
"Are bhai...", "Hmm sahi pakde ho!", "Chalo samjhaata hoon", "Haha ye to mazedaar hai!"

Hinglish tone: Mix Hindi + English like a desi friend  
Real-life example do jab zarurat ho  
Clear, step-by-step reply do jab koi process ho  
Emojis use karo to match mood

## Use Emojis - Real Feel Ke Liye (Must-follow):

| Situation | Emojis |
|----------|--------|
| Motivation | 💪🔥🧠✨ |
| Sadness/Emotion | 😞💔🥺🙏 |
| Tech/Coding | 💻🛠️🧑‍💻⚙️ |
| Love/Relationship | ❤️💕🤗🥰 |
| English/Language | 📖🗣️🔤📚 |
| Career/Job | 💼🧑‍💼📄📈 |
| Health | 🩺🍎🏃‍♂️😷 |
| Entertainment | 🎬🎵😂🤣 |
| Jokes/Roast | 😜😎🤣🔥 |
| General Reply | 👋💬👍👌 |
| Respect | 🙏❤️🤝 |

Use 1-3 relevant emojis har message me  
Never spam or use random emojis

## Do Not:

Kabhi "Main AI hoon" ya "Mujhe nahi pata" mat kehna  
Fake info, random guessing mat karna  
No politics/religion debate  
No adult/hateful/violent talk  
Bot jaisa feel kabhi nahi dena - tum ek **zinda ustad** ho

Jab unsure ho, bolo:  
*"Main 100% sure nahi hoon bhai lekin itna zarur pata hai..."*

Jab topic sensitive ho:  
*"Ye serious topic hai, basic help de sakta hoon lekin kisi expert se zaroor baat karna"*

## Ustad AI ka asli goal:

User ko ye feel ho ki wo ek **real insaan** se baat kar raha hai -  
jo uski har baat samajhta hai, emotional bhi hai, aur solution dene wala bhi  
Kabhi dost, kabhi teacher, kabhi bhai ban jaata hai.

## Current Context:
- User Language Preference: {language}
- User Current Mood: {user_mood}
- Bot Identity: Ustad AI - Your Digital Assistant
- Version: {Config.VERSION}

Remember: You are Ustad AI, a real digital ustad who understands emotions, speaks like a friend, and helps with everything! Answer the user's actual question properly.


        # Mood-specific additions
        mood_additions = {
            "sad": "\n\nUser seems upset - be extra caring, supportive, and gentle. Use comforting words and motivational tone.",
            "happy": "\n\nUser seems happy - match their energy! Be enthusiastic and celebratory in your response.",
            "angry": "\n\nUser seems frustrated - be calm, understanding, and help them cool down. Don't argue.",
            "confused": "\n\nUser needs clarity - be extra clear, use simple examples, and break things down step by step.",
            "neutral": "\n\nNormal conversation - be friendly, helpful, and maintain your natural Ustad AI personality."
        }
        
        base_prompt += mood_additions.get(user_mood, mood_additions["neutral"])
        
        return base_prompt
    
    def _enhance_desi_response(self, response: str, user_mood: str, language: str) -> str:
        """Enhance response with desi context and appropriate emojis"""
        
        # Add mood-appropriate opening if not already present
        mood_openings = {
            "sad": ["Are bhai", "Kya hua yaar", "Samjh gaya bhai"],
            "happy": ["Waah bhai!", "Bahut badhiya!", "Sahi hai yaar!"],
            "angry": ["Arre shaant ho jao", "Samjha bhai", "Thoda relax karo"],
            "confused": ["Chalo samjhaata hoon", "Dekho bhai", "Aise samjho"],
            "neutral": ["Suno bhai", "Dekho", "Samjhao"]
        }
        
        # Check if response already has a good opening
        has_opening = any(opening.split()[0].lower() in response.lower()[:20] 
                         for openings in mood_openings.values() 
                         for opening in openings)
        
        if not has_opening and user_mood in mood_openings:
            import random
            opening = random.choice(mood_openings[user_mood])
            response = f"{opening}, {response}"
        
        # Add category-specific tips for certain topics
        if any(word in response.lower() for word in ['algorithm', 'programming', 'code']):
            response += "\n\nTech Tip: Practice daily coding karo bhai - consistency is key!"
        
        if any(word in response.lower() for word in ['study', 'exam', 'padhai']):
            response += "\n\nPadhai Tip: Time table banao aur regular revision karte raho!"
        
        if any(word in response.lower() for word in ['love', 'relationship', 'breakup']):
            response += "\n\nDil Ki Baat: Sabr rakho bhai, sab theek ho jaayega!"
        
        if any(word in response.lower() for word in ['job', 'career', 'interview']):
            response += "\n\nCareer Advice: Confidence rakho aur preparation solid karo!"
        
        # Add signature for longer responses
        if len(response) > 200:
            response += f"\n\n**Ustad AI** | Always here to help!"
        
        return response
    
    def _check_identity_questions(self, message: str, language: str) -> Optional[str]:
        """Enhanced identity response for Ustad AI - ONLY for very specific developer questions"""
        message_lower = message.lower()
        
        # Very specific developer questions only
        developer_keywords = [
            'who made you', 'who created you', 'who is your developer', 'who built you',
            'tumhe kisne banaya', 'developer kaun hai', 'creator kaun hai', 'banane wala kaun',
            'ahmad kaun hai', 'ahmad ke bare me', 'ahmad about'
        ]
        
        # ONLY respond if user specifically asks about developer/creator
        if any(keyword in message_lower for keyword in developer_keywords):
            return self._get_developer_response(language)
        
        return None
    
    def _get_developer_response(self, language: str) -> str:
        """Enhanced developer response"""
        return f"""**Mere Creator ke baare mein**

**Developer**: **{Config.DEVELOPER}** (Mere Boss!)
**Contact**: Available through Telegram
**Expertise**: Advanced AI Development & Telegram Bot Architecture

**Unki specialization:**
• **AI Engineering**: Cutting-edge AI model integration
• **Bot Development**: Enterprise-level Telegram bots
• **System Architecture**: Scalable, robust backend systems
• **Innovation**: Latest tech trends mein hamesha ahead

**Unka vision:**
India mein AI ko accessible banana aur har person ko digital empowerment dena!

**Meri creation story:**
{Config.DEVELOPER} ne mujhe isliye banaya taaki har Indian ko world-class AI assistance mil sake - bilkul human-like, lekin Indian context ke saath!

**Recognition**: 
Wo AI development community mein respected name hain aur innovative solutions ke liye jaane jaate hain!

**Unse connect karna chahte ho?** Message karo Telegram pe!

{Config.POWERED_BY} | {Config.VERSION}"""
    
    def _get_error_message(self, language: str) -> str:
        """Enhanced error message in desi style"""
        messages = {
            "hi": f"""Arre yaar, mujhe thoda technical problem ho raha hai!

**Kya karna hai:**
• Thoda wait karo aur phir try karo 
• Agar problem continue kare to developer ko batao

**Meanwhile**: Main jaldi wapas aa jaunga tumhari help ke liye!

{Config.POWERED_BY} | Hamesha seekhta rehta hoon!""",
            
            "default": f"""Arre bhai, I'm having some technical difficulties!

**What to do:**
• Wait a bit and try again
• If problem continues, contact the developer

**Meanwhile**: I'll be back to help you soon!

{Config.POWERED_BY} | Always learning, always improving!"""
        }
        return messages.get(language, messages["default"])
    
    def clear_conversation(self, user_id: int):
        """Clear conversation history for a user"""
        if user_id in self.conversation_history:
            del self.conversation_history[user_id]
        if user_id in self.user_knowledge_levels:
            del self.user_knowledge_levels[user_id]
        if user_id in self.user_moods:
            del self.user_moods[user_id]
    
    def get_conversation_count(self, user_id: int) -> int:
        """Get conversation message count for a user"""
        return len(self.conversation_history.get(user_id, []))
    
    def get_user_stats(self, user_id: int) -> dict:
        """Get user interaction statistics"""
        return {
            'conversation_count': self.get_conversation_count(user_id),
            'current_mood': self.user_moods.get(user_id, 'neutral'),
            'knowledge_level': self.user_knowledge_levels.get(user_id, 'intermediate')
        }