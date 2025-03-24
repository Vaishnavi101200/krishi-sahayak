import scrapy
from scrapy.crawler import CrawlerProcess
from bs4 import BeautifulSoup
import requests
import logging
import os
from datetime import datetime
from typing import List, Dict, Any
import json
from urllib.parse import urljoin
import PyPDF2
import io

class SchemeSpider(scrapy.Spider):
    name = 'scheme_spider'
    
    def __init__(self, *args, **kwargs):
        super(SchemeSpider, self).__init__(*args, **kwargs)
        self.logger = logging.getLogger(__name__)
        self.start_urls = [
            'https://agricoop.nic.in/en/Major-Schemes',
            'https://pmkisan.gov.in/',
            'https://mkisan.gov.in/Home/Schemes'
        ]
    
    def parse(self, response):
        try:
            # Extract scheme links
            scheme_links = response.css('a[href*="scheme"]::attr(href)').getall()
            scheme_links.extend(response.css('a[href*="Scheme"]::attr(href)').getall())
            
            for link in scheme_links:
                absolute_url = response.urljoin(link)
                yield scrapy.Request(
                    absolute_url,
                    callback=self.parse_scheme,
                    errback=self.handle_error
                )
        
        except Exception as e:
            self.logger.error(f"Error parsing page {response.url}: {e}")
    
    def parse_scheme(self, response):
        try:
            # Extract scheme details
            scheme_data = {
                'url': response.url,
                'name': self._extract_text(response, 'h1::text, h2::text'),
                'description': self._extract_text(response, 'p::text'),
                'pdf_links': response.css('a[href$=".pdf"]::attr(href)').getall(),
                'last_updated': datetime.utcnow().isoformat(),
                'source': response.url.split('/')[2]
            }
            
            # Download PDFs
            scheme_data['pdf_contents'] = []
            for pdf_link in scheme_data['pdf_links']:
                pdf_url = response.urljoin(pdf_link)
                pdf_content = self._download_pdf(pdf_url)
                if pdf_content:
                    scheme_data['pdf_contents'].append({
                        'url': pdf_url,
                        'content': pdf_content
                    })
            
            yield scheme_data
            
        except Exception as e:
            self.logger.error(f"Error parsing scheme page {response.url}: {e}")
    
    def _extract_text(self, response, selector):
        """Extract and clean text from selector."""
        texts = response.css(selector).getall()
        return ' '.join([text.strip() for text in texts if text.strip()])
    
    def _download_pdf(self, url: str) -> str:
        """Download and extract text from PDF."""
        try:
            response = requests.get(url)
            if response.status_code == 200:
                pdf_file = io.BytesIO(response.content)
                reader = PyPDF2.PdfReader(pdf_file)
                text = ''
                for page in reader.pages:
                    text += page.extract_text() + '\n'
                return text
            return None
        except Exception as e:
            self.logger.error(f"Error downloading PDF {url}: {e}")
            return None
    
    def handle_error(self, failure):
        self.logger.error(f"Request failed: {failure.value}")

class SchemeScraper:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.process = CrawlerProcess({
            'USER_AGENT': 'Krishi Sahayak Bot (+https://krishisahayak.org)',
            'ROBOTSTXT_OBEY': True,
            'CONCURRENT_REQUESTS': 16,
            'DOWNLOAD_DELAY': 1,
            'COOKIES_ENABLED': False,
        })
    
    def start_scraping(self) -> None:
        """
        Start the scraping process.
        """
        try:
            self.process.crawl(SchemeSpider)
            self.process.start()
        except Exception as e:
            self.logger.error(f"Error starting scraper: {e}")
    
    def scrape_specific_scheme(self, url: str) -> Dict[str, Any]:
        """
        Scrape a specific scheme URL.
        """
        try:
            response = requests.get(url)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                scheme_data = {
                    'url': url,
                    'name': self._extract_scheme_name(soup),
                    'description': self._extract_description(soup),
                    'pdf_links': self._extract_pdf_links(soup, url),
                    'last_updated': datetime.utcnow().isoformat()
                }
                
                # Download PDFs
                scheme_data['pdf_contents'] = []
                for pdf_link in scheme_data['pdf_links']:
                    pdf_content = self._download_pdf(pdf_link)
                    if pdf_content:
                        scheme_data['pdf_contents'].append({
                            'url': pdf_link,
                            'content': pdf_content
                        })
                
                return scheme_data
            
            else:
                self.logger.error(f"Failed to fetch URL {url}: {response.status_code}")
                return None
                
        except Exception as e:
            self.logger.error(f"Error scraping scheme {url}: {e}")
            return None
    
    def _extract_scheme_name(self, soup: BeautifulSoup) -> str:
        """Extract scheme name from BeautifulSoup object."""
        for tag in ['h1', 'h2']:
            element = soup.find(tag)
            if element:
                return element.text.strip()
        return "Unknown Scheme"
    
    def _extract_description(self, soup: BeautifulSoup) -> str:
        """Extract scheme description from BeautifulSoup object."""
        paragraphs = soup.find_all('p')
        return ' '.join([p.text.strip() for p in paragraphs if p.text.strip()])
    
    def _extract_pdf_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract PDF links from BeautifulSoup object."""
        pdf_links = []
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.lower().endswith('.pdf'):
                absolute_url = urljoin(base_url, href)
                pdf_links.append(absolute_url)
        return pdf_links
    
    def _download_pdf(self, url: str) -> str:
        """Download and extract text from PDF."""
        try:
            response = requests.get(url)
            if response.status_code == 200:
                pdf_file = io.BytesIO(response.content)
                reader = PyPDF2.PdfReader(pdf_file)
                text = ''
                for page in reader.pages:
                    text += page.extract_text() + '\n'
                return text
            return None
        except Exception as e:
            self.logger.error(f"Error downloading PDF {url}: {e}")
            return None 