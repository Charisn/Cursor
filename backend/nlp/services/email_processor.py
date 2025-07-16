"""
Email processing service for cleaning and intent classification
"""
import re
from typing import Literal
from loguru import logger

class EmailProcessor:
    """Service for processing and analyzing email content"""
    
    def __init__(self):
        self.room_keywords = [
            'room', 'rooms', 'accommodation', 'booking', 'reservation',
            'availability', 'available', 'check-in', 'check-out', 'stay',
            'night', 'nights', 'suite', 'hotel', 'lodge'
        ]
        
        self.generic_keywords = [
            'information', 'contact', 'location', 'directions', 'hours',
            'amenities', 'facilities', 'services', 'policy', 'policies'
        ]
        
        self.complaint_keywords = [
            'complaint', 'problem', 'issue', 'disappointed', 'unsatisfied',
            'refund', 'cancel', 'terrible', 'awful', 'bad experience'
        ]
    
    def clean_email_content(self, content: str) -> str:
        """
        Clean and normalize email content
        """
        try:
            # Remove email signatures and forwarded message headers
            content = re.sub(r'--+.*?(?=\n|$)', '', content, flags=re.DOTALL)
            content = re.sub(r'From:.*?(?=\n\n)', '', content, flags=re.DOTALL)
            content = re.sub(r'Sent:.*?(?=\n)', '', content)
            content = re.sub(r'Subject:.*?(?=\n)', '', content)
            
            # Remove HTML tags if any
            content = re.sub(r'<[^>]+>', '', content)
            
            # Remove extra whitespace and newlines
            content = re.sub(r'\n\s*\n', '\n\n', content)
            content = re.sub(r'[ \t]+', ' ', content)
            
            # Remove URLs
            content = re.sub(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', '', content)
            
            return content.strip()
            
        except Exception as e:
            logger.error(f"Error cleaning email content: {str(e)}")
            return content
    
    def classify_intent(self, content: str) -> Literal["room_availability", "generic", "complaint", "cancellation"]:
        """
        Classify the intent of the email content
        """
        try:
            content_lower = content.lower()
            
            # Count keyword matches
            room_score = sum(1 for keyword in self.room_keywords if keyword in content_lower)
            generic_score = sum(1 for keyword in self.generic_keywords if keyword in content_lower)
            complaint_score = sum(1 for keyword in self.complaint_keywords if keyword in content_lower)
            
            # Check for date patterns (strong indicator of booking intent)
            date_patterns = [
                r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',  # MM/DD/YYYY or MM-DD-YYYY
                r'\b\d{1,2}\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{2,4}\b',  # DD Month YYYY
                r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2}[,\s]+\d{2,4}\b'  # Month DD, YYYY
            ]
            
            has_dates = any(re.search(pattern, content, re.IGNORECASE) for pattern in date_patterns)
            
            # Check for guest count patterns
            guest_patterns = [
                r'\b\d+\s+(guest|person|people|adult|child)\b',
                r'\b(single|double|triple|quad)\b',
                r'\bparty\s+of\s+\d+\b'
            ]
            
            has_guest_info = any(re.search(pattern, content, re.IGNORECASE) for pattern in guest_patterns)
            
            # Decision logic
            if complaint_score > 0:
                return "complaint"
            elif (room_score >= 2 or has_dates or has_guest_info) and room_score > generic_score:
                return "room_availability"
            elif generic_score > room_score:
                return "generic"
            else:
                # Default case - if unclear, treat as room availability to be safe
                return "room_availability" if room_score > 0 else "generic"
                
        except Exception as e:
            logger.error(f"Error classifying intent: {str(e)}")
            return "generic"  # Safe default
    
    def extract_urgency_level(self, content: str) -> str:
        """
        Extract urgency level from email content
        """
        urgent_keywords = ['urgent', 'asap', 'immediately', 'emergency', 'rush']
        content_lower = content.lower()
        
        if any(keyword in content_lower for keyword in urgent_keywords):
            return "high"
        elif "soon" in content_lower:
            return "medium"
        else:
            return "normal"