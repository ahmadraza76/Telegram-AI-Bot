# AI-Powered Telegram Bot
**Developer**: G A RAZA  
**Description**: A Telegram bot with AI Humanizer, SEO article generation, grammar checker, writing assistant, PDF download, featuring bilingual support (English/Hindi). Built with Python, Dockerized, and enhanced with pink glass buttons, typing animation, and image integration for a premium UI/UX.

## Features
- **AI Humanizer**: Converts AI-generated text to human-like text in English or Hindi.
- **SEO-Optimized Article**: Generates articles with keyword optimization.
- **Grammar Check**: Detects grammar issues (English-only).
- **Writing Assistant**: Provides suggestions for text improvement.
- **PDF Download**: Downloads content as a PDF.
- **Bilingual Support**: Responds in the user's input language (English or Hindi).
- **Interactive Menu**: Inline keyboard with pink glass buttons (✨💗💗).
- **Typing Animation**: Shows a typing effect before responding.
- **Image Integration**: Includes images in responses for a visually rich experience.

## Setup
1. **Install Docker**:
   - Follow [Docker's installation guide](https://docs.docker.com/get-docker/) for your OS.
2. **Create a Telegram Bot**:
   - Contact `@BotFather` on Telegram, send `/newbot`, and get your token.
   - Set bot description: "AI-Powered Bot with Humanizer, SEO Articles, Grammar Checker, and Writing Assistant. Developed by G A RAZA."
3. **Configure Environment**:
   - Create a `.env` file:
     ```
     TELEGRAM_TOKEN=YOUR_BOT_TOKEN_HERE
     AI_API_KEY=YOUR_AI_API_KEY
     ```
4. **Build and Run**:
   - Run: `docker-compose up --build -d`
5. **Test Commands**:
   - Use `/start` or `/menu` to access the menu with images and buttons.
   - Try `/humanize नमस्ते, यह एक टेक्स्ट है` (Hindi) or `/humanize Hello, this is a test` (English).
   - Download PDF with `/download`.

## Docker Deployment
- **Local**:
  - Run `docker-compose up -d`.
  - Logs: `docker-compose logs`.
- **Cloud** (AWS, Azure):
  - Push to Docker Hub:
    ```bash
    docker build -t ahmadraza76/ahmad-ai-bot .
    docker push ahmadraza76/ahmad-ai-bot
    ```
  - Deploy on Azure Container Instances, setting `TELEGRAM_TOKEN` and `AI_API_KEY`.

## Commands
- `/start`: Show welcome message with image.
- `/help`: Display commands with image.
- `/humanize <text>`: Humanize text with image.
- `/seoarticle <topic>`: Generate SEO article with image.
- `/grammar <text>`: Check grammar with image.
- `/assist <text>`: Writing suggestions with image.
- `/menu`: Interactive menu with image and buttons.
- `/download`: Download PDF with image.

## License
MIT License. See [LICENSE](LICENSE).

## Notes
- **AI API**: Replace placeholder in `ai_integration.py` with a real AI API (e.g., OpenAI).
- **PDF**: Uses LaTeX in Docker image.
- **Grammar**: English-only (TextBlob limitation).
- **Security**: Keep `.env` secure.
- **UI/UX**: Images, pink glass buttons (✨💗💗), and typing animation.

## Developer
Created by **G A RAZA** for xAI.
