# Krishi Sahayak

A multilingual web application that provides easy access to agricultural schemes and benefits for farmers. The application scrapes information from government agricultural websites, processes scheme documents, and presents them in English, Hindi, and Marathi.

## Features

- 🌐 **Multilingual Support**: Available in English, Hindi, and Marathi
- 📑 **Scheme Categorization**: Organizes schemes into Central and State levels
- 🔍 **Smart Search**: Easy filtering of schemes based on categories
- 📄 **PDF Processing**: Automatically extracts and structures information from government PDFs
- 🔄 **Auto Translation**: Translates scheme information into multiple languages
- 💻 **User-Friendly Interface**: Clean and intuitive web interface

## Information Extracted for Each Scheme

- Scheme Name – The official name of the scheme
- Scheme Description – A brief summary of the scheme
- Eligibility Criteria – Who can apply (e.g., age, landholding, income limit)
- Benefits/Assistance Provided – Monetary/non-monetary benefits
- Application Process – Steps to apply and required documents
- Deadline – Last date for application submission
- Source Link – Government portal link for verification
- Scheme Category – Type of scheme (e.g., subsidies, insurance, training, loans)

## Tech Stack

- Backend: FastAPI
- Frontend: HTML, CSS, JavaScript
- PDF Processing: PyPDF2, spaCy
- Translation: Google Translate API
- Web Scraping: BeautifulSoup4
- Language Processing: spaCy

## Installation

1. Clone the repository

```sh
git clone https://github.com/Vaishnavi101200/krishi-sahayak.git
cd krishi-sahayak
```

2. Create and activate virtual environment

```sh
python -m venv venv
source venv/bin/activate
```


3. Install dependencies

```sh
pip install -r requirements.txt
```

4. Download spaCy model

```sh
python -m spacy download en_core_web_sm
```

## Project Structure

Krishi-sahayak/

├── src/

│ ├── api/ # FastAPI application

│ │ ├── main.py # API endpoints

│ │ ├── models.py # Data models

│ │ └── service.py # Business logic

│ ├── frontend/ # Web interface

│ │ ├── static/ # CSS files

│ │ └── templates/ # HTML templates

│ ├── processors/ # PDF processing

│ ├── scrapers/ # Web scraping

│ ├── translators/ # Translation services

│ └── utils/ # Utility functions

├── data/

│ ├── raw_pdfs/ # Downloaded PDFs

│ ├── processed_pdfs/ # Extracted information

│ └── translated_schemes/ # Translated data

└── config.py # Configuration

## Usage

1. Start the application

```sh
python run_api.py
```

2. Open your browser and navigate to `http://localhost:8000`

3. Use the interface to:
   - Select scheme level (Central/State)
   - Choose language preference (English/Hindi/Marathi)
   - View scheme details and documentation

## Data Processing Pipeline

1. **Web Scraping**: Downloads PDFs from government agricultural websites
2. **PDF Processing**: Extracts structured information using NLP
3. **Scheme Classification**: Categorizes schemes as Central or State
4. **Translation**: Converts content to Hindi and Marathi
5. **API Service**: Serves processed data through REST endpoints

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Ministry of Agriculture & Farmers Welfare, Government of India
- Agricultural Welfare Portal (https://agriwelfare.gov.in/en/Major)
