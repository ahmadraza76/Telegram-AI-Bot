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
        
        # Popular Indian languages for quick selection
        self.popular_languages = {
            'hi': '🇮🇳 हिंदी (~52 करोड़)',
            'bn': '🇮🇳 বাংলা (~10 करोड़)',
            'mr': '🇮🇳 मराठी (~9.5 करोड़)',
            'te': '🇮🇳 తెలుగు (~8.1 करोड़)',
            'ta': '🇮🇳 தமிழ் (~7.8 करोड़)',
            'gu': '🇮🇳 ગુજરાતી (~5.5 करोड़)',
            'ur': '🇵🇰 اردو (~5.0 करोड़)',
            'kn': '🇮🇳 ಕನ್ನಡ (~4.5 करोड़)',
            'or': '🇮🇳 ଓଡ଼ିଆ (~3.5 करोड़)',
            'pa': '🇮🇳 ਪੰਜਾਬੀ (~3.2 करोड़)',
            'en': '🌍 English (Global)'
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
            'en': f"""🌍 **Language Settings**

**Current Language**: {self.language_names.get(lang_code, 'English')}

Choose your preferred language for conversations:

🇮🇳 **Indian Languages (भारतीय भाषाएं):**
• हिंदी - 52+ करोड़ बोलने वाले
• বাংলা - 10+ करोड़ बोलने वाले  
• मराठी - 9.5 करोड़ बोलने वाले
• తెలుగు - 8.1 करोड़ बोलने वाले
• தமிழ் - 7.8 करोड़ बोलने वाले
• ગુજરાતી - 5.5 करोड़ बोलने वाले
• اردو - 5.0 करोड़ बोलने वाले
• ಕನ್ನಡ - 4.5 करोड़ बोलने वाले
• ଓଡ଼ିଆ - 3.5 करोड़ बोलने वाले
• ਪੰਜਾਬੀ - 3.2 करोड़ बोलने वाले

**Note**: You can change language anytime using the settings menu.

{Config.POWERED_BY} | {Config.VERSION}""",
            
            'hi': f"""🌍 **भाषा सेटिंग्स**

**वर्तमान भाषा**: {self.language_names.get(lang_code, 'हिंदी')}

बातचीत के लिए अपनी पसंदीदा भाषा चुनें:

🇮🇳 **भारतीय भाषाएं:**
• हिंदी - 52+ करोड़ बोलने वाले
• বাংলা - 10+ करोड़ बोलने वाले  
• मराठी - 9.5 करोड़ बोलने वाले
• తెలుగు - 8.1 करोड़ बोलने वाले
• தமிழ் - 7.8 करोड़ बोलने वाले
• ગુજરાતી - 5.5 करोड़ बोलने वाले
• اردو - 5.0 करोड़ बोलने वाले
• ಕನ್ನಡ - 4.5 करोड़ बोलने वाले
• ଓଡ଼ିଆ - 3.5 करोड़ बोलने वाले
• ਪੰਜਾਬੀ - 3.2 करोड़ बोलने वाले

**नोट**: आप सेटिंग्स मेनू का उपयोग करके कभी भी भाषा बदल सकते हैं।

{Config.POWERED_BY} | {Config.VERSION}""",
            
            'ur': f"""🌍 **زبان کی سیٹنگز**

**موجودہ زبان**: {self.language_names.get(lang_code, 'اردو')}

بات چیت کے لیے اپنی پسندیدہ زبان منتخب کریں:

🇮🇳 **ہندوستانی زبانیں:**
• हिंदी - 52+ کروڑ بولنے والے
• বাংলা - 10+ کروڑ بولنے والے  
• मराठी - 9.5 کروڑ بولنے والے
• తెలుగు - 8.1 کروڑ بولنے والے
• தமிழ் - 7.8 کروڑ بولنے والے
• ગુજરાતી - 5.5 کروڑ بولنے والے
• اردو - 5.0 کروڑ بولنے والے
• ಕನ್ನಡ - 4.5 کروڑ بولنے والے
• ଓଡ଼ିଆ - 3.5 کروڑ بولنے والے
• ਪੰਜਾਬੀ - 3.2 کروڑ بولنے والے

**نوٹ**: آپ سیٹنگز مینو استعمال کرکے کبھی بھی زبان تبدیل کر سکتے ہیں۔

{Config.POWERED_BY} | {Config.VERSION}""",
            
            'bn': f"""🌍 **ভাষার সেটিংস**

**বর্তমান ভাষা**: {self.language_names.get(lang_code, 'বাংলা')}

কথোপকথনের জন্য আপনার পছন্দের ভাষা বেছে নিন:

🇮🇳 **ভারতীয় ভাষাসমূহ:**
• हिंदी - 52+ কোটি বক্তা
• বাংলা - 10+ কোটি বক্তা  
• मराठी - 9.5 কোটি বক্তা
• తెలుగు - 8.1 কোটি বক্তা
• தமிழ் - 7.8 কোটি বক্তা
• ગુજરાતી - 5.5 কোটি বক্তা
• اردو - 5.0 কোটি বক্তা
• ಕನ್ನಡ - 4.5 কোটি বক্তা
• ଓଡ଼ିଆ - 3.5 কোটি বক্তা
• ਪੰਜਾਬੀ - 3.2 কোটি বক্তা

**নোট**: আপনি সেটিংস মেনু ব্যবহার করে যেকোনো সময় ভাষা পরিবর্তন করতে পারেন।

{Config.POWERED_BY} | {Config.VERSION}"""
        }
        
        return messages.get(lang_code, messages['hi'])
    
    def get_welcome_message(self, lang_code: str) -> Dict[str, str]:
        """Get welcome message in detected language"""
        messages = {
            'en': {
                'welcome': f"🎯 Welcome to {Config.BOT_NAME} {Config.VERSION}\n\n🧠 I'm your advanced AI assistant, powered by cutting-edge technology. I understand and respond in your language with human-like intelligence!\n\n{Config.POWERED_BY} | Developer: {Config.DEVELOPER}",
                'description': "🔥 **What makes me special:**\n• 🇮🇳 Indian Language Support (11 languages)\n• 🧠 Context-aware conversations\n• ⚡ Lightning-fast responses\n• 🎯 Human-like understanding\n• 💡 Creative problem solving\n• 📚 Vast knowledge base",
                'start_chat': "💬 **Ready to chat?** Just send me any message and experience the future of AI!"
            },
            'hi': {
                'welcome': f"🎯 {Config.BOT_NAME} {Config.VERSION} में आपका स्वागत है\n\n🧠 मैं आपका एडवांस AI असिस्टेंट हूं, अत्याधुनिक तकनीक से संचालित। मैं आपकी भाषा समझता हूं और इंसान की तरह जवाब देता हूं!\n\n{Config.POWERED_BY} | डेवलपर: {Config.DEVELOPER}",
                'description': "🔥 **मुझे खास क्या बनाता है:**\n• 🇮🇳 भारतीय भाषा समर्थन (11 भाषाएं)\n• 🧠 संदर्भ-जागरूक बातचीत\n• ⚡ बिजली की तरह तेज़ जवाब\n• 🎯 इंसान जैसी समझ\n• 💡 रचनात्मक समस्या समाधान\n• 📚 विशाल ज्ञान भंडार",
                'start_chat': "💬 **बात करने के लिए तैयार?** बस मुझे कोई भी संदेश भेजें और AI के भविष्य का अनुभव करें!"
            },
            'ur': {
                'welcome': f"🎯 {Config.BOT_NAME} {Config.VERSION} میں خوش آمدید\n\n🧠 میں آپ کا ایڈوانس AI اسسٹنٹ ہوں، جدید ترین ٹیکنالوجی سے چلایا جاتا ہوں۔ میں آپ کی زبان سمجھتا ہوں اور انسان کی طرح جواب دیتا ہوں!\n\n{Config.POWERED_BY} | ڈیولپر: {Config.DEVELOPER}",
                'description': "🔥 **مجھے خاص کیا بناتا ہے:**\n• 🇮🇳 ہندوستانی زبان کی سپورٹ (11 زبانیں)\n• 🧠 سیاق و سباق کے ساتھ گفتگو\n• ⚡ بجلی کی طرح تیز جوابات\n• 🎯 انسان جیسی سمجھ\n• 💡 تخلیقی مسئلہ حل کرنا\n• 📚 وسیع علمی ذخیرہ",
                'start_chat': "💬 **بات کرنے کے لیے تیار؟** بس مجھے کوئی بھی پیغام بھیجیں اور AI کے مستقبل کا تجربہ کریں!"
            },
            'bn': {
                'welcome': f"🎯 {Config.BOT_NAME} {Config.VERSION} এ স্বাগতম\n\n🧠 আমি আপনার উন্নত AI সহায়ক, অত্যাধুনিক প্রযুক্তি দ্বারা চালিত। আমি আপনার ভাষা বুঝি এবং মানুষের মতো উত্তর দিই!\n\n{Config.POWERED_BY} | ডেভেলপার: {Config.DEVELOPER}",
                'description': "🔥 **আমাকে বিশেষ করে তোলে:**\n• 🇮🇳 ভারতীয় ভাষা সমর্থন (11টি ভাষা)\n• 🧠 প্রসঙ্গ-সচেতন কথোপকথন\n• ⚡ বিদ্যুৎ-দ্রুত প্রতিক্রিয়া\n• 🎯 মানুষের মতো বোঝাপড়া\n• 💡 সৃজনশীল সমস্যা সমাধান\n• 📚 বিশাল জ্ঞানের ভাণ্ডার",
                'start_chat': "💬 **চ্যাট করতে প্রস্তুত?** শুধু আমাকে যেকোনো বার্তা পাঠান এবং AI এর ভবিষ্যতের অভিজ্ঞতা নিন!"
            },
            'mr': {
                'welcome': f"🎯 {Config.BOT_NAME} {Config.VERSION} मध्ये आपले स्वागत आहे\n\n🧠 मी तुमचा प्रगत AI सहाय्यक आहे, अत्याधुनिक तंत्रज्ञानाने चालवलेला। मी तुमची भाषा समजतो आणि माणसासारखे उत्तर देतो!\n\n{Config.POWERED_BY} | डेव्हलपर: {Config.DEVELOPER}",
                'description': "🔥 **मला विशेष काय बनवते:**\n• 🇮🇳 भारतीय भाषा समर्थन (11 भाषा)\n• 🧠 संदर्भ-जागरूक संभाषण\n• ⚡ विजेसारखे वेगवान उत्तरे\n• 🎯 माणसासारखी समज\n• 💡 सर्जनशील समस्या निराकरण\n• 📚 विशाल ज्ञान भांडार",
                'start_chat': "💬 **गप्पा मारायला तयार?** फक्त मला कोणताही संदेश पाठवा आणि AI च्या भविष्याचा अनुभव घ्या!"
            },
            'te': {
                'welcome': f"🎯 {Config.BOT_NAME} {Config.VERSION} కు స్వాగతం\n\n🧠 నేను మీ అధునాతన AI సహాయకుడిని, అత్యాధునిక సాంకేతికతతో శక్తివంతం. నేను మీ భాషను అర్థం చేసుకుని మనిషిలా జవాబిస్తాను!\n\n{Config.POWERED_BY} | డెవలపర్: {Config.DEVELOPER}",
                'description': "🔥 **నన్ను ప్రత్యేకం చేసేవి:**\n• 🇮🇳 భారతీయ భాషా మద్దతు (11 భాషలు)\n• 🧠 సందర్భ-అవగాహన సంభాషణలు\n• ⚡ మెరుపు-వేగ ప్రతిస్పందనలు\n• 🎯 మానవ-వంటి అవగాహన\n• 💡 సృజనాత్మక సమస్య పరిష్కారం\n• 📚 విస్తృత జ్ఞాన భాండాగారం",
                'start_chat': "💬 **చాట్ చేయడానికి సిద్ధంగా ఉన్నారా?** నాకు ఏదైనా సందేశం పంపండి మరియు AI భవిష్యత్తును అనుభవించండి!"
            },
            'ta': {
                'welcome': f"🎯 {Config.BOT_NAME} {Config.VERSION} க்கு வரவேற்கிறோம்\n\n🧠 நான் உங்கள் மேம்பட்ட AI உதவியாளர், அதிநவீன தொழில்நுட்பத்தால் இயக்கப்படுகிறேன். நான் உங்கள் மொழியைப் புரிந்துகொண்டு மனிதனைப் போல பதிலளிக்கிறேன்!\n\n{Config.POWERED_BY} | டெவலப்பர்: {Config.DEVELOPER}",
                'description': "🔥 **என்னை சிறப்பாக்குவது:**\n• 🇮🇳 இந்திய மொழி ஆதரவு (11 மொழிகள்)\n• 🧠 சூழல்-விழிப்புணர்வு உரையாடல்கள்\n• ⚡ மின்னல்-வேக பதில்கள்\n• 🎯 மனித-போன்ற புரிதல்\n• 💡 ஆக்கப்பூர்வ சிக்கல் தீர்வு\n• 📚 பரந்த அறிவுக் களஞ்சியம்",
                'start_chat': "💬 **அரட்டையடிக்க தயாரா?** எனக்கு ஏதேனும் செய்தி அனுப்பி AI இன் எதிர்காலத்தை அனுபவியுங்கள்!"
            },
            'gu': {
                'welcome': f"🎯 {Config.BOT_NAME} {Config.VERSION} માં તમારું સ્વાગત છે\n\n🧠 હું તમારો અદ્યતન AI સહાયક છું, અત્યાધુનિક ટેકનોલોજીથી સંચાલિત. હું તમારી ભાષા સમજું છું અને માનવીની જેમ જવાબ આપું છું!\n\n{Config.POWERED_BY} | ડેવલપર: {Config.DEVELOPER}",
                'description': "🔥 **મને વિશેષ બનાવે છે:**\n• 🇮🇳 ભારતીય ભાષા સપોર્ટ (11 ભાષાઓ)\n• 🧠 સંદર્ભ-જાગૃત વાતચીત\n• ⚡ વીજળી-ઝડપી જવાબો\n• 🎯 માનવ-જેવી સમજ\n• 💡 સર્જનાત્મક સમસ્યા નિરાકરણ\n• 📚 વિશાળ જ્ઞાન ભંડાર",
                'start_chat': "💬 **ચેટ કરવા તૈયાર છો?** મને કોઈપણ સંદેશ મોકલો અને AI ના ભવિષ્યનો અનુભવ કરો!"
            },
            'kn': {
                'welcome': f"🎯 {Config.BOT_NAME} {Config.VERSION} ಗೆ ಸ್ವಾಗತ\n\n🧠 ನಾನು ನಿಮ್ಮ ಸುಧಾರಿತ AI ಸಹಾಯಕ, ಅತ್ಯಾಧುನಿಕ ತಂತ್ರಜ್ಞಾನದಿಂದ ಚಾಲಿತ. ನಾನು ನಿಮ್ಮ ಭಾಷೆಯನ್ನು ಅರ್ಥಮಾಡಿಕೊಂಡು ಮನುಷ್ಯನಂತೆ ಉತ್ತರಿಸುತ್ತೇನೆ!\n\n{Config.POWERED_BY} | ಡೆವಲಪರ್: {Config.DEVELOPER}",
                'description': "🔥 **ನನ್ನನ್ನು ವಿಶೇಷಗೊಳಿಸುವುದು:**\n• 🇮🇳 ಭಾರತೀಯ ಭಾಷಾ ಬೆಂಬಲ (11 ಭಾಷೆಗಳು)\n• 🧠 ಸಂದರ್ಭ-ಅರಿವಿನ ಸಂಭಾಷಣೆಗಳು\n• ⚡ ಮಿಂಚು-ವೇಗದ ಪ್ರತಿಕ್ರಿಯೆಗಳು\n• 🎯 ಮಾನವ-ತರಹದ ತಿಳುವಳಿಕೆ\n• 💡 ಸೃಜನಾತ್ಮಕ ಸಮಸ್ಯೆ ಪರಿಹಾರ\n• 📚 ವಿಶಾಲ ಜ್ಞಾನ ಭಂಡಾರ",
                'start_chat': "💬 **ಚಾಟ್ ಮಾಡಲು ಸಿದ್ಧರಿದ್ದೀರಾ?** ನನಗೆ ಯಾವುದೇ ಸಂದೇಶವನ್ನು ಕಳುಹಿಸಿ ಮತ್ತು AI ಯ ಭವಿಷ್ಯವನ್ನು ಅನುಭವಿಸಿ!"
            },
            'or': {
                'welcome': f"🎯 {Config.BOT_NAME} {Config.VERSION} କୁ ସ୍ୱାଗତ\n\n🧠 ମୁଁ ଆପଣଙ୍କର ଉନ୍ନତ AI ସହାୟକ, ଅତ୍ୟାଧୁନିକ ପ୍ରଯୁକ୍ତିବିଦ୍ୟା ଦ୍ୱାରା ଚାଳିତ। ମୁଁ ଆପଣଙ୍କ ଭାଷା ବୁଝେ ଏବଂ ମଣିଷ ପରି ଉତ୍ତର ଦିଏ!\n\n{Config.POWERED_BY} | ଡେଭେଲପର: {Config.DEVELOPER}",
                'description': "🔥 **ମୋତେ ବିଶେଷ କରେ:**\n• 🇮🇳 ଭାରତୀୟ ଭାଷା ସମର୍ଥନ (11 ଭାଷା)\n• 🧠 ପ୍ରସଙ୍ଗ-ସଚେତନ କଥାବାର୍ତ୍ତା\n• ⚡ ବିଜୁଳି-ଦ୍ରୁତ ପ୍ରତିକ୍ରିୟା\n• 🎯 ମାନବ-ପରି ବୁଝାମଣା\n• 💡 ସୃଜନଶୀଳ ସମସ୍ୟା ସମାଧାନ\n• 📚 ବିଶାଳ ଜ୍ଞାନ ଭଣ୍ଡାର",
                'start_chat': "💬 **ଚାଟ୍ କରିବାକୁ ପ୍ରସ୍ତୁତ?** ମୋତେ କୌଣସି ବାର୍ତ୍ତା ପଠାନ୍ତୁ ଏବଂ AI ର ଭବିଷ୍ୟତ ଅନୁଭବ କରନ୍ତୁ!"
            },
            'pa': {
                'welcome': f"🎯 {Config.BOT_NAME} {Config.VERSION} ਵਿੱਚ ਤੁਹਾਡਾ ਸੁਆਗਤ ਹੈ\n\n🧠 ਮੈਂ ਤੁਹਾਡਾ ਉੱਨਤ AI ਸਹਾਇਕ ਹਾਂ, ਅਤਿ-ਆਧੁਨਿਕ ਤਕਨਾਲੋਜੀ ਨਾਲ ਚਲਾਇਆ ਗਿਆ। ਮੈਂ ਤੁਹਾਡੀ ਭਾਸ਼ਾ ਸਮਝਦਾ ਹਾਂ ਅਤੇ ਇਨਸਾਨ ਵਾਂਗ ਜਵਾਬ ਦਿੰਦਾ ਹਾਂ!\n\n{Config.POWERED_BY} | ਡਿਵੈਲਪਰ: {Config.DEVELOPER}",
                'description': "🔥 **ਮੈਨੂੰ ਖਾਸ ਕੀ ਬਣਾਉਂਦਾ ਹੈ:**\n• 🇮🇳 ਭਾਰਤੀ ਭਾਸ਼ਾ ਸਹਾਇਤਾ (11 ਭਾਸ਼ਾਵਾਂ)\n• 🧠 ਸੰਦਰਭ-ਜਾਗਰੂਕ ਗੱਲਬਾਤ\n• ⚡ ਬਿਜਲੀ-ਤੇਜ਼ ਜਵਾਬ\n• 🎯 ਇਨਸਾਨ-ਵਰਗੀ ਸਮਝ\n• 💡 ਰਚਨਾਤਮਕ ਸਮੱਸਿਆ ਹੱਲ\n• 📚 ਵਿਸ਼ਾਲ ਗਿਆਨ ਭੰਡਾਰ",
                'start_chat': "💬 **ਚੈਟ ਕਰਨ ਲਈ ਤਿਆਰ?** ਮੈਨੂੰ ਕੋਈ ਵੀ ਸੰਦੇਸ਼ ਭੇਜੋ ਅਤੇ AI ਦੇ ਭਵਿੱਖ ਦਾ ਅਨੁਭਵ ਕਰੋ!"
            }
        }
        
        return messages.get(lang_code, messages['hi'])
    
    def get_help_message(self, lang_code: str) -> str:
        """Get help message in detected language"""
        help_messages = {
            'en': f"""🆘 **{Config.BOT_NAME} Help Guide**

🎯 **How to use me:**
• Just send any message - I'll respond intelligently
• I understand context and remember our conversation
• I can help with any topic in Indian languages

💡 **Available Commands:**
• `/start` - Welcome message and main menu
• `/help` - Show this help guide
• `/info` - Bot information and developer details

🌟 **Pro Tips:**
• Ask specific questions for better answers
• I work best with clear, detailed queries
• Switch languages anytime - I'll adapt automatically
• Use language settings to set your preferred language

🇮🇳 **Supported Indian Languages:**
हिंदी, বাংলা, मराठी, తెలుగు, தமிழ், ગુજરાતી, اردو, ಕನ್ನಡ, ଓଡ଼ିଆ, ਪੰਜਾਬੀ

{Config.POWERED_BY} | {Config.VERSION}""",
            
            'hi': f"""🆘 **{Config.BOT_NAME} सहायता गाइड**

🎯 **मुझे कैसे उपयोग करें:**
• बस कोई भी संदेश भेजें - मैं बुद्धिमानी से जवाब दूंगा
• मैं संदर्भ समझता हूं और हमारी बातचीत याद रखता हूं
• मैं भारतीय भाषाओं में किसी भी विषय पर मदद कर सकता हूं

💡 **उपलब्ध कमांड:**
• `/start` - स्वागत संदेश और मुख्य मेनू
• `/help` - यह सहायता गाइड दिखाएं
• `/info` - बॉट जानकारी और डेवलपर विवरण

🌟 **प्रो टिप्स:**
• बेहतर उत्तर के लिए विशिष्ट प्रश्न पूछें
• मैं स्पष्ट, विस्तृत प्रश्नों के साथ सबसे अच्छा काम करता हूं
• कभी भी भाषा बदलें - मैं अपने आप अनुकूलित हो जाऊंगा
• अपनी पसंदीदा भाषा सेट करने के लिए भाषा सेटिंग्स का उपयोग करें

🇮🇳 **समर्थित भारतीय भाषाएं:**
हिंदी, বাংলা, मराठी, తెలుగు, தமிழ், ગુજરાતી, اردو, ಕನ್ನಡ, ଓଡ଼ିଆ, ਪੰਜਾਬੀ

{Config.POWERED_BY} | {Config.VERSION}""",
            
            'ur': f"""🆘 **{Config.BOT_NAME} ہیلپ گائیڈ**

🎯 **مجھے کیسے استعمال کریں:**
• بس کوئی بھی پیغام بھیجیں - میں ذہانت سے جواب دوں گا
• میں سیاق سمجھتا ہوں اور ہماری گفتگو یاد رکھتا ہوں
• میں ہندوستانی زبانوں میں کسی بھی موضوع پر مدد کر سکتا ہوں

💡 **دستیاب کمانڈز:**
• `/start` - خوش آمدید پیغام اور مین مینو
• `/help` - یہ ہیلپ گائیڈ دکھائیں
• `/info` - بوٹ کی معلومات اور ڈیولپر کی تفصیلات

🌟 **پرو ٹپس:**
• بہتر جوابات کے لیے مخصوص سوالات پوچھیں
• میں واضح، تفصیلی سوالات کے ساتھ بہترین کام کرتا ہوں
• کبھی بھی زبان تبدیل کریں - میں خودکار طور پر ڈھل جاؤں گا
• اپنی پسندیدہ زبان سیٹ کرنے کے لیے زبان کی سیٹنگز استعمال کریں

🇮🇳 **سپورٹ شدہ ہندوستانی زبانیں:**
हिंदी, বাংলা, मराठी, తెలుగు, தமிழ், ગુજરાતી, اردو, ಕನ್ನಡ, ଓଡ଼ିଆ, ਪੰਜਾਬੀ

{Config.POWERED_BY} | {Config.VERSION}""",
            
            'bn': f"""🆘 **{Config.BOT_NAME} সাহায্য গাইড**

🎯 **আমাকে কীভাবে ব্যবহার করবেন:**
• শুধু যেকোনো বার্তা পাঠান - আমি বুদ্ধিমত্তার সাথে উত্তর দেব
• আমি প্রসঙ্গ বুঝি এবং আমাদের কথোপকথন মনে রাখি
• আমি ভারতীয় ভাষায় যেকোনো বিষয়ে সাহায্য করতে পারি

💡 **উপলব্ধ কমান্ড:**
• `/start` - স্বাগত বার্তা এবং মূল মেনু
• `/help` - এই সাহায্য গাইড দেখান
• `/info` - বট তথ্য এবং ডেভেলপার বিবরণ

🌟 **প্রো টিপস:**
• ভাল উত্তরের জন্য নির্দিষ্ট প্রশ্ন জিজ্ঞাসা করুন
• আমি স্পষ্ট, বিস্তারিত প্রশ্নের সাথে সবচেয়ে ভাল কাজ করি
• যেকোনো সময় ভাষা পরিবর্তন করুন - আমি স্বয়ংক্রিয়ভাবে মানিয়ে নেব
• আপনার পছন্দের ভাষা সেট করতে ভাষা সেটিংস ব্যবহার করুন

🇮🇳 **সমর্থিত ভারতীয় ভাষা:**
हिंदी, বাংলা, मराठी, తెలుగు, தமிழ், ગુજરાતી, اردو, ಕನ್ನಡ, ଓଡ଼ିଆ, ਪੰਜਾਬੀ

{Config.POWERED_BY} | {Config.VERSION}"""
        }
        
        return help_messages.get(lang_code, help_messages['hi'])
    
    def get_info_message(self, lang_code: str) -> str:
        """Get bot info message in detected language"""
        info_messages = {
            'en': f"""ℹ️ **{Config.BOT_NAME} Information**

🤖 **Bot Details:**
• Name: {Config.BOT_NAME}
• Version: {Config.VERSION}
• Model: Groq LLaMA 3 8B (Lightning Fast)
• Developer: {Config.DEVELOPER}

🔥 **Advanced Features:**
• 🇮🇳 Indian Language Support (11 languages)
• 🧠 Context-Aware AI
• ⚡ Real-time Responses
• 🎯 Human-like Intelligence
• 💡 Creative Problem Solving
• 📚 Vast Knowledge Base
• 🌐 Language Preferences

🛠️ **Technical Specs:**
• Built with Python & Groq API
• Advanced Language Detection
• Smart Response Formatting
• Optimized Performance
• Secure & Private

👨‍💻 **Developer Info:**
• Created by: {Config.DEVELOPER}
• Specialized in AI Development
• Telegram Bot Expert
• {Config.POWERED_BY}

🇮🇳 **Supported Languages:**
हिंदी (~52 करोड़), বাংলা (~10 करोड़), मराठी (~9.5 करोड़), తెలుగు (~8.1 करोड़), தமிழ் (~7.8 करोड़), ગુજરાતી (~5.5 करोड़), اردو (~5.0 करोड़), ಕನ್ನಡ (~4.5 करोड़), ଓଡ଼ିଆ (~3.5 करोड़), ਪੰਜਾਬੀ (~3.2 करोड़)

💬 Ready to experience the future of AI? Just send me any message!""",
            
            'hi': f"""ℹ️ **{Config.BOT_NAME} जानकारी**

🤖 **बॉट विवरण:**
• नाम: {Config.BOT_NAME}
• संस्करण: {Config.VERSION}
• मॉडल: Groq LLaMA 3 8B (बिजली की तरह तेज़)
• डेवलपर: {Config.DEVELOPER}

🔥 **एडवांस फीचर्स:**
• 🇮🇳 भारतीय भाषा समर्थन (11 भाषाएं)
• 🧠 संदर्भ-जागरूक AI
• ⚡ रियल-टाइम रिस्पॉन्स
• 🎯 इंसान जैसी बुद्धिमत्ता
• 💡 रचनात्मक समस्या समाधान
• 📚 विशाल ज्ञान भंडार
• 🌐 भाषा प्राथमिकताएं

🛠️ **तकनीकी विशेषताएं:**
• Python और Groq API के साथ निर्मित
• एडवांस भाषा पहचान
• स्मार्ट रिस्पॉन्स फॉर्मेटिंग
• अनुकूलित प्रदर्शन
• सुरक्षित और निजी

👨‍💻 **डेवलपर जानकारी:**
• निर्माता: {Config.DEVELOPER}
• AI डेवलपमेंट में विशेषज्ञ
• टेलीग्राम बॉट एक्सपर्ट
• {Config.POWERED_BY}

🇮🇳 **समर्थित भाषाएं:**
हिंदी (~52 करोड़), বাংলা (~10 करोड़), मराठी (~9.5 करोड़), తెలుగు (~8.1 करोड़), தமிழ் (~7.8 करोड़), ગુજરાતી (~5.5 करोड़), اردو (~5.0 करोड़), ಕನ್ನಡ (~4.5 करोड़), ଓଡ଼ିଆ (~3.5 करोड़), ਪੰਜਾਬੀ (~3.2 करोड़)

💬 AI के भविष्य का अनुभव करने के लिए तैयार? बस मुझे कोई भी संदेश भेजें!""",
            
            'ur': f"""ℹ️ **{Config.BOT_NAME} معلومات**

🤖 **بوٹ کی تفصیلات:**
• نام: {Config.BOT_NAME}
• ورژن: {Config.VERSION}
• ماڈل: Groq LLaMA 3 8B (بجلی کی طرح تیز)
• ڈیولپر: {Config.DEVELOPER}

🔥 **ایڈوانس فیچرز:**
• 🇮🇳 ہندوستانی زبان کی سپورٹ (11 زبانیں)
• 🧠 سیاق آگاہ AI
• ⚡ ریئل ٹائم جوابات
• 🎯 انسان جیسی ذہانت
• 💡 تخلیقی مسئلہ حل کرنا
• 📚 وسیع علمی ذخیرہ
• 🌐 زبان کی ترجیحات

🛠️ **تکنیکی خصوصیات:**
• Python اور Groq API کے ساتھ بنایا گیا
• ایڈوانس زبان کی شناخت
• سمارٹ رسپانس فارمیٹنگ
• بہتر کارکردگی
• محفوظ اور نجی

👨‍💻 **ڈیولپر کی معلومات:**
• بنانے والا: {Config.DEVELOPER}
• AI ڈیولپمنٹ میں ماہر
• ٹیلیگرام بوٹ ایکسپرٹ
• {Config.POWERED_BY}

🇮🇳 **سپورٹ شدہ زبانیں:**
हिंदी (~52 کروڑ), বাংলা (~10 کروڑ), मराठी (~9.5 کروڑ), తెలుగు (~8.1 کروڑ), தமிழ் (~7.8 کروڑ), ગુજરાતી (~5.5 کروڑ), اردو (~5.0 کروڑ), ಕನ್ನಡ (~4.5 کروڑ), ଓଡ଼ିଆ (~3.5 کروڑ), ਪੰਜਾਬੀ (~3.2 کروڑ)

💬 AI کے مستقبل کا تجربہ کرنے کے لیے تیار؟ بس مجھے کوئی بھی پیغام بھیجیں!"""
        }
        
        return info_messages.get(lang_code, info_messages['hi'])