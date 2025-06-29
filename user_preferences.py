# user_preferences.py
# Developer: Mr @Mrnick66
# User preferences and language settings for USTAAD-AI

import json
import os
from typing import Dict, Optional
from config import Config

class UserPreferences:
    def __init__(self):
        self.preferences_file = os.path.join(Config.TEMP_DIR, "user_preferences.json")
        self.user_data = self._load_preferences()
    
    def _load_preferences(self) -> Dict:
        """Load user preferences from file"""
        try:
            if os.path.exists(self.preferences_file):
                with open(self.preferences_file, 'r', encoding='utf-8') as f:
                    return json.load(f)
        except Exception:
            pass
        return {}
    
    def _save_preferences(self):
        """Save user preferences to file"""
        try:
            os.makedirs(os.path.dirname(self.preferences_file), exist_ok=True)
            with open(self.preferences_file, 'w', encoding='utf-8') as f:
                json.dump(self.user_data, f, ensure_ascii=False, indent=2)
        except Exception:
            pass
    
    def set_user_language(self, user_id: int, language: str):
        """Set user's preferred language"""
        user_key = str(user_id)
        if user_key not in self.user_data:
            self.user_data[user_key] = {}
        
        self.user_data[user_key]['language'] = language
        self._save_preferences()
    
    def get_user_language(self, user_id: int) -> Optional[str]:
        """Get user's preferred language"""
        user_key = str(user_id)
        return self.user_data.get(user_key, {}).get('language')
    
    def get_user_preferences(self, user_id: int) -> Dict:
        """Get all user preferences"""
        user_key = str(user_id)
        return self.user_data.get(user_key, {})
    
    def set_user_preference(self, user_id: int, key: str, value):
        """Set a specific user preference"""
        user_key = str(user_id)
        if user_key not in self.user_data:
            self.user_data[user_key] = {}
        
        self.user_data[user_key][key] = value
        self._save_preferences()