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
from youtubesearchpython import VideosSearch
from config import Config

logger = logging.getLogger(__name__)

class MusicService:
    def __init__(self):
        self.download_dir = os.path.join(Config.TEMP_DIR, "music")
        os.makedirs(self.download_dir, exist_ok=True)
        logger.info(f"Music service initialized with directory: {self.download_dir}")
        
        # yt-dlp options for audio-only download
        self.ydl_opts = {
            'format': 'bestaudio/best',
            'outtmpl': os.path.join(self.download_dir, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '128',  # Lower quality for faster download
            }],
            'quiet': False,  # Enable logs for debugging
            'no_warnings': False,
            'extractflat': False,
            'ignoreerrors': True,
        }
    
    def is_music_request(self, text: str) -> bool:
        """Check if the text is likely a music request"""
        if not text or len(text.strip()) < 2:
            logger.debug(f"Text too short: '{text}'")
            return False
            
        text_lower = text.lower().strip()
        logger.debug(f"Checking music request for: '{text_lower}'")
        
        # Popular Hindi/English songs - EXPANDED LIST
        popular_songs = [
            # Hindi Popular Songs
            'kesariya', 'tum hi ho', 'kabira', 'raabta', 'tera ban jaunga',
            'apna bana le', 'mann mera', 'kalank', 'bekhayali', 've maahi',
            'dilbar', 'naah', 'lahore', 'high rated gabru', 'suit suit',
            'kar gayi chull', 'kala chashma', 'tera ban jaunga', 'pachtaoge',
            'filhaal', 'qismat', 'titliaan', 'kya baat ay', 'leja re',
            
            # English Popular Songs
            'perfect', 'shape of you', 'despacito', 'closer', 'faded',
            'believer', 'thunder', 'radioactive', 'demons', 'counting stars',
            'sunflower', 'blinding lights', 'watermelon sugar', 'levitating',
            'bad guy', 'someone you loved', 'memories', 'circles', 'roxanne',
            'stay', 'good 4 u', 'drivers license', 'positions', 'willow',
            'heat waves', 'industry baby', 'stay', 'ghost', 'shivers'
        ]
        
        # Music keywords in different languages
        music_keywords = [
            # Hindi
            'गाना', 'गीत', 'संगीत', 'बजाओ', 'सुनाओ', 'song', 'music', 'bajao', 'sunao',
            # Urdu  
            'گانا', 'موسیقی', 'گیت', 'بجاؤ', 'سناؤ',
            # English
            'play', 'song', 'music', 'audio', 'track', 'tune', 'download'
        ]
        
        # Check for popular songs FIRST
        for song in popular_songs:
            if song in text_lower:
                logger.info(f"✅ Popular song detected: '{text}' matches '{song}'")
                return True
        
        # Check for music keywords
        for keyword in music_keywords:
            if keyword in text_lower:
                logger.info(f"✅ Music keyword detected: '{text}' contains '{keyword}'")
                return True
        
        # Check if it's a potential song name (3-50 characters, no question words)
        if 3 <= len(text.strip()) <= 50:
            # Exclude common conversational phrases
            exclude_phrases = [
                'hello', 'hi', 'how are you', 'what', 'why', 'when', 'where',
                'thanks', 'thank you', 'ok', 'okay', 'yes', 'no', 'help',
                'हैलो', 'हाय', 'कैसे हो', 'क्या', 'क्यों', 'कब', 'कहाँ',
                'धन्यवाद', 'ठीक है', 'हाँ', 'नहीं', 'मदद', 'who are you',
                'your name', 'what is your name', 'तुम्हारा नाम', 'आप कौन हैं',
                'how to', 'tell me', 'explain', 'what is', 'who is'
            ]
            
            # Check if it's not a common phrase
            is_excluded = any(phrase in text_lower for phrase in exclude_phrases)
            if not is_excluded:
                # Check if it doesn't contain question words
                question_words = ['what', 'how', 'why', 'when', 'where', 'who', 'which', 'क्या', 'कैसे', 'क्यों', 'कब', 'कहाँ', 'कौन']
                has_question = any(word in text_lower for word in question_words)
                if not has_question:
                    logger.info(f"✅ Potential song name detected: '{text}'")
                    return True
                else:
                    logger.debug(f"❌ Contains question word: '{text}'")
            else:
                logger.debug(f"❌ Excluded phrase: '{text}'")
        else:
            logger.debug(f"❌ Length not suitable: '{text}' (length: {len(text.strip())})")
        
        logger.debug(f"❌ Not a music request: '{text}'")
        return False
    
    async def search_youtube(self, query: str) -> Optional[Dict]:
        """Search for music on YouTube"""
        try:
            # Add "song" to query for better music results
            search_query = f"{query} song"
            logger.info(f"🔍 Searching YouTube for: '{search_query}'")
            
            videos_search = VideosSearch(search_query, limit=5)  # Get more results
            results = videos_search.result()
            
            if results and results.get('result'):
                # Filter for music videos (prefer shorter videos, music channels)
                videos = results['result']
                
                # Sort by relevance (prefer videos with "song", "music", "official" in title)
                def score_video(video):
                    title = video.get('title', '').lower()
                    score = 0
                    if 'song' in title: score += 3
                    if 'music' in title: score += 2
                    if 'official' in title: score += 2
                    if 'video' in title: score += 1
                    return score
                
                videos.sort(key=score_video, reverse=True)
                video = videos[0]
                
                video_info = {
                    'title': video.get('title', 'Unknown Title'),
                    'url': video.get('link', ''),
                    'thumbnail': video.get('thumbnails', [{}])[0].get('url', '') if video.get('thumbnails') else '',
                    'duration': video.get('duration', 'Unknown'),
                    'channel': video.get('channel', {}).get('name', 'Unknown') if video.get('channel') else 'Unknown'
                }
                
                logger.info(f"✅ Found video: '{video_info['title']}' by {video_info['channel']}")
                return video_info
            
            logger.warning(f"❌ No results found for: '{query}'")
            return None
            
        except Exception as e:
            logger.error(f"❌ YouTube search error: {e}")
            return None
    
    async def download_audio(self, video_info: Dict) -> Optional[str]:
        """Download audio from YouTube video"""
        try:
            logger.info(f"⬇️ Starting download for: '{video_info['title']}'")
            
            # Clean filename
            safe_title = re.sub(r'[^\w\s-]', '', video_info['title'])
            safe_title = re.sub(r'[-\s]+', '-', safe_title)[:50]  # Limit length
            safe_title = safe_title.strip('-')
            
            if not safe_title:
                safe_title = "downloaded_song"
            
            # Update output template with safe title
            output_path = os.path.join(self.download_dir, f"{safe_title}.%(ext)s")
            self.ydl_opts['outtmpl'] = output_path
            
            logger.info(f"📁 Output path: {output_path}")
            
            with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                # Download the audio
                logger.info(f"🎵 Downloading from: {video_info['url']}")
                await asyncio.to_thread(ydl.download, [video_info['url']])
                
                # Find the downloaded file
                mp3_file = os.path.join(self.download_dir, f"{safe_title}.mp3")
                
                if os.path.exists(mp3_file):
                    logger.info(f"✅ Successfully downloaded: {mp3_file}")
                    return mp3_file
                else:
                    # Try to find any mp3 file in the directory (fallback)
                    logger.info("🔍 Searching for downloaded file...")
                    for file in os.listdir(self.download_dir):
                        if file.endswith('.mp3'):
                            full_path = os.path.join(self.download_dir, file)
                            logger.info(f"✅ Found downloaded file: {full_path}")
                            return full_path
                
                logger.error(f"❌ Downloaded file not found: {mp3_file}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Download error: {e}")
            return None
    
    async def process_music_request(self, query: str) -> Optional[Tuple[str, Dict]]:
        """Process music request and return audio file path and info"""
        try:
            logger.info(f"🎵 Processing music request: '{query}'")
            
            # Search for the song
            video_info = await self.search_youtube(query)
            if not video_info:
                logger.error("❌ No video found")
                return None
            
            # Download audio
            audio_file = await self.download_audio(video_info)
            if not audio_file:
                logger.error("❌ Audio download failed")
                return None
            
            logger.info(f"✅ Music processing completed: {audio_file}")
            return audio_file, video_info
            
        except Exception as e:
            logger.error(f"❌ Music processing error: {e}")
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
                        logger.info(f"🗑️ Cleaned up old file: {filename}")
                        
        except Exception as e:
            logger.error(f"❌ Cleanup error: {e}")