from googletrans import Translator
from src.utils.logger import setup_logger
import json
from pathlib import Path
import time

class SchemeTranslator:
    def __init__(self):
        self.logger = setup_logger("translator")
        self.translator = Translator()
        self.fields_to_translate = [
            'scheme_name',
            'description',
            'eligibility',
            'benefits',
            'application_process',
            'deadline',
            'category'
        ]
        
    def translate_text(self, text, target_lang):
        """Translate text with retry mechanism and rate limiting"""
        if not text:
            return text
            
        max_retries = 3
        for attempt in range(max_retries):
            try:
                # Add delay to avoid rate limiting
                time.sleep(1)
                translation = self.translator.translate(text, dest=target_lang)
                return translation.text
            except Exception as e:
                self.logger.error(f"Translation attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_retries - 1:
                    return text  # Return original text if translation fails
                time.sleep(2 ** attempt)  # Exponential backoff
    
    def translate_scheme(self, scheme_data, target_lang):
        """Translate a single scheme's data"""
        translated_scheme = scheme_data.copy()
        
        for field in self.fields_to_translate:
            if translated_scheme.get(field):
                translated_scheme[field] = self.translate_text(
                    translated_scheme[field], 
                    target_lang
                )
                
        return translated_scheme
    
    def translate_all_schemes(self, input_file, output_dir):
        """Translate all schemes to multiple languages"""
        # Load original JSON data
        with open(input_file, 'r', encoding='utf-8') as f:
            schemes_data = json.load(f)
            
        # Target languages
        languages = {
            'hi': 'hindi',
            'mr': 'marathi'
        }
        
        # Translate to each language
        for lang_code, lang_name in languages.items():
            self.logger.info(f"Translating schemes to {lang_name}")
            translated_schemes = {}
            
            for level, schemes in schemes_data.items():
                translated_schemes[level] = {}
                for scheme_id, scheme in schemes.items():
                    translated_schemes[level][scheme_id] = self.translate_scheme(
                        scheme, 
                        lang_code
                    )
            
            # Save translated data
            output_file = output_dir / f'processed_schemes_{lang_name}.json'
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(translated_schemes, f, indent=4, ensure_ascii=False)
                
            self.logger.info(f"Saved {lang_name} translations to {output_file}") 