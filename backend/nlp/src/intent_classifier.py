"""Intent classification using Google Gemini 2.5."""

import json
import re
from typing import Optional

import google.generativeai as genai

from .config import get_settings
from .models import EmailMessage, IntentClassificationResult, IntentType


class IntentClassifier:
    """Classifies email intent using Gemini 2.5."""
    
    def __init__(self):
        """Initialize intent classifier."""
        self.settings = get_settings()
        
        # Initialize Gemini with API key
        if self.settings.google_api_key:
            genai.configure(api_key=self.settings.google_api_key)
            self.model = genai.GenerativeModel('gemini-pro')
        else:
            raise ValueError("Google API key is required for NLP service")
        
        # Classification prompt template
        self.classification_prompt = """
You are an email intent classifier for a hotel booking system called Staydesk.

Your task is to classify emails into one of these three categories:

1. AVAILABILITY_REQUEST: Customer is asking about room availability, rates, or booking information
   - Keywords: "room", "available", "book", "reservation", "check-in", "check-out", "rates", "price"
   - Questions about specific dates, room types, amenities
   - Requests for quotes or availability

2. GENERIC_QUERY: Customer has general questions that require human response
   - General information requests
   - Complaints or feedback
   - Questions about policies, location, services
   - Requests that don't involve booking

3. IGNORE: Spam, automated messages, or irrelevant content
   - Marketing emails
   - System notifications
   - Clearly spam content
   - Unrelated business inquiries

Email to classify:
Subject: {subject}
Body: {body}

Respond with a JSON object containing:
{{
    "intent": "AVAILABILITY_REQUEST" | "GENERIC_QUERY" | "IGNORE",
    "confidence": 0.0-1.0,
    "reasoning": "Brief explanation of the classification decision"
}}

Be conservative - if you're unsure whether something is an availability request, classify as GENERIC_QUERY.
Confidence should be high (>0.8) only when you're very certain.
"""
    
    def classify_intent(self, email: EmailMessage) -> IntentClassificationResult:
        """Classify email intent using Gemini."""
        try:
            # Prepare the prompt
            prompt = self.classification_prompt.format(
                subject=email.subject,
                body=email.body[:2000]  # Truncate very long emails
            )
            
            # Generate response
            response = self.model.generate_content(
                prompt,
                generation_config=genai.types.GenerationConfig(
                    temperature=0.1,  # Low temperature for consistent results
                    max_output_tokens=256,
                )
            )
            
            # Parse the response
            result = self._parse_classification_response(response.text)
            
            # Validate confidence threshold
            if result.confidence < self.settings.confidence_threshold:
                # If confidence is low, default to generic query for safety
                result.intent = IntentType.GENERIC_QUERY
                result.reasoning = f"Low confidence ({result.confidence:.2f}) - defaulting to generic query"
            
            return result
            
        except Exception as e:
            # On any error, default to generic query for safety
            return IntentClassificationResult(
                intent=IntentType.GENERIC_QUERY,
                confidence=0.5,
                reasoning=f"Error during classification: {str(e)}"
            )
    
    def _parse_classification_response(self, response_text: str) -> IntentClassificationResult:
        """Parse Gemini response into structured result."""
        try:
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if not json_match:
                raise ValueError("No JSON found in response")
            
            json_str = json_match.group(0)
            data = json.loads(json_str)
            
            # Validate intent type
            intent_str = data.get('intent', '').upper()
            if intent_str == 'AVAILABILITY_REQUEST':
                intent = IntentType.AVAILABILITY_REQUEST
            elif intent_str == 'GENERIC_QUERY':
                intent = IntentType.GENERIC_QUERY
            elif intent_str == 'IGNORE':
                intent = IntentType.IGNORE
            else:
                # Default to generic query for unknown intents
                intent = IntentType.GENERIC_QUERY
            
            # Extract confidence
            confidence = float(data.get('confidence', 0.5))
            confidence = max(0.0, min(1.0, confidence))  # Clamp to [0, 1]
            
            # Extract reasoning
            reasoning = data.get('reasoning', 'No reasoning provided')
            
            return IntentClassificationResult(
                intent=intent,
                confidence=confidence,
                reasoning=reasoning
            )
            
        except (json.JSONDecodeError, ValueError, KeyError) as e:
            # Return default result on parsing error
            return IntentClassificationResult(
                intent=IntentType.GENERIC_QUERY,
                confidence=0.5,
                reasoning=f"Failed to parse classification response: {str(e)}"
            )
    
    def batch_classify(self, emails: list[EmailMessage]) -> list[IntentClassificationResult]:
        """Classify multiple emails in batch."""
        results = []
        
        for email in emails:
            result = self.classify_intent(email)
            results.append(result)
        
        return results
    
    def is_availability_request(self, email: EmailMessage) -> bool:
        """Quick check if email is likely an availability request."""
        result = self.classify_intent(email)
        return (
            result.intent == IntentType.AVAILABILITY_REQUEST and 
            result.confidence >= self.settings.confidence_threshold
        ) 