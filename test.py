from src.utils.logger import setup_logger
import os
import spacy
from pathlib import Path

def create_project_structure():
    # Define all required directories
    directories = [
        "data/raw_pdfs",
        "data/processed_pdfs",
        "logs",
        "src/scrapers",
        "src/utils"
    ]
    
    # Create each directory
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)

def test_setup():
    # Create project structure first
    create_project_structure()
    
    # Test logger
    logger = setup_logger("test")
    logger.info("Testing setup components...")

    # Test if directories exist
    directories = [
        "data/raw_pdfs",
        "data/processed_pdfs",
        "logs",
        "src/scrapers",
        "src/utils"
    ]
    
    for directory in directories:
        if os.path.exists(directory):
            logger.info(f"✓ Directory exists: {directory}")
        else:
            logger.error(f"✗ Directory missing: {directory}")

    # Test spaCy
    try:
        nlp = spacy.load("en_core_web_sm")
        logger.info("✓ spaCy model loaded successfully")
    except Exception as e:
        logger.error(f"✗ Error loading spaCy model: {str(e)}")

    logger.info("Setup verification completed!")

if __name__ == "__main__":
    test_setup() 