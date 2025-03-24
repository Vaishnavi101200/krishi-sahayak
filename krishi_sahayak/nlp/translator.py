from typing import Dict, List, Any, Union
import logging
from googletrans import Translator as GoogleTranslator
import requests
import os
from dotenv import load_dotenv
import json

class Translator:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        load_dotenv()
        
        # Initialize Google Translator as fallback
        self.google_translator = GoogleTranslator()
        
        # Initialize IndicTrans API key
        self.indic_api_key = os.getenv('INDIC_TRANS_API_KEY')
        self.indic_api_url = os.getenv('INDIC_TRANS_API_URL')
    
    def translate_text(self, text: str, target_language: str) -> str:
        """
        Translate text to target language using IndicTrans or fallback to Google Translate.
        """
        try:
            if target_language in ['hi', 'mr'] and self.indic_api_key:
                return self._translate_indic(text, target_language)
            else:
                return self._translate_google(text, target_language)
        except Exception as e:
            self.logger.error(f"Translation error: {e}")
            return text  # Return original text on error
    
    def translate_schemes(self, schemes: List[Dict[str, Any]], target_language: str) -> str:
        """
        Translate scheme information to target language and format for WhatsApp.
        """
        try:
            translated_text = ["📱 Available Schemes:"]
            
            for scheme in schemes:
                # Translate scheme name
                name = self.translate_text(scheme['name'], target_language)
                translated_text.append(f"\n🌾 {name}")
                
                # Translate and add key information
                if 'summary' in scheme:
                    summary = self.translate_text(scheme['summary'], target_language)
                    translated_text.append(summary)
                
                if 'deadline' in scheme:
                    deadline = self.translate_text(f"Deadline: {scheme['deadline']}", target_language)
                    translated_text.append(deadline)
                
                if 'benefits' in scheme:
                    benefits = self.translate_text(f"Benefits: {scheme['benefits']}", target_language)
                    translated_text.append(benefits)
                
                translated_text.append("---")
            
            return "\n".join(translated_text)
        except Exception as e:
            self.logger.error(f"Error translating schemes: {e}")
            return "Sorry, translation service is temporarily unavailable."
    
    def _translate_indic(self, text: str, target_language: str) -> str:
        """
        Translate text using IndicTrans API.
        """
        try:
            headers = {
                'Content-Type': 'application/json',
                'Authorization': f'Bearer {self.indic_api_key}'
            }
            
            payload = {
                'text': text,
                'source_language': 'en',
                'target_language': target_language
            }
            
            response = requests.post(
                self.indic_api_url,
                headers=headers,
                json=payload
            )
            
            if response.status_code == 200:
                return response.json()['translated_text']
            else:
                self.logger.warning(f"IndicTrans API error: {response.text}")
                return self._translate_google(text, target_language)
                
        except Exception as e:
            self.logger.error(f"IndicTrans translation error: {e}")
            return self._translate_google(text, target_language)
    
    def _translate_google(self, text: str, target_language: str) -> str:
        """
        Translate text using Google Translate API.
        """
        try:
            # Map language codes
            lang_map = {
                'hi': 'hi',
                'mr': 'mr',
                'en': 'en'
            }
            target = lang_map.get(target_language, 'en')
            
            translation = self.google_translator.translate(
                text,
                dest=target
            )
            return translation.text
            
        except Exception as e:
            self.logger.error(f"Google translation error: {e}")
            return text  # Return original text on error
    
    def detect_language(self, text: str) -> str:
        """
        Detect the language of input text.
        """
        try:
            detection = self.google_translator.detect(text)
            return detection.lang
        except Exception as e:
            self.logger.error(f"Language detection error: {e}")
            return 'en'  # Default to English on error 