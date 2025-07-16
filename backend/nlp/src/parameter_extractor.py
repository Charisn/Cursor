"""Parameter extraction for room availability requests."""

import json
import re
from datetime import date, datetime, timedelta
from typing import List, Optional, Tuple

import dateparser
import vertexai
from vertexai.generative_models import GenerativeModel

from .config import get_settings
from .models import EmailMessage, ParameterExtractionResult, RoomRequest


class ParameterExtractor:
    """Extracts structured parameters from room availability requests."""
    
    def __init__(self):
        """Initialize parameter extractor."""
        self.settings = get_settings()
        
        # Initialize Vertex AI
        vertexai.init(
            project=self.settings.google_cloud_project,
            location=self.settings.vertex_ai_location
        )
        
        # Initialize Gemini model
        self.model = GenerativeModel(self.settings.gemini_model)
        
        # Parameter extraction prompt
        self.extraction_prompt = """
You are a parameter extraction system for a hotel booking system.

Extract the following information from the email text:

1. DATE: Check-in date (format: YYYY-MM-DD)
2. ROOM_COUNT: Number of rooms needed (integer, 1-10)
3. BUDGET: Budget per room per night (number, in USD)
4. VIEW_PREFERENCE: Preferred view type (ocean, city, garden, etc.)
5. SPECIAL_REQUESTS: Any special requests or notes

Email content:
Subject: {subject}
Body: {body}

Current date: {current_date}

Rules:
- Only extract information that is explicitly mentioned
- For dates, prefer specific dates over relative terms
- If budget is mentioned in total, calculate per room per night
- Use null for missing information
- Be conservative - don't guess or infer

Respond with JSON:
{{
    "date": "YYYY-MM-DD" | null,
    "room_count": integer | null,
    "budget": number | null,
    "view_preference": "string" | null,
    "special_requests": "string" | null,
    "confidence": 0.0-1.0,
    "missing_fields": ["field1", "field2"]
}}
"""
        
        # Regex patterns for common extractions
        self.date_patterns = [
            r'(\d{1,2}[/-]\d{1,2}[/-]\d{2,4})',  # MM/DD/YYYY or DD/MM/YYYY
            r'(\d{4}[/-]\d{1,2}[/-]\d{1,2})',    # YYYY/MM/DD
            r'(January|February|March|April|May|June|July|August|September|October|November|December)\s+\d{1,2},?\s+\d{4}',
            r'(Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)\s+\d{1,2},?\s+\d{4}',
        ]
        
        self.room_patterns = [
            r'(\d+)\s*(?:rooms?|bedrooms?)',
            r'(?:need|want|looking for)\s*(\d+)\s*(?:rooms?)',
            r'(\d+)\s*(?:single|double|twin|suite)',
        ]
        
        self.budget_patterns = [
            r'\$(\d+(?:\.\d{2})?)',
            r'(\d+(?:\.\d{2})?)\s*(?:dollars?|USD|usd)',
            r'budget\s*(?:of|is|:)?\s*\$?(\d+(?:\.\d{2})?)',
            r'up\s*to\s*\$?(\d+(?:\.\d{2})?)',
        ]
    
    def extract_parameters(self, email: EmailMessage) -> ParameterExtractionResult:
        """Extract parameters from email using hybrid approach."""
        try:
            # First try regex-based extraction for structured data
            regex_params = self._extract_with_regex(email)
            
            # Then use Gemini for complex extraction and validation
            gemini_params = self._extract_with_gemini(email)
            
            # Combine results, preferring Gemini for text analysis
            final_params = self._merge_extraction_results(regex_params, gemini_params)
            
            # Validate and identify missing fields
            missing_fields = self._identify_missing_fields(final_params)
            
            # Calculate confidence based on extracted fields
            confidence = self._calculate_confidence(final_params, missing_fields)
            
            return ParameterExtractionResult(
                params=final_params,
                confidence=confidence,
                missing_fields=missing_fields
            )
            
        except Exception as e:
            # Return empty result on error
            return ParameterExtractionResult(
                params=RoomRequest(),
                confidence=0.0,
                missing_fields=["date", "room_count", "budget"]
            )
    
    def _extract_with_regex(self, email: EmailMessage) -> RoomRequest:
        """Extract parameters using regex patterns."""
        text = f"{email.subject} {email.body}".lower()
        
        # Extract date
        extracted_date = self._extract_date_regex(text)
        
        # Extract room count
        room_count = self._extract_room_count_regex(text)
        
        # Extract budget
        budget = self._extract_budget_regex(text)
        
        return RoomRequest(
            date=extracted_date,
            room_count=room_count,
            budget=budget
        )
    
    def _extract_with_gemini(self, email: EmailMessage) -> RoomRequest:
        """Extract parameters using Gemini."""
        try:
            prompt = self.extraction_prompt.format(
                subject=email.subject,
                body=email.body[:1500],  # Truncate long emails
                current_date=date.today().isoformat()
            )
            
            response = self.model.generate_content(
                prompt,
                generation_config={
                    "temperature": 0.1,
                    "max_output_tokens": 512,
                }
            )
            
            # Parse response
            return self._parse_gemini_response(response.text)
            
        except Exception:
            return RoomRequest()
    
    def _parse_gemini_response(self, response_text: str) -> RoomRequest:
        """Parse Gemini response into RoomRequest."""
        try:
            # Extract JSON from response
            json_match = re.search(r'\{.*\}', response_text, re.DOTALL)
            if not json_match:
                return RoomRequest()
            
            data = json.loads(json_match.group(0))
            
            # Parse date
            date_str = data.get('date')
            parsed_date = None
            if date_str:
                try:
                    parsed_date = datetime.fromisoformat(date_str).date()
                except ValueError:
                    parsed_date = dateparser.parse(date_str)
                    if parsed_date:
                        parsed_date = parsed_date.date()
            
            return RoomRequest(
                date=parsed_date,
                room_count=data.get('room_count'),
                budget=data.get('budget'),
                view_preference=data.get('view_preference'),
                special_requests=data.get('special_requests')
            )
            
        except (json.JSONDecodeError, ValueError):
            return RoomRequest()
    
    def _extract_date_regex(self, text: str) -> Optional[date]:
        """Extract date using regex patterns."""
        for pattern in self.date_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    parsed_date = dateparser.parse(match, settings={'PREFER_DATES_FROM': 'future'})
                    if parsed_date and parsed_date.date() >= date.today():
                        return parsed_date.date()
                except:
                    continue
        return None
    
    def _extract_room_count_regex(self, text: str) -> Optional[int]:
        """Extract room count using regex patterns."""
        for pattern in self.room_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    count = int(match)
                    if 1 <= count <= 10:
                        return count
                except ValueError:
                    continue
        return None
    
    def _extract_budget_regex(self, text: str) -> Optional[float]:
        """Extract budget using regex patterns."""
        for pattern in self.budget_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                try:
                    budget = float(match)
                    if 10 <= budget <= 10000:  # Reasonable budget range
                        return budget
                except ValueError:
                    continue
        return None
    
    def _merge_extraction_results(self, regex_result: RoomRequest, gemini_result: RoomRequest) -> RoomRequest:
        """Merge results from regex and Gemini extraction."""
        return RoomRequest(
            date=gemini_result.date or regex_result.date,
            room_count=gemini_result.room_count or regex_result.room_count,
            budget=gemini_result.budget or regex_result.budget,
            view_preference=gemini_result.view_preference,  # Prefer Gemini for text analysis
            special_requests=gemini_result.special_requests
        )
    
    def _identify_missing_fields(self, params: RoomRequest) -> List[str]:
        """Identify missing critical fields."""
        missing = []
        
        if not params.date:
            missing.append("date")
        
        if not params.room_count:
            missing.append("room_count")
        
        # Budget is not always required
        
        return missing
    
    def _calculate_confidence(self, params: RoomRequest, missing_fields: List[str]) -> float:
        """Calculate confidence score based on extracted parameters."""
        total_fields = 5  # date, room_count, budget, view_preference, special_requests
        critical_fields = 2  # date, room_count
        
        # Count extracted fields
        extracted_count = 0
        if params.date:
            extracted_count += 1
        if params.room_count:
            extracted_count += 1
        if params.budget:
            extracted_count += 1
        if params.view_preference:
            extracted_count += 1
        if params.special_requests:
            extracted_count += 1
        
        # Base confidence on extracted fields
        base_confidence = extracted_count / total_fields
        
        # Penalize missing critical fields heavily
        critical_penalty = len([f for f in missing_fields if f in ["date", "room_count"]]) * 0.3
        
        confidence = max(0.0, base_confidence - critical_penalty)
        
        return round(confidence, 2)
    
    def has_sufficient_parameters(self, params: RoomRequest) -> bool:
        """Check if we have sufficient parameters to proceed."""
        return params.date is not None and params.room_count is not None 