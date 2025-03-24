from flask import Flask, request, jsonify
from googletrans import Translator
import logging
from logging.handlers import RotatingFileHandler
import os
from dotenv import load_dotenv

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

# Initialize translator
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

@app.route('/')
def home():
    return """<h1>Krishi Sahayak API</h1>
    <p>Welcome to the Krishi Sahayak API. Send POST requests to /webhook to interact with the bot.</p>"""

@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Get message data
        data = request.get_json()
        if not data:
            data = request.form.to_dict()
        
        # Extract message and language (default to English)
        message = data.get('message', '').strip().lower()
        language = data.get('language', 'en')
        
        # Process the message
        if message in ['hi', 'hello', 'namaste', 'नमस्ते', 'नमस्कार']:
            response = get_welcome_message(language)
        elif message == '1':
            response = "Here are the latest schemes: [Demo Scheme List]"
            if language != 'en':
                response = translator.translate(response, dest=language).text
        elif message == '2':
            response = "Please enter keywords to search for schemes."
            if language != 'en':
                response = translator.translate(response, dest=language).text
        elif message == '3':
            response = "You will receive updates about new schemes."
            if language != 'en':
                response = translator.translate(response, dest=language).text
        elif message == '4':
            response = """Select your preferred language:
1. English
2. हिंदी (Hindi)
3. मराठी (Marathi)"""
        elif message == '5':
            response = "For assistance, please contact support@krishisahayak.com"
            if language != 'en':
                response = translator.translate(response, dest=language).text
        else:
            response = "I'm sorry, I don't understand that command. Please select an option from the menu."
            if language != 'en':
                response = translator.translate(response, dest=language).text
        
        return jsonify({
            'status': 'success',
            'response': response
        })
        
    except Exception as e:
        app.logger.error(f'Error processing message: {str(e)}')
        return jsonify({
            'status': 'error',
            'message': 'An error occurred while processing your request.'
        }), 500

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 