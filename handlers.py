# handlers.py
# Developer: G A RAZA
# Command, message, and callback handlers for the Telegram bot with image integration, typing animation, and pink glass buttons

from telegram import Update, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup, ChatAction
from telegram.ext import ContextTypes
from ai_integration import humanize_text, generate_seo_article, check_grammar, assist_writing
from utilities import detect_language, generate_pdf, log_interaction
import asyncio
import requests

# Image URL for visual enhancement
IMAGE_URL = "https://graph.org/file/ff596066ce32ae4a5e635-1a9f69e38ad3c19549.jpg"

async def send_image(update: Update):
    """Send the specified image if accessible, with fallback."""
    try:
        # Verify image URL
        response = requests.head(IMAGE_URL, timeout=5)
        if response.status_code == 200:
            await update.message.chat.send_photo(photo=IMAGE_URL)
        else:
            await update.message.reply_text("Image unavailable, proceeding without it. 💗")
    except Exception as e:
        await update.message.reply_text("Image unavailable, proceeding without it. 💗")

async def show_typing(update: Update):
    """Show typing animation before responding."""
    await update.message.chat.send_action(ChatAction.TYPING)
    await asyncio.sleep(1)  # Simulate typing delay

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /start command."""
    await show_typing(update)
    user_id = update.effective_user.id
    lang = detect_language(update.message.text or "Hello")
    await send_image(update)
    keyboard = [
        ["/menu", "/help"],
        ["/humanize", "/seoarticle"],
        ["/grammar", "/assist"],
        ["/download"]
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    if lang == "hi":
        message = (
            "जी ए राजा द्वारा बनाए गए AI-पावर्ड बॉट में आपका स्वागत है! 🤖\n"
            "कमांड्स का उपयोग करके सुविधाओं तक पहुंचें:\n"
            "- /humanize: टेक्स्ट को मानव जैसा बनाएं\n"
            "- /seoarticle: SEO-अनुकूलित लेख बनाएं\n"
            "- /grammar: व्याकरण जांचें\n"
            "- /assist: लेखन सुझाव प्राप्त करें\n"
            "- /menu: इंटरैक्टिव मेनू देखें\n"
            "- /download: PDF के रूप में सामग्री डाउनलोड करें\n"
            "- /help: यह संदेश दिखाएं"
        )
    else:
        message = (
            "Welcome to the AI-Powered Bot by G A RAZA! 🤖\n"
            "Use commands to access features:\n"
            "- /humanize: Make text human-like\n"
            "- /seoarticle: Generate SEO-optimized articles\n"
            "- /grammar: Check grammar\n"
            "- /assist: Get writing suggestions\n"
            "- /menu: View interactive menu\n"
            "- /download: Download content as PDF\n"
            "- /help: Show this message"
        )
    await update.message.reply_text(message, reply_markup=reply_markup)
    log_interaction(user_id, "/start", "Started bot")

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /help command."""
    await show_typing(update)
    user_id = update.effective_user.id
    lang = detect_language(update.message.text or "Hello")
    await send_image(update)
    if lang == "hi":
        message = (
            "AI-पावर्ड बॉट | डेवलपर: जी ए राजा\n\n"
            "उपलब्ध कमांड्स:\n"
            "/humanize - टेक्स्ट को मानव जैसा बनाएं\n"
            "/seoarticle - SEO-अनुकूलित लेख बनाएं\n"
            "/grammar - टेक्स्ट में व्याकरण जांचें\n"
            "/assist - लेखन में सुधार के लिए सुझाव\n"
            "/menu - इंटरैक्टिव मेनू\n"
            "/download - सामग्री को PDF के रूप में डाउनलोड करें\n"
            "/help - यह सहायता संदेश"
        )
    else:
        message = (
            "AI-Powered Bot | Developer: G A RAZA\n\n"
            "Available commands:\n"
            "/humanize - Humanize AI-generated text\n"
            "/seoarticle - Generate an SEO-optimized article\n"
            "/grammar - Check grammar in your text\n"
            "/assist - Get writing suggestions\n"
            "/menu - Interactive menu\n"
            "/download - Download content as PDF\n"
            "/help - Show this help message"
        )
    await update.message.reply_text(message)
    log_interaction(user_id, "/help", "Help requested")

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for the /menu command with pink glass buttons."""
    await show_typing(update)
    user_id = update.effective_user.id
    lang = detect_language(update.message.text or "Hello")
    await send_image(update)
    keyboard = [
        [InlineKeyboardButton("✨💗 Humanize Text" if lang == "en" else "✨💗 टेक्स्ट मानवकृत करें", callback_data="humanize")],
        [InlineKeyboardButton("✨💗 SEO Article" if lang == "en" else "✨💗 SEO लेख", callback_data="seoarticle")],
        [InlineKeyboardButton("✨💗 Grammar Check" if lang == "en" else "✨💗 व्याकरण जांच", callback_data="grammar")],
        [InlineKeyboardButton("✨💗 Writing Assistant" if lang == "en" else "✨💗 लेखन सहायक", callback_data="assist")],
        [InlineKeyboardButton("✨💗 Download PDF" if lang == "en" else "✨💗 PDF डाउनलोड करें", callback_data="download")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    message = "Select a feature: 💗" if lang == "en" else "एक सुविधा चुनें: 💗"
    await update.message.reply_text(message, reply_markup=reply_markup)
    log_interaction(user_id, "/menu", message)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle inline button clicks."""
    query = update.callback_query
    await query.answer()
    await query.message.chat.send_action(ChatAction.TYPING)
    await asyncio.sleep(1)
    lang = detect_language(query.data or "Hello")
    command = query.data
    if command in ["humanize", "seoarticle", "grammar", "assist", "download"]:
        message = {
            "humanize": "Please provide text to humanize. 💗" if lang == "en" else "कृपया टेक्स्ट प्रदान करें जिसे मानवकृत करना है। 💗",
            "seoarticle": "Please provide a topic and keywords. 💗" if lang == "en" else "कृपया विषय और कीवर्ड प्रदान करें। 💗",
            "grammar": "Please provide text to check grammar. 💗" if lang == "en" else "कृपया व्याकरण जांच के लिए टेक्स्ट प्रदान करें। 💗",
            "assist": "Please provide text for writing assistance. 💗" if lang == "en" else "कृपया लेखन सहायता के लिए टेक्स्ट प्रदान करें। 💗",
            "download": "Please provide text to download as PDF. 💗" if lang == "en" else "कृपया PDF के रूप में डाउनलोड करने के लिए टेक्स्ट प्रदान करें। 💗"
        }[command]
        context.user_data["last_command"] = command
        await query.message.reply_text(message)
    log_interaction(update.effective_user.id, f"button_{command}", "Button clicked")

