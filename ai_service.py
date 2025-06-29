# ai_service.py
# Developer: G A RAZA
# Advanced AI service with OpenAI integration

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
            "hi": """आप एक बहुत ही बुद्धिमान और सहायक AI असिस्टेंट हैं। आप हिंदी में बातचीत कर रहे हैं।
            - हमेशा विनम्र और सहायक रहें
            - जटिल विषयों को सरल भाषा में समझाएं
            - यदि आप किसी चीज़ के बारे में निश्चित नहीं हैं तो स्वीकार करें
            - उपयोगकर्ता की भाषा और संस्कृति का सम्मान करें""",
            
            "ur": """آپ ایک انتہائی ذہین اور مددگار AI اسسٹنٹ ہیں۔ آپ اردو میں بات چیت کر رہے ہیں۔
            - ہمیشہ مہذب اور مددگار رہیں
            - پیچیدہ موضوعات کو آسان زبان میں سمجھائیں
            - اگر آپ کسی چیز کے بارے میں یقین نہیں ہیں تو تسلیم کریں
            - صارف کی زبان اور ثقافت کا احترام کریں""",
            
            "ar": """أنت مساعد ذكي ومفيد جداً. أنت تتحدث باللغة العربية.
            - كن مهذباً ومفيداً دائماً
            - اشرح المواضيع المعقدة بلغة بسيطة
            - اعترف إذا لم تكن متأكداً من شيء ما
            - احترم لغة وثقافة المستخدم""",
            
            "default": """You are an extremely intelligent and helpful AI assistant.
            - Always be polite and helpful
            - Explain complex topics in simple language
            - Acknowledge if you're not certain about something
            - Respect the user's language and culture
            - Respond in the same language the user is using"""
        }
        
        return prompts.get(language, prompts["default"])
    
    def _get_error_message(self, language: str) -> str:
        """Get error message in appropriate language"""
        messages = {
            "hi": "माफ़ करें, मुझे कुछ तकनीकी समस्या हो रही है। कृपया थोड़ी देर बाद कोशिश करें। 🙏",
            "ur": "معذرت، مجھے کچھ تکنیکی مسئلہ ہو رہا ہے۔ براہ کرم تھوڑی دیر بعد کوشش کریں۔ 🙏",
            "ar": "عذراً، أواجه مشكلة تقنية. يرجى المحاولة مرة أخرى لاحقاً. 🙏",
            "default": "Sorry, I'm experiencing some technical difficulties. Please try again later. 🙏"
        }
        return messages.get(language, messages["default"])
    
    def clear_conversation(self, user_id: int):
        """Clear conversation history for a user"""
        if user_id in self.conversation_history:
            del self.conversation_history[user_id]
    
    def get_conversation_count(self, user_id: int) -> int:
        """Get conversation message count for a user"""
        return len(self.conversation_history.get(user_id, []))