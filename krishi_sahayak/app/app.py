from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from twilio.rest import Client
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from datetime import datetime
import json
import logging
from logging.handlers import RotatingFileHandler

# Import custom modules
from nlp.language_processor import LanguageProcessor
from nlp.scheme_processor import SchemeProcessor
from nlp.translator import Translator

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Configure logging
if not os.path.exists('logs'):
    os.makedirs('logs')

file_handler = RotatingFileHandler('logs/krishi_sahayak.log', maxBytes=10240, backupCount=10)
file_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
))
file_handler.setLevel(logging.INFO)
app.logger.addHandler(file_handler)
app.logger.setLevel(logging.INFO)
app.logger.info('Krishi Sahayak startup')

# Initialize Twilio client
twilio_client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))

# Initialize MongoDB client
mongo_client = MongoClient(os.getenv('MONGODB_URI'))
db = mongo_client.krishi_sahayak

# Initialize processors
language_processor = LanguageProcessor()
scheme_processor = SchemeProcessor()
translator = Translator()

def get_welcome_message(language='en'):
    messages = {
        'en': """Welcome to Krishi Sahayak! 🌾
        
Choose an option:
1. View Latest Schemes
2. Search Schemes
3. Get Scheme Updates
4. Change Language
5. Help""",
        'hi': """कृषि सहायक में आपका स्वागत है! 🌾
        
एक विकल्प चुनें:
1. नवीनतम योजनाएं देखें
2. योजनाएं खोजें
3. योजना अपडेट प्राप्त करें
4. भाषा बदलें
5. सहायता""",
        'mr': """कृषी सहायक मध्ये आपले स्वागत आहे! 🌾
        
एक पर्याय निवडा:
1. नवीनतम योजना पहा
2. योजना शोधा
3. योजना अपडेट्स मिळवा
4. भाषा बदला
5. मदत"""
    }
    return messages.get(language, messages['en'])

@app.route('/webhook', methods=['POST'])
def webhook():
    incoming_msg = request.values.get('Body', '').strip().lower()
    sender = request.values.get('From', '')
    
    # Get user's language preference
    user = db.users.find_one({'phone': sender})
    language = user['language'] if user else 'en'
    
    resp = MessagingResponse()
    msg = resp.message()
    
    try:
        if incoming_msg in ['hi', 'hello', 'namaste', 'नमस्ते', 'नमस्कार']:
            msg.body(get_welcome_message(language))
        
        elif incoming_msg == '1':  # View Latest Schemes
            schemes = scheme_processor.get_latest_schemes()
            translated_schemes = translator.translate_schemes(schemes, language)
            msg.body(translated_schemes)
        
        elif incoming_msg == '2':  # Search Schemes
            msg.body(translator.translate_text(
                "Please enter your search query or keywords related to the scheme.",
                language
            ))
        
        elif incoming_msg == '3':  # Get Scheme Updates
            updates = scheme_processor.get_scheme_updates(sender)
            translated_updates = translator.translate_text(updates, language)
            msg.body(translated_updates)
        
        elif incoming_msg == '4':  # Change Language
            msg.body("""Select your preferred language:
            1. English
            2. हिंदी (Hindi)
            3. मराठी (Marathi)""")
        
        elif incoming_msg == '5':  # Help
            help_text = translator.translate_text(
                "For assistance, please type your query or contact our support team at support@krishisahayak.com",
                language
            )
            msg.body(help_text)
        
        else:
            # Process the query using NLP
            response = language_processor.process_query(incoming_msg, language)
            msg.body(response)
        
        # Log the interaction
        db.interactions.insert_one({
            'user': sender,
            'message': incoming_msg,
            'response': msg.body,
            'timestamp': datetime.utcnow()
        })
        
    except Exception as e:
        app.logger.error(f'Error processing message: {str(e)}')
        error_msg = translator.translate_text(
            "Sorry, I encountered an error. Please try again later.",
            language
        )
        msg.body(error_msg)
    
    return str(resp)

if __name__ == '__main__':
    app.run(debug=True) 