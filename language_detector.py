# language_detector.py
# Developer: G A RAZA
# Advanced language detection and localization

import re
from langdetect import detect, DetectorFactory
from typing import Dict, Optional

# Set seed for consistent results
DetectorFactory.seed = 0

class LanguageDetector:
    def __init__(self):
        self.language_patterns = {
            'hi': re.compile(r'[\u0900-\u097F]'),  # Devanagari
            'ur': re.compile(r'[\u0600-\u06FF]'),  # Arabic/Urdu
            'ar': re.compile(r'[\u0600-\u06FF]'),  # Arabic
            'bn': re.compile(r'[\u0980-\u09FF]'),  # Bengali
            'ta': re.compile(r'[\u0B80-\u0BFF]'),  # Tamil
            'te': re.compile(r'[\u0C00-\u0C7F]'),  # Telugu
        }
        
        self.language_names = {
            'en': 'English',
            'hi': 'हिंदी',
            'ur': 'اردو',
            'ar': 'العربية',
            'bn': 'বাংলা',
            'ta': 'தமிழ்',
            'te': 'తెలుగు',
            'es': 'Español',
            'fr': 'Français',
            'de': 'Deutsch',
            'it': 'Italiano',
            'pt': 'Português',
            'ru': 'Русский',
            'ja': '日本語',
            'ko': '한국어',
            'zh': '中文'
        }
    
    def detect_language(self, text: str) -> str:
        """Detect language of the input text"""
        if not text or len(text.strip()) < 3:
            return 'en'
        
        try:
            # First check for script patterns
            for lang, pattern in self.language_patterns.items():
                if pattern.search(text):
                    return lang
            
            # Use langdetect for other languages
            detected = detect(text)
            return detected if detected in self.language_names else 'en'
            
        except Exception:
            return 'en'
    
    def get_language_name(self, lang_code: str) -> str:
        """Get language name in its native script"""
        return self.language_names.get(lang_code, 'English')
    
    def get_welcome_message(self, lang_code: str) -> Dict[str, str]:
        """Get welcome message in detected language"""
        messages = {
            'en': {
                'welcome': "🌟 Welcome to Premium AI Assistant!\n\nI'm your intelligent companion, ready to help you with anything. Just send me a message and I'll respond in your language!",
                'features': "✨ What I can do:\n• Answer questions in any language\n• Help with writing and creativity\n• Solve problems and explain concepts\n• Have natural conversations\n• Remember our chat context",
                'start_chat': "💬 Start chatting with me now!"
            },
            'hi': {
                'welcome': "🌟 प्रीमियम AI असिस्टेंट में आपका स्वागत है!\n\nमैं आपका बुद्धिमान साथी हूं, आपकी किसी भी मदद के लिए तैयार हूं। बस मुझे एक संदेश भेजें और मैं आपकी भाषा में जवाब दूंगा!",
                'features': "✨ मैं क्या कर सकता हूं:\n• किसी भी भाषा में सवालों के जवाब\n• लेखन और रचनात्मकता में मदद\n• समस्याओं का समाधान और अवधारणाओं की व्याख्या\n• प्राकृतिक बातचीत\n• हमारी चैट का संदर्भ याद रखना",
                'start_chat': "💬 अब मुझसे बात करना शुरू करें!"
            },
            'ur': {
                'welcome': "🌟 پریمیم AI اسسٹنٹ میں خوش آمدید!\n\nمیں آپ کا ذہین ساتھی ہوں، آپ کی ہر مدد کے لیے تیار ہوں۔ بس مجھے ایک پیغام بھیجیں اور میں آپ کی زبان میں جواب دوں گا!",
                'features': "✨ میں کیا کر سکتا ہوں:\n• کسی بھی زبان میں سوالات کے جوابات\n• تحریر اور تخلیقی کام میں مدد\n• مسائل کا حل اور تصورات کی وضاحت\n• فطری گفتگو\n• ہماری چیٹ کا سیاق یاد رکھنا",
                'start_chat': "💬 اب مجھ سے بات کرنا شروع کریں!"
            },
            'ar': {
                'welcome': "🌟 مرحباً بك في المساعد الذكي المتقدم!\n\nأنا رفيقك الذكي، مستعد لمساعدتك في أي شيء. فقط أرسل لي رسالة وسأرد بلغتك!",
                'features': "✨ ما يمكنني فعله:\n• الإجابة على الأسئلة بأي لغة\n• المساعدة في الكتابة والإبداع\n• حل المشاكل وشرح المفاهيم\n• إجراء محادثات طبيعية\n• تذكر سياق محادثتنا",
                'start_chat': "💬 ابدأ المحادثة معي الآن!"
            }
        }
        
        return messages.get(lang_code, messages['en'])