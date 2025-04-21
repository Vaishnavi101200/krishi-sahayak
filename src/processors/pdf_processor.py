import PyPDF2
import re
from pathlib import Path
from src.utils.logger import setup_logger
from config import PDF_DIR
import spacy

class PDFProcessor:
    def __init__(self):
        self.logger = setup_logger("pdf_processor")
        self.pdf_dir = PDF_DIR
        # Load spaCy model for better text processing
        self.nlp = spacy.load("en_core_web_sm")
        
    def extract_text_from_pdf(self, pdf_path):
        """Extract text from a PDF file with improved cleaning"""
        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text = ""
                
                for page in reader.pages:
                    page_text = page.extract_text()
                    # Basic text cleaning
                    page_text = self.clean_text(page_text)
                    text += page_text + "\n"
                    
                self.logger.info(f"Successfully extracted text from {pdf_path.name}")
                return text
                
        except Exception as e:
            self.logger.error(f"Failed to extract text from {pdf_path.name}: {str(e)}")
            return None

    def clean_text(self, text):
        """Clean extracted text"""
        if not text:
            return ""
            
        # Remove multiple spaces
        text = re.sub(r'\s+', ' ', text)
        # Remove multiple newlines
        text = re.sub(r'\n\s*\n', '\n\n', text)
        # Fix common PDF extraction issues
        text = text.replace('•', '\n•')
        return text.strip()

    def extract_section(self, text, section_patterns, max_words=100):
        """Extract section content using multiple patterns"""
        for pattern in section_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE | re.DOTALL)
            for match in matches:
                content = match.group(1) if len(match.groups()) > 0 else match.group(0)
                # Clean and limit content
                content = re.sub(r'\s+', ' ', content).strip()
                words = content.split()
                if len(words) <= max_words:  # Avoid capturing too much text
                    return content
        return None

    def determine_scheme_level(self, text):
        """Determine if scheme is Central or State level"""
        central_indicators = [
            r'(?i)central(\s+sector)?\s+scheme',
            r'(?i)government\s+of\s+india',
            r'(?i)ministry\s+of',
            r'(?i)pradhan\s+mantri',
            r'(?i)national\s+scheme',
            r'(?i)centrally\s+sponsored',
            r'(?i)PMKSY',  # Add specific scheme abbreviations
            r'(?i)PM-KISAN',
            r'(?i)union government',
            r'(?i)niti aayog',
            r'(?i)department of agriculture',
            r'(?i)ministry of agriculture',
            r'(?i)goi scheme',
            r'(?i)central assistance',
            r'(?i)central government'
        ]
        
        state_indicators = [
            r'(?i)state(\s+sector)?\s+scheme',
            r'(?i)state\s+government',
            r'(?i)mukhya\s+mantri',
            r'(?i)state\s+sponsored',
            r'(?i)state level',
            r'(?i)state department',
            r'(?i)state agriculture department',
            r'(?i)state sponsored scheme'
        ]
        
        # Check for central scheme indicators with confidence score
        central_matches = sum(1 for pattern in central_indicators if re.search(pattern, text))
        state_matches = sum(1 for pattern in state_indicators if re.search(pattern, text))
        
        # Determine level based on matches
        if central_matches > state_matches:
            return "central"
        elif state_matches > central_matches:
            return "state"
        elif central_matches > 0:  # If equal matches but at least one central indicator
            return "central"
        
        return "unspecified"

    def structure_scheme_data(self, text):
        """Structure the extracted text with improved patterns"""
        scheme_data = {
            'scheme_name': None,
            'scheme_level': None,
            'description': None,
            'eligibility': None,
            'benefits': None,
            'application_process': None,
            'deadline': None,
            'source_link': None,
            'category': None
        }
        
        # Enhanced patterns for each field
        patterns = {
            'scheme_name': [
                r'(?i)scheme\s+name[:\s]+(.*?)(?=\n|$)',
                r'(?i)name of (?:the\s+)?scheme[:\s]+(.*?)(?=\n|$)',
                r'^([^.\n]+(?:scheme|yojana|program))[.\n]'
            ],
            'eligibility': [
                r'(?i)eligibility[:\s]+(.*?)(?=\n\n|$)',
                r'(?i)who can apply[?\s:]+(.*?)(?=\n\n|$)',
                r'(?i)eligible[^:\n]*:[:\s]+(.*?)(?=\n\n|$)'
            ],
            'benefits': [
                r'(?i)benefits[:\s]+(.*?)(?=\n\n|$)',
                r'(?i)assistance provided[:\s]+(.*?)(?=\n\n|$)',
                r'(?i)financial assistance[:\s]+(.*?)(?=\n\n|$)'
            ],
            'application_process': [
                r'(?i)(?:how to apply|application process)[:\s]+(.*?)(?=\n\n|$)',
                r'(?i)procedure for application[:\s]+(.*?)(?=\n\n|$)',
                r'(?i)application procedure[:\s]+(.*?)(?=\n\n|$)'
            ],
            'deadline': [
                r'(?i)(?:last date|deadline)[:\s]+(.*?)(?=\n|$)',
                r'(?i)submission deadline[:\s]+(.*?)(?=\n|$)',
                r'(?i)apply before[:\s]+(.*?)(?=\n|$)'
            ],
            'category': [
                r'(?i)category[:\s]+(.*?)(?=\n|$)',
                r'(?i)type of scheme[:\s]+(.*?)(?=\n|$)',
                r'(?i)scheme type[:\s]+(.*?)(?=\n|$)'
            ]
        }
        
        # Extract information using enhanced patterns
        for field, field_patterns in patterns.items():
            content = self.extract_section(text, field_patterns)
            if content:
                scheme_data[field] = content

        # Extract description using NLP
        if scheme_data['scheme_name']:
            doc = self.nlp(text)
            # Get first few sentences after scheme name
            desc_sentences = []
            found_name = False
            for sent in doc.sents:
                if scheme_data['scheme_name'].lower() in sent.text.lower():
                    found_name = True
                    continue
                if found_name and len(desc_sentences) < 3:
                    desc_sentences.append(sent.text)
            if desc_sentences:
                scheme_data['description'] = ' '.join(desc_sentences)

        # Add scheme level determination
        scheme_data['scheme_level'] = self.determine_scheme_level(text)

        return scheme_data
        
    def process_all_pdfs(self):
        """Process all PDFs in the directory"""
        processed_data = []
        
        for pdf_file in self.pdf_dir.glob('*.pdf'):
            self.logger.info(f"Processing {pdf_file.name}")
            
            # Extract text
            text = self.extract_text_from_pdf(pdf_file)
            if text:
                # Structure data
                scheme_data = self.structure_scheme_data(text)
                scheme_data['source_link'] = f"https://agriwelfare.gov.in/en/Major/{pdf_file.name}"
                processed_data.append(scheme_data)
                
        return processed_data 