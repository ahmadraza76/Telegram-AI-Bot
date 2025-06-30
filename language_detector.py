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
            'hi': re.compile(r'[\u0900-\u097F]'),  # Devanagari (Hindi)
            'bn': re.compile(r'[\u0980-\u09FF]'),  # Bengali
            'mr': re.compile(r'[\u0900-\u097F]'),  # Marathi (uses Devanagari)
            'te': re.compile(r'[\u0C00-\u0C7F]'),  # Telugu
            'ta': re.compile(r'[\u0B80-\u0BFF]'),  # Tamil
            'gu': re.compile(r'[\u0A80-\u0AFF]'),  # Gujarati
            'ur': re.compile(r'[\u0600-\u06FF]'),  # Urdu (Arabic script)
            'kn': re.compile(r'[\u0C80-\u0CFF]'),  # Kannada
            'or': re.compile(r'[\u0B00-\u0B7F]'),  # Odia
            'pa': re.compile(r'[\u0A00-\u0A7F]'),  # Punjabi (Gurmukhi)
        }
        
        self.language_names = {
            'en': 'English',
            'hi': 'हिंदी',
            'bn': 'বাংলা',
            'mr': 'मराठी',
            'te': 'తెలుగు',
            'ta': 'தமிழ்',
            'gu': 'ગુજરાતી',
            'ur': 'اردو',
            'kn': 'ಕನ್ನಡ',
            'or': 'ଓଡ଼ିଆ',
            'pa': 'ਪੰਜਾਬੀ'
        }
        
        # Clean popular languages without speaker numbers
        self.popular_languages = {
            'hi': 'Hindi',
            'bn': 'Bengali',
            'mr': 'Marathi',
            'te': 'Telugu',
            'ta': 'Tamil',
            'gu': 'Gujarati',
            'ur': 'Urdu',
            'kn': 'Kannada',
            'or': 'Odia',
            'pa': 'Punjabi',
            'en': 'English'
        }
    
    def detect_language(self, text: str) -> str:
        """Detect language of the input text"""
        if not text or len(text.strip()) < 3:
            return 'hi'  # Default to Hindi
        
        try:
            # First check for script patterns
            for lang, pattern in self.language_patterns.items():
                if pattern.search(text):
                    return lang
            
            # Use langdetect for other languages
            detected = detect(text)
            return detected if detected in self.language_names else 'hi'
            
        except Exception:
            return 'hi'  # Default to Hindi
    
    def get_language_name(self, lang_code: str) -> str:
        """Get language name in its native script"""
        return self.language_names.get(lang_code, 'हिंदी')
    
    def get_popular_languages(self) -> Dict[str, str]:
        """Get popular languages for selection"""
        return self.popular_languages
    
    def get_language_settings_message(self, lang_code: str) -> str:
        """Get language settings message"""
        messages = {
            'en': f"""**Language Settings**

**Current Language**: {self.language_names.get(lang_code, 'English')}

Choose your preferred language for conversations:

**Indian Languages:**
1. Hindi
2. Bengali
3. Marathi
4. Telugu
5. Tamil
6. Gujarati
7. Urdu
8. Kannada
9. Odia
10. Punjabi

**Note**: You can change language anytime using the settings menu.

{Config.POWERED_BY} | {Config.VERSION}""",
            
            'hi': f"""**भाषा सेटिंग्स**

**वर्तमान भाषा**: {self.language_names.get(lang_code, 'हिंदी')}

बातचीत के लिए अपनी पसंदीदा भाषा चुनें:

**भारतीय भाषाएं:**
1. Hindi
2. Bengali
3. Marathi
4. Telugu
5. Tamil
6. Gujarati
7. Urdu
8. Kannada
9. Odia
10. Punjabi

**नोट**: आप सेटिंग्स मेनू का उपयोग करके कभी भी भाषा बदल सकते हैं।

{Config.POWERED_BY} | {Config.VERSION}""",
            
            'ur': f"""**زبان کی سیٹنگز**

**موجودہ زبان**: {self.language_names.get(lang_code, 'اردو')}

بات چیت کے لیے اپنی پسندیدہ زبان منتخب کریں:

**ہندوستانی زبانیں:**
1. Hindi
2. Bengali
3. Marathi
4. Telugu
5. Tamil
6. Gujarati
7. Urdu
8. Kannada
9. Odia
10. Punjabi

**نوٹ**: آپ سیٹنگز مینو استعمال کرکے کبھی بھی زبان تبدیل کر سکتے ہیں۔

{Config.POWERED_BY} | {Config.VERSION}""",
            
            'bn': f"""**ভাষার সেটিংস**

**বর্তমান ভাষা**: {self.language_names.get(lang_code, 'বাংলা')}

কথোপকথনের জন্য আপনার পছন্দের ভাষা বেছে নিন:

**ভারতীয় ভাষাসমূহ:**
1. Hindi
2. Bengali
3. Marathi
4. Telugu
5. Tamil
6. Gujarati
7. Urdu
8. Kannada
9. Odia
10. Punjabi

**নোট**: আপনি সেটিংস মেনু ব্যবহার করে যেকোনো সময় ভাষা পরিবর্তন করতে পারেন।

{Config.POWERED_BY} | {Config.VERSION}"""
        }
        
        return messages.get(lang_code, messages['hi'])
    
    def get_welcome_message(self, lang_code: str) -> Dict[str, str]:
        """Get welcome message in detected language"""
        messages = {
            'en': {
                'welcome': f"Welcome to {Config.BOT_NAME} {Config.VERSION}\n\nI'm your advanced AI assistant, powered by cutting-edge technology. I understand and respond in your language with human-like intelligence!\n\n{Config.POWERED_BY} | Developer: {Config.DEVELOPER}",
                'description': "**What makes me special:**\n• Indian Language Support (11 languages)\n• Context-aware conversations\n• Lightning-fast responses\n• Human-like understanding\n• Creative problem solving\n• Vast knowledge base",
                'start_chat': "**Ready to chat?** Just send me any message and experience the future of AI!"
            },
            'hi': {
                'welcome': f"{Config.BOT_NAME} {Config.VERSION} में आपका स्वागत है\n\nमैं आपका एडवांस AI असिस्टेंट हूं, अत्याधुनिक तकनीक से संचालित। मैं आपकी भाषा समझता हूं और इंसान की तरह जवाब देता हूं!\n\n{Config.POWERED_BY} | डेवलपर: {Config.DEVELOPER}",
                'description': "**मुझे खास क्या बनाता है:**\n• भारतीय भाषा समर्थन (11 भाषाएं)\n• संदर्भ-जागरूक बातचीत\n• बिजली की तरह तेज़ जवाब\n• इंसान जैसी समझ\n• रचनात्मक समस्या समाधान\n• विशाल ज्ञान भंडार",
                'start_chat': "**बात करने के लिए तैयार?** बस मुझे कोई भी संदेश भेजें और AI के भविष्य का अनुभव करें!"
            },
            'ur': {
                'welcome': f"{Config.BOT_NAME} {Config.VERSION} میں خوش آمدید\n\nمیں آپ کا ایڈوانس AI اسسٹنٹ ہوں، جدید ترین ٹیکنالوجی سے چلایا جاتا ہوں۔ میں آپ کی زبان سمجھتا ہوں اور انسان کی طرح جواب دیتا ہوں!\n\n{Config.POWERED_BY} | ڈیولپر: {Config.DEVELOPER}",
                'description': "**مجھے خاص کیا بناتا ہے:**\n• ہندوستانی زبان کی سپورٹ (11 زبانیں)\n• سیاق و سباق کے ساتھ گفتگو\n• بجلی کی طرح تیز جوابات\n• انسان جیسی سمجھ\n• تخلیقی مسئلہ حل کرنا\n• وسیع علمی ذخیرہ",
                'start_chat': "**بات کرنے کے لیے تیار؟** بس مجھے کوئی بھی پیغام بھیجیں اور AI کے مستقبل کا تجربہ کریں!"
            },
            'bn': {
                'welcome': f"{Config.BOT_NAME} {Config.VERSION} এ স্বাগতম\n\nআমি আপনার উন্নত AI সহায়ক, অত্যাধুনিক প্রযুক্তি দ্বারা চালিত। আমি আপনার ভাষা বুঝি এবং মানুষের মতো উত্তর দিই!\n\n{Config.POWERED_BY} | ডেভেলপার: {Config.DEVELOPER}",
                'description': "**আমাকে বিশেষ করে তোলে:**\n• ভারতীয় ভাষা সমর্থন (11টি ভাষা)\n• প্রসঙ্গ-সচেতন কথোপকথন\n• বিদ্যুৎ-দ্রুত প্রতিক্রিয়া\n• মানুষের মতো বোঝাপড়া\n• সৃজনশীল সমস্যা সমাধান\n• বিশাল জ্ঞানের ভাণ্ডার",
                'start_chat': "**চ্যাট করতে প্রস্তুত?** শুধু আমাকে যেকোনো বার্তা পাঠান এবং AI এর ভবিষ্যতের অভিজ্ঞতা নিন!"
            },
            'mr': {
                'welcome': f"{Config.BOT_NAME} {Config.VERSION} मध्ये आपले स्वागत आहे\n\nमी तुमचा प्रगत AI सहाय्यक आहे, अत्याधुनिक तंत्रज्ञानाने चालवलेला। मी तुमची भाषा समजतो आणि माणसासारखे उत्तर देतो!\n\n{Config.POWERED_BY} | डेव्हलपर: {Config.DEVELOPER}",
                'description': "**मला विशेष काय बनवते:**\n• भारतीय भाषा समर्थन (11 भाषा)\n• संदर्भ-जागरूक संभाषण\n• विजेसारखे वेगवान उत्तरे\n• माणसासारखी समज\n• सर्जनशील समस्या निराकरण\n• विशाल ज्ञान भांडार",
                'start_chat': "**गप्पा मारायला तयार?** फक्त मला कोणताही संदेश पाठवा आणि AI च्या भविष्याचा अनुभव घ्या!"
            },
            'te': {
                'welcome': f"{Config.BOT_NAME} {Config.VERSION} కు స్వాగతం\n\nనేను మీ అధునాతన AI సహాయకుడిని, అత్యాధునిక సాంకేతికతతో శక్తివంతం। నేను మీ భాషను అర్థం చేసుకుని మనిషిలా జవాబిస్తాను!\n\n{Config.POWERED_BY} | డెవలపర్: {Config.DEVELOPER}",
                'description': "**నన్ను ప్రత్యేకం చేసేవి:**\n• భారతీయ భాషా మద్దతు (11 భాషలు)\n• సందర్భ-అవగాహన సంభాషణలు\n• మెరుపు-వేగ ప్రతిస్పందనలు\n• మానవ-వంటి అవగాహన\n• సృజనాత్మక సమస్య పరిష్కారం\n• విస్తృత జ్ఞాన భాండాగారం",
                'start_chat': "**చాట్ చేయడానికి సిద్ధంగా ఉన్నారా?** నాకు ఏదైనా సందేశం పంపండి మరియు AI భవిష్యత్తును అనుభవించండి!"
            },
            'ta': {
                'welcome': f"{Config.BOT_NAME} {Config.VERSION} க்கு வரவேற்கிறோம்\n\nநான் உங்கள் மேம்பட்ட AI உதவியாளர், அதிநவீன தொழில்நுட்பத்தால் இயக்கப்படுகிறேன். நான் உங்கள் மொழியைப் புரிந்துகொண்டு மனிதனைப் போல பதிலளிக்கிறேன்!\n\n{Config.POWERED_BY} | டெவலப்பர்: {Config.DEVELOPER}",
                'description': "**என்னை சிறப்பாக்குவது:**\n• இந்திய மொழி ஆதரவு (11 மொழிகள்)\n• சூழல்-விழிப்புணர்வு உரையாடல்கள்\n• மின்னல்-வேக பதில்கள்\n• மனித-போன்ற புரிதல்\n• ஆக்கப்பூர்வ சிக்கல் தீர்வு\n• பரந்த அறிவுக் களஞ்சியம்",
                'start_chat': "**அரட்டையடிக்க தயாரா?** எனக்கு ஏதேனும் செய்தி அனுப்பி AI இன் எதிர்காலத்தை அனுபவியுங்கள்!"
            },
            'gu': {
                'welcome': f"{Config.BOT_NAME} {Config.VERSION} માં તમારું સ્વાગત છે\n\nહું તમારો અદ્યતન AI સહાયક છું, અત્યાધુનિક ટેકનોલોજીથી સંચાલિત. હું તમારી ભાષા સમજું છું અને માનવીની જેમ જવાબ આપું છું!\n\n{Config.POWERED_BY} | ડેવલપર: {Config.DEVELOPER}",
                'description': "**મને વિશેષ બનાવે છે:**\n• ભારતીય ભાષા સપોર્ટ (11 ભાષાઓ)\n• સંદર્ભ-જાગૃત વાતચીત\n• વીજળી-ઝડપી જવાબો\n• માનવ-જેવી સમજ\n• સર્જનાત્મક સમસ્યા નિરાકરણ\n• વિશાળ જ્ઞાન ભંડાર",
                'start_chat': "**ચેટ કરવા તૈયાર છો?** મને કોઈપણ સંદેશ મોકલો અને AI ના ભવિષ્યનો અનુભવ કરો!"
            },
            'kn': {
                'welcome': f"{Config.BOT_NAME} {Config.VERSION} ಗೆ ಸ್ವಾಗತ\n\nನಾನು ನಿಮ್ಮ ಸುಧಾರಿತ AI ಸಹಾಯಕ, ಅತ್ಯಾಧುನಿಕ ತಂತ್ರಜ್ಞಾನದಿಂದ ಚಾಲಿತ. ನಾನು ನಿಮ್ಮ ಭಾಷೆಯನ್ನು ಅರ್ಥಮಾಡಿಕೊಂಡು ಮನುಷ್ಯನಂತೆ ಉತ್ತರಿಸುತ್ತೇನೆ!\n\n{Config.POWERED_BY} | ಡೆವಲಪರ್: {Config.DEVELOPER}",
                'description': "**ನನ್ನನ್ನು ವಿಶೇಷಗೊಳಿಸುವುದು:**\n• ಭಾರತೀಯ ಭಾಷಾ ಬೆಂಬಲ (11 ಭಾಷೆಗಳು)\n• ಸಂದರ್ಭ-ಅರಿವಿನ ಸಂಭಾಷಣೆಗಳು\n• ಮಿಂಚು-ವೇಗದ ಪ್ರತಿಕ್ರಿಯೆಗಳು\n• ಮಾನವ-ತರಹದ ತಿಳುವಳಿಕೆ\n• ಸೃಜನಾತ್ಮಕ ಸಮಸ್ಯೆ ಪರಿಹಾರ\n• ವಿಶಾಲ ಜ್ಞಾನ ಭಂಡಾರ",
                'start_chat': "**ಚಾಟ್ ಮಾಡಲು ಸಿದ್ಧರಿದ್ದೀರಾ?** ನನಗೆ ಯಾವುದೇ ಸಂದೇಶವನ್ನು ಕಳುಹಿಸಿ ಮತ್ತು AI ಯ ಭವಿಷ್ಯವನ್ನು ಅನುಭವಿಸಿ!"
            },
            'or': {
                'welcome': f"{Config.BOT_NAME} {Config.VERSION} କୁ ସ୍ୱାଗତ\n\nମୁଁ ଆପଣଙ୍କର ଉନ୍ନତ AI ସହାୟକ, ଅତ୍ୟାଧୁନିକ ପ୍ରଯୁକ୍ତିବିଦ୍ୟା ଦ୍ୱାରା ଚାଳିତ। ମୁଁ ଆପଣଙ୍କ ଭାଷା ବୁଝେ ଏବଂ ମଣିଷ ପରି ଉତ୍ତର ଦିଏ!\n\n{Config.POWERED_BY} | ଡେଭେଲପର: {Config.DEVELOPER}",
                'description': "**ମୋତେ ବିଶେଷ କରେ:**\n• ଭାରତୀୟ ଭାଷା ସମର୍ଥନ (11 ଭାଷା)\n• ପ୍ରସଙ୍ଗ-ସଚେତନ କଥାବାର୍ତ୍ତା\n• ବିଜୁଳି-ଦ୍ରୁତ ପ୍ରତିକ୍ରିୟା\n• ମାନବ-ପରି ବୁଝାମଣା\n• ସୃଜନଶୀଳ ସମସ୍ୟା ସମାଧାନ\n• ବିଶାଳ ଜ୍ଞାନ ଭଣ୍ଡାର",
                'start_chat': "**ଚାଟ୍ କରିବାକୁ ପ୍ରସ୍ତୁତ?** ମୋତେ କୌଣସି ବାର୍ତ୍ତା ପଠାନ୍ତୁ ଏବଂ AI ର ଭବିଷ୍ୟତ ଅନୁଭବ କରନ୍ତୁ!"
            },
            'pa': {
                'welcome': f"{Config.BOT_NAME} {Config.VERSION} ਵਿੱਚ ਤੁਹਾਡਾ ਸੁਆਗਤ ਹੈ\n\nਮੈਂ ਤੁਹਾਡਾ ਉੱਨਤ AI ਸਹਾਇਕ ਹਾਂ, ਅਤਿ-ਆਧੁਨਿਕ ਤਕਨਾਲੋਜੀ ਨਾਲ ਚਲਾਇਆ ਗਿਆ। ਮੈਂ ਤੁਹਾਡੀ ਭਾਸ਼ਾ ਸਮਝਦਾ ਹਾਂ ਅਤੇ ਇਨਸਾਨ ਵਾਂਗ ਜਵਾਬ ਦਿੰਦਾ ਹਾਂ!\n\n{Config.POWERED_BY} | ਡਿਵੈਲਪਰ: {Config.DEVELOPER}",
                'description': "**ਮੈਨੂੰ ਖਾਸ ਕੀ ਬਣਾਉਂਦਾ ਹੈ:**\n• ਭਾਰਤੀ ਭਾਸ਼ਾ ਸਹਾਇਤਾ (11 ਭਾਸ਼ਾਵਾਂ)\n• ਸੰਦਰਭ-ਜਾਗਰੂਕ ਗੱਲਬਾਤ\n• ਬਿਜਲੀ-ਤੇਜ਼ ਜਵਾਬ\n• ਇਨਸਾਨ-ਵਰਗੀ ਸਮਝ\n• ਰਚਨਾਤਮਕ ਸਮੱਸਿਆ ਹੱਲ\n• ਵਿਸ਼ਾਲ ਗਿਆਨ ਭੰਡਾਰ",
                'start_chat': "**ਚੈਟ ਕਰਨ ਲਈ ਤਿਆਰ?** ਮੈਨੂੰ ਕੋਈ ਵੀ ਸੰਦੇਸ਼ ਭੇਜੋ ਅਤੇ AI ਦੇ ਭਵਿੱਖ ਦਾ ਅਨੁਭਵ ਕਰੋ!"
            }
        }
        
        return messages.get(lang_code, messages['hi'])
    
    def get_help_message(self, lang_code: str) -> str:
        """Get help message in detected language"""
        help_messages = {
            'en': f"""**USTAAD-AI HELP GUIDE v2.5.0**
=============================

**HOW TO USE:**
- Send any message to receive intelligent responses
- Maintains conversation context automatically
- Supports all topics across multiple languages

**AVAILABLE COMMANDS:**
/start  : Display welcome message and main menu
/help   : Show this help documentation
/info   : View system specifications and developer info

**USAGE RECOMMENDATIONS:**
1. Formulate specific questions for precise answers
2. Provide clear, detailed queries for optimal results
3. Language switching supported mid-conversation

**TECHNICAL DETAILS:**
- AI Model: Groq LLaMA 3 8B
- Framework: USTAAD-AI Engine
- Developer: {Config.DEVELOPER}
- System Version: {Config.VERSION}

**SYSTEM STATUS**: [ONLINE]

{Config.POWERED_BY} | {Config.VERSION}""",
            
            'hi': f"""**USTAAD-AI HELP GUIDE v2.5.0**
=============================

**उपयोग कैसे करें:**
- बुद्धिमान उत्तर प्राप्त करने के लिए कोई भी संदेश भेजें
- बातचीत का संदर्भ स्वचालित रूप से बनाए रखता है
- कई भाषाओं में सभी विषयों का समर्थन करता है

**उपलब्ध कमांड:**
/start  : स्वागत संदेश और मुख्य मेनू प्रदर्शित करें
/help   : यह सहायता दस्तावेज़ दिखाएं
/info   : सिस्टम विनिर्देश और डेवलपर जानकारी देखें

**उपयोग की सिफारिशें:**
1. सटीक उत्तरों के लिए विशिष्ट प्रश्न तैयार करें
2. इष्टतम परिणामों के लिए स्पष्ट, विस्तृत प्रश्न प्रदान करें
3. बातचीत के बीच में भाषा बदलना समर्थित है

**तकनीकी विवरण:**
- AI मॉडल: Groq LLaMA 3 8B
- फ्रेमवर्क: USTAAD-AI Engine
- डेवलपर: {Config.DEVELOPER}
- सिस्टम संस्करण: {Config.VERSION}

**सिस्टम स्थिति**: [ऑनलाइन]

{Config.POWERED_BY} | {Config.VERSION}""",
            
            'ur': f"""**USTAAD-AI HELP GUIDE v2.5.0**
=============================

**استعمال کیسے کریں:**
- ذہین جوابات حاصل کرنے کے لیے کوئی بھی پیغام بھیجیں
- گفتگو کا سیاق خودکار طور پر برقرار رکھتا ہے
- متعدد زبانوں میں تمام موضوعات کی حمایت کرتا ہے

**دستیاب کمانڈز:**
/start  : خوش آمدید پیغام اور مین مینو دکھائیں
/help   : یہ مدد کی دستاویز دکھائیں
/info   : سسٹم کی تفصیلات اور ڈیولپر کی معلومات دیکھیں

**استعمال کی تجاویز:**
1. درست جوابات کے لیے مخصوص سوالات تیار کریں
2. بہترین نتائج کے لیے واضح، تفصیلی سوالات فراہم کریں
3. گفتگو کے دوران زبان تبدیل کرنا سپورٹ شدہ ہے

**تکنیکی تفصیلات:**
- AI ماڈل: Groq LLaMA 3 8B
- فریم ورک: USTAAD-AI Engine
- ڈیولپر: {Config.DEVELOPER}
- سسٹم ورژن: {Config.VERSION}

**سسٹم کی حالت**: [آن لائن]

{Config.POWERED_BY} | {Config.VERSION}"""
        }
        
        return help_messages.get(lang_code, help_messages['hi'])
    
    def get_info_message(self, lang_code: str) -> str:
        """Get bot info message in detected language"""
        info_messages = {
            'en': f"""╔══════════════════════════════════════════════╗
║   ██╗   ██╗███████╗████████╗ █████╗ █████╗   ║
║   ██║   ██║██╔════╝╚══██╔══╝██╔══██╗██╔══██╗ ║
║   ██║   ██║███████╗   ██║   ███████║██║  ██║ ║
║   ██║   ██║╚════██║   ██║   ██╔══██║██║  ██║ ║
║   ╚██████╔╝███████║   ██║   ██║  ██║╚█████╔╝ ║
║    ╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚════╝  ║
╠══════════════════════════════════════════════╣
║           USTAAD-AI CORE v2.5.0              ║
╚══════════════════════════════════════════════╝

[ CORE ARCHITECTURE ]
┌───────────────────┬──────────────────────────┐
│  AI Model         │ Groq LLaMA 3 8B          │
│  Language         │ Python 3.11              │
│  Framework        │ UstaadAI Engine          │
│  Security         │ Enterprise-Grade         │
└───────────────────┴──────────────────────────┘

[ KEY CAPABILITIES ]
├─ Supports 50+ Global Languages
├─ Advanced Context Understanding
├─ Instant Response Generation
├─ Natural Conversation Flow

[ SYSTEM DETAILS ]
• Developer: {Config.DEVELOPER}
• Specialization: AI Chat Systems
• Platform: Telegram Messenger
• Last Updated: June 2024

[ GET STARTED ]
1. Begin with: /start
2. Type your query
3. For help: /help

[ SYSTEM STATUS ] >>> Operational""",
            
            'hi': f"""╔══════════════════════════════════════════════╗
║   ██╗   ██╗███████╗████████╗ █████╗ █████╗   ║
║   ██║   ██║██╔════╝╚══██╔══╝██╔══██╗██╔══██╗ ║
║   ██║   ██║███████╗   ██║   ███████║██║  ██║ ║
║   ██║   ██║╚════██║   ██║   ██╔══██║██║  ██║ ║
║   ╚██████╔╝███████║   ██║   ██║  ██║╚█████╔╝ ║
║    ╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚════╝  ║
╠══════════════════════════════════════════════╣
║           USTAAD-AI CORE v2.5.0              ║
╚══════════════════════════════════════════════╝

[ मुख्य आर्किटेक्चर ]
┌───────────────────┬──────────────────────────┐
│  AI मॉडल          │ Groq LLaMA 3 8B          │
│  भाषा             │ Python 3.11              │
│  फ्रेमवर्क         │ UstaadAI Engine          │
│  सुरक्षा           │ Enterprise-Grade         │
└───────────────────┴──────────────────────────┘

[ मुख्य क्षमताएं ]
├─ 50+ वैश्विक भाषाओं का समर्थन
├─ उन्नत संदर्भ समझ
├─ तत्काल प्रतिक्रिया उत्पादन
├─ प्राकृतिक बातचीत प्रवाह

[ सिस्टम विवरण ]
• डेवलपर: {Config.DEVELOPER}
• विशेषज्ञता: AI चैट सिस्टम
• प्लेटफॉर्म: टेलीग्राम मैसेंजर
• अंतिम अपडेट: जून 2024

[ शुरुआत करें ]
1. शुरू करें: /start
2. अपना प्रश्न टाइप करें
3. सहायता के लिए: /help

[ सिस्टम स्थिति ] >>> परिचालन""",
            
            'ur': f"""╔══════════════════════════════════════════════╗
║   ██╗   ██╗███████╗████████╗ █████╗ █████╗   ║
║   ██║   ██║██╔════╝╚══██╔══╝██╔══██╗██╔══██╗ ║
║   ██║   ██║███████╗   ██║   ███████║██║  ██║ ║
║   ██║   ██║╚════██║   ██║   ██╔══██║██║  ██║ ║
║   ╚██████╔╝███████║   ██║   ██║  ██║╚█████╔╝ ║
║    ╚═════╝ ╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚════╝  ║
╠══════════════════════════════════════════════╣
║           USTAAD-AI CORE v2.5.0              ║
╚══════════════════════════════════════════════╝

[ بنیادی فن تعمیر ]
┌───────────────────┬──────────────────────────┐
│  AI ماڈل          │ Groq LLaMA 3 8B          │
│  زبان             │ Python 3.11              │
│  فریم ورک         │ UstaadAI Engine          │
│  سیکیورٹی         │ Enterprise-Grade         │
└───────────────────┴──────────────────────────┘

[ اہم صلاحیات ]
├─ 50+ عالمی زبانوں کی حمایت
├─ اعلیٰ درجے کی سیاق فہمی
├─ فوری جواب کی تخلیق
├─ قدرتی گفتگو کا بہاؤ

[ سسٹم کی تفصیلات ]
• ڈیولپر: {Config.DEVELOPER}
• مہارت: AI چیٹ سسٹمز
• پلیٹ فارم: ٹیلیگرام میسنجر
• آخری اپڈیٹ: جون 2024

[ شروعات کریں ]
1. شروع کریں: /start
2. اپنا سوال ٹائپ کریں
3. مدد کے لیے: /help

[ سسٹم کی حالت ] >>> فعال"""
        }
        
        return info_messages.get(lang_code, info_messages['hi'])