from src.processors.pdf_processor import PDFProcessor
import json
from pathlib import Path
from collections import defaultdict

def test_pdf_processor():
    processor = PDFProcessor()
    processed_data = processor.process_all_pdfs()
    
    # Create output directory if it doesn't exist
    output_dir = Path('data/processed_pdfs')
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Organize schemes by level
    schemes_by_level = defaultdict(list)
    for scheme in processed_data:
        level = scheme.get('scheme_level', 'unspecified')
        schemes_by_level[level].append(scheme)
    
    # Create numbered schemes dictionary organized by level
    organized_schemes = {}
    for level in ['central', 'state', 'unspecified']:
        if schemes_by_level[level]:
            level_schemes = {
                f"{level}_scheme_{str(idx+1).zfill(2)}": scheme
                for idx, scheme in enumerate(schemes_by_level[level])
            }
            organized_schemes[level] = level_schemes
    
    # Save processed data to JSON
    output_file = output_dir / 'processed_schemes.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(organized_schemes, f, indent=4, ensure_ascii=False)
    
    # Print summary of extraction
    print("\nExtraction Summary:")
    print("-" * 50)
    for level, schemes in organized_schemes.items():
        print(f"\n{level.upper()} LEVEL SCHEMES:")
        print("-" * 30)
        for scheme_id, scheme in schemes.items():
            print(f"\n{scheme_id}:")
            print(f"Scheme: {scheme['scheme_name'] or 'Unknown'}")
            for field, value in scheme.items():
                if field not in ['scheme_name', 'scheme_level']:
                    status = "✓" if value else "✗"
                    print(f"{field}: {status}")
    
    # Print total counts
    print("\nScheme Counts:")
    for level, schemes in organized_schemes.items():
        print(f"{level.capitalize()} Level Schemes: {len(schemes)}")
    print(f"Total Schemes: {sum(len(schemes) for schemes in organized_schemes.values())}")
    print(f"\nResults saved to: {output_file}")

if __name__ == "__main__":
    test_pdf_processor() 