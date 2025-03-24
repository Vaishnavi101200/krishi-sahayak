from typing import List, Dict, Any
import logging
from datetime import datetime
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from google.cloud import vision
import pytesseract
from pdf2image import convert_from_path
import requests
import json

class SchemeProcessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        load_dotenv()
        
        # Initialize MongoDB connection
        self.mongo_client = MongoClient(os.getenv('MONGODB_URI'))
        self.db = self.mongo_client.krishi_sahayak
        
        # Initialize Google Vision client
        try:
            self.vision_client = vision.ImageAnnotatorClient()
        except Exception as e:
            self.logger.warning(f"Could not initialize Google Vision client: {e}")
            self.vision_client = None
    
    def get_latest_schemes(self, limit: int = 5) -> List[Dict[str, Any]]:
        """
        Retrieve the latest government schemes from the database.
        """
        try:
            schemes = list(self.db.schemes.find(
                {'status': 'active'},
                {'_id': 0}
            ).sort('published_date', -1).limit(limit))
            return schemes
        except Exception as e:
            self.logger.error(f"Error fetching latest schemes: {e}")
            return []
    
    def get_scheme_updates(self, user_phone: str) -> str:
        """
        Get relevant scheme updates for a specific user.
        """
        try:
            # Get user preferences
            user = self.db.users.find_one({'phone': user_phone})
            if not user:
                return "Please set up your preferences to receive personalized updates."
            
            # Find matching schemes based on user preferences
            preferences = user.get('preferences', {})
            query = self._build_scheme_query(preferences)
            
            schemes = list(self.db.schemes.find(query).sort('updated_date', -1).limit(3))
            
            if not schemes:
                return "No new updates found for your preferred schemes."
            
            # Format updates
            updates = ["Here are your latest scheme updates:"]
            for scheme in schemes:
                updates.append(f"\n📌 {scheme['name']}")
                if 'deadline' in scheme:
                    updates.append(f"Deadline: {scheme['deadline']}")
                if 'updates' in scheme:
                    updates.append(f"Update: {scheme['updates'][-1]}")
            
            return "\n".join(updates)
        except Exception as e:
            self.logger.error(f"Error getting scheme updates: {e}")
            return "Sorry, I couldn't fetch the updates at this moment."
    
    def process_pdf_document(self, pdf_path: str) -> Dict[str, Any]:
        """
        Process PDF documents to extract scheme information.
        """
        try:
            # Convert PDF to images
            images = convert_from_path(pdf_path)
            
            extracted_text = []
            for image in images:
                if self.vision_client:
                    # Use Google Vision API
                    image_content = self._get_image_content(image)
                    response = self.vision_client.document_text_detection(
                        vision.Image({'content': image_content})
                    )
                    extracted_text.append(response.full_text_annotation.text)
                else:
                    # Fallback to Tesseract
                    text = pytesseract.image_to_string(image)
                    extracted_text.append(text)
            
            # Combine extracted text
            full_text = "\n".join(extracted_text)
            
            # Process and structure the extracted text
            structured_data = self._structure_scheme_data(full_text)
            return structured_data
            
        except Exception as e:
            self.logger.error(f"Error processing PDF document: {e}")
            return {'error': str(e)}
    
    def _build_scheme_query(self, preferences: Dict) -> Dict:
        """
        Build MongoDB query based on user preferences.
        """
        query = {'status': 'active'}
        
        if 'categories' in preferences:
            query['category'] = {'$in': preferences['categories']}
        
        if 'state' in preferences:
            query['$or'] = [
                {'state': preferences['state']},
                {'state': 'ALL'},
                {'type': 'CENTRAL'}
            ]
        
        return query
    
    def _get_image_content(self, image) -> bytes:
        """
        Convert PIL Image to bytes for Google Vision API.
        """
        import io
        img_byte_arr = io.BytesIO()
        image.save(img_byte_arr, format='PNG')
        return img_byte_arr.getvalue()
    
    def _structure_scheme_data(self, text: str) -> Dict[str, Any]:
        """
        Structure extracted text into scheme data format.
        """
        # TODO: Implement more sophisticated text structuring
        # For now, return basic structure
        return {
            'raw_text': text,
            'extracted_date': datetime.utcnow(),
            'status': 'pending_review'
        }
    
    def save_scheme(self, scheme_data: Dict[str, Any]) -> bool:
        """
        Save processed scheme data to database.
        """
        try:
            result = self.db.schemes.insert_one(scheme_data)
            return bool(result.inserted_id)
        except Exception as e:
            self.logger.error(f"Error saving scheme data: {e}")
            return False 