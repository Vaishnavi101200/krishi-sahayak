# Krishi Sahayak - Agricultural Scheme WhatsApp Bot 🌾

Krishi Sahayak is an AI-powered WhatsApp bot that provides multilingual information about government agricultural schemes to farmers. The bot can scrape, process, and deliver scheme information in English, Hindi, and Marathi.

## Features 🌟

- **Multilingual Support**: Access information in English, Hindi, and Marathi
- **Automated Scraping**: Regular updates from government websites
- **Smart Processing**: AI-powered text extraction and summarization
- **Interactive Interface**: Easy-to-use WhatsApp menu system
- **Real-time Updates**: Get notifications about new schemes and deadlines
- **Voice Support**: Send voice messages for queries
- **Personalized Experience**: Receive updates based on preferences

## Tech Stack 💻

- **Backend**: Python, Flask
- **NLP**: Transformers, DeepSeek API, LLaMA 2
- **Translation**: IndicTrans, Google Translate API
- **OCR**: Google Vision API, Tesseract
- **Database**: MongoDB
- **Message Queue**: Apache Kafka
- **Caching**: Redis
- **Deployment**: Docker, Kubernetes

## Prerequisites 📋

1. Python 3.9+
2. Docker and Docker Compose
3. MongoDB
4. Redis
5. Apache Kafka
6. Twilio Account
7. Google Cloud Account (for Vision API)
8. IndicTrans API Access

## Setup Instructions 🚀

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/krishi-sahayak.git
   cd krishi-sahayak
   ```

2. **Environment Setup**
   ```bash
   # Copy example environment file
   cp .env.example .env
   
   # Edit .env with your credentials
   nano .env
   ```

3. **Install Dependencies**
   ```bash
   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   
   # Install requirements
   pip install -r requirements.txt
   ```

4. **Docker Deployment**
   ```bash
   # Build and start services
   docker-compose up -d
   
   # Check logs
   docker-compose logs -f
   ```

## Project Structure 📁

```
krishi_sahayak/
├── app/
│   └── app.py              # Main Flask application
├── nlp/
│   ├── language_processor.py
│   ├── scheme_processor.py
│   └── translator.py
├── scrapers/
│   └── scheme_scraper.py
├── config/
│   └── config.py
├── docs/
│   └── api.md
├── tests/
│   └── test_app.py
├── .env.example
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

## API Endpoints 🔌

### WhatsApp Webhook
- **URL**: `/webhook`
- **Method**: `POST`
- **Description**: Handles incoming WhatsApp messages

## Configuration ⚙️

1. **Twilio Setup**
   - Create a Twilio account
   - Set up WhatsApp sandbox
   - Configure webhook URL

2. **Google Cloud Setup**
   - Create a project
   - Enable Vision API
   - Download credentials

3. **MongoDB Setup**
   - Create database
   - Configure collections
   - Set up indexes

## Deployment 🚀

### Local Development
```bash
# Start services
docker-compose up -d

# Run Flask application
flask run
```

### Production Deployment
1. **Kubernetes**
   ```bash
   # Apply configurations
   kubectl apply -f k8s/
   ```

2. **Cloud Deployment (AWS/GCP)**
   - Follow cloud-specific deployment guides in `docs/`
   - Configure auto-scaling
   - Set up monitoring

## Monitoring and Logging 📊

- Logs are stored in `logs/` directory
- Use Prometheus/Grafana for monitoring
- Configure alerts for critical events

## Contributing 🤝

1. Fork the repository
2. Create a feature branch
3. Commit changes
4. Push to the branch
5. Create a Pull Request

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Support 💬

For support and queries:
- Email: support@krishisahayak.com
- WhatsApp: Your-Support-Number
- Documentation: docs/

## Acknowledgments 🙏

- Government Agricultural Portals
- Open Source Community
- Contributors and Testers 