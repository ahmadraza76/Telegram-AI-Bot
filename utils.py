# utils.py
# Developer: G A RAZA
# Utility functions for the premium Telegram bot

import os
import logging
import asyncio
from datetime import datetime
from typing import Optional
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from config import Config

logger = logging.getLogger(__name__)

class Utils:
    @staticmethod
    def setup_directories():
        """Create necessary directories"""
        directories = [Config.LOGS_DIR, Config.TEMP_DIR]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
    
    @staticmethod
    def log_user_interaction(user_id: int, username: str, message: str, response_length: int):
        """Log user interactions"""
        try:
            log_file = os.path.join(Config.LOGS_DIR, f"interactions_{datetime.now().strftime('%Y%m')}.log")
            timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            
            with open(log_file, 'a', encoding='utf-8') as f:
                f.write(f"{timestamp} | User: {user_id} (@{username}) | "
                       f"Message: {message[:100]}... | Response Length: {response_length}\n")
        except Exception as e:
            logger.error(f"Failed to log interaction: {e}")
    
    @staticmethod
    def split_long_message(text: str, max_length: int = Config.MAX_MESSAGE_LENGTH) -> list:
        """Split long messages into chunks"""
        if len(text) <= max_length:
            return [text]
        
        chunks = []
        current_chunk = ""
        
        # Split by paragraphs first
        paragraphs = text.split('\n\n')
        
        for paragraph in paragraphs:
            if len(current_chunk + paragraph) <= max_length:
                current_chunk += paragraph + '\n\n'
            else:
                if current_chunk:
                    chunks.append(current_chunk.strip())
                    current_chunk = ""
                
                # If paragraph is too long, split by sentences
                if len(paragraph) > max_length:
                    sentences = paragraph.split('. ')
                    for sentence in sentences:
                        if len(current_chunk + sentence) <= max_length:
                            current_chunk += sentence + '. '
                        else:
                            if current_chunk:
                                chunks.append(current_chunk.strip())
                            current_chunk = sentence + '. '
                else:
                    current_chunk = paragraph + '\n\n'
        
        if current_chunk:
            chunks.append(current_chunk.strip())
        
        return chunks
    
    @staticmethod
    async def generate_pdf(content: str, title: str = "AI Chat Export") -> str:
        """Generate PDF from text content"""
        try:
            filename = f"chat_export_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
            filepath = os.path.join(Config.TEMP_DIR, filename)
            
            # Create PDF
            doc = SimpleDocTemplate(filepath, pagesize=letter)
            styles = getSampleStyleSheet()
            
            # Custom styles
            title_style = ParagraphStyle(
                'CustomTitle',
                parent=styles['Heading1'],
                fontSize=16,
                spaceAfter=30,
                alignment=1  # Center alignment
            )
            
            content_style = ParagraphStyle(
                'CustomContent',
                parent=styles['Normal'],
                fontSize=11,
                spaceAfter=12,
                leftIndent=20,
                rightIndent=20
            )
            
            # Build PDF content
            story = []
            story.append(Paragraph(title, title_style))
            story.append(Spacer(1, 20))
            
            # Split content into paragraphs
            paragraphs = content.split('\n\n')
            for para in paragraphs:
                if para.strip():
                    story.append(Paragraph(para.strip(), content_style))
                    story.append(Spacer(1, 10))
            
            doc.build(story)
            return filepath
            
        except Exception as e:
            logger.error(f"Failed to generate PDF: {e}")
            raise
    
    @staticmethod
    def format_response_with_emojis(text: str, language: str) -> str:
        """Add appropriate emojis based on content and language"""
        # Add thinking emoji for questions
        if '?' in text or 'how' in text.lower() or 'what' in text.lower():
            text = f"{Config.THINKING_EMOJI} {text}"
        
        # Add success emoji for positive responses
        positive_words = {
            'en': ['yes', 'correct', 'right', 'good', 'excellent', 'perfect'],
            'hi': ['हाँ', 'सही', 'अच्छा', 'बेहतरीन', 'परफेक्ट'],
            'ur': ['ہاں', 'صحیح', 'اچھا', 'بہترین', 'پرفیکٹ'],
            'ar': ['نعم', 'صحيح', 'جيد', 'ممتاز', 'مثالي']
        }
        
        words = positive_words.get(language, positive_words['en'])
        if any(word in text.lower() for word in words):
            text = f"{Config.SUCCESS_EMOJI} {text}"
        
        return text
    
    @staticmethod
    async def simulate_typing(chat_id, context, duration: int = Config.TYPING_DELAY):
        """Simulate typing animation"""
        try:
            await context.bot.send_chat_action(chat_id=chat_id, action='typing')
            await asyncio.sleep(duration)
        except Exception as e:
            logger.error(f"Failed to simulate typing: {e}")
    
    @staticmethod
    def get_user_info(update) -> dict:
        """Extract user information from update"""
        user = update.effective_user
        return {
            'id': user.id,
            'username': user.username or 'Unknown',
            'first_name': user.first_name or '',
            'last_name': user.last_name or '',
            'language_code': user.language_code or 'en'
        }
    
    @staticmethod
    def is_admin(user_id: int) -> bool:
        """Check if user is admin"""
        return user_id == Config.ADMIN_USER_ID