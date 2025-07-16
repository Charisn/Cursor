"""
Response generation service for creating email replies
"""
from typing import Dict, Any, Optional
from loguru import logger

from ..models.email_models import ProcessedEmail, ResponseTemplate

class ResponseGenerator:
    """Service for generating appropriate email responses"""
    
    def __init__(self):
        self.templates = {
            "availability_check": {
                "subject": "Room Availability - Your Inquiry",
                "content": """Dear Guest,

Thank you for your inquiry about room availability.

Based on your request, we have found the following options:

{room_details}

Total Cost: {total_cost} {currency}

Please let us know if you would like to proceed with the booking or if you need any additional information.

Best regards,
Hotel Reservation Team"""
            },
            
            "clarification_request": {
                "subject": "Additional Information Needed - Your Room Inquiry",
                "content": """Dear Guest,

Thank you for your interest in staying with us.

To better assist you with your room availability inquiry, we need some additional information:

{missing_info}

Once we receive this information, we'll be happy to check availability and provide you with our best options.

Best regards,
Hotel Reservation Team"""
            },
            
            "generic_response": {
                "subject": "Thank You for Your Inquiry",
                "content": """Dear Guest,

Thank you for contacting us.

We have received your message and our team will review it carefully. We will get back to you promptly with a detailed response.

If you have an urgent inquiry, please feel free to call us directly at our main number.

Best regards,
Hotel Customer Service Team"""
            },
            
            "no_availability": {
                "subject": "Room Availability Update",
                "content": """Dear Guest,

Thank you for your inquiry about room availability.

Unfortunately, we don't have availability for your requested dates ({check_in} to {check_out}).

However, we have the following alternative suggestions:

{alternatives}

Please let us know if any of these options work for you, and we'll be happy to assist with your booking.

Best regards,
Hotel Reservation Team"""
            }
        }
    
    async def generate_response(self, processed_email: ProcessedEmail, booking_data: Optional[Dict[str, Any]] = None) -> str:
        """
        Generate appropriate email response based on processed email and booking data
        """
        try:
            response_type = processed_email.response_type
            
            if response_type == "availability_check":
                return self._generate_availability_response(processed_email, booking_data)
            
            elif response_type == "clarification_request":
                return self._generate_clarification_response(processed_email)
            
            elif response_type == "generic_response":
                return self._generate_generic_response()
            
            else:
                logger.warning(f"Unknown response type: {response_type}")
                return self._generate_generic_response()
                
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            return self._generate_generic_response()
    
    def _generate_availability_response(self, processed_email: ProcessedEmail, booking_data: Optional[Dict[str, Any]]) -> str:
        """Generate response for availability check"""
        try:
            template = self.templates["availability_check"]
            
            if booking_data and booking_data.get("available"):
                # Rooms are available
                room_details = self._format_room_details(booking_data.get("rooms", []))
                total_cost = booking_data.get("total_cost", "N/A")
                currency = booking_data.get("currency", "USD")
                
                return template["content"].format(
                    room_details=room_details,
                    total_cost=total_cost,
                    currency=currency
                )
            
            else:
                # No availability - use alternative template
                template = self.templates["no_availability"]
                params = processed_email.extracted_parameters
                check_in = params.get("check_in_date", "N/A")
                check_out = params.get("check_out_date", "N/A")
                
                alternatives = "We will search for alternative dates and get back to you shortly."
                if booking_data and booking_data.get("suggestions"):
                    alternatives = self._format_alternatives(booking_data["suggestions"])
                
                return template["content"].format(
                    check_in=check_in,
                    check_out=check_out,
                    alternatives=alternatives
                )
                
        except Exception as e:
            logger.error(f"Error generating availability response: {str(e)}")
            return self._generate_generic_response()
    
    def _generate_clarification_response(self, processed_email: ProcessedEmail) -> str:
        """Generate response requesting clarification"""
        try:
            template = self.templates["clarification_request"]
            missing_fields = processed_email.clarification_needed
            
            missing_info_text = self._format_missing_info(missing_fields)
            
            return template["content"].format(missing_info=missing_info_text)
            
        except Exception as e:
            logger.error(f"Error generating clarification response: {str(e)}")
            return self._generate_generic_response()
    
    def _generate_generic_response(self) -> str:
        """Generate generic response"""
        template = self.templates["generic_response"]
        return template["content"]
    
    def _format_room_details(self, rooms: list) -> str:
        """Format room details for email"""
        if not rooms:
            return "No rooms found matching your criteria."
        
        details = []
        for room in rooms:
            room_info = f"""
- {room.get('name', 'Room')} ({room.get('type', 'Standard')})
  Capacity: {room.get('capacity', 'N/A')} guests
  Price: ${room.get('price_per_night', 'N/A')} per night
  Amenities: {', '.join(room.get('amenities', []))}
"""
            details.append(room_info.strip())
        
        return '\n\n'.join(details)
    
    def _format_alternatives(self, suggestions: list) -> str:
        """Format alternative suggestions"""
        if not suggestions:
            return "We will search for alternative dates and get back to you shortly."
        
        alternatives = []
        for suggestion in suggestions[:3]:  # Limit to top 3
            room = suggestion.get('room', {})
            dates = suggestion.get('available_dates', [])
            
            if dates:
                date_text = f"Available: {dates[0]}"
                if len(dates) > 1:
                    date_text += f" - {dates[-1]}"
            else:
                date_text = "Flexible dates available"
            
            alt_info = f"- {room.get('name', 'Room')} - {date_text} - ${room.get('price_per_night', 'N/A')}/night"
            alternatives.append(alt_info)
        
        return '\n'.join(alternatives)
    
    def _format_missing_info(self, missing_fields: list) -> str:
        """Format missing information request"""
        field_descriptions = {
            'check_in_date': '• Check-in date',
            'check_out_date': '• Check-out date',
            'guests': '• Number of guests',
            'room_type': '• Preferred room type (optional)',
            'budget_max': '• Budget range (optional)'
        }
        
        missing_info = []
        for field in missing_fields:
            if field in field_descriptions:
                missing_info.append(field_descriptions[field])
            else:
                missing_info.append(f'• {field.replace("_", " ").title()}')
        
        return '\n'.join(missing_info)
    
    def get_subject_line(self, response_type: str, processed_email: ProcessedEmail) -> str:
        """Get appropriate subject line for response"""
        try:
            if response_type in self.templates:
                return self.templates[response_type]["subject"]
            else:
                return "Thank You for Your Inquiry"
        except:
            return "Thank You for Your Inquiry"