async def humanize(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /humanize command or text messages."""
    await show_typing(update)
    user_id = update.effective_user.id
    text = ' '.join(context.args) if context.args else update.message.text
    lang = detect_language(text or "Hello")
    if not text.startswith('/'):
        await send_image(update)
    if not text or text.startswith('/'):
        message = "Please provide text to humanize. Example: /humanize Your text here 💗" if lang == "en" else "कृपया टेक्स्ट प्रदान करें जिसे मानवकृत करना है। उदाहरण: /humanize_आपका_टेक्स्ट_यहाँ 💗"
        await update.message.reply_text(message)
        return
    humanized_text = humanize_text(text, lang)
    await update.message.reply_text(f"{'Humanized Text' if lang == 'en' else 'मानवकृत टेक्स्ट'}:\n{humanized_text} 💗💗")
    context.user_data["last_output"] = humanized_text
    log_interaction(user_id, "/humanize", text)

async def seo_article(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /seoarticle command."""
    await show_typing(update)
    user_id = update.effective_user.id
    text = ' '.join(context.args)
    lang = detect_language(text or "Hello")
    await send_image(update)
    if not text:
        message = "Please provide a topic and keywords. Example: /seoarticle Topic: AI Bots Keywords: AI, chatbot 💗" if lang == "en" else "कृपया विषय और कीवर्ड प्रदान करें। उदाहरण: /seoarticle_विषय: AI_बॉट्स_कीवर्ड:_AI,_चैटबॉट 💗"
        await update.message.reply_text(message)
        return
    article = generate_seo_article(text, lang)
    await update.message.reply_text(f"{'SEO-Optimized Article' if lang == 'en' else 'SEO अनुकूलित लेख'}:\n{article} 💗💗")
    context.user_data["last_output"] = article
    log_interaction(user_id, "/seoarticle", text)

async def grammar_check(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /grammar command."""
    await show_typing(update)
    user_id = update.effective_user.id
    text = ' '.join(context.args)
    lang = detect_language(text or "Hello")
    await send_image(update)
    if not text:
        message = "Please provide text to check grammar. Example: /grammar Your text here 💗" if lang == "en" else "कृपया व्याकरण जांच के लिए टेक्स्ट प्रदान करें। उदाहरण: /grammar_आपका_टेक्स्ट_यहाँ 💗"
        await update.message.reply_text(message)
        return
    corrections = check_grammar(text)
    await update.message.reply_text(f"{'Grammar Check' if lang == 'en' else 'व्याकरण जांच'}:\n{corrections} 💗💗")
    context.user_data["last_output"] = corrections
    log_interaction(user_id, "/grammar", text)

async def writing_assist(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /assist command."""
    await show_typing(update)
    user_id = update.effective_user.id
    text = ' '.join(context.args)
    lang = detect_language(text or "Hello")
    await send_image(update)
    if not text:
        message = "Please provide text for writing assistance. Example: /assist Your text here 💗" if lang == "en" else "कृपया लेखन सहायता के लिए टेक्स्ट प्रदान करें। उदाहरण: /assist_आपका_टेक्स्ट_यहाँ 💗"
        await update.message.reply_text(message)
        return
    suggestions = assist_writing(text, lang)
    await update.message.reply_text(f"{'Writing Suggestions' if lang == 'en' else 'लेखन सुझाव'}:\n{suggestions} 💗💗")
    context.user_data["last_output"] = suggestions
    log_interaction(user_id, "/assist", text)

async def download(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handler for /download command."""
    await show_typing(update)
    user_id = update.effective_user.id
    lang = detect_language(update.message.text or "Hello")
    await send_image(update)
    if "last_output" not in context.user_data:
        message = "No content available to download. Please use a command like /humanize or /seoarticle first. 💗" if lang == "en" else "डाउनलोड करने के लिए कोई सामग्री उपलब्ध नहीं है। कृपया पहले /humanize या /seoarticle जैसे कमांड करें। 💗"
        await update.message.reply_text(message)
        return
    content = context.user_data["last_output"]
    pdf_path = generate_pdf(content, lang)
    with open(pdf_path, "rb") as f:
        await update.message.reply_document(document=f, filename="output.pdf")
    message = "PDF downloaded successfully! 💗💗" if lang == "en" else "PDF सफलतापूर्वक डाउनलोड हो गया! 💗💗"
    await update.message.reply_text(message)
    log_interaction(user_id, "/download", "PDF downloaded")
