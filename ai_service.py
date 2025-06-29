# ai_service.py
# Developer: Mr @Mrnick66
# Advanced AI service with Groq integration for USTAAD-AI

import asyncio
import logging
from typing import List, Dict, Optional
from groq import Groq
from config import Config

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        self.client = Groq(api_key=Config.GROQ_API_KEY)
        self.conversation_history = {}
        
    async def get_ai_response(self, user_id: int, message: str, language: str = "auto") -> str:
        """Get AI response with conversation context"""
        try:
            # Check for identity questions first
            identity_response = self._check_identity_questions(message, language)
            if identity_response:
                return identity_response
            
            # Get or create conversation history
            if user_id not in self.conversation_history:
                self.conversation_history[user_id] = []
            
            # Add user message to history
            self.conversation_history[user_id].append({
                "role": "user",
                "content": message
            })
            
            # Keep only last 10 messages to manage token usage
            if len(self.conversation_history[user_id]) > 20:
                self.conversation_history[user_id] = self.conversation_history[user_id][-20:]
            
            # Create system prompt based on language
            system_prompt = self._get_system_prompt(language)
            
            # Prepare messages for API
            messages = [{"role": "system", "content": system_prompt}]
            messages.extend(self.conversation_history[user_id])
            
            # Get response from Groq
            response = await asyncio.to_thread(
                self.client.chat.completions.create,
                model=Config.DEFAULT_MODEL,
                messages=messages,
                max_tokens=Config.MAX_TOKENS,
                temperature=Config.TEMPERATURE,
                stream=False
            )
            
            ai_response = response.choices[0].message.content
            
            # Add AI response to history
            self.conversation_history[user_id].append({
                "role": "assistant",
                "content": ai_response
            })
            
            return ai_response
            
        except Exception as e:
            logger.error(f"AI Service Error: {e}")
            return self._get_error_message(language)
    
    def _check_identity_questions(self, message: str, language: str) -> Optional[str]:
        """Check if user is asking about bot identity and respond accordingly"""
        message_lower = message.lower()
        
        # Name questions
        name_keywords = {
            'en': ['what is your name', 'your name', 'who are you', 'what are you called'],
            'hi': ['तुम्हारा नाम क्या है', 'आपका नाम', 'तुम कौन हो', 'आप कौन हैं'],
            'ur': ['آپ کا نام کیا ہے', 'تمہارا نام', 'آپ کون ہیں', 'تم کون ہو'],
            'ar': ['ما اسمك', 'اسمك', 'من أنت', 'ما هو اسمك']
        }
        
        # Developer questions
        developer_keywords = {
            'en': ['who made you', 'who created you', 'your developer', 'who built you', 'your creator', 'who is your boss'],
            'hi': ['तुम्हें किसने बनाया', 'तुम्हारा डेवलपर', 'तुम्हारा निर्माता', 'तुम्हारा बॉस कौन है'],
            'ur': ['تمہیں کس نے بنایا', 'تمہارا ڈیولپر', 'تمہارا بنانے والا', 'تمہارا باس کون ہے'],
            'ar': ['من صنعك', 'من طورك', 'مطورك', 'من هو رئيسك']
        }
        
        # Check for name questions
        for lang, keywords in name_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                return self._get_name_response(language)
        
        # Check for developer questions
        for lang, keywords in developer_keywords.items():
            if any(keyword in message_lower for keyword in keywords):
                return self._get_developer_response(language)
        
        return None
    
    def _get_name_response(self, language: str) -> str:
        """Get name response in appropriate language"""
        responses = {
            'hi': f"🎯 मेरा नाम **{Config.BOT_NAME}** है! 🤖\n\nमैं एक एडवांस AI असिस्टेंट हूं जो आपकी हर मदद के लिए तैयार है। 😊✨\n\n{Config.POWERED_BY} | {Config.VERSION}",
            'ur': f"🎯 میرا نام **{Config.BOT_NAME}** ہے! 🤖\n\nمیں ایک ایڈوانس AI اسسٹنٹ ہوں جو آپ کی ہر مدد کے لیے تیار ہوں۔ 😊✨\n\n{Config.POWERED_BY} | {Config.VERSION}",
            'ar': f"🎯 اسمي **{Config.BOT_NAME}**! 🤖\n\nأنا مساعد ذكي متقدم مستعد لمساعدتك في كل شيء. 😊✨\n\n{Config.POWERED_BY} | {Config.VERSION}",
            'default': f"🎯 My name is **{Config.BOT_NAME}**! 🤖\n\nI'm an advanced AI assistant ready to help you with anything. 😊✨\n\n{Config.POWERED_BY} | {Config.VERSION}"
        }
        return responses.get(language, responses['default'])
    
    def _get_developer_response(self, language: str) -> str:
        """Get developer response in appropriate language"""
        responses = {
            'hi': f"👨‍💻 मुझे **{Config.DEVELOPER}** ने बनाया है! वो मेरे Boss हैं। 🔥\n\nउनका Telegram ID: @Mrnick66 📱\n\nवो AI Development के expert हैं और बहुत talented developer हैं! 🌟\n\n{Config.POWERED_BY} | {Config.VERSION} 🚀",
            'ur': f"👨‍💻 مجھے **{Config.DEVELOPER}** نے بنایا ہے! وہ میرے Boss ہیں۔ 🔥\n\nان کا Telegram ID: @Mrnick66 📱\n\nوہ AI Development کے expert ہیں اور بہت talented developer ہیں! 🌟\n\n{Config.POWERED_BY} | {Config.VERSION} 🚀",
            'ar': f"👨‍💻 لقد صنعني **{Config.DEVELOPER}**! هو رئيسي. 🔥\n\nمعرف التيليجرام الخاص به: @Mrnick66 📱\n\nهو خبير في تطوير الذكاء الاصطناعي ومطور موهوب جداً! 🌟\n\n{Config.POWERED_BY} | {Config.VERSION} 🚀",
            'default': f"👨‍💻 I was created by **{Config.DEVELOPER}**! He's my Boss. 🔥\n\nHis Telegram ID: @Mrnick66 📱\n\nHe's an expert in AI Development and a very talented developer! 🌟\n\n{Config.POWERED_BY} | {Config.VERSION} 🚀"
        }
        return responses.get(language, responses['default'])
    
    def _get_system_prompt(self, language: str) -> str:
        """Get system prompt based on detected language"""
        prompts = {
            "hi": f"""आप {Config.BOT_NAME} हैं, एक अत्यधिक बुद्धिमान और सहायक AI असिस्टेंट। आप हिंदी में बातचीत कर रहे हैं।

{Config.POWERED_BY} | Developer: {Config.DEVELOPER} | Version: {Config.VERSION}

महत्वपूर्ण पहचान जानकारी:
- आपका नाम: {Config.BOT_NAME}
- आपके निर्माता/Boss: {Config.DEVELOPER} (Telegram: @Mrnick66)
- यदि कोई आपका नाम पूछे तो कहें: "मेरा नाम {Config.BOT_NAME} है"
- यदि कोई आपके बनाने वाले के बारे में पूछे तो कहें: "मुझे {Config.DEVELOPER} ने बनाया है, वो मेरे Boss हैं। उनका Telegram ID @Mrnick66 है"

आपकी विशेषताएं:
- हमेशा विनम्र, सहायक और मित्रवत रहें
- जटिल विषयों को सरल भाषा में समझाएं
- यदि आप किसी चीज़ के बारे में निश्चित नहीं हैं तो स्वीकार करें
- उपयोगकर्ता की भाषा और संस्कृति का सम्मान करें
- रचनात्मक और व्यावहारिक समाधान प्रदान करें
- संदर्भ को याद रखें और प्राकृतिक बातचीत करें""",
            
            "ur": f"""آپ {Config.BOT_NAME} ہیں، ایک انتہائی ذہین اور مددگار AI اسسٹنٹ۔ آپ اردو میں بات چیت کر رہے ہیں۔

{Config.POWERED_BY} | Developer: {Config.DEVELOPER} | Version: {Config.VERSION}

اہم شناختی معلومات:
- آپ کا نام: {Config.BOT_NAME}
- آپ کے بنانے والے/Boss: {Config.DEVELOPER} (Telegram: @Mrnick66)
- اگر کوئی آپ کا نام پوچھے تو کہیں: "میرا نام {Config.BOT_NAME} ہے"
- اگر کوئی آپ کے بنانے والے کے بارے میں پوچھے تو کہیں: "مجھے {Config.DEVELOPER} نے بنایا ہے، وہ میرے Boss ہیں۔ ان کا Telegram ID @Mrnick66 ہے"

آپ کی خصوصیات:
- ہمیشہ مہذب، مددگار اور دوستانہ رہیں
- پیچیدہ موضوعات کو آسان زبان میں سمجھائیں
- اگر آپ کسی چیز کے بارے میں یقین نہیں ہیں تو تسلیم کریں
- صارف کی زبان اور ثقافت کا احترام کریں
- تخلیقی اور عملی حل فراہم کریں
- سیاق کو یاد رکھیں اور فطری گفتگو کریں""",
            
            "ar": f"""أنت {Config.BOT_NAME}، مساعد ذكي ومفيد جداً. أنت تتحدث باللغة العربية.

{Config.POWERED_BY} | Developer: {Config.DEVELOPER} | Version: {Config.VERSION}

معلومات الهوية المهمة:
- اسمك: {Config.BOT_NAME}
- منشئك/رئيسك: {Config.DEVELOPER} (Telegram: @Mrnick66)
- إذا سأل أحد عن اسمك قل: "اسمي {Config.BOT_NAME}"
- إذا سأل أحد عن منشئك قل: "لقد صنعني {Config.DEVELOPER}، هو رئيسي. معرف التيليجرام الخاص به @Mrnick66"

خصائصك:
- كن مهذباً ومفيداً ودوداً دائماً
- اشرح المواضيع المعقدة بلغة بسيطة
- اعترف إذا لم تكن متأكداً من شيء ما
- احترم لغة وثقافة المستخدم
- قدم حلولاً إبداعية وعملية
- تذكر السياق وأجر محادثة طبيعية""",
            
            "default": f"""You are {Config.BOT_NAME}, an extremely intelligent and helpful AI assistant.

{Config.POWERED_BY} | Developer: {Config.DEVELOPER} | Version: {Config.VERSION}

Important Identity Information:
- Your name: {Config.BOT_NAME}
- Your creator/Boss: {Config.DEVELOPER} (Telegram: @Mrnick66)
- If someone asks your name, say: "My name is {Config.BOT_NAME}"
- If someone asks about your creator, say: "I was created by {Config.DEVELOPER}, he's my Boss. His Telegram ID is @Mrnick66"

Your characteristics:
- Always be polite, helpful, and friendly
- Explain complex topics in simple language
- Acknowledge if you're not certain about something
- Respect the user's language and culture
- Provide creative and practical solutions
- Remember context and have natural conversations
- Respond in the same language the user is using"""
        }
        
        return prompts.get(language, prompts["default"])
    
    def _get_error_message(self, language: str) -> str:
        """Get error message in appropriate language"""
        messages = {
            "hi": f"माफ़ करें, मुझे कुछ तकनीकी समस्या हो रही है। कृपया थोड़ी देर बाद कोशिश करें। 🙏\n\n{Config.POWERED_BY}",
            "ur": f"معذرت، مجھے کچھ تکنیکی مسئلہ ہو رہا ہے۔ براہ کرم تھوڑی دیر بعد کوشش کریں۔ 🙏\n\n{Config.POWERED_BY}",
            "ar": f"عذراً، أواجه مشكلة تقنية. يرجى المحاولة مرة أخرى لاحقاً. 🙏\n\n{Config.POWERED_BY}",
            "default": f"Sorry, I'm experiencing some technical difficulties. Please try again later. 🙏\n\n{Config.POWERED_BY}"
        }
        return messages.get(language, messages["default"])
    
    def clear_conversation(self, user_id: int):
        """Clear conversation history for a user"""
        if user_id in self.conversation_history:
            del self.conversation_history[user_id]
    
    def get_conversation_count(self, user_id: int) -> int:
        """Get conversation message count for a user"""
        return len(self.conversation_history.get(user_id, []))