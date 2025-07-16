"""Edge case handling and clarification logic."""

from typing import List

from .models import (
    EmailMessage,
    NextAction,
    ParameterExtractionResult,
    RoomRequest
)


class EdgeCaseResult:
    """Result of edge case handling."""
    
    def __init__(
        self,
        next_action: NextAction,
        clarification_needed: bool = False,
        clarification_questions: List[str] = None
    ):
        self.next_action = next_action
        self.clarification_needed = clarification_needed
        self.clarification_questions = clarification_questions or []


class EdgeCaseHandler:
    """Handles edge cases and determines clarification needs."""
    
    def __init__(self):
        """Initialize edge case handler."""
        pass
    
    def handle_availability_request(
        self, 
        email: EmailMessage, 
        extraction_result: ParameterExtractionResult
    ) -> EdgeCaseResult:
        """Handle edge cases for availability requests."""
        params = extraction_result.params
        missing_fields = extraction_result.missing_fields
        
        # Check for missing critical information
        if self._needs_clarification(params, missing_fields):
            questions = self._generate_clarification_questions(params, missing_fields)
            return EdgeCaseResult(
                next_action=NextAction.REQUEST_CLARIFICATION,
                clarification_needed=True,
                clarification_questions=questions
            )
        
        # Check for multi-room requests
        if self._is_multi_room_request(params):
            # For multi-room requests, we can still proceed to API
            # The API will return top 5 suggestions
            return EdgeCaseResult(
                next_action=NextAction.CALL_AVAILABILITY_API,
                clarification_needed=False
            )
        
        # Standard availability request with sufficient info
        if self._has_sufficient_info(params):
            return EdgeCaseResult(
                next_action=NextAction.CALL_AVAILABILITY_API,
                clarification_needed=False
            )
        
        # Default to clarification if uncertain
        questions = self._generate_clarification_questions(params, missing_fields)
        return EdgeCaseResult(
            next_action=NextAction.REQUEST_CLARIFICATION,
            clarification_needed=True,
            clarification_questions=questions
        )
    
    def _needs_clarification(self, params: RoomRequest, missing_fields: List[str]) -> bool:
        """Determine if clarification is needed."""
        # Critical fields that must be present
        critical_missing = [field for field in missing_fields if field in ["date", "room_count"]]
        
        if critical_missing:
            return True
        
        # Check for ambiguous or unrealistic values
        if params.date and params.room_count:
            # Check if room count is too high (might need clarification)
            if params.room_count > 5:
                return True
            
            # Check if budget is unusually low or high
            if params.budget:
                if params.budget < 30 or params.budget > 2000:
                    return True
        
        return False
    
    def _is_multi_room_request(self, params: RoomRequest) -> bool:
        """Check if this is a multi-room request."""
        return params.room_count and params.room_count > 1
    
    def _has_sufficient_info(self, params: RoomRequest) -> bool:
        """Check if we have sufficient information to proceed."""
        return (
            params.date is not None and 
            params.room_count is not None and
            params.room_count >= 1
        )
    
    def _generate_clarification_questions(
        self, 
        params: RoomRequest, 
        missing_fields: List[str]
    ) -> List[str]:
        """Generate appropriate clarification questions."""
        questions = []
        
        if "date" in missing_fields:
            questions.append("What is your preferred check-in date?")
        
        if "room_count" in missing_fields:
            questions.append("How many rooms do you need?")
        
        # Additional questions based on extracted but questionable data
        if params.room_count and params.room_count > 5:
            questions.append(
                f"You mentioned {params.room_count} rooms. Can you confirm this number? "
                "For large bookings, we may need to check group rates."
            )
        
        if params.budget:
            if params.budget < 30:
                questions.append(
                    f"Your budget of ${params.budget} per night seems quite low. "
                    "Could you confirm your budget range?"
                )
            elif params.budget > 2000:
                questions.append(
                    f"Your budget of ${params.budget} per night is quite high. "
                    "Are you looking for luxury suites or premium accommodations?"
                )
        
        # If no specific questions, provide a general one
        if not questions:
            if not params.budget:
                questions.append("What is your preferred budget range per room per night?")
            else:
                questions.append("Could you provide any additional preferences for your stay?")
        
        return questions
    
    def generate_clarification_email_template(
        self, 
        original_email: EmailMessage,
        questions: List[str]
    ) -> dict:
        """Generate a clarification email template."""
        
        question_text = "\n".join(f"• {q}" for q in questions)
        
        email_body = f"""
Dear {self._extract_customer_name(original_email.sender)},

Thank you for your interest in staying with us!

To provide you with the best room availability and rates, we need a bit more information:

{question_text}

Once we have these details, we'll be happy to check availability and send you our best options.

Looking forward to your response!

Best regards,
Staydesk Team
        """.strip()
        
        return {
            "to": original_email.sender,
            "subject": f"Re: {original_email.subject}",
            "body": email_body,
            "type": "clarification_request"
        }
    
    def generate_generic_reply_template(self, original_email: EmailMessage) -> dict:
        """Generate a generic reply template."""
        
        email_body = f"""
Dear {self._extract_customer_name(original_email.sender)},

Thank you for contacting Staydesk!

We have received your message and one of our team members will review it and get back to you promptly within 24 hours.

If you have any urgent requests, please don't hesitate to call us directly.

Best regards,
Staydesk Team
        """.strip()
        
        return {
            "to": original_email.sender,
            "subject": f"Re: {original_email.subject}",
            "body": email_body,
            "type": "generic_reply"
        }
    
    def _extract_customer_name(self, email_address: str) -> str:
        """Extract customer name from email address for personalization."""
        # Simple extraction from email
        if "@" in email_address:
            local_part = email_address.split("@")[0]
            # Remove dots and numbers, capitalize
            name_parts = local_part.replace(".", " ").replace("_", " ").split()
            cleaned_parts = []
            
            for part in name_parts:
                # Skip parts that are all numbers
                if not part.isdigit():
                    cleaned_parts.append(part.capitalize())
            
            if cleaned_parts:
                return " ".join(cleaned_parts)
        
        return "Guest"  # Fallback
    
    def should_escalate_to_human(self, email: EmailMessage, params: RoomRequest) -> bool:
        """Determine if request should be escalated to human agent."""
        
        # Escalate complex special requests
        if params.special_requests:
            complex_keywords = [
                "wheelchair", "disability", "medical", "allergy", 
                "group booking", "corporate", "wedding", "event",
                "complaint", "problem", "issue", "refund"
            ]
            
            special_req_lower = params.special_requests.lower()
            if any(keyword in special_req_lower for keyword in complex_keywords):
                return True
        
        # Escalate very large bookings
        if params.room_count and params.room_count > 10:
            return True
        
        # Escalate if email contains complaint keywords
        email_text = f"{email.subject} {email.body}".lower()
        complaint_keywords = [
            "complaint", "disappointed", "terrible", "awful", 
            "refund", "cancel", "problem", "issue", "manager"
        ]
        
        if any(keyword in email_text for keyword in complaint_keywords):
            return True
        
        return False 