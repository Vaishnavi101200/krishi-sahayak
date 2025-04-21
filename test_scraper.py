from src.scrapers.pdf_scraper import PDFScraper

def test_pdf_scraper():
    scraper = PDFScraper()
    scraper.scrape()

if __name__ == "__main__":
    test_pdf_scraper() 