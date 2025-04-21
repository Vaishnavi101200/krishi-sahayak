import requests
from bs4 import BeautifulSoup
from pathlib import Path
from urllib.parse import urljoin
import time
from src.utils.logger import setup_logger
from config import BASE_URL, PDF_DIR

class PDFScraper:
    def __init__(self):
        self.logger = setup_logger("pdf_scraper")
        self.base_url = BASE_URL
        self.pdf_dir = PDF_DIR
        self.session = requests.Session()
        
    def get_page_content(self, url):
        """Fetch webpage content with retry mechanism"""
        max_retries = 3
        for attempt in range(max_retries):
            try:
                response = self.session.get(url, timeout=30)
                response.raise_for_status()
                return response.text
            except requests.RequestException as e:
                self.logger.error(f"Attempt {attempt + 1} failed: {str(e)}")
                if attempt == max_retries - 1:
                    raise
                time.sleep(2 ** attempt)  # Exponential backoff
                
    def extract_pdf_links(self, html_content):
        """Extract PDF links from HTML content"""
        soup = BeautifulSoup(html_content, 'html.parser')
        pdf_links = []
        
        # Find all links that might contain PDFs
        for link in soup.find_all('a'):
            href = link.get('href', '')
            if href.lower().endswith('.pdf'):
                full_url = urljoin(self.base_url, href)
                pdf_links.append({
                    'url': full_url,
                    'text': link.get_text(strip=True)
                })
                
        self.logger.info(f"Found {len(pdf_links)} PDF links")
        return pdf_links
    
    def download_pdf(self, pdf_url, filename):
        """Download and save PDF file"""
        try:
            response = self.session.get(pdf_url, stream=True)
            response.raise_for_status()
            
            file_path = self.pdf_dir / filename
            with open(file_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            self.logger.info(f"Successfully downloaded: {filename}")
            return True
            
        except Exception as e:
            self.logger.error(f"Failed to download {filename}: {str(e)}")
            return False
            
    def scrape(self):
        """Main scraping method"""
        try:
            # Get main page content
            html_content = self.get_page_content(self.base_url)
            
            # Extract PDF links
            pdf_links = self.extract_pdf_links(html_content)
            
            # Download each PDF
            for pdf in pdf_links:
                filename = Path(pdf['url']).name
                self.download_pdf(pdf['url'], filename)
                
        except Exception as e:
            self.logger.error(f"Scraping failed: {str(e)}")
            raise 