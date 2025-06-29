# 🤖 Premium ChatGPT-like Telegram Bot

**Developer**: G A RAZA  
**Version**: 2.0.0  
**Description**: An advanced AI-powered Telegram bot that mimics ChatGPT functionality with multilingual support, context awareness, and premium UI/UX.

## ✨ Features

### 🧠 Advanced AI Capabilities
- **ChatGPT-like Intelligence**: Powered by OpenAI's GPT models
- **Context Awareness**: Remembers conversation history
- **Natural Conversations**: Human-like responses and interactions
- **Smart Response Formatting**: Automatic emoji integration and text formatting

### 🌍 Multilingual Support
- **Auto Language Detection**: Automatically detects user's language
- **50+ Languages Supported**: Including Hindi, Urdu, Arabic, Bengali, Tamil, Telugu, and more
- **Native Script Support**: Proper rendering of Devanagari, Arabic, and other scripts
- **Cultural Sensitivity**: Responses adapted to cultural context

### 🎨 Premium UI/UX
- **Modern Interface**: Clean, intuitive design with inline keyboards
- **Typing Animations**: Realistic typing indicators
- **Smart Message Splitting**: Long responses split intelligently
- **Visual Feedback**: Emojis and status indicators
- **Responsive Design**: Works perfectly on all devices

### 📊 Advanced Features
- **PDF Export**: Export conversations as formatted PDFs
- **Chat Statistics**: Track conversation metrics
- **Session Management**: Start fresh conversations anytime
- **Admin Controls**: Special features for administrators
- **Comprehensive Logging**: Detailed interaction logs

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Docker & Docker Compose
- Telegram Bot Token (from @BotFather)
- OpenAI API Key

### Installation

1. **Clone the repository**
```bash
git clone <repository-url>
cd premium-ai-telegram-bot
```

2. **Set up environment variables**
```bash
cp .env.example .env
# Edit .env with your actual values
```

3. **Using Docker (Recommended)**
```bash
docker-compose up -d
```

4. **Or run locally**
```bash
pip install -r requirements.txt
python main.py
```

## ⚙️ Configuration

### Environment Variables
```env
TELEGRAM_BOT_TOKEN=your_bot_token_here
OPENAI_API_KEY=your_openai_api_key_here
BOT_USERNAME=your_bot_username
ADMIN_USER_ID=your_telegram_user_id
```

### Bot Settings
- **Model**: GPT-3.5-turbo (configurable)
- **Max Tokens**: 4000
- **Temperature**: 0.7
- **Context Length**: 20 messages

## 🎯 Usage

### Basic Commands
- **Start chatting**: Just send any message
- **/start**: Initialize the bot and see welcome message
- **/new**: Start a fresh conversation
- **/export**: Download chat history as PDF

### Interactive Features
- **Smart Responses**: Bot understands context and provides relevant answers
- **Language Switching**: Automatically adapts to your language
- **Conversation Memory**: Remembers previous messages in the session
- **Rich Formatting**: Supports markdown, emojis, and structured responses

## 🏗️ Architecture

### Core Components
- **AI Service**: OpenAI integration with conversation management
- **Language Detector**: Advanced multilingual detection and localization
- **Handlers**: Telegram bot event handlers
- **Utils**: PDF generation, logging, and utility functions
- **Config**: Centralized configuration management

### File Structure
```
├── main.py              # Application entry point
├── config.py            # Configuration settings
├── ai_service.py        # OpenAI integration
├── language_detector.py # Language detection & localization
├── handlers.py          # Telegram bot handlers
├── utils.py             # Utility functions
├── requirements.txt     # Python dependencies
├── Dockerfile          # Docker configuration
├── docker-compose.yml  # Docker Compose setup
└── README.md           # Documentation
```

## 🔧 Advanced Configuration

### AI Model Settings
```python
# In config.py
DEFAULT_MODEL = "gpt-3.5-turbo"  # or "gpt-4"
MAX_TOKENS = 4000
TEMPERATURE = 0.7
```

### Language Support
The bot automatically detects and supports:
- **South Asian**: Hindi, Urdu, Bengali, Tamil, Telugu, Gujarati
- **Middle Eastern**: Arabic, Persian, Hebrew
- **European**: English, Spanish, French, German, Italian, Russian
- **East Asian**: Chinese, Japanese, Korean
- **And many more...**

### PDF Export Features
- **Formatted Output**: Professional PDF layout
- **Conversation History**: Complete chat export
- **Multilingual Support**: Proper font rendering for all languages
- **Automatic Cleanup**: Temporary files managed automatically

## 📊 Monitoring & Logging

### Log Files
- `logs/bot.log`: General bot operations
- `logs/interactions_YYYYMM.log`: User interaction logs

### Health Checks
- Docker health checks included
- API connectivity monitoring
- Automatic restart on failure

## 🔒 Security Features

- **Environment Variables**: Sensitive data protected
- **Input Validation**: All user inputs validated
- **Rate Limiting**: Built-in protection against spam
- **Admin Controls**: Special privileges for administrators
- **Secure Logging**: No sensitive data in logs

## 🚀 Deployment

### Local Development
```bash
python main.py
```

### Docker Deployment
```bash
docker-compose up -d
```

### Cloud Deployment
- **AWS ECS**: Use provided Docker configuration
- **Google Cloud Run**: Deploy with Docker
- **Azure Container Instances**: Direct Docker deployment
- **Heroku**: Use Docker stack

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🆘 Support

For support and questions:
- Create an issue on GitHub
- Contact: G A RAZA

## 🔄 Updates & Changelog

### Version 2.0.0
- Complete rewrite with modern architecture
- Advanced AI integration with OpenAI
- Multilingual support with auto-detection
- Premium UI/UX with typing animations
- PDF export functionality
- Comprehensive logging and monitoring
- Docker containerization
- Context-aware conversations

---

**Made with ❤️ by G A RAZA**

*This bot represents the future of AI-powered communication on Telegram, combining cutting-edge AI technology with exceptional user experience.*