import json
from pathlib import Path
from typing import Dict, List, Optional

class SchemeService:
    def __init__(self):
        self.data_dir = Path('data/translated_schemes')
        self.schemes_data = {}
        self.load_all_data()
        
    def load_all_data(self):
        """Load data for all languages"""
        # Load English data
        eng_file = Path('data/processed_pdfs/processed_schemes.json')
        self.schemes_data['en'] = self.load_json_file(eng_file)
        
        # Load translations with proper language mapping
        lang_mapping = {
            'processed_schemes_hindi.json': 'hi',
            'processed_schemes_marathi.json': 'mr'
        }
        
        # Load translations
        for filename, lang_code in lang_mapping.items():
            file_path = self.data_dir / filename
            if file_path.exists():
                self.schemes_data[lang_code] = self.load_json_file(file_path)
            else:
                print(f"Warning: Translation file {filename} not found")
    
    def load_json_file(self, file_path: Path) -> Dict:
        """Load JSON file"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: File not found: {file_path}")
            return {}
        except json.JSONDecodeError:
            print(f"Warning: Invalid JSON in file: {file_path}")
            return {}
    
    def get_all_schemes(self, lang: str = 'en', level: Optional[str] = None) -> List[Dict]:
        """Get all schemes with optional filtering by level"""
        # Validate language
        if lang not in self.schemes_data:
            raise ValueError(f"Language '{lang}' not supported. Available languages: {list(self.schemes_data.keys())}")
            
        result = []
        data = self.schemes_data[lang]
        
        # Handle empty data
        if not data:
            return []
            
        # Normalize level input
        if level:
            level = level.lower()
            if level not in ['central', 'state']:
                raise ValueError("Level must be either 'central' or 'state'")
        
        # Process schemes
        for scheme_level, schemes in data.items():
            if level and scheme_level != level:
                continue
            for scheme_id, scheme_details in schemes.items():
                result.append({
                    "scheme_id": scheme_id,
                    "details": scheme_details
                })
                
        return result
    
    def get_scheme_by_id(self, scheme_id: str, lang: str = 'en') -> Optional[Dict]:
        """Get specific scheme by ID"""
        # Validate language
        if lang not in self.schemes_data:
            raise ValueError(f"Language '{lang}' not supported. Available languages: {list(self.schemes_data.keys())}")
            
        data = self.schemes_data[lang]
        if not data:
            return None
            
        # Search for scheme in all levels
        for level_schemes in data.values():
            if scheme_id in level_schemes:
                return {
                    "scheme_id": scheme_id,
                    "details": level_schemes[scheme_id]
                }
        return None 