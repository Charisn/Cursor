"""
Parameter extraction service for extracting booking information from emails
"""
import re
from datetime import datetime, date, timedelta
from dateutil import parser
from typing import Dict, Any, Optional, List
from loguru import logger

from ..models.email_models import BookingParameters, ValidationResult

class ParameterExtractor:
    """Service for extracting booking parameters from email content"""
    
    def __init__(self):
        self.room_types = [
            'single', 'double', 'twin', 'queen', 'king', 'suite', 'deluxe',
            'standard', 'executive', 'family', 'studio', 'penthouse'
        ]
        
        self.amenity_keywords = [
            'wifi', 'pool', 'gym', 'spa', 'breakfast', 'parking',
            'balcony', 'ocean view', 'city view', 'kitchenette'
        ]
    
    def extract_booking_parameters(self, content: str) -> Dict[str, Any]:
        """
        Extract all booking parameters from email content
        """
        try:
            params = {}
            
            # Extract dates
            dates = self._extract_dates(content)
            if dates:
                params['check_in_date'] = dates.get('check_in')
                params['check_out_date'] = dates.get('check_out')
            
            # Extract guest count
            guests = self._extract_guest_count(content)
            if guests:
                params['guests'] = guests
            
            # Extract room type
            room_type = self._extract_room_type(content)
            if room_type:
                params['room_type'] = room_type
            
            # Extract budget information
            budget = self._extract_budget(content)
            if budget:
                params.update(budget)
            
            # Extract special requirements
            requirements = self._extract_requirements(content)
            if requirements:
                params['special_requirements'] = requirements
            
            return params
            
        except Exception as e:
            logger.error(f"Error extracting parameters: {str(e)}")
            return {}
    
    def _extract_dates(self, content: str) -> Optional[Dict[str, date]]:
        """Extract check-in and check-out dates"""
        try:
            dates_found = []
            
            # Multiple date patterns
            date_patterns = [
                r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b',
                r'\b\d{1,2}\s+(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{2,4}\b',
                r'\b(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\s+\d{1,2}[,\s]+\d{2,4}\b'
            ]
            
            for pattern in date_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                for match in matches:
                    try:
                        if isinstance(match, tuple):
                            match = ' '.join(match)
                        parsed_date = parser.parse(match, fuzzy=True).date()
                        if parsed_date >= date.today():
                            dates_found.append(parsed_date)
                    except:
                        continue
            
            # Remove duplicates and sort
            dates_found = sorted(list(set(dates_found)))
            
            if len(dates_found) >= 2:
                return {
                    'check_in': dates_found[0],
                    'check_out': dates_found[1]
                }
            elif len(dates_found) == 1:
                # If only one date, assume it's check-in
                return {'check_in': dates_found[0]}
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting dates: {str(e)}")
            return None
    
    def _extract_guest_count(self, content: str) -> Optional[int]:
        """Extract number of guests"""
        try:
            guest_patterns = [
                r'(\d+)\s+guest[s]?',
                r'(\d+)\s+person[s]?',
                r'(\d+)\s+people',
                r'(\d+)\s+adult[s]?',
                r'party\s+of\s+(\d+)',
                r'for\s+(\d+)'
            ]
            
            for pattern in guest_patterns:
                match = re.search(pattern, content, re.IGNORECASE)
                if match:
                    count = int(match.group(1))
                    if 1 <= count <= 20:  # Reasonable range
                        return count
            
            # Check for room type indicators
            if re.search(r'\bsingle\b', content, re.IGNORECASE):
                return 1
            elif re.search(r'\bdouble\b', content, re.IGNORECASE):
                return 2
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting guest count: {str(e)}")
            return None
    
    def _extract_room_type(self, content: str) -> Optional[str]:
        """Extract room type preferences"""
        try:
            content_lower = content.lower()
            
            for room_type in self.room_types:
                if room_type in content_lower:
                    return room_type
            
            return None
            
        except Exception as e:
            logger.error(f"Error extracting room type: {str(e)}")
            return None
    
    def _extract_budget(self, content: str) -> Dict[str, float]:
        """Extract budget information"""
        try:
            budget = {}
            
            # Price patterns
            price_patterns = [
                r'\$(\d+(?:,\d{3})*(?:\.\d{2})?)',  # $1,000.00
                r'(\d+(?:,\d{3})*(?:\.\d{2})?)\s*(?:dollars?|usd)',  # 1000 dollars
                r'budget.*?(\d+(?:,\d{3})*(?:\.\d{2})?)',  # budget of 1000
                r'under\s*\$?(\d+(?:,\d{3})*(?:\.\d{2})?)',  # under $1000
                r'maximum.*?\$?(\d+(?:,\d{3})*(?:\.\d{2})?)'  # maximum $1000
            ]
            
            for pattern in price_patterns:
                matches = re.findall(pattern, content, re.IGNORECASE)
                if matches:
                    prices = []
                    for match in matches:
                        try:
                            price = float(match.replace(',', ''))
                            if 10 <= price <= 10000:  # Reasonable range
                                prices.append(price)
                        except:
                            continue
                    
                    if prices:
                        if 'under' in pattern or 'maximum' in pattern:
                            budget['budget_max'] = max(prices)
                        else:
                            if len(prices) == 1:
                                budget['budget_max'] = prices[0]
                            else:
                                budget['budget_min'] = min(prices)
                                budget['budget_max'] = max(prices)
                        break
            
            return budget
            
        except Exception as e:
            logger.error(f"Error extracting budget: {str(e)}")
            return {}
    
    def _extract_requirements(self, content: str) -> List[str]:
        """Extract special requirements and preferences"""
        try:
            requirements = []
            content_lower = content.lower()
            
            # Check for amenities
            for amenity in self.amenity_keywords:
                if amenity in content_lower:
                    requirements.append(amenity)
            
            # Check for accessibility needs
            accessibility_keywords = ['wheelchair', 'accessible', 'disabled', 'mobility']
            for keyword in accessibility_keywords:
                if keyword in content_lower:
                    requirements.append('accessibility')
                    break
            
            # Check for pet-friendly
            if any(word in content_lower for word in ['pet', 'dog', 'cat', 'animal']):
                requirements.append('pet-friendly')
            
            # Check for smoking preference
            if 'non-smoking' in content_lower or 'no smoking' in content_lower:
                requirements.append('non-smoking')
            elif 'smoking' in content_lower:
                requirements.append('smoking-allowed')
            
            return requirements
            
        except Exception as e:
            logger.error(f"Error extracting requirements: {str(e)}")
            return []
    
    def validate_parameters(self, params: Dict[str, Any]) -> ValidationResult:
        """
        Validate extracted parameters and determine confidence
        """
        try:
            missing_fields = []
            invalid_fields = []
            confidence = 1.0
            
            # Check required fields
            if not params.get('check_in_date'):
                missing_fields.append('check_in_date')
                confidence -= 0.3
            
            if not params.get('check_out_date'):
                missing_fields.append('check_out_date')
                confidence -= 0.2
            
            if not params.get('guests'):
                missing_fields.append('guests')
                confidence -= 0.2
            
            # Validate date logic
            if params.get('check_in_date') and params.get('check_out_date'):
                if params['check_out_date'] <= params['check_in_date']:
                    invalid_fields.append('check_out_date')
                    confidence -= 0.4
            
            # Validate guest count
            if params.get('guests') and (params['guests'] < 1 or params['guests'] > 20):
                invalid_fields.append('guests')
                confidence -= 0.3
            
            # Determine if parameters are sufficient for booking
            is_valid = (
                len(missing_fields) <= 1 and  # Allow one missing field
                len(invalid_fields) == 0 and
                confidence >= 0.5
            )
            
            return ValidationResult(
                is_valid=is_valid,
                confidence=max(0.0, confidence),
                missing_fields=missing_fields,
                invalid_fields=invalid_fields
            )
            
        except Exception as e:
            logger.error(f"Error validating parameters: {str(e)}")
            return ValidationResult(
                is_valid=False,
                confidence=0.0,
                missing_fields=['validation_error']
            )