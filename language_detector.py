# language_detector.py
# Developer: Mr Ahmad 
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
            'en': f"""🌍 *Language Settings* 🌍

🔹 *Current Language*: {self.language_names.get(lang_code, 'English')}

Choose your preferred language for conversations:

*Indian Languages:*
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

📌 *Note*: You can change language anytime using /settings command.

{Config.POWERED_BY} | {Config.VERSION}""",
            
            'hi': f"""🌍 *भाषा सेटिंग्स* 🌍

🔹 *वर्तमान भाषा*: {self.language_names.get(lang_code, 'हिंदी')}

बातचीत के लिए अपनी पसंदीदा भाषा चुनें:

*भारतीय भाषाएं:*
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

📌 *नोट*: आप /settings कमांड से कभी भी भाषा बदल सकते हैं।

{Config.POWERED_BY} | {Config.VERSION}""",
            
            'ur': f"""🌍 *زبان کی ترتیبات* 🌍

🔹 *موجودہ زبان*: {self.language_names.get(lang_code, 'اردو')}

بات چیت کے لیے اپنی پسندیدہ زبان منتخب کریں:

*ہندوستانی زبانیں:*
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

📌 *نوٹ*: آپ /settings کمانڈ کا استعمال کرتے ہوئے کسی بھی وقت زبان تبدیل کر سکتے ہیں۔

{Config.POWERED_BY} | {Config.VERSION}""",
            
            'bn': f"""🌍 *ভাষা সেটিংস* 🌍

🔹 *বর্তমান ভাষা*: {self.language_names.get(lang_code, 'বাংলা')}

কথোপকথনের জন্য আপনার পছন্দের ভাষা বেছে নিন:

*ভারতীয় ভাষাসমূহ:*
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

📌 *নোট*: আপনি /settings কমান্ড ব্যবহার করে যেকোনো সময় ভাষা পরিবর্তন করতে পারেন।

{Config.POWERED_BY} | {Config.VERSION}""",
            
            'mr': f"""🌍 *भाषा सेटिंग्ज* 🌍

🔹 *सध्याची भाषा*: {self.language_names.get(lang_code, 'मराठी')}

संभाषणासाठी आपली पसंतीची भाषा निवडा:

*भारतीय भाषा:*
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

📌 *टीप*: आपण /settings कमांड वापरून कोणत्याही वेळी भाषा बदलू शकता.

{Config.POWERED_BY} | {Config.VERSION}""",
            
            'te': f"""🌍 *భాషా సెట్టింగ్స్* 🌍

🔹 *ప్రస్తుత భాష*: {self.language_names.get(lang_code, 'తెలుగు')}

సంభాషణల కోసం మీకు ఇష్టమైన భాషను ఎంచుకోండి:

*భారతీయ భాషలు:*
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

📌 *గమనిక*: మీరు /settings కమాండ్ ఉపయోగించి ఎప్పుడైనా భాషను మార్చవచ్చు.

{Config.POWERED_BY} | {Config.VERSION}""",
            
            'ta': f"""🌍 *மொழி அமைப்புகள்* 🌍

🔹 *தற்போதைய மொழி*: {self.language_names.get(lang_code, 'தமிழ்')}

உரையாடலுக்கு உங்களுக்கு விருப்பமான மொழியைத் தேர்ந்தெடுக்கவும்:

*இந்திய மொழிகள்:*
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

📌 *குறிப்பு*: /settings கட்டளையைப் பயன்படுத்தி எந்நேரமும் மொழியை மாற்றலாம்.

{Config.POWERED_BY} | {Config.VERSION}""",
            
            'gu': f"""🌍 *ભાષા સેટિંગ્સ* 🌍

🔹 *વર્તમાન ભાષા*: {self.language_names.get(lang_code, 'ગુજરાતી')}

વાર્તાલાપ માટે તમારી પસંદગીની ભાષા પસંદ કરો:

*ભારતીય ભાષાઓ:*
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

📌 *નોંધ*: તમે /settings આદેશનો ઉપયોગ કરીને કોઈપણ સમયે ભાષા બદલી શકો છો.

{Config.POWERED_BY} | {Config.VERSION}""",
            
            'kn': f"""🌍 *ಭಾಷಾ ಸೆಟ್ಟಿಂಗ್ಗಳು* 🌍

🔹 *ಪ್ರಸ್ತುತ ಭಾಷೆ*: {self.language_names.get(lang_code, 'ಕನ್ನಡ')}

ಸಂಭಾಷಣೆಗಳಿಗಾಗಿ ನಿಮ್ಮ ಆದ್ಯತೆಯ ಭಾಷೆಯನ್ನು ಆರಿಸಿ:

*ಭಾರತೀಯ ಭಾಷೆಗಳು:*
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

📌 *ಗಮನಿಸಿ*: /settings ಆಜ್ಞೆಯನ್ನು ಬಳಸಿ ನೀವು ಯಾವುದೇ ಸಮಯದಲ್ಲಿ ಭಾಷೆಯನ್ನು ಬದಲಾಯಿಸಬಹುದು.

{Config.POWERED_BY} | {Config.VERSION}""",
            
            'or': f"""🌍 *ଭାଷା ସେଟିଂସ୍* 🌍

🔹 *ବର୍ତ୍ତମାନର ଭାଷା*: {self.language_names.get(lang_code, 'ଓଡ଼ିଆ')}

କଥୋପକଥନ ପାଇଁ ଆପଣଙ୍କର ପସନ୍ଦର ଭାଷା ବାଛନ୍ତୁ:

*ଭାରତୀୟ ଭାଷା:*
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

📌 *ଟିପ୍ପଣୀ*: ଆପଣ /settings କମାଣ୍ଡ ବ୍ୟବହାର କରି ଯେକୌଣସି ସମୟରେ ଭାଷା ପରିବର୍ତ୍ତନ କରିପାରିବେ.

{Config.POWERED_BY} | {Config.VERSION}""",
            
            'pa': f"""🌍 *ਭਾਸ਼ਾ ਸੈਟਿੰਗਾਂ* 🌍

🔹 *ਮੌਜੂਦਾ ਭਾਸ਼ਾ*: {self.language_names.get(lang_code, 'ਪੰਜਾਬੀ')}

ਗੱਲਬਾਤ ਲਈ ਆਪਣੀ ਪਸੰਦੀਦਾ ਭਾਸ਼ਾ ਚੁਣੋ:

*ਭਾਰਤੀ ਭਾਸ਼ਾਵਾਂ:*
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

📌 *ਨੋਟ*: ਤੁਸੀਂ /settings ਕਮਾਂਡ ਦੀ ਵਰਤੋਂ ਕਰਕੇ ਕਿਸੇ ਵੀ ਸਮੇਂ ਭਾਸ਼ਾ ਬਦਲ ਸਕਦੇ ਹੋ.

{Config.POWERED_BY} | {Config.VERSION}"""
        }
        
        return messages.get(lang_code, messages['hi'])
    
    def get_welcome_message(self, lang_code: str) -> Dict[str, str]:
        """Get welcome message in detected language"""
        messages = {
            'en': {
                'welcome': f"""✨ *Welcome to {Config.BOT_NAME} {Config.VERSION}* ✨

🤖 I'm your advanced AI assistant, powered by cutting-edge technology. I understand and respond in your language with human-like intelligence!

{Config.POWERED_BY} | Developer: {Config.DEVELOPER}""",
                'description': """🌟 *What makes me special:*
• 🇮🇳 Indian Language Support (11 languages)
• 🧠 Context-aware conversations
• ⚡ Lightning-fast responses
• 💡 Human-like understanding
• 🎨 Creative problem solving
• 📚 Vast knowledge base""",
                'start_chat': """💬 *Ready to chat?* 
Just send me any message and experience the future of AI!"""
            },
            'hi': {
                'welcome': f"""✨ *{Config.BOT_NAME} {Config.VERSION} में आपका स्वागत है* ✨

🤖 मैं आपका एडवांस AI असिस्टेंट हूं, अत्याधुनिक तकनीक से संचालित। मैं आपकी भाषा समझता हूं और इंसान की तरह जवाब देता हूं!

{Config.POWERED_BY} | डेवलपर: {Config.DEVELOPER}""",
                'description': """🌟 *मुझे खास क्या बनाता है:*
• 🇮🇳 भारतीय भाषा समर्थन (11 भाषाएं)
• 🧠 संदर्भ-जागरूक बातचीत
• ⚡ बिजली की तरह तेज़ जवाब
• 💡 इंसान जैसी समझ
• 🎨 रचनात्मक समस्या समाधान
• 📚 विशाल ज्ञान भंडार""",
                'start_chat': """💬 *बात करने के लिए तैयार?* 
बस मुझे कोई भी संदेश भेजें और AI के भविष्य का अनुभव करें!"""
            },
            'ur': {
                'welcome': f"""✨ *{Config.BOT_NAME} {Config.VERSION} میں خوش آمدید* ✨

🤖 میں آپ کا ایڈوانس AI اسسٹنٹ ہوں، جدید ترین ٹیکنالوجی سے چلایا جاتا ہوں۔ میں آپ کی زبان سمجھتا ہوں اور انسان کی طرح جواب دیتا ہوں!

{Config.POWERED_BY} | ڈویلپر: {Config.DEVELOPER}""",
                'description': """🌟 *مجھے خاص کیا بناتا ہے:*
• 🇮🇳 ہندوستانی زبان کی سپورٹ (11 زبانیں)
• 🧠 سیاق و سباق کے ساتھ گفتگو
• ⚡ بجلی کی طرح تیز جوابات
• 💡 انسان جیسی سمجھ
• 🎨 تخلیقی مسئلہ حل کرنا
• 📚 وسیع علمی ذخیرہ""",
                'start_chat': """💬 *بات کرنے کے لیے تیار؟* 
بس مجھے کوئی بھی پیغام بھیجیں اور AI کے مستقبل کا تجربہ کریں!"""
            },
            'bn': {
                'welcome': f"""✨ *{Config.BOT_NAME} {Config.VERSION} এ স্বাগতম* ✨

🤖 আমি আপনার উন্নত AI সহায়ক, অত্যাধুনিক প্রযুক্তি দ্বারা চালিত। আমি আপনার ভাষা বুঝি এবং মানুষের মতো উত্তর দিই!

{Config.POWERED_BY} | ডেভেলপার: {Config.DEVELOPER}""",
                'description': """🌟 *আমাকে বিশেষ করে তোলে:*
• 🇮🇳 ভারতীয় ভাষা সমর্থন (11টি ভাষা)
• 🧠 প্রসঙ্গ-সচেতন কথোপকথন
• ⚡ বিদ্যুৎ-দ্রুত প্রতিক্রিয়া
• 💡 মানুষের মতো বোঝাপড়া
• 🎨 সৃজনশীল সমস্যা সমাধান
• 📚 বিশাল জ্ঞানের ভাণ্ডার""",
                'start_chat': """💬 *চ্যাট করতে প্রস্তুত?* 
শুধু আমাকে যেকোনো বার্তা পাঠান এবং AI এর ভবিষ্যতের অভিজ্ঞতা নিন!"""
            },
            'mr': {
                'welcome': f"""✨ *{Config.BOT_NAME} {Config.VERSION} मध्ये आपले स्वागत आहे* ✨

🤖 मी तुमचा प्रगत AI सहाय्यक आहे, अत्याधुनिक तंत्रज्ञानाने चालवलेला। मी तुमची भाषा समजतो आणि माणसासारखे उत्तर देतो!

{Config.POWERED_BY} | डेव्हलपर: {Config.DEVELOPER}""",
                'description': """🌟 *मला विशेष काय बनवते:*
• 🇮🇳 भारतीय भाषा समर्थन (11 भाषा)
• 🧠 संदर्भ-जागरूक संभाषण
• ⚡ विजेसारखे वेगवान उत्तरे
• 💡 माणसासारखी समज
• 🎨 सर्जनशील समस्या निराकरण
• 📚 विशाल ज्ञान भांडार""",
                'start_chat': """💬 *गप्पा मारायला तयार?* 
फक्त मला कोणताही संदेश पाठवा आणि AI च्या भविष्याचा अनुभव घ्या!"""
            },
            'te': {
                'welcome': f"""✨ *{Config.BOT_NAME} {Config.VERSION} కు స్వాగతం* ✨

🤖 నేను మీ అధునాతన AI సహాయకుడిని, అత్యాధునిక సాంకేతికతతో శక్తివంతం। నేను మీ భాషను అర్థం చేసుకుని మనిషిలా జవాబిస్తాను!

{Config.POWERED_BY} | డెవలపర్: {Config.DEVELOPER}""",
                'description': """🌟 *నన్ను ప్రత్యేకం చేసేవి:*
• 🇮🇳 భారతీయ భాషా మద్దతు (11 భాషలు)
• 🧠 సందర్భ-అవగాహన సంభాషణలు
• ⚡ మెరుపు-వేగ ప్రతిస్పందనలు
• 💡 మానవ-వంటి అవగాహన
• 🎨 సృజనాత్మక సమస్య పరిష్కారం
• 📚 విస్తృత జ్ఞాన భాండాగారం""",
                'start_chat': """💬 *చాట్ చేయడానికి సిద్ధంగా ఉన్నారా?* 
నాకు ఏదైనా సందేశం పంపండి మరియు AI భవిష్యత్తును అనుభవించండి!"""
            },
            'ta': {
                'welcome': f"""✨ *{Config.BOT_NAME} {Config.VERSION} க்கு வரவேற்கிறோம்* ✨

🤖 நான் உங்கள் மேம்பட்ட AI உதவியாளர், அதிநவீன தொழில்நுட்பத்தால் இயக்கப்படுகிறேன். நான் உங்கள் மொழியைப் புரிந்துகொண்டு மனிதனைப் போல பதிலளிக்கிறேன்!

{Config.POWERED_BY} | டெவலப்பர்: {Config.DEVELOPER}""",
                'description': """🌟 *என்னை சிறப்பாக்குவது:*
• 🇮🇳 இந்திய மொழி ஆதரவு (11 மொழிகள்)
• 🧠 சூழல்-விழிப்புணர்வு உரையாடல்கள்
• ⚡ மின்னல்-வேக பதில்கள்
• 💡 மனித-போன்ற புரிதல்
• 🎨 ஆக்கப்பூர்வ சிக்கல் தீர்வு
• 📚 பரந்த அறிவுக் களஞ்சியம்""",
                'start_chat': """💬 *அரட்டையடிக்க தயாரா?* 
எனக்கு ஏதேனும் செய்தி அனுப்பி AI இன் எதிர்காலத்தை அனுபவியுங்கள்!"""
            },
            'gu': {
                'welcome': f"""✨ *{Config.BOT_NAME} {Config.VERSION} માં તમારું સ્વાગત છે* ✨

🤖 હું તમારો અદ્યતન AI સહાયક છું, અત્યાધુનિક ટેકનોલોજીથી સંચાલિત. હું તમારી ભાષા સમજું છું અને માનવીની જેમ જવાબ આપું છું!

{Config.POWERED_BY} | ડેવલપર: {Config.DEVELOPER}""",
                'description': """🌟 *મને વિશેષ બનાવે છે:*
• 🇮🇳 ભારતીય ભાષા સપોર્ટ (11 ભાષાઓ)
• 🧠 સંદર્ભ-જાગૃત વાતચીત
• ⚡ વીજળી-ઝડપી જવાબો
• 💡 માનવ-જેવી સમજ
• 🎨 સર્જનાત્મક સમસ્યા નિરાકરણ
• 📚 વિશાળ જ્ઞાન ભંડાર""",
                'start_chat': """💬 *ચેટ કરવા તૈયાર છો?* 
મને કોઈપણ સંદેશ મોકલો અને AI ના ભવિષ્યનો અનુભવ કરો!"""
            },
            'kn': {
                'welcome': f"""✨ *{Config.BOT_NAME} {Config.VERSION} ಗೆ ಸ್ವಾಗತ* ✨

🤖 ನಾನು ನಿಮ್ಮ ಸುಧಾರಿತ AI ಸಹಾಯಕ, ಅತ್ಯಾಧುನಿಕ ತಂತ್ರಜ್ಞಾನದಿಂದ ಚಾಲಿತ. ನಾನು ನಿಮ್ಮ ಭಾಷೆಯನ್ನು ಅರ್ಥಮಾಡಿಕೊಂಡು ಮನುಷ್ಯನಂತೆ ಉತ್ತರಿಸುತ್ತೇನೆ!

{Config.POWERED_BY} | ಡೆವಲಪರ್: {Config.DEVELOPER}""",
                'description': """🌟 *ನನ್ನನ್ನು ವಿಶೇಷಗೊಳಿಸುವುದು:*
• 🇮🇳 ಭಾರತೀಯ ಭಾಷಾ ಬೆಂಬಲ (11 ಭಾಷೆಗಳು)
• 🧠 ಸಂದರ್ಭ-ಅರಿವಿನ ಸಂಭಾಷಣೆಗಳು
• ⚡ ಮಿಂಚು-ವೇಗದ ಪ್ರತಿಕ್ರಿಯೆಗಳು
• 💡 ಮಾನವ-ತರಹದ ತಿಳುವಳಿಕೆ
• 🎨 ಸೃಜನಾತ್ಮಕ ಸಮಸ್ಯೆ ಪರಿಹಾರ
• 📚 ವಿಶಾಲ ಜ್ಞಾನ ಭಂಡಾರ""",
                'start_chat': """💬 *ಚಾಟ್ ಮಾಡಲು ಸಿದ್ಧರಿದ್ದೀರಾ?* 
ನನಗೆ ಯಾವುದೇ ಸಂದೇಶವನ್ನು ಕಳುಹಿಸಿ ಮತ್ತು AI ಯ ಭವಿಷ್ಯವನ್ನು ಅನುಭವಿಸಿ!"""
            },
            'or': {
                'welcome': f"""✨ *{Config.BOT_NAME} {Config.VERSION} କୁ ସ୍ୱାଗତ* ✨

🤖 ମୁଁ ଆପଣଙ୍କର ଉନ୍ନତ AI ସହାୟକ, ଅତ୍ୟାଧୁନିକ ପ୍ରଯୁକ୍ତିବିଦ୍ୟା ଦ୍ୱାରା ଚାଳିତ। ମୁଁ ଆପଣଙ୍କ ଭାଷା ବୁଝେ ଏବଂ ମଣିଷ ପରି ଉତ୍ତର ଦିଏ!

{Config.POWERED_BY} | ଡେଭେଲପର: {Config.DEVELOPER}""",
                'description': """🌟 *ମୋତେ ବିଶେଷ କରେ:*
• 🇮🇳 ଭାରତୀୟ ଭାଷା ସମର୍ଥନ (11 ଭାଷା)
• 🧠 ପ୍ରସଙ୍ଗ-ସଚେତନ କଥାବାର୍ତ୍ତା
• ⚡ ବିଜୁଳି-ଦ୍ରୁତ ପ୍ରତିକ୍ରିୟା
• 💡 ମାନବ-ପରି ବୁଝାମଣା
• 🎨 ସୃଜନଶୀଳ ସମସ୍ୟା ସମାଧାନ
• 📚 ବିଶାଳ ଜ୍ଞାନ ଭଣ୍ଡାର""",
                'start_chat': """💬 *ଚାଟ୍ କରିବାକୁ ପ୍ରସ୍ତୁତ?* 
ମୋତେ କୌଣସି ବାର୍ତ୍ତା ପଠାନ୍ତୁ ଏବଂ AI ର ଭବିଷ୍ୟତ ଅନୁଭବ କରନ୍ତୁ!"""
            },
            'pa': {
                'welcome': f"""✨ *{Config.BOT_NAME} {Config.VERSION} ਵਿੱਚ ਤੁਹਾਡਾ ਸੁਆਗਤ ਹੈ* ✨

🤖 ਮੈਂ ਤੁਹਾਡਾ ਉੱਨਤ AI ਸਹਾਇਕ ਹਾਂ, ਅਤਿ-ਆਧੁਨਿਕ ਤਕਨਾਲੋਜੀ ਨਾਲ ਚਲਾਇਆ ਗਿਆ। ਮੈਂ ਤੁਹਾਡੀ ਭਾਸ਼ਾ ਸਮਝਦਾ ਹਾਂ ਅਤੇ ਇਨਸਾਨ ਵਾਂਗ ਜਵਾਬ ਦਿੰਦਾ ਹਾਂ!

{Config.POWERED_BY} | ਡਿਵੈਲਪਰ: {Config.DEVELOPER}""",
                'description': """🌟 *ਮੈਨੂੰ ਖਾਸ ਕੀ ਬਣਾਉਂਦਾ ਹੈ:*
• 🇮🇳 ਭਾਰਤੀ ਭਾਸ਼ਾ ਸਹਾਇਤਾ (11 ਭਾਸ਼ਾਵਾਂ)
• 🧠 ਸੰਦਰਭ-ਜਾਗਰੂਕ ਗੱਲਬਾਤ
• ⚡ ਬਿਜਲੀ-ਤੇਜ਼ ਜਵਾਬ
• 💡 ਇਨਸਾਨ-ਵਰਗੀ ਸਮਝ
• 🎨 ਰਚਨਾਤਮਕ ਸਮੱਸਿਆ ਹੱਲ
• 📚 ਵਿਸ਼ਾਲ ਗਿਆਨ ਭੰਡਾਰ""",
                'start_chat': """💬 *ਚੈਟ ਕਰਨ ਲਈ ਤਿਆਰ?* 
ਮੈਨੂੰ ਕੋਈ ਵੀ ਸੰਦੇਸ਼ ਭੇਜੋ ਅਤੇ AI ਦੇ ਭਵਿੱਖ ਦਾ ਅਨੁਭਵ ਕਰੋ!"""
            }
        }
        
        return messages.get(lang_code, messages['hi'])
    
    def get_help_message(self, lang_code: str) -> str:
        """Get help message in detected language"""
        help_messages = {
            'en': f"""🆘 *{Config.BOT_NAME} Help Guide v2.5.0* 🆘
══════════════════════════════

📚 *HOW TO USE:*
- Send any message to receive intelligent responses
- Maintains conversation context automatically
- Supports all topics across multiple languages

🔧 *AVAILABLE COMMANDS:*
/start  - Display welcome message and main menu
/help   - Show this help documentation
/info   - View system specifications
/settings - Change language/preferences

💡 *USAGE RECOMMENDATIONS:*
1. Formulate specific questions for precise answers
2. Provide clear, detailed queries for optimal results
3. Language switching supported mid-conversation

⚙️ *TECHNICAL DETAILS:*
- AI Model: Groq LLaMA 3 8B
- Framework: USTAAD-AI Engine
- Developer: {Config.DEVELOPER}
- System Version: {Config.VERSION}

🟢 *SYSTEM STATUS*: [ONLINE]

{Config.POWERED_BY} | {Config.VERSION}""",
            
            'hi': f"""🆘 *{Config.BOT_NAME} सहायता गाइड v2.5.0* 🆘
══════════════════════════════

📚 *उपयोग कैसे करें:*
- बुद्धिमान उत्तर प्राप्त करने के लिए कोई भी संदेश भेजें
- बातचीत का संदर्भ स्वचालित रूप से बनाए रखता है
- कई भाषाओं में सभी विषयों का समर्थन करता है

🔧 *उपलब्ध कमांड:*
/start  - स्वागत संदेश और मुख्य मेनू प्रदर्शित करें
/help   - यह सहायता दस्तावेज़ दिखाएं
/info   - सिस्टम विनिर्देश देखें
/settings - भाषा/वरीयताएं बदलें

💡 *उपयोग की सिफारिशें:*
1. सटीक उत्तरों के लिए विशिष्ट प्रश्न तैयार करें
2. इष्टतम परिणामों के लिए स्पष्ट, विस्तृत प्रश्न प्रदान करें
3. बातचीत के बीच में भाषा बदलना समर्थित है

⚙️ *तकनीकी विवरण:*
- AI मॉडल: Groq LLaMA 3 8B
- फ्रेमवर्क: USTAAD-AI Engine
- डेवलपर: {Config.DEVELOPER}
- सिस्टम संस्करण: {Config.VERSION}

🟢 *सिस्टम स्थिति*: [ऑनलाइन]

{Config.POWERED_BY} | {Config.VERSION}""",
            
            'ur': f"""🆘 *{Config.BOT_NAME} مدد گائیڈ v2.5.0* 🆘
══════════════════════════════

📚 *استعمال کیسے کریں:*
- ذہین جوابات حاصل کرنے کے لیے کوئی بھی پیغام بھیجیں
- گفتگو کا سیاق خودکار طور پر برقرار رکھتا ہے
- متعدد زبانوں میں تمام موضوعات کی حمایت کرتا ہے

🔧 *دستیاب کمانڈز:*
/start  - خوش آمدید پیغام اور مین مینو دکھائیں
/help   - یہ مدد کی دستاویز دکھائیں
/info   - سسٹم کی تفصیلات دیکھیں
/settings - زبان/ترجیحات تبدیل کریں

💡 *استعمال کی تجاویز:*
1. درست جوابات کے لیے مخصوص سوالات تیار کریں
2. بہترین نتائج کے لیے واضح، تفصیلی سوالات فراہم کریں
3. گفتگو کے دوران زبان تبدیل کرنا سپورٹ شدہ ہے

⚙️ *تکنیکی تفصیلات:*
- AI ماڈل: Groq LLaMA 3 8B
- فریم ورک: USTAAD-AI Engine
- ڈیولپر: {Config.DEVELOPER}
- سسٹم ورژن: {Config.VERSION}

🟢 *سسٹم کی حالت*: [آن لائن]

{Config.POWERED_BY} | {Config.VERSION}""",
            
            'bn': f"""🆘 *{Config.BOT_NAME} সাহায্য গাইড v2.5.0* 🆘
══════════════════════════════

📚 *কিভাবে ব্যবহার করবেন:*
- বুদ্ধিমান উত্তর পেতে যেকোনো বার্তা পাঠান
- স্বয়ংক্রিয়ভাবে কথোপকথনের প্রসঙ্গ বজায় রাখে
- একাধিক ভাষায় সমস্ত বিষয় সমর্থন করে

🔧 *উপলব্ধ কমান্ড:*
/start  - স্বাগত বার্তা এবং প্রধান মেনু প্রদর্শন করুন
/help   - এই সাহায্য নথি দেখান
/info   - সিস্টেম বিবরণ দেখুন
/settings - ভাষা/পছন্দ পরিবর্তন করুন

💡 *ব্যবহারের সুপারিশ:*
1. সুনির্দিষ্ট উত্তর পেতে নির্দিষ্ট প্রশ্ন তৈরি করুন
2. সর্বোত্তম ফলাফলের জন্য স্পষ্ট, বিস্তারিত প্রশ্ন প্রদান করুন
3. কথোপকথনের মাঝে ভাষা পরিবর্তন সমর্থিত

⚙️ *প্রযুক্তিগত বিবরণ:*
- AI মডেল: Groq LLaMA 3 8B
- ফ্রেমওয়ার্ক: USTAAD-AI Engine
- ডেভেলপার: {Config.DEVELOPER}
- সিস্টেম সংস্করণ: {Config.VERSION}

🟢 *সিস্টেম অবস্থা*: [অনলাইন]

{Config.POWERED_BY} | {Config.VERSION}""",
            
            'mr': f"""🆘 *{Config.BOT_NAME} मदत मार्गदर्शक v2.5.0* 🆘
══════════════════════════════

📚 *कसे वापरायचे:*
- बुद्धिमान उत्तरे मिळविण्यासाठी कोणतेही संदेश पाठवा
- संभाषण संदर्भ स्वयंचलितपणे राखतो
- एकाधिक भाषांमध्ये सर्व विषयांना समर्थन देते

🔧 *उपलब्ध आज्ञा:*
/start  - स्वागत संदेश आणि मुख्य मेनू दाखवा
/help   - हे मदत दस्तऐवज दाखवा
/info   - प्रणाली तपशील पहा
/settings - भाषा/प्राधान्ये बदला

💡 *वापर शिफारसी:*
1. अचूक उत्तरांसाठी विशिष्ट प्रश्न तयार करा
2. इष्टतम परिणामांसाठी स्पष्ट, तपशीलवार प्रश्न द्या
3. संभाषणाच्या मध्यात भाषा बदलणे समर्थित

⚙️ *तांत्रिक तपशील:*
- AI मॉडेल: Groq LLaMA 3 8B
- फ्रेमवर्क: USTAAD-AI Engine
- विकसक: {Config.DEVELOPER}
- प्रणाली आवृत्ती: {Config.VERSION}

🟢 *प्रणाली स्थिती*: [ऑनलाइन]

{Config.POWERED_BY} | {Config.VERSION}""",
            
            'te': f"""🆘 *{Config.BOT_NAME} సహాయం గైడ్ v2.5.0* 🆘
══════════════════════════════

📚 *ఎలా ఉపయోగించాలో:*
- తెలివైన ప్రతిస్పందనలను పొందడానికి ఏదైనా సందేశాన్ని పంపండి
- సంభాషణ సందర్భాన్ని స్వయంచాలకంగా నిర్వహిస్తుంది
- బహుళ భాషలలో అన్ని అంశాలకు మద్దతు ఇస్తుంది

🔧 *అందుబాటులో ఉన్న ఆదేశాలు:*
/start  - స్వాగత సందేశం మరియు ప్రధాన మెనూ ప్రదర్శించండి
/help   - ఈ సహాయం డాక్యుమెంటేషన్ చూపించు
/info   - సిస్టమ్ స్పెసిఫికేషన్లు వీక్షించండి
/settings - భాష/ప్రాధాన్యతలు మార్చండి

💡 *వినియోగ సిఫార్సులు:*
1. ఖచ్చితమైన సమాధానాల కోసం నిర్దిష్ట ప్రశ్నలను రూపొందించండి
2. అనుకూల ఫలితాల కోసం స్పష్టమైన, వివరణాత్మక ప్రశ్నలు అందించండి
3. సంభాషణ మధ్యలో భాష మార్పు మద్దతు

⚙️ *సాంకేతిక వివరాలు:*
- AI మోడల్: Groq LLaMA 3 8B
- ఫ్రేమ్వర్క్: USTAAD-AI Engine
- డెవలపర్: {Config.DEVELOPER}
- సిస్టమ్ వెర్షన్: {Config.VERSION}

🟢 *సిస్టమ్ స్థితి*: [ఆన్లైన్]

{Config.POWERED_BY} | {Config.VERSION}""",
            
            'ta': f"""🆘 *{Config.BOT_NAME} உதவி வழிகாட்டி v2.5.0* 🆘
══════════════════════════════

📚 *எப்படி பயன்படுத்துவது:*
- அறிவார்ந்த பதில்களைப் பெற எந்தவொரு செய்தியையும் அனுப்பவும்
- உரையாடல் சூழலை தானாகவே பராமரிக்கிறது
- பல மொழிகளில் அனைத்து தலைப்புகளையும் ஆதரிக்கிறது

🔧 *கிடைக்கும் கட்டளைகள்:*
/start  - வரவேற்பு செய்தி மற்றும் முதன்மை மெனு காட்டு
/help   - இந்த உதவி ஆவணத்தைக் காட்டு
/info   - கணினி விவரக்குறிப்புகளைப் பார்க்கவும்
/settings - மொழி/விருப்பத்தேர்வுகளை மாற்றவும்

💡 *பயன்பாட்டு பரிந்துரைகள்:*
1. துல்லியமான பதில்களுக்கு குறிப்பிட்ட கேள்விகளை உருவாக்கவும்
2. உகந்த முடிவுகளுக்கு தெளிவான, விரிவான கேள்விகளை வழங்கவும்
3. உரையாடலின் நடுவில் மொழி மாற்றம் ஆதரிக்கப்படுகிறது

⚙️ *தொழில்நுட்ப விவரங்கள்:*
- AI மாதிரி: Groq LLaMA 3 8B
- கட்டமைப்பு: USTAAD-AI Engine
- டெவலப்பர்: {Config.DEVELOPER}
- கணினி பதிப்பு: {Config.VERSION}

🟢 *கணினி நிலை*: [ஆன்லைன்]

{Config.POWERED_BY} | {Config.VERSION}""",
            
            'gu': f"""🆘 *{Config.BOT_NAME} મદદ માર્ગદર્શિકા v2.5.0* 🆘
══════════════════════════════

📚 *કેવી રીતે વાપરવું:*
- બુદ્ધિશાળી પ્રતિભાવો મેળવવા માટે કોઈપણ સંદેશ મોકલો
- સંવાદ સંદર્ભ આપમેળે જાળવે છે
- બહુવિધ ભાષાઓમાં તમામ વિષયોને આધાર આપે છે

🔧 *ઉપલબ્ધ આદેશો:*
/start  - સ્વાગત સંદેશ અને મુખ્ય મેનુ પ્રદર્શિત કરો
/help   - આ મદદ દસ્તાવેજીકરણ બતાવો
/info   - સિસ્ટમ સ્પષ્ટીકરણો જુઓ
/settings - ભાષા/પસંદગીઓ બદલો

💡 *ઉપયોગ ભલામણો:*
1. ચોક્કસ જવાબો માટે ચોક્કસ પ્રશ્નો ઘડો
2. શ્રેષ્ઠ પરિણામો માટે સ્પષ્ટ, વિગતવાર પ્રશ્નો પ્રદાન કરો
3. સંવાદ દરમિયાન ભાષા બદલવાનું સમર્થન

⚙️ *ટેકનિકલ વિગતો:*
- AI મોડેલ: Groq LLaMA 3 8B
- ફ્રેમવર્ક: USTAAD-AI Engine
- ડેવલપર: {Config.DEVELOPER}
- સિસ્ટમ સંસ્કરણ: {Config.VERSION}

🟢 *સિસ્ટમ સ્થિતિ*: [ઑનલાઇન]

{Config.POWERED_BY} | {Config.VERSION}""",
            
            'kn': f"""🆘 *{Config.BOT_NAME} ಸಹಾಯ ಮಾರ್ಗದರ್ಶಿ v2.5.0* 🆘
══════════════════════════════

📚 *ಹೇಗೆ ಬಳಸುವುದು:*
- ಬುದ್ಧಿವಂತ ಪ್ರತಿಕ್ರಿಯೆಗಳನ್ನು ಪಡೆಯಲು ಯಾವುದೇ ಸಂದೇಶವನ್ನು ಕಳುಹಿಸಿ
- ಸಂಭಾಷಣೆಯ ಸಂದರ್ಭವನ್ನು ಸ್ವಯಂಚಾಲಿತವಾಗಿ ನಿರ್ವಹಿಸುತ್ತದೆ
- ಬಹು ಭಾಷೆಗಳಲ್ಲಿ ಎಲ್ಲಾ ವಿಷಯಗಳನ್ನು ಬೆಂಬಲಿಸುತ್ತದೆ

🔧 *ಲಭ್ಯವಿರುವ ಆಜ್ಞೆಗಳು:*
/start  - ಸ್ವಾಗತ ಸಂದೇಶ ಮತ್ತು ಮುಖ್ಯ ಮೆನು ಪ್ರದರ್ಶಿಸಿ
/help   - ಈ ಸಹಾಯ ದಾಖಲೆಯನ್ನು ತೋರಿಸಿ
/info   - ಸಿಸ್ಟಮ್ ವಿವರಗಳನ್ನು ವೀಕ್ಷಿಸಿ
/settings - ಭಾಷೆ/ಪ್ರಾಧಾನ್ಯತೆಗಳನ್ನು ಬದಲಾಯಿಸಿ

💡 *ಬಳಕೆ ಶಿಫಾರಸುಗಳು:*
1. ನಿಖರವಾದ ಉತ್ತರಗಳಿಗಾಗಿ ನಿರ್ದಿಷ್ಟ ಪ್ರಶ್ನೆಗಳನ್ನು ರೂಪಿಸಿ
2. ಉತ್ತಮ ಫಲಿತಾಂಶಗಳಿಗಾಗಿ ಸ್ಪಷ್ಟ, ವಿವರವಾದ ಪ್ರಶ್ನೆಗಳನ್ನು ನೀಡಿ
3. ಸಂಭಾಷಣೆಯ ಮಧ್ಯದಲ್ಲಿ ಭಾಷೆ ಬದಲಾಯಿಸಲು ಬೆಂಬಲ

⚙️ *ತಾಂತ್ರಿಕ ವಿವರಗಳು:*
- AI ಮಾದರಿ: Groq LLaMA 3 8B
- ಚೌಕಟ್ಟು: USTAAD-AI Engine
- ಡೆವಲಪರ್: {Config.DEVELOPER}
- ಸಿಸ್ಟಮ್ ಆವೃತ್ತಿ: {Config.VERSION}

🟢 *ಸಿಸ್ಟಮ್ ಸ್ಥಿತಿ*: [ಆನ್ಲೈನ್]

{Config.POWERED_BY} | {Config.VERSION}""",
            
            'or': f"""🆘 *{Config.BOT_NAME} ସାହାଯ୍ୟ ମାର୍ଗଦର୍ଶିକା v2.5.0* 🆘
══════════════════════════════

📚 *କିପରି ବ୍ୟବହାର କରିବେ:*
- ବୁଦ୍ଧିମାନ ପ୍ରତିକ୍ରିୟା ପାଇଁ ଯେକ any ଣସି ବାର୍ତ୍ତା ପଠାନ୍ତୁ
- ସଂଳାପ ସନ୍ଦର୍ଭ ସ୍ୱୟଂଚାଳିତ ଭାବରେ ବଜାୟ ରଖେ
- ଏକାଧିକ ଭାଷାରେ ସମସ୍ତ ବିଷୟକୁ ସମର୍ଥନ କରେ

🔧 *ଉପଲବ୍ଧ ନିର୍ଦ୍ଦେଶ:*
/start  - ସ୍ୱାଗତ ବାର୍ତ୍ତା ଏବଂ ମୁଖ୍ୟ ମେନୁ ପ୍ରଦର୍ଶନ କରନ୍ତୁ
/help   - ଏହି ସାହାଯ୍ୟ ଡକ୍ୟୁମେଣ୍ଟେସନ୍ ଦେଖାନ୍ତୁ
/info   - ସିଷ୍ଟମ୍ ସ୍ପେସିଫିକେସନ୍ ଦେଖନ୍ତୁ
/settings - ଭାଷା / ପସନ୍ଦ ପରିବର୍ତ୍ତନ କରନ୍ତୁ

💡 *ବ୍ୟବହାର ସୁପାରିଶ:*
1. ସଠିକ୍ ଉତ୍ତର ପାଇଁ ନିର୍ଦ୍ଦିଷ୍ଟ ପ୍ରଶ୍ନ ତିଆରି କରନ୍ତୁ
2. ଉତ୍ତମ ଫଳାଫଳ ପାଇଁ ସ୍ପଷ୍ଟ, ବିସ୍ତୃତ ପ୍ରଶ୍ନ ଦିଅନ୍ତୁ
3. ସଂଳାପ ମଧ୍ୟରେ ଭାଷା ପରିବର୍ତ୍ତନ ସମର୍ଥିତ

⚙️ *ଟେକ୍ନିକାଲ୍ ବିବରଣୀ:*
- AI ମଡେଲ୍: Groq LLaMA 3 8B
- ଫ୍ରେମୱାର୍କ: USTAAD-AI ଇଞ୍ଜିନ୍
- ବିକାଶକାରୀ: {Config.DEVELOPER}
- ସିଷ୍ଟମ୍ ସଂସ୍କରଣ: {Config.VERSION}

🟢 *ସିଷ୍ଟମ୍ ସ୍ଥିତି*: [ଅନଲାଇନ୍]

{Config.POWERED_BY} | {Config.VERSION}""",
            
            'pa': f"""🆘 *{Config.BOT_NAME} ਮਦਦ ਗਾਈਡ v2.5.0* 🆘
══════════════════════════════

📚 *ਵਰਤੋਂ ਕਿਵੇਂ ਕਰੀਏ:*
- ਬੁੱਧੀਮਾਨ ਜਵਾਬਾਂ ਪ੍ਰਾਪਤ ਕਰਨ ਲਈ ਕੋਈ ਵੀ ਸੰਦੇਸ਼ ਭੇਜੋ
- ਗੱਲਬਾਤ ਦੇ ਸੰਦਰਭ ਨੂੰ ਆਪਣੇ ਆਪ ਬਣਾਈ ਰੱਖਦਾ ਹੈ
- ਕਈ ਭਾਸ਼ਾਵਾਂ ਵਿੱਚ ਸਾਰੇ ਵਿਸ਼ਿਆਂ ਨੂੰ ਸਹਾਇਤਾ ਕਰਦਾ ਹੈ

🔧 *ਉਪਲਬਧ ਕਮਾਂਡ:*
/start  - ਸਵਾਗਤ ਸੰਦੇਸ਼ ਅਤੇ ਮੁੱਖ ਮੀਨੂੰ ਪ੍ਰਦਰਸ਼ਿਤ ਕਰੋ
/help   - ਇਹ ਮਦਦ ਦਸਤਾਵੇਜ਼ ਦਿਖਾਓ
/info   - ਸਿਸਟਮ ਵਿਸ਼ੇਸ਼ਤਾਵਾਂ ਦੇਖੋ
/settings - ਭਾਸ਼ਾ/ਤਰਜੀਹਾਂ ਬਦਲੋ

💡 *ਵਰਤੋਂ ਦੀਆਂ ਸਿਫਾਰਸ਼ਾਂ:*
1. ਸਹੀ ਜਵਾਬਾਂ ਲਈ ਖਾਸ ਸਵਾਲ ਤਿਆਰ ਕਰੋ
2. ਵਧੀਆ ਨਤੀਜਿਆਂ ਲਈ ਸਪਸ਼ਟ, ਵਿਸਤ੍ਰਿਤ ਸਵਾਲ ਦਿਓ
3. ਗੱਲਬਾਤ ਦੇ ਦੌਰਾਨ ਭਾਸ਼ਾ ਬਦਲਣਾ ਸਹਾਇਕ ਹੈ

⚙️ *ਤਕਨੀਕੀ ਵੇਰਵੇ:*
- AI ਮਾਡਲ: Groq LLaMA 3 8B
- ਫਰੇਮਵਰਕ: USTAAD-AI ਇੰਜਨ
- ਡਿਵੈਲਪਰ: {Config.DEVELOPER}
- ਸਿਸਟਮ ਵਰਜ਼ਨ: {Config.VERSION}

🟢 *ਸਿਸਟਮ ਸਥਿਤੀ*: [ਆਨਲਾਈਨ]

{Config.POWERED_BY} | {Config.VERSION}"""
        }
        
        return help_messages.get(lang_code, help_messages['hi'])
    
    def get_info_message(self, lang_code: str) -> str:
        """Get bot info message in detected language"""
        info_messages = {
            'en': f"""🤖 *{Config.BOT_NAME} System Information* 🤖
══════════════════════════════

⚙️ *CORE ARCHITECTURE*
├─ AI Model: Groq LLaMA 3 8B
├─ Framework: USTAAD-AI Engine
├─ Language: Python 3.11
└─ Security: Enterprise-Grade

🌟 *KEY CAPABILITIES*
├─ Supports 50+ Global Languages
├─ Advanced Context Understanding
├─ Instant Response Generation
├─ Natural Conversation Flow

📋 *SYSTEM DETAILS*
├─ Developer: {Config.DEVELOPER}
├─ Specialization: AI Chat Systems
├─ Platform: Telegram Messenger
├─ Version: {Config.VERSION}
└─ Last Updated: June 2024

💡 *GETTING STARTED*
1. Begin with: /start
2. Type your query
3. For help: /help

🟢 *SYSTEM STATUS*: OPERATIONAL

{Config.POWERED_BY} | {Config.VERSION}""",
            
            'hi': f"""🤖 *{Config.BOT_NAME} सिस्टम जानकारी* 🤖
══════════════════════════════

⚙️ *मुख्य आर्किटेक्चर*
├─ AI मॉडल: Groq LLaMA 3 8B
├─ फ्रेमवर्क: USTAAD-AI Engine
├─ भाषा: Python 3.11
└─ सुरक्षा: एंटरप्राइज़-ग्रेड

🌟 *मुख्य क्षमताएं*
├─ 50+ वैश्विक भाषाओं का समर्थन
├─ उन्नत संदर्भ समझ
├─ तत्काल प्रतिक्रिया उत्पादन
├─ प्राकृतिक बातचीत प्रवाह

📋 *सिस्टम विवरण*
├─ डेवलपर: {Config.DEVELOPER}
├─ विशेषज्ञता: AI चैट सिस्टम
├─ प्लेटफॉर्म: टेलीग्राम मैसेंजर
├─ संस्करण: {Config.VERSION}
└─ अंतिम अपडेट: जून 2024

💡 *शुरुआत करें*
1. शुरू करने के लिए: /start
2. अपना प्रश्न टाइप करें
3. सहायता के लिए: /help

🟢 *सिस्टम स्थिति*: परिचालन

{Config.POWERED_BY} | {Config.VERSION}""",
            
            'ur': f"""🤖 *{Config.BOT_NAME} نظام کی معلومات* 🤖
══════════════════════════════

⚙️ *بنیادی فن تعمیر*
├─ AI ماڈل: Groq LLaMA 3 8B
├─ فریم ورک: USTAAD-AI Engine
├─ زبان: Python 3.11
└ـ سیکورٹی: انٹرپرائز-گریڈ

🌟 *اہم صلاحیتیں*
├─ 50+ عالمی زبانوں کی حمایت
├ـ اعلیٰ درجے کی سیاق و سباق کی سمجھ
├ـ فوری جواب کی تخلیق
├ـ قدرتی گفتگو کا بہاؤ

📋 *نظام کی تفصیلات*
├ـ ڈویلپر: {Config.DEVELOPER}
├ـ مہارت: AI چیٹ سسٹمز
├ـ پلیٹ فارم: ٹیلی گرام میسنجر
├ـ ورژن: {Config.VERSION}
└ـ آخری اپ ڈیٹ: جون 2024

💡 *شروع کرنے کا طریقہ*
1. شروع کرنے کے لیے: /start
2. اپنا سوال ٹائپ کریں
3. مدد کے لیے: /help

🟢 *نظام کی حیثیت*: کام کر رہا ہے

{Config.POWERED_BY} | {Config.VERSION}""",
            
            'bn': f"""🤖 *{Config.BOT_NAME} সিস্টেম তথ্য* 🤖
══════════════════════════════

⚙️ *মূল স্থাপত্য*
├─ AI মডেল: Groq LLaMA 3 8B
├─ ফ্রেমওয়ার্ক: USTAAD-AI ইঞ্জিন
├─ ভাষা: Python 3.11
└─ নিরাপত্তা: এন্টারপ্রাইজ-গ্রেড

🌟 *প্রধান ক্ষমতা*
├─ 50+ বৈশ্বিক ভাষা সমর্থন
├─ উন্নত প্রসঙ্গ বোঝা
├─ তাৎক্ষণিক প্রতিক্রিয়া উৎপাদন
├─ প্রাকৃতিক কথোপকথন প্রবাহ

📋 *সিস্টেম বিবরণ*
├─ ডেভেলপার: {Config.DEVELOPER}
├─ বিশেষীকরণ: AI চ্যাট সিস্টেম
├─ প্ল্যাটফর্ম: টেলিগ্রাম মেসেঞ্জার
├─ সংস্করণ: {Config.VERSION}
└─ শেষ আপডেট: জুন 2024

💡 *শুরু করা*
1. শুরু করতে: /start
2. আপনার প্রশ্ন টাইপ করুন
3. সাহায্যের জন্য: /help

🟢 *সিস্টেম অবস্থা*: পরিচালনাযোগ্য

{Config.POWERED_BY} | {Config.VERSION}""",
            
            'mr': f"""🤖 *{Config.BOT_NAME} सिस्टम माहिती* 🤖
══════════════════════════════

⚙️ *कोर आर्किटेक्चर*
├─ AI मॉडेल: Groq LLaMA 3 8B
├─ फ्रेमवर्क: USTAAD-AI इंजिन
├─ भाषा: Python 3.11
└─ सुरक्षा: एंटरप्राइझ-ग्रेड

🌟 *मुख्य क्षमता*
├─ 50+ जागतिक भाषांना समर्थन
├─ प्रगत संदर्भ समज
├─ त्वरित प्रतिसाद निर्मिती
├─ नैसर्गिक संभाषण प्रवाह

📋 *सिस्टम तपशील*
├─ विकसक: {Config.DEVELOPER}
├─ विशेषीकरण: AI चॅट सिस्टम
├─ प्लॅटफॉर्म: टेलिग्राम मेसेंजर
├─ आवृत्ती: {Config.VERSION}
└─ शेवटचे अद्यतन: जून 2024

💡 *सुरु करणे*
1. सुरू करा: /start
2. तुमचा प्रश्न टाइप करा
3. मदतीसाठी: /help

🟢 *सिस्टम स्थिती*: कार्यरत

{Config.POWERED_BY} | {Config.VERSION}""",
            
            'te': f"""🤖 *{Config.BOT_NAME} సిస్టమ్ సమాచారం* 🤖
══════════════════════════════

⚙️ *కోర్ ఆర్కిటెక్చర్*
├─ AI మోడల్: Groq LLaMA 3 8B
├─ ఫ్రేమ్వర్క్: USTAAD-AI ఇంజిన్
├─ భాష: Python 3.11
└─ భద్రత: ఎంటర్ప్రైజ్-గ్రేడ్

🌟 *ప్రధాన సామర్థ్యాలు*
├─ 50+ గ్లోబల్ భాషలకు మద్దతు
├─ అధునాతన సందర్భం అవగాహన
├─ తక్షణ ప్రతిస్పందన ఉత్పత్తి
├─ సహజ సంభాషణ ప్రవాహం

📋 *సిస్టమ్ వివరాలు*
├─ డెవలపర్: {Config.DEVELOPER}
├─ స్పెషలైజేషన్: AI చాట్ సిస్టమ్స్
├─ ప్లాట్ఫారమ్: టెలిగ్రామ్ మెసెంజర్
├─ వెర్షన్: {Config.VERSION}
└─ చివరి నవీకరణ: జూన్ 2024

💡 *ప్రారంభించడం*
1. ప్రారంభించండి: /start
2. మీ ప్రశ్నను టైప్ చేయండి
3. సహాయం కోసం: /help

🟢 *సిస్టమ్ స్థితి*: కార్యాచరణ

{Config.POWERED_BY} | {Config.VERSION}""",
            
            'ta': f"""🤖 *{Config.BOT_NAME} அமைப்பு தகவல்* 🤖
══════════════════════════════

⚙️ *கோர் கட்டமைப்பு*
├─ AI மாதிரி: Groq LLaMA 3 8B
├─ கட்டமைப்பு: USTAAD-AI இயந்திரம்
├─ மொழி: Python 3.11
└─ பாதுகாப்பு: நிறுவன-தரம்

🌟 *முக்கிய திறன்கள்*
├─ 50+ உலகளாவிய மொழிகளுக்கு ஆதரவு
├─ மேம்பட்ட சூழல் புரிதல்
├─ உடனடி பதில் உருவாக்கம்
├─ இயற்கையான உரையாடல் ஓட்டம்

📋 *அமைப்பு விவரங்கள்*
├─ டெவலப்பர்: {Config.DEVELOPER}
├─ நிபுணத்துவம்: AI அரட்டை அமைப்புகள்
├─ மேடை: டெலிகிராம் மெசஞ்சர்
├─ பதிப்பு: {Config.VERSION}
└─ கடைசியாக புதுப்பிக்கப்பட்டது: ஜூன் 2024

💡 *தொடங்குதல்*
1. தொடங்கவும்: /start
2. உங்கள் கேள்வியை தட்டச்சு செய்யவும்
3. உதவிக்கு: /help

🟢 *அமைப்பு நிலை*: செயல்பாட்டில்

{Config.POWERED_BY} | {Config.VERSION}""",
            
            'gu': f"""🤖 *{Config.BOT_NAME} સિસ્ટમ માહિતી* 🤖
══════════════════════════════

⚙️ *કોર આર્કિટેક્ચર*
├─ AI મોડેલ: Groq LLaMA 3 8B
├─ ફ્રેમવર્ક: USTAAD-AI એન્જિન
├─ ભાષા: Python 3.11
└─ સુરક્ષા: એન્ટરપ્રાઇઝ-ગ્રેડ

🌟 *મુખ્ય ક્ષમતાઓ*
├─ 50+ ગ્લોબલ ભાષાઓને આધાર
├─ અદ્યતન સંદર્ભ સમજ
├─ ત્વરિત પ્રતિભાવ ઉત્પાદન
├─ કુદરતી સંવાદ પ્રવાહ

📋 *સિસ્ટમ વિગતો*
├─ ડેવલપર: {Config.DEVELOPER}
├─ વિશેષતા: AI ચેટ સિસ્ટમ્સ
├─ પ્લેટફોર્મ: ટેલિગ્રામ મેસેન્જર
├─ આવૃત્તિ: {Config.VERSION}
└─ છેલ્લી અપડેટ: જૂન 2024

💡 *પ્રારંભ કરી રહ્યા છીએ*
1. શરૂ કરો: /start
2. તમારી ક્વેરી ટાઇપ કરો
3. મદદ માટે: /help

🟢 *સિસ્ટમ સ્થિતિ*: ઓપરેશનલ

{Config.POWERED_BY} | {Config.VERSION}""",
            
            'kn': f"""🤖 *{Config.BOT_NAME} ವ್ಯವಸ್ಥೆಯ ಮಾಹಿತಿ* 🤖
══════════════════════════════

⚙️ *ಕೋರ್ ಆರ್ಕಿಟೆಕ್ಚರ್*
├─ AI ಮಾದರಿ: Groq LLaMA 3 8B
├─ ಚೌಕಟ್ಟು: USTAAD-AI ಎಂಜಿನ್
├─ ಭಾಷೆ: Python 3.11
└─ ಭದ್ರತೆ: ಎಂಟರ್ಪ್ರೈಸ್-ಗ್ರೇಡ್

🌟 *ಪ್ರಮುಖ ಸಾಮರ್ಥ್ಯಗಳು*
├─ 50+ ಜಾಗತಿಕ ಭಾಷೆಗಳಿಗೆ ಬೆಂಬಲ
├─ ಸುಧಾರಿತ ಸಂದರ್ಭ ತಿಳುವಳಿಕೆ
├─ ತ್ವರಿತ ಪ್ರತಿಕ್ರಿಯೆ ಉತ್ಪಾದನೆ
├─ ಸಹಜ ಸಂಭಾಷಣೆ ಹರಿವು

📋 *ವ್ಯವಸ್ಥೆಯ ವಿವರಗಳು*
├─ ಡೆವಲಪರ್: {Config.DEVELOPER}
├─ ವಿಶೇಷತೆ: AI ಚಾಟ್ ವ್ಯವಸ್ಥೆಗಳು
├─ ವೇದಿಕೆ: ಟೆಲಿಗ್ರಾಮ್ ಮೆಸೆಂಜರ್
├─ ಆವೃತ್ತಿ: {Config.VERSION}
└─ ಕೊನೆಯ ನವೀಕರಣ: ಜೂನ್ 2024

💡 *ಪ್ರಾರಂಭಿಸುವುದು*
1. ಪ್ರಾರಂಭಿಸಿ: /start
2. ನಿಮ್ಮ ಪ್ರಶ್ನೆಯನ್ನು ಟೈಪ್ ಮಾಡಿ
3. ಸಹಾಯಕ್ಕಾಗಿ: /help

🟢 *ವ್ಯವಸ್ಥೆಯ ಸ್ಥಿತಿ*: ಕಾರ್ಯಾಚರಣೆಯಲ್ಲಿದೆ

{Config.POWERED_BY} | {Config.VERSION}""",
            
            'or': f"""🤖 *{Config.BOT_NAME} ସିଷ୍ଟମ୍ ସୂଚନା* 🤖
══════════════════════════════

⚙️ *କୋର୍ ଆର୍କିଟେକ୍ଚର୍*
├─ AI ମଡେଲ୍: Groq LLaMA 3 8B
├─ ଫ୍ରେମୱାର୍କ: USTAAD-AI ଇଞ୍ଜିନ୍
├─ ଭାଷା: Python 3.11
└─ ସୁରକ୍ଷା: ଏଣ୍ଟରପ୍ରାଇଜ୍-ଗ୍ରେଡ୍

🌟 *ମୁଖ୍ୟ କ୍ଷମତା*
├─ 50+ ଗ୍ଲୋବାଲ୍ ଭାଷାକୁ ସମର୍ଥନ
├─ ଉନ୍ନତ ସନ୍ଦର୍ଭ ବୁଝାମଣା
├─ ତତକ୍ଷଣାତ୍ ପ୍ରତିକ୍ରିୟା ଉତ୍ପାଦନ
├─ ପ୍ରାକୃତିକ କଥୋପକଥନ ପ୍ରବାହ

📋 *ସିଷ୍ଟମ୍ ବିବରଣୀ*
├─ ଡେଭଲପର୍: {Config.DEVELOPER}
├─ ବିଶେଷତା: AI ଚାଟ୍ ସିଷ୍ଟମ୍
├─ ପ୍ଲାଟଫର୍ମ: ଟେଲିଗ୍ରାମ୍ ମେସେଞ୍ଜର୍
├─ ସଂସ୍କରଣ: {Config.VERSION}
└─ ଶେଷ ଅଦ୍ୟତନ: ଜୁନ୍ 2024

💡 *ଆରମ୍ଭ କରିବା*
1. ଆରମ୍ଭ କରନ୍ତୁ: /start
2. ଆପଣଙ୍କର ପ୍ରଶ୍ନ ଟାଇପ୍ କରନ୍ତୁ
3. ସାହାଯ୍ୟ ପାଇଁ: /help

🟢 *ସିଷ୍ଟମ୍ ସ୍ଥିତି*: କାର୍ଯ୍ୟକାରୀ

{Config.POWERED_BY} | {Config.VERSION}""",
            
            'pa': f"""🤖 *{Config.BOT_NAME} ਸਿਸਟਮ ਜਾਣਕਾਰੀ* 🤖
══════════════════════════════

⚙️ *ਕੋਰ ਆਰਕੀਟੈਕਚਰ*
├─ AI ਮਾਡਲ: Groq LLaMA 3 8B
├─ ਫਰੇਮਵਰਕ: USTAAD-AI ਇੰਜਨ
├─ ਭਾਸ਼ਾ: Python 3.11
└─ ਸੁਰੱਖਿਆ: ਐਂਟਰਪ੍ਰਾਈਜ਼-ਗ੍ਰੇਡ

🌟 *ਮੁੱਖ ਸਮਰੱਥਾਵਾਂ*
├─ 50+ ਵਿਸ਼ਵ ਭਾਸ਼ਾਵਾਂ ਦਾ ਸਮਰਥਨ
├─ ਉੱਨਤ ਸੰਦਰਭ ਸਮਝ
├─ ਤੁਰੰਤ ਜਵਾਬ ਪੈਦਾਵਾਰ
├─ ਕੁਦਰਤੀ ਗੱਲਬਾਤ ਦਾ ਪ੍ਰਵਾਹ

📋 *ਸਿਸਟਮ ਵੇਰਵੇ*
├─ ਡਿਵੈਲਪਰ: {Config.DEVELOPER}
├─ ਵਿਸ਼ੇਸ਼ਤਾ: AI ਚੈਟ ਸਿਸਟਮ
├─ ਪਲੇਟਫਾਰਮ: ਟੈਲੀਗ੍ਰਾਮ ਮੈਸੇਂਜਰ
├─ ਵਰਜਨ: {Config.VERSION}
└─ ਆਖਰੀ ਅਪਡੇਟ: ਜੂਨ 2024

💡 *ਸ਼ੁਰੂ ਕਰਨਾ*
1. ਸ਼ੁਰੂ ਕਰੋ: /start
2. ਆਪਣਾ ਸਵਾਲ ਟਾਈਪ ਕਰੋ
3. ਮਦਦ ਲਈ: /help

🟢 *ਸਿਸਟਮ ਸਥਿਤੀ*: ਚਾਲੂ

{Config.POWERED_BY} | {Config.VERSION}"""
        }
        
        return info_messages.get(lang_code, info_messages['hi'])
