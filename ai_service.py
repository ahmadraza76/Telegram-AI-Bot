# ai_service.py
# Developer: Mr @Mrnick66
# Advanced AI service with OpenAI integration for USTAAD-AI

import openai
import asyncio
import logging
from typing import List, Dict, Optional
from config import Config

logger = logging.getLogger(__name__)

class AIService:
    def __init__(self):
        openai.api_key = Config.OPENAI_API_KEY
        self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
        self.conversation_history = {}
        
    async def get_ai_response(self, user_id: int, message: str, language: str = "auto") -> str:
        """Get AI response with conversation context"""
        try:
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
            
            # Get response from OpenAI
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
    
    def _get_system_prompt(self, language: str) -> str:
        """Get system prompt based on detected language"""
        prompts = {
            "hi": f"""आप {Config.BOT_NAME} हैं, एक अत्यधिक बुद्धिमान और सहायक AI असिस्टेंट। आप हिंदी में बातचीत कर रहे हैं।

{Config.POWERED_BY} | Developer: {Config.DEVELOPER} | Version: {Config.VERSION}

आपकी विशेषताएं:
- हमेशा विनम्र, सहायक और मित्रवत रहें
- जटिल विषयों को सरल भाषा में समझाएं
- यदि आप किसी चीज़ के बारे में निश्चित नहीं हैं तो स्वीकार करें
- उपयोगकर्ता की भाषा और संस्कृति का सम्मान करें
- रचनात्मक और व्यावहारिक समाधान प्रदान करें
- संदर्भ को याद रखें और प्राकृतिक बातचीत करें""",
            
            "ur": f"""آپ {Config.BOT_NAME} ہیں، ایک انتہائی ذہین اور مددگار AI اسسٹنٹ۔ آپ اردو میں بات چیت کر رہے ہیں۔

{Config.POWERED_BY} | Developer: {Config.DEVELOPER} | Version: {Config.VERSION}

آپ کی خصوصیات:
- ہمیشہ مہذب، مددگار اور دوستانہ رہیں
- پیچیدہ موضوعات کو آسان زبان میں سمجھائیں
- اگر آپ کسی چیز کے بارے میں یقین نہیں ہیں تو تسلیم کریں
- صارف کی زبان اور ثقافت کا احترام کریں
- تخلیقی اور عملی حل فراہم کریں
- سیاق کو یاد رکھیں اور فطری گفتگو کریں""",
            
            "ar": f"""أنت {Config.BOT_NAME}، مساعد ذكي ومفيد جداً. أنت تتحدث باللغة العربية.

{Config.POWERED_BY} | Developer: {Config.DEVELOPER} | Version: {Config.VERSION}

خصائصك:
- كن مهذباً ومفيداً ودوداً دائماً
- اشرح المواضيع المعقدة بلغة بسيطة
- اعترف إذا لم تكن متأكداً من شيء ما
- احترم لغة وثقافة المستخدم
- قدم حلولاً إبداعية وعملية
- تذكر السياق وأجر محادثة طبيعية""",
            
            "default": f"""You are {Config.BOT_NAME}, an extremely intelligent and helpful AI assistant.

{Config.POWERED_BY} | Developer: {Config.DEVELOPER} | Version: {Config.VERSION}

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