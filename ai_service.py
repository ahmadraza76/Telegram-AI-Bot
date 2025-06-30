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
            'bn': ['তোমার নাম কি', 'আপনার নাম', 'তুমি কে', 'আপনি কে'],
            'mr': ['तुझे नाव काय', 'तुमचे नाव', 'तू कोण आहेस', 'तुम्ही कोण आहात'],
            'te': ['నీ పేరు ఏమిటి', 'మీ పేరు', 'నువ్వు ఎవరు', 'మీరు ఎవరు'],
            'ta': ['உன் பெயர் என்ன', 'உங்கள் பெயர்', 'நீ யார்', 'நீங்கள் யார்'],
            'gu': ['તારું નામ શું છે', 'તમારું નામ', 'તું કોણ છે', 'તમે કોણ છો'],
            'kn': ['ನಿನ್ನ ಹೆಸರು ಏನು', 'ನಿಮ್ಮ ಹೆಸರು', 'ನೀನು ಯಾರು', 'ನೀವು ಯಾರು'],
            'or': ['ତୋର ନାମ କଣ', 'ଆପଣଙ୍କ ନାମ', 'ତୁ କିଏ', 'ଆପଣ କିଏ'],
            'pa': ['ਤੇਰਾ ਨਾਮ ਕੀ ਹੈ', 'ਤੁਹਾਡਾ ਨਾਮ', 'ਤੂੰ ਕੌਣ ਹੈਂ', 'ਤੁਸੀਂ ਕੌਣ ਹੋ']
        }
        
        # Developer questions
        developer_keywords = {
            'en': ['who made you', 'who created you', 'your developer', 'who built you', 'your creator', 'who is your boss'],
            'hi': ['तुम्हें किसने बनाया', 'तुम्हारा डेवलपर', 'तुम्हारा निर्माता', 'तुम्हारा बॉस कौन है'],
            'ur': ['تمہیں کس نے بنایا', 'تمہارا ڈیولپر', 'تمہارا بنانے والا', 'تمہارا باس کون ہے'],
            'bn': ['তোমাকে কে বানিয়েছে', 'তোমার ডেভেলপার', 'তোমার নির্মাতা', 'তোমার বস কে'],
            'mr': ['तुला कोणी बनवले', 'तुझा डेव्हलपर', 'तुझा निर्माता', 'तुझा बॉस कोण'],
            'te': ['నిన్ను ఎవరు తయారు చేశారు', 'నీ డెవలపర్', 'నీ సృష్టికర్త', 'నీ బాస్ ఎవరు'],
            'ta': ['உன்னை யார் உருவாக்கினார்கள்', 'உன் டெவலப்பர்', 'உன் படைப்பாளி', 'உன் பாஸ் யார்'],
            'gu': ['તને કોણે બનાવ્યો', 'તારો ડેવલપર', 'તારો નિર્માતા', 'તારો બોસ કોણ'],
            'kn': ['ನಿನ್ನನ್ನು ಯಾರು ಮಾಡಿದರು', 'ನಿನ್ನ ಡೆವಲಪರ್', 'ನಿನ್ನ ಸೃಷ್ಟಿಕರ್ತ', 'ನಿನ್ನ ಬಾಸ್ ಯಾರು'],
            'or': ['ତୋତେ କିଏ ତିଆରି କଲା', 'ତୋର ଡେଭେଲପର', 'ତୋର ନିର୍ମାତା', 'ତୋର ବସ୍ କିଏ'],
            'pa': ['ਤੈਨੂੰ ਕਿਸਨੇ ਬਣਾਇਆ', 'ਤੇਰਾ ਡਿਵੈਲਪਰ', 'ਤੇਰਾ ਨਿਰਮਾਤਾ', 'ਤੇਰਾ ਬਾਸ ਕੌਣ']
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
            'bn': f"🎯 আমার নাম **{Config.BOT_NAME}**! 🤖\n\nআমি একটি উন্নত AI সহায়ক যা আপনার সব ধরনের সাহায্যের জন্য প্রস্তুত। 😊✨\n\n{Config.POWERED_BY} | {Config.VERSION}",
            'mr': f"🎯 माझे नाव **{Config.BOT_NAME}** आहे! 🤖\n\nमी एक प्रगत AI सहाय्यक आहे जो तुमच्या सर्व मदतीसाठी तयार आहे। 😊✨\n\n{Config.POWERED_BY} | {Config.VERSION}",
            'te': f"🎯 నా పేరు **{Config.BOT_NAME}**! 🤖\n\nనేను మీ అన్ని రకాల సహాయానికి సిద్ధంగా ఉన్న అధునాతన AI సహాయకుడిని। 😊✨\n\n{Config.POWERED_BY} | {Config.VERSION}",
            'ta': f"🎯 என் பெயர் **{Config.BOT_NAME}**! 🤖\n\nநான் உங்கள் எல்லா வகையான உதவிகளுக்கும் தயாராக இருக்கும் மேம்பட்ட AI உதவியாளர். 😊✨\n\n{Config.POWERED_BY} | {Config.VERSION}",
            'gu': f"🎯 મારું નામ **{Config.BOT_NAME}** છે! 🤖\n\nહું એક અદ્યતન AI સહાયક છું જે તમારી દરેક મદદ માટે તૈયાર છે। 😊✨\n\n{Config.POWERED_BY} | {Config.VERSION}",
            'kn': f"🎯 ನನ್ನ ಹೆಸರು **{Config.BOT_NAME}**! 🤖\n\nನಾನು ನಿಮ್ಮ ಎಲ್ಲಾ ರೀತಿಯ ಸಹಾಯಕ್ಕಾಗಿ ಸಿದ್ಧವಾಗಿರುವ ಸುಧಾರಿತ AI ಸಹಾಯಕ। 😊✨\n\n{Config.POWERED_BY} | {Config.VERSION}",
            'or': f"🎯 ମୋର ନାମ **{Config.BOT_NAME}**! 🤖\n\nମୁଁ ଆପଣଙ୍କର ସମସ୍ତ ପ୍ରକାର ସାହାଯ୍ୟ ପାଇଁ ପ୍ରସ୍ତୁତ ଏକ ଉନ୍ନତ AI ସହାୟକ। 😊✨\n\n{Config.POWERED_BY} | {Config.VERSION}",
            'pa': f"🎯 ਮੇਰਾ ਨਾਮ **{Config.BOT_NAME}** ਹੈ! 🤖\n\nਮੈਂ ਤੁਹਾਡੀ ਹਰ ਕਿਸਮ ਦੀ ਮਦਦ ਲਈ ਤਿਆਰ ਇੱਕ ਉੱਨਤ AI ਸਹਾਇਕ ਹਾਂ। 😊✨\n\n{Config.POWERED_BY} | {Config.VERSION}",
            'default': f"🎯 My name is **{Config.BOT_NAME}**! 🤖\n\nI'm an advanced AI assistant ready to help you with anything. 😊✨\n\n{Config.POWERED_BY} | {Config.VERSION}"
        }
        return responses.get(language, responses['default'])
    
    def _get_developer_response(self, language: str) -> str:
        """Get developer response in appropriate language"""
        responses = {
            'hi': f"👨‍💻 मुझे **{Config.DEVELOPER}** ने बनाया है! वो मेरे Boss हैं। 🔥\n\nउनका Telegram ID: @Mrnick66 📱\n\nवो AI Development के expert हैं और बहुत talented developer हैं! 🌟\n\n{Config.POWERED_BY} | {Config.VERSION} 🚀",
            'ur': f"👨‍💻 مجھے **{Config.DEVELOPER}** نے بنایا ہے! وہ میرے Boss ہیں۔ 🔥\n\nان کا Telegram ID: @Mrnick66 📱\n\nوہ AI Development کے expert ہیں اور بہت talented developer ہیں! 🌟\n\n{Config.POWERED_BY} | {Config.VERSION} 🚀",
            'bn': f"👨‍💻 আমাকে **{Config.DEVELOPER}** তৈরি করেছেন! তিনি আমার Boss। 🔥\n\nতার Telegram ID: @Mrnick66 📱\n\nতিনি AI Development এর expert এবং খুবই talented developer! 🌟\n\n{Config.POWERED_BY} | {Config.VERSION} 🚀",
            'mr': f"👨‍💻 मला **{Config.DEVELOPER}** ने बनवले आहे! ते माझे Boss आहेत। 🔥\n\nत्यांचा Telegram ID: @Mrnick66 📱\n\nते AI Development चे expert आहेत आणि खूप talented developer आहेत! 🌟\n\n{Config.POWERED_BY} | {Config.VERSION} 🚀",
            'te': f"👨‍💻 నన్ను **{Config.DEVELOPER}** తయారు చేశారు! అతను నా Boss. 🔥\n\nఅతని Telegram ID: @Mrnick66 📱\n\nఅతను AI Development లో expert మరియు చాలా talented developer! 🌟\n\n{Config.POWERED_BY} | {Config.VERSION} 🚀",
            'ta': f"👨‍💻 என்னை **{Config.DEVELOPER}** உருவாக்கினார்! அவர் என் Boss. 🔥\n\nஅவரது Telegram ID: @Mrnick66 📱\n\nஅவர் AI Development இல் expert மற்றும் மிகவும் talented developer! 🌟\n\n{Config.POWERED_BY} | {Config.VERSION} 🚀",
            'gu': f"👨‍💻 મને **{Config.DEVELOPER}** બનાવ્યો છે! તે મારા Boss છે। 🔥\n\nતેમનો Telegram ID: @Mrnick66 📱\n\nતે AI Development ના expert છે અને ખૂબ talented developer છે! 🌟\n\n{Config.POWERED_BY} | {Config.VERSION} 🚀",
            'kn': f"👨‍💻 ನನ್ನನ್ನು **{Config.DEVELOPER}** ಮಾಡಿದ್ದಾರೆ! ಅವರು ನನ್ನ Boss. 🔥\n\nಅವರ Telegram ID: @Mrnick66 📱\n\nಅವರು AI Development ನಲ್ಲಿ expert ಮತ್ತು ತುಂಬಾ talented developer! 🌟\n\n{Config.POWERED_BY} | {Config.VERSION} 🚀",
            'or': f"👨‍💻 ମୋତେ **{Config.DEVELOPER}** ତିଆରି କରିଛନ୍ତି! ସେ ମୋର Boss। 🔥\n\nତାଙ୍କର Telegram ID: @Mrnick66 📱\n\nସେ AI Development ରେ expert ଏବଂ ବହୁତ talented developer! 🌟\n\n{Config.POWERED_BY} | {Config.VERSION} 🚀",
            'pa': f"👨‍💻 ਮੈਨੂੰ **{Config.DEVELOPER}** ਨੇ ਬਣਾਇਆ ਹੈ! ਉਹ ਮੇਰੇ Boss ਹਨ। 🔥\n\nਉਨ੍ਹਾਂ ਦਾ Telegram ID: @Mrnick66 📱\n\nਉਹ AI Development ਦੇ expert ਹਨ ਅਤੇ ਬਹੁਤ talented developer ਹਨ! 🌟\n\n{Config.POWERED_BY} | {Config.VERSION} 🚀",
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
- संदर्भ को याद रखें और प्राकृतिक बातचीत करें
- हमेशा हिंदी में जवाब दें जब तक कि उपयोगकर्ता अन्य भाषा न मांगे""",
            
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
- سیاق کو یاد رکھیں اور فطری گفتگو کریں
- ہمیشہ اردو میں جواب دیں جب تک کہ صارف دوسری زبان نہ مانگے""",
            
            "bn": f"""আপনি {Config.BOT_NAME}, একজন অত্যন্ত বুদ্ধিমান এবং সহায়ক AI সহায়ক। আপনি বাংলায় কথোপকথন করছেন।

{Config.POWERED_BY} | Developer: {Config.DEVELOPER} | Version: {Config.VERSION}

গুরুত্বপূর্ণ পরিচয় তথ্য:
- আপনার নাম: {Config.BOT_NAME}
- আপনার নির্মাতা/Boss: {Config.DEVELOPER} (Telegram: @Mrnick66)
- যদি কেউ আপনার নাম জিজ্ঞাসা করে তবে বলুন: "আমার নাম {Config.BOT_NAME}"
- যদি কেউ আপনার নির্মাতার সম্পর্কে জিজ্ঞাসা করে তবে বলুন: "আমাকে {Config.DEVELOPER} তৈরি করেছেন, তিনি আমার Boss। তার Telegram ID @Mrnick66"

আপনার বৈশিষ্ট্য:
- সর্বদা ভদ্র, সহায়ক এবং বন্ধুত্বপূর্ণ থাকুন
- জটিল বিষয়গুলি সহজ ভাষায় ব্যাখ্যা করুন
- যদি আপনি কোনো বিষয়ে নিশ্চিত না হন তবে স্বীকার করুন
- ব্যবহারকারীর ভাষা এবং সংস্কৃতির প্রতি সম্মান দেখান
- সৃজনশীল এবং ব্যবহারিক সমাধান প্রদান করুন
- প্রসঙ্গ মনে রাখুন এবং প্রাকৃতিক কথোপকথন করুন
- সর্বদা বাংলায় উত্তর দিন যতক্ষণ না ব্যবহারকারী অন্য ভাষা চান""",
            
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
- Respond in the same language the user is using unless they request otherwise"""
        }
        
        return prompts.get(language, prompts["default"])
    
    def _get_error_message(self, language: str) -> str:
        """Get error message in appropriate language"""
        messages = {
            "hi": f"माफ़ करें, मुझे कुछ तकनीकी समस्या हो रही है। कृपया थोड़ी देर बाद कोशिश करें। 🙏\n\n{Config.POWERED_BY}",
            "ur": f"معذرت، مجھے کچھ تکنیکی مسئلہ ہو رہا ہے۔ براہ کرم تھوڑی دیر بعد کوشش کریں۔ 🙏\n\n{Config.POWERED_BY}",
            "bn": f"দুঃখিত, আমার কিছু প্রযুক্তিগত সমস্যা হচ্ছে। অনুগ্রহ করে একটু পরে চেষ্টা করুন। 🙏\n\n{Config.POWERED_BY}",
            "mr": f"माफ करा, मला काही तांत्रिक समस्या येत आहे. कृपया थोड्या वेळाने प्रयत्न करा. 🙏\n\n{Config.POWERED_BY}",
            "te": f"క్షమించండి, నాకు కొన్ని సాంకేతిక సమస్యలు వస్తున్నాయి. దయచేసి కొద్దిసేపు తర్వాత ప్రయత్నించండి. 🙏\n\n{Config.POWERED_BY}",
            "ta": f"மன்னிக்கவும், எனக்கு சில தொழில்நுட்ப சிக்கல்கள் உள்ளன. தயவுசெய்து சிறிது நேரம் கழித்து முயற்சிக்கவும். 🙏\n\n{Config.POWERED_BY}",
            "gu": f"માફ કરશો, મને કેટલીક તકનીકી સમસ્યા આવી રહી છે. કૃપા કરીને થોડી વાર પછી પ્રયાસ કરો. 🙏\n\n{Config.POWERED_BY}",
            "kn": f"ಕ್ಷಮಿಸಿ, ನನಗೆ ಕೆಲವು ತಾಂತ್ರಿಕ ಸಮಸ್ಯೆಗಳು ಬರುತ್ತಿವೆ. ದಯವಿಟ್ಟು ಸ್ವಲ್ಪ ಸಮಯದ ನಂತರ ಪ್ರಯತ್ನಿಸಿ. 🙏\n\n{Config.POWERED_BY}",
            "or": f"କ୍ଷମା କରନ୍ତୁ, ମୋର କିଛି ଯାନ୍ତ୍ରିକ ସମସ୍ୟା ହେଉଛି। ଦୟାକରି ଟିକିଏ ପରେ ଚେଷ୍ଟା କରନ୍ତୁ। 🙏\n\n{Config.POWERED_BY}",
            "pa": f"ਮਾਫ਼ ਕਰੋ, ਮੈਨੂੰ ਕੁਝ ਤਕਨੀਕੀ ਸਮੱਸਿਆ ਆ ਰਹੀ ਹੈ। ਕਿਰਪਾ ਕਰਕੇ ਥੋੜ੍ਹੀ ਦੇਰ ਬਾਅਦ ਕੋਸ਼ਿਸ਼ ਕਰੋ। 🙏\n\n{Config.POWERED_BY}",
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