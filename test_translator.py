from src.translators.translator import SchemeTranslator
from pathlib import Path

def test_translator():
    # Initialize translator
    translator = SchemeTranslator()
    
    # Set up input and output paths
    input_file = Path('data/processed_pdfs/processed_schemes.json')
    output_dir = Path('data/translated_schemes')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Translate schemes
    translator.translate_all_schemes(input_file, output_dir)

if __name__ == "__main__":
    test_translator() 