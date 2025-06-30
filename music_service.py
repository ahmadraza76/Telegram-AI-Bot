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
        logger.info(f"🎵 Music service initialized with directory: {self.download_dir}")
        
        # yt-dlp options for audio-only download
        self.ydl_opts = {
            'format': 'bestaudio[ext=m4a]/bestaudio/best',
            'outtmpl': os.path.join(self.download_dir, '%(title)s.%(ext)s'),
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '128',
            }],
            'quiet': True,
            'no_warnings': True,
            'extractflat': False,
            'ignoreerrors': False,
            'socket_timeout': 30,
            'retries': 3,
        }
    
    def is_music_request(self, text: str) -> bool:
        """Check if the text is likely a music request"""
        if not text or len(text.strip()) < 2:
            logger.debug(f"Text too short: '{text}'")
            return False
            
        text_lower = text.lower().strip()
        logger.debug(f"🔍 Checking music request for: '{text_lower}'")
        
        # Enhanced popular songs list with better matching
        popular_songs = [
            # Hindi Popular Songs
            'kesariya', 'tum hi ho', 'kabira', 'raabta', 'tera ban jaunga',
            'apna bana le', 'mann mera', 'kalank', 'bekhayali', 've maahi',
            'dilbar', 'naah', 'lahore', 'high rated gabru', 'suit suit',
            'kar gayi chull', 'kala chashma', 'pachtaoge', 'filhaal', 'qismat',
            'titliaan', 'kya baat ay', 'leja re', 'dil ke armaan', 'armaan',
            'salman khan', 'shahrukh khan', 'arijit singh', 'shreya ghoshal',
            'atif aslam', 'rahat fateh ali khan', 'sonu nigam', 'lata mangeshkar',
            
            # English Popular Songs
            'perfect', 'shape of you', 'despacito', 'closer', 'faded',
            'believer', 'thunder', 'radioactive', 'demons', 'counting stars',
            'sunflower', 'blinding lights', 'watermelon sugar', 'levitating',
            'bad guy', 'someone you loved', 'memories', 'circles', 'roxanne',
            'stay', 'good 4 u', 'drivers license', 'positions', 'willow',
            'heat waves', 'industry baby', 'ghost', 'shivers', 'as it was',
            
            # Artist names
            'ed sheeran', 'taylor swift', 'justin bieber', 'ariana grande',
            'billie eilish', 'the weeknd', 'dua lipa', 'post malone'
        ]
        
        # Music keywords in different languages
        music_keywords = [
            # Hindi/Urdu
            'गाना', 'गीत', 'संगीत', 'बजाओ', 'सुनाओ', 'song', 'music', 'bajao', 'sunao',
            'गाना चाहिए', 'music chahiye', 'download karo', 'play karo',
            # Urdu  
            'گانا', 'موسیقی', 'گیت', 'بجاؤ', 'سناؤ', 'ڈاؤن لوڈ',
            # English
            'play', 'song', 'music', 'audio', 'track', 'tune', 'download',
            'listen', 'hear', 'sound', 'mp3', 'singer', 'artist'
        ]
        
        # Check for popular songs/artists FIRST
        for song in popular_songs:
            if song in text_lower:
                logger.info(f"✅ Popular song/artist detected: '{text}' matches '{song}'")
                return True
        
        # Check for music keywords
        for keyword in music_keywords:
            if keyword in text_lower:
                logger.info(f"✅ Music keyword detected: '{text}' contains '{keyword}'")
                return True
        
        # Check if it looks like a song name (improved logic)
        if 3 <= len(text.strip()) <= 60:
            # Exclude common conversational phrases
            exclude_phrases = [
                'hello', 'hi', 'how are you', 'what', 'why', 'when', 'where',
                'thanks', 'thank you', 'ok', 'okay', 'yes', 'no', 'help',
                'हैलो', 'हाय', 'कैसे हो', 'क्या', 'क्यों', 'कब', 'कहाँ',
                'धन्यवाद', 'ठीक है', 'हाँ', 'नहीं', 'मदद', 'who are you',
                'your name', 'what is your name', 'तुम्हारा नाम', 'आप कौन हैं',
                'how to', 'tell me', 'explain', 'what is', 'who is', 'i want',
                'i need', 'can you', 'please', 'मैं चाहता', 'मुझे चाहिए'
            ]
            
            # Check if it's not a common phrase
            is_excluded = any(phrase in text_lower for phrase in exclude_phrases)
            if not is_excluded:
                # Check if it doesn't start with question words
                question_starters = ['what', 'how', 'why', 'when', 'where', 'who', 'which', 'can', 'could', 'would', 'should']
                starts_with_question = any(text_lower.startswith(word) for word in question_starters)
                
                if not starts_with_question:
                    # Additional check: if it contains common song patterns
                    song_patterns = ['ke', 'ka', 'ki', 'se', 'me', 'hai', 'song', 'by', 'from']
                    has_song_pattern = any(pattern in text_lower for pattern in song_patterns)
                    
                    if has_song_pattern or len(text.split()) <= 5:  # Short phrases are likely song names
                        logger.info(f"✅ Potential song name detected: '{text}'")
                        return True
                    else:
                        logger.debug(f"❌ No song pattern found: '{text}'")
                else:
                    logger.debug(f"❌ Starts with question word: '{text}'")
            else:
                logger.debug(f"❌ Excluded phrase: '{text}'")
        else:
            logger.debug(f"❌ Length not suitable: '{text}' (length: {len(text.strip())})")
        
        logger.debug(f"❌ Not a music request: '{text}'")
        return False
    
    async def search_youtube(self, query: str) -> Optional[Dict]:
        """Search for music on YouTube with better search terms"""
        try:
            # Improve search query
            search_queries = [
                f"{query} song",
                f"{query} official video",
                f"{query} audio",
                f"{query} music video",
                query  # Original query as fallback
            ]
            
            for search_query in search_queries:
                logger.info(f"🔍 Searching YouTube for: '{search_query}'")
                
                try:
                    videos_search = VideosSearch(search_query, limit=10)
                    results = videos_search.result()
                    
                    if results and results.get('result'):
                        videos = results['result']
                        
                        # Filter and score videos
                        def score_video(video):
                            title = video.get('title', '').lower()
                            channel = video.get('channel', {}).get('name', '').lower() if video.get('channel') else ''
                            duration = video.get('duration', '')
                            
                            score = 0
                            
                            # Prefer music-related content
                            if 'song' in title: score += 5
                            if 'music' in title: score += 4
                            if 'official' in title: score += 3
                            if 'video' in title: score += 2
                            if 'audio' in title: score += 3
                            
                            # Prefer known music channels
                            music_channels = ['t-series', 'sony music', 'zee music', 'tips music', 'speed records']
                            if any(ch in channel for ch in music_channels): score += 4
                            
                            # Prefer reasonable duration (not too long, not too short)
                            if duration:
                                try:
                                    # Parse duration like "3:45" or "4:12"
                                    if ':' in duration:
                                        parts = duration.split(':')
                                        if len(parts) == 2:
                                            minutes = int(parts[0])
                                            if 2 <= minutes <= 8:  # Typical song length
                                                score += 3
                                except:
                                    pass
                            
                            # Boost if query terms appear in title
                            query_words = query.lower().split()
                            for word in query_words:
                                if word in title:
                                    score += 2
                            
                            return score
                        
                        # Sort by score
                        videos.sort(key=score_video, reverse=True)
                        
                        # Take the best match
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
                        
                except Exception as search_error:
                    logger.error(f"Search attempt failed for '{search_query}': {search_error}")
                    continue
            
            logger.warning(f"❌ No results found for any search variation of: '{query}'")
            return None
            
        except Exception as e:
            logger.error(f"❌ YouTube search error: {e}")
            return None
    
    async def download_audio(self, video_info: Dict) -> Optional[str]:
        """Download audio from YouTube video with better error handling"""
        try:
            logger.info(f"⬇️ Starting download for: '{video_info['title']}'")
            
            # Clean filename more aggressively
            safe_title = re.sub(r'[^\w\s-]', '', video_info['title'])
            safe_title = re.sub(r'[-\s]+', '_', safe_title)[:40]  # Shorter limit
            safe_title = safe_title.strip('_')
            
            if not safe_title:
                safe_title = f"song_{hash(video_info['url']) % 10000}"
            
            # Update output template
            output_path = os.path.join(self.download_dir, f"{safe_title}.%(ext)s")
            self.ydl_opts['outtmpl'] = output_path
            
            logger.info(f"📁 Output path template: {output_path}")
            
            # Try download with timeout
            try:
                with yt_dlp.YoutubeDL(self.ydl_opts) as ydl:
                    logger.info(f"🎵 Downloading from: {video_info['url']}")
                    
                    # Download with timeout
                    download_task = asyncio.to_thread(ydl.download, [video_info['url']])
                    await asyncio.wait_for(download_task, timeout=120)  # 2 minute timeout
                    
                    # Find the downloaded file
                    mp3_file = os.path.join(self.download_dir, f"{safe_title}.mp3")
                    
                    if os.path.exists(mp3_file):
                        logger.info(f"✅ Successfully downloaded: {mp3_file}")
                        return mp3_file
                    else:
                        # Search for any new mp3 file
                        logger.info("🔍 Searching for downloaded file...")
                        for file in os.listdir(self.download_dir):
                            if file.endswith('.mp3') and safe_title in file:
                                full_path = os.path.join(self.download_dir, file)
                                logger.info(f"✅ Found downloaded file: {full_path}")
                                return full_path
                        
                        # Last resort: find any recent mp3 file
                        mp3_files = [f for f in os.listdir(self.download_dir) if f.endswith('.mp3')]
                        if mp3_files:
                            # Get the most recent file
                            latest_file = max(mp3_files, key=lambda f: os.path.getctime(os.path.join(self.download_dir, f)))
                            full_path = os.path.join(self.download_dir, latest_file)
                            logger.info(f"✅ Using latest file: {full_path}")
                            return full_path
                    
                    logger.error(f"❌ Downloaded file not found: {mp3_file}")
                    return None
                    
            except asyncio.TimeoutError:
                logger.error("❌ Download timeout (2 minutes)")
                return None
            except Exception as download_error:
                logger.error(f"❌ Download failed: {download_error}")
                return None
                
        except Exception as e:
            logger.error(f"❌ Download error: {e}")
            return None
    
    async def process_music_request(self, query: str) -> Optional[Tuple[str, Dict]]:
        """Process music request and return audio file path and info"""
        try:
            logger.info(f"🎵 Processing music request: '{query}'")
            
            # Clean up old files first
            self.cleanup_old_files()
            
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
                    # Delete files older than 30 minutes
                    if current_time - os.path.getctime(file_path) > 1800:
                        os.remove(file_path)
                        logger.info(f"🗑️ Cleaned up old file: {filename}")
                        
        except Exception as e:
            logger.error(f"❌ Cleanup error: {e}")