# language_detector.py
# Developer: Mr @Mrnick66
# Advanced language detection and localization for USTAAD-AI

import re
from langdetect import detect, DetectorFactory
from typing import Dict, Optional
from config import Config

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
                'welcome': f"🎯 Welcome to {Config.BOT_NAME} {Config.VERSION}\n\n🧠 I'm your advanced AI assistant, powered by cutting-edge technology. I understand and respond in your language with human-like intelligence!\n\n{Config.POWERED_BY} | Developer: {Config.DEVELOPER}",
                'description': "🔥 **What makes me special:**\n• 🌍 Multi-language support (50+ languages)\n• 🧠 Context-aware conversations\n• ⚡ Lightning-fast responses\n• 🎯 Human-like understanding\n• 💡 Creative problem solving\n• 📚 Vast knowledge base",
                'start_chat': "💬 **Ready to chat?** Just send me any message and experience the future of AI!"
            },
            'hi': {
                'welcome': f"🎯 {Config.BOT_NAME} {Config.VERSION} में आपका स्वागत है\n\n🧠 मैं आपका एडवांस AI असिस्टेंट हूं, अत्याधुनिक तकनीक से संचालित। मैं आपकी भाषा समझता हूं और इंसान की तरह जवाब देता हूं!\n\n{Config.POWERED_BY} | डेवलपर: {Config.DEVELOPER}",
                'description': "🔥 **मुझे खास क्या बनाता है:**\n• 🌍 बहुभाषी समर्थन (50+ भाषाएं)\n• 🧠 संदर्भ-जागरूक बातचीत\n• ⚡ बिजली की तरह तेज़ जवाब\n• 🎯 इंसान जैसी समझ\n• 💡 रचनात्मक समस्या समाधान\n• 📚 विशाल ज्ञान भंडार",
                'start_chat': "💬 **बात करने के लिए तैयार?** बस मुझे कोई भी संदेश भेजें और AI के भविष्य का अनुभव करें!"
            },
            'ur': {
                'welcome': f"🎯 {Config.BOT_NAME} {Config.VERSION} میں خوش آمدید\n\n🧠 میں آپ کا ایڈوانس AI اسسٹنٹ ہوں، جدید ترین ٹیکنالوجی سے چلایا جاتا ہوں۔ میں آپ کی زبان سمجھتا ہوں اور انسان کی طرح جواب دیتا ہوں!\n\n{Config.POWERED_BY} | ڈیولپر: {Config.DEVELOPER}",
                'description': "🔥 **مجھے خاص کیا بناتا ہے:**\n• 🌍 کثیر لسانی سپورٹ (50+ زبانیں)\n• 🧠 سیاق و سباق کے ساتھ گفتگو\n• ⚡ بجلی کی طرح تیز جوابات\n• 🎯 انسان جیسی سمجھ\n• 💡 تخلیقی مسئلہ حل کرنا\n• 📚 وسیع علمی ذخیرہ",
                'start_chat': "💬 **بات کرنے کے لیے تیار؟** بس مجھے کوئی بھی پیغام بھیجیں اور AI کے مستقبل کا تجربہ کریں!"
            },
            'ar': {
                'welcome': f"🎯 مرحباً بك في {Config.BOT_NAME} {Config.VERSION}\n\n🧠 أنا مساعدك الذكي المتقدم، مدعوم بأحدث التقنيات. أفهم لغتك وأرد بذكاء يشبه البشر!\n\n{Config.POWERED_BY} | المطور: {Config.DEVELOPER}",
                'description': "🔥 **ما يجعلني مميزاً:**\n• 🌍 دعم متعدد اللغات (50+ لغة)\n• 🧠 محادثات واعية بالسياق\n• ⚡ ردود سريعة كالبرق\n• 🎯 فهم يشبه البشر\n• 💡 حل المشاكل الإبداعي\n• 📚 قاعدة معرفية واسعة",
                'start_chat': "💬 **مستعد للدردشة؟** فقط أرسل لي أي رسالة واختبر مستقبل الذكاء الاصطناعي!"
            }
        }
        
        return messages.get(lang_code, messages['en'])
    
    def get_help_message(self, lang_code: str) -> str:
        """Get help message in detected language"""
        help_messages = {
            'en': f"""🆘 **{Config.BOT_NAME} Help Guide**

🎯 **How to use me:**
• Just send any message - I'll respond intelligently
• I understand context and remember our conversation
• I can help with any topic in any language

💡 **Available Commands:**
• `/start` - Welcome message and main menu
• `/help` - Show this help guide
• `/info` - Bot information and developer details

🌟 **Pro Tips:**
• Ask specific questions for better answers
• I work best with clear, detailed queries
• Switch languages anytime - I'll adapt automatically

{Config.POWERED_BY} | {Config.VERSION}""",
            
            'hi': f"""🆘 **{Config.BOT_NAME} सहायता गाइड**

🎯 **मुझे कैसे उपयोग करें:**
• बस कोई भी संदेश भेजें - मैं बुद्धिमानी से जवाब दूंगा
• मैं संदर्भ समझता हूं और हमारी बातचीत याद रखता हूं
• मैं किसी भी भाषा में किसी भी विषय पर मदद कर सकता हूं

💡 **उपलब्ध कमांड:**
• `/start` - स्वागत संदेश और मुख्य मेनू
• `/help` - यह सहायता गाइड दिखाएं
• `/info` - बॉट जानकारी और डेवलपर विवरण

🌟 **प्रो टिप्स:**
• बेहतर उत्तर के लिए विशिष्ट प्रश्न पूछें
• मैं स्पष्ट, विस्तृत प्रश्नों के साथ सबसे अच्छा काम करता हूं
• कभी भी भाषा बदलें - मैं अपने आप अनुकूलित हो जाऊंगा

{Config.POWERED_BY} | {Config.VERSION}""",
            
            'ur': f"""🆘 **{Config.BOT_NAME} ہیلپ گائیڈ**

🎯 **مجھے کیسے استعمال کریں:**
• بس کوئی بھی پیغام بھیجیں - میں ذہانت سے جواب دوں گا
• میں سیاق سمجھتا ہوں اور ہماری گفتگو یاد رکھتا ہوں
• میں کسی بھی زبان میں کسی بھی موضوع پر مدد کر سکتا ہوں

💡 **دستیاب کمانڈز:**
• `/start` - خوش آمدید پیغام اور مین مینو
• `/help` - یہ ہیلپ گائیڈ دکھائیں
• `/info` - بوٹ کی معلومات اور ڈیولپر کی تفصیلات

🌟 **پرو ٹپس:**
• بہتر جوابات کے لیے مخصوص سوالات پوچھیں
• میں واضح، تفصیلی سوالات کے ساتھ بہترین کام کرتا ہوں
• کبھی بھی زبان تبدیل کریں - میں خودکار طور پر ڈھل جاؤں گا

{Config.POWERED_BY} | {Config.VERSION}""",
            
            'ar': f"""🆘 **دليل مساعدة {Config.BOT_NAME}**

🎯 **كيفية استخدامي:**
• فقط أرسل أي رسالة - سأرد بذكاء
• أفهم السياق وأتذكر محادثتنا
• يمكنني المساعدة في أي موضوع بأي لغة

💡 **الأوامر المتاحة:**
• `/start` - رسالة الترحيب والقائمة الرئيسية
• `/help` - إظهار دليل المساعدة هذا
• `/info` - معلومات البوت وتفاصيل المطور

🌟 **نصائح احترافية:**
• اطرح أسئلة محددة للحصول على إجابات أفضل
• أعمل بشكل أفضل مع الاستفسارات الواضحة والمفصلة
• غيّر اللغات في أي وقت - سأتكيف تلقائياً

{Config.POWERED_BY} | {Config.VERSION}"""
        }
        
        return help_messages.get(lang_code, help_messages['en'])
    
    def get_info_message(self, lang_code: str) -> str:
        """Get bot info message in detected language"""
        info_messages = {
            'en': f"""ℹ️ **{Config.BOT_NAME} Information**

🤖 **Bot Details:**
• Name: {Config.BOT_NAME}
• Version: {Config.VERSION}
• Model: GPT-3.5 Turbo
• Developer: {Config.DEVELOPER}

🔥 **Advanced Features:**
• 🌍 50+ Language Support
• 🧠 Context-Aware AI
• ⚡ Real-time Responses
• 🎯 Human-like Intelligence
• 💡 Creative Problem Solving
• 📚 Vast Knowledge Base

🛠️ **Technical Specs:**
• Built with Python & OpenAI API
• Advanced Language Detection
• Smart Response Formatting
• Optimized Performance
• Secure & Private

👨‍💻 **Developer Info:**
• Created by: {Config.DEVELOPER}
• Specialized in AI Development
• Telegram Bot Expert
• {Config.POWERED_BY}

💬 Ready to experience the future of AI? Just send me any message!""",
            
            'hi': f"""ℹ️ **{Config.BOT_NAME} जानकारी**

🤖 **बॉट विवरण:**
• नाम: {Config.BOT_NAME}
• संस्करण: {Config.VERSION}
• मॉडल: GPT-3.5 Turbo
• डेवलपर: {Config.DEVELOPER}

🔥 **एडवांस फीचर्स:**
• 🌍 50+ भाषा समर्थन
• 🧠 संदर्भ-जागरूक AI
• ⚡ रियल-टाइम रिस्पॉन्स
• 🎯 इंसान जैसी बुद्धिमत्ता
• 💡 रचनात्मक समस्या समाधान
• 📚 विशाल ज्ञान भंडार

🛠️ **तकनीकी विशेषताएं:**
• Python और OpenAI API के साथ निर्मित
• एडवांस भाषा पहचान
• स्मार्ट रिस्पॉन्स फॉर्मेटिंग
• अनुकूलित प्रदर्शन
• सुरक्षित और निजी

👨‍💻 **डेवलपर जानकारी:**
• निर्माता: {Config.DEVELOPER}
• AI डेवलपमेंट में विशेषज्ञ
• टेलीग्राम बॉट एक्सपर्ट
• {Config.POWERED_BY}

💬 AI के भविष्य का अनुभव करने के लिए तैयार? बस मुझे कोई भी संदेश भेजें!""",
            
            'ur': f"""ℹ️ **{Config.BOT_NAME} معلومات**

🤖 **بوٹ کی تفصیلات:**
• نام: {Config.BOT_NAME}
• ورژن: {Config.VERSION}
• ماڈل: GPT-3.5 Turbo
• ڈیولپر: {Config.DEVELOPER}

🔥 **ایڈوانس فیچرز:**
• 🌍 50+ زبانوں کی سپورٹ
• 🧠 سیاق آگاہ AI
• ⚡ ریئل ٹائم جوابات
• 🎯 انسان جیسی ذہانت
• 💡 تخلیقی مسئلہ حل کرنا
• 📚 وسیع علمی ذخیرہ

🛠️ **تکنیکی خصوصیات:**
• Python اور OpenAI API کے ساتھ بنایا گیا
• ایڈوانس زبان کی شناخت
• سمارٹ رسپانس فارمیٹنگ
• بہتر کارکردگی
• محفوظ اور نجی

👨‍💻 **ڈیولپر کی معلومات:**
• بنانے والا: {Config.DEVELOPER}
• AI ڈیولپمنٹ میں ماہر
• ٹیلیگرام بوٹ ایکسپرٹ
• {Config.POWERED_BY}

💬 AI کے مستقبل کا تجربہ کرنے کے لیے تیار؟ بس مجھے کوئی بھی پیغام بھیجیں!""",
            
            'ar': f"""ℹ️ **معلومات {Config.BOT_NAME}**

🤖 **تفاصيل البوت:**
• الاسم: {Config.BOT_NAME}
• الإصدار: {Config.VERSION}
• النموذج: GPT-3.5 Turbo
• المطور: {Config.DEVELOPER}

🔥 **الميزات المتقدمة:**
• 🌍 دعم 50+ لغة
• 🧠 ذكاء اصطناعي واعي بالسياق
• ⚡ ردود فورية
• 🎯 ذكاء يشبه البشر
• 💡 حل المشاكل الإبداعي
• 📚 قاعدة معرفية واسعة

🛠️ **المواصفات التقنية:**
• مبني بـ Python و OpenAI API
• كشف لغة متقدم
• تنسيق ردود ذكي
• أداء محسّن
• آمن وخاص

👨‍💻 **معلومات المطور:**
• المنشئ: {Config.DEVELOPER}
• متخصص في تطوير الذكاء الاصطناعي
• خبير بوتات تيليجرام
• {Config.POWERED_BY}

💬 مستعد لتجربة مستقبل الذكاء الاصطناعي؟ فقط أرسل لي أي رسالة!"""
        }
        
        return info_messages.get(lang_code, info_messages['en'])