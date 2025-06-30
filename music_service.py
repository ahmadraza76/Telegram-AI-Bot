# music_service.py
# Developer: Mr @Mrnick66
# Music download and processing service for USTAAD-AI

import os
import re
import asyncio
import logging
import yt_dlp
import requests
from typing import Optional, Dict, Tuple
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, TIT2, TPE1, TALB
from youtubesearchpython import VideosSearch
from config import Config

logger = logging.getLogger(__name__)

class MusicService:
    def __init__(self):
        self.download_dir = os.path.join(Config.TEMP_DIR, "music")
        os.makedirs(self.download_dir, exist_ok=True)
        
        # yt-dlp options for audio-only download
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(self.download_dir, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
            'quiet': True,
            'no_warnings': True,
            'extractflat': False,
        }
    
    def is_music_request(self, text: str) -> bool:
        """Check if the text is likely a music request"""
        # Common music-related keywords
        music_keywords = [
            # Hindi songs
            'kesariya', 'tum hi ho', 'kabira', 'raabta', 'tera ban jaunga',
            'perfect', 'shape of you', 'despacito', 'closer', 'faded',
            'believer', 'thunder', 'radioactive', 'demons', 'counting stars',
            # Hindi keywords
            'गाना', 'song', 'music', 'गीत', 'संगीत', 'बजाओ', 'सुनाओ',
            # Urdu keywords  
            'گانا', 'موسیقی', 'گیت', 'بجاؤ', 'سناؤ',
            # Common song patterns
            'play', 'bajao', 'sunao', 'music', 'song', 'gana', 'geet'
        ]
        
        text_lower = text.lower()
        
        # Check for music keywords
        if any(keyword in text_lower for keyword in music_keywords):
            return True
        
        # Check if it's a short text that could be a song name (3-50 characters)
        if 3 <= len(text.strip()) <= 50:
            # Exclude common conversational phrases
            exclude_phrases = [
                'hello', 'hi', 'how are you', 'what', 'why', 'when', 'where',
                'thanks', 'thank you', 'ok', 'okay', 'yes', 'no', 'help',
                'हैलो', 'हाय', 'कैसे हो', 'क्या', 'क्यों', 'कब', 'कहाँ',
                'धन्यवाद', 'ठीक है', 'हाँ', 'नहीं', 'मदद'
            ]
            
            if not any(phrase in text_lower for phrase in exclude_phrases):
                # If it doesn't contain common question words, might be a song
                question_words = ['what', 'how', 'why', 'when', 'where', 'who', 'which']
                if not any(word in text_lower for word in question_words):
                    return True
        
        return False
    
    async def search_youtube(self, query: str) -> Optional[Dict]:
        """Search for music on YouTube"""
        try:
            # Add "song" to query for better music results
            search_query = f"{query} song"
            
            videos_search = VideosSearch(search_query, limit=1)
            results = videos_search.result()
            
            if results['result']:
                video = results['result'][0]
                return {
                    'title': video['title'],
                    'url': video['link'],
                    'thumbnail': video['thumbnails'][0]['url'] if video['thumbnails'] else None,
                    'duration': video.get('duration', 'Unknown'),
                    'channel': video.get('channel', {}).get('name', 'Unknown')
                }
            
            return None
            
        except Exception as e:
            logger.error(f"YouTube search error: {e}")
            return None
    
    async def download_audio(self, video_info: Dict) -> Optional[str]:
        """Download audio from YouTube video"""
        try:
            # Clean filename
            safe_title = re.sub(r'[^\w\s-]', '', video_info['title'])
            safe_title = re.sub(r'[-\s]+', '-', safe_title)
            
            # Update output template with safe title
            self.ydl_opts['outtmpl'] = os.path.join(
                self.download_dir, 
                f"{safe_title}.%(ext)s"
            )
            
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                # Download the audio
                await asyncio.to_thread(ydl.download, [video_info['url']])
                
                # Find the downloaded file
                mp3_file = os.path.join(self.download_dir, f"{safe_title}.mp3")
                
                if os.path.exists(mp3_file):
                    # Add metadata and thumbnail
                    await self.add_metadata(mp3_file, video_info)
                    return mp3_file
                
                return None
                
        except Exception as e:
            logger.error(f"Download error: {e}")
            return None
    
    async def add_metadata(self, audio_file: str, video_info: Dict):
        """Add metadata and thumbnail to audio file"""
        try:
            # Download thumbnail
            thumbnail_data = None
            if video_info.get('thumbnail'):
                try:
                    response = requests.get(video_info['thumbnail'], timeout=10)
                    if response.status_code == 200:
                        thumbnail_data = response.content
                except Exception as e:
                    logger.error(f"Thumbnail download error: {e}")
            
            # Add metadata
            audio = MP3(audio_file, ID3=ID3)
            
            # Add ID3 tags
            audio.tags.add(TIT2(encoding=3, text=video_info['title']))
            audio.tags.add(TPE1(encoding=3, text=video_info.get('channel', 'Unknown Artist')))
            audio.tags.add(TALB(encoding=3, text='Downloaded from YouTube'))
            
            # Add thumbnail as album art
            if thumbnail_data:
                audio.tags.add(APIC(
                    encoding=3,
                    mime='image/jpeg',
                    type=3,  # Cover (front)
                    desc='Cover',
                    data=thumbnail_data
                ))
            
            audio.save()
            
        except Exception as e:
            logger.error(f"Metadata error: {e}")
    
    async def process_music_request(self, query: str) -> Optional[Tuple[str, Dict]]:
        """Process music request and return audio file path and info"""
        try:
            logger.info(f"Processing music request: {query}")
            
            # Search for the song
            video_info = await self.search_youtube(query)
            if not video_info:
                return None
            
            logger.info(f"Found video: {video_info['title']}")
            
            # Download audio
            audio_file = await self.download_audio(video_info)
            if not audio_file:
                return None
            
            logger.info(f"Downloaded audio: {audio_file}")
            
            return audio_file, video_info
            
        except Exception as e:
            logger.error(f"Music processing error: {e}")
            return None
    
    def cleanup_old_files(self):
        """Clean up old downloaded files"""
        try:
            import time
            current_time = time.time()
            
            for filename in os.listdir(self.download_dir):
                file_path = os.path.join(self.download_dir, filename)
                if os.path.isfile(file_path):
                    # Delete files older than 1 hour
                    if current_time - os.path.getctime(file_path) > 3600:
                        os.remove(file_path)
                        logger.info(f"Cleaned up old file: {filename}")
                        
        except Exception as e:
            logger.error(f"Cleanup error: {e}")