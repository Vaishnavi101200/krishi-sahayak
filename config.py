import os
from pathlib import Path

# Base directory of project
BASE_DIR = Path(__file__).resolve().parent

# Directory for storing PDFs
PDF_DIR = BASE_DIR / 'data' / 'raw_pdfs'

# Create directories if they don't exist
PDF_DIR.mkdir(parents=True, exist_ok=True)

# Base URL for scraping
BASE_URL = "https://agriwelfare.gov.in/en/Major"

# Configure any other constants here 