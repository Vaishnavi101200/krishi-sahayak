import langdetect
import fasttext
from transformers import pipeline
from typing import Dict, List, Any
import logging

class LanguageProcessor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
        self.qa_pipeline = pipeline("question-answering", model="deepset/roberta-base-squad2")
        
        # Load language detection model
        try:
            self.lang_model = fasttext.load_model('lid.176.bin')
        except Exception as e:
            self.logger.warning(f"Could not load fasttext model: {e}. Falling back to langdetect.")
            self.lang_model = None
    
    def detect_language(self, text: str) -> str:
        """
        Detect the language of the input text.
        Returns language code: 'en', 'hi', or 'mr'
        """
        try:
            if self.lang_model:
                pred = self.lang_model.predict(text)[0][0]
                lang = pred.replace('__label__', '')
            else:
                lang = langdetect.detect(text)
            
            # Map to supported languages
            lang_map = {
                'en': 'en',
                'hi': 'hi',
                'mr': 'mr',
                'mar': 'mr'  # Map Marathi variations
            }
            return lang_map.get(lang, 'en')
        except Exception as e:
            self.logger.error(f"Language detection error: {e}")
            return 'en'
    
    def extract_key_info(self, text: str) -> Dict[str, Any]:
        """
        Extract key information from scheme text using NLP.
        """
        try:
            # Generate summary
            summary = self.summarizer(text, max_length=130, min_length=30, do_sample=False)[0]['summary_text']
            
            # Extract structured information using QA pipeline
            info = {
                'scheme_name': self._extract_answer(text, "What is the name of the scheme?"),
                'eligibility': self._extract_answer(text, "What are the eligibility criteria?"),
                'benefits': self._extract_answer(text, "What are the benefits of this scheme?"),
                'application_process': self._extract_answer(text, "How to apply for this scheme?"),
                'deadline': self._extract_answer(text, "What is the deadline or last date to apply?"),
                'summary': summary
            }
            return info
        except Exception as e:
            self.logger.error(f"Error extracting key info: {e}")
            return {'error': str(e)}
    
    def _extract_answer(self, context: str, question: str) -> str:
        """
        Extract specific information using question-answering.
        """
        try:
            result = self.qa_pipeline(question=question, context=context)
            return result['answer']
        except Exception as e:
            self.logger.error(f"QA pipeline error: {e}")
            return ""
    
    def process_query(self, query: str, target_language: str) -> str:
        """
        Process user queries and generate appropriate responses.
        """
        try:
            # Detect query language
            query_lang = self.detect_language(query)
            
            # TODO: Implement more sophisticated query processing
            # For now, we'll use a simple keyword-based approach
            keywords = query.lower().split()
            
            if any(word in keywords for word in ['deadline', 'last date', 'when']):
                return self._get_deadline_info(target_language)
            elif any(word in keywords for word in ['apply', 'how', 'process']):
                return self._get_application_process(target_language)
            elif any(word in keywords for word in ['eligible', 'qualify']):
                return self._get_eligibility_info(target_language)
            else:
                return self._get_general_info(target_language)
        
        except Exception as e:
            self.logger.error(f"Query processing error: {e}")
            return "I apologize, but I couldn't process your query. Please try rephrasing it."
    
    def _get_deadline_info(self, language: str) -> str:
        # Placeholder - implement actual deadline retrieval logic
        return "I'll check the latest deadline information for you."
    
    def _get_application_process(self, language: str) -> str:
        # Placeholder - implement actual application process retrieval logic
        return "I'll guide you through the application process."
    
    def _get_eligibility_info(self, language: str) -> str:
        # Placeholder - implement actual eligibility info retrieval logic
        return "I'll check the eligibility criteria for you."
    
    def _get_general_info(self, language: str) -> str:
        # Placeholder - implement general information retrieval logic
        return "I'll provide you with general information about available schemes." 