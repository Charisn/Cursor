"""Pydantic models for NLP data structures."""

from datetime import date, datetime
from enum import Enum
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, validator


class IntentType(str, Enum):
    """Possible intent types for email classification."""
    
    AVAILABILITY_REQUEST = "availability_request"
    GENERIC_QUERY = "generic_query"
    IGNORE = "ignore"


class NextAction(str, Enum):
    """Possible next actions after intent classification."""
    
    CALL_AVAILABILITY_API = "call_availability_api"
    SEND_GENERIC_REPLY = "send_generic_reply"
    REQUEST_CLARIFICATION = "request_clarification"
    IGNORE_EMAIL = "ignore_email"


class RoomRequest(BaseModel):
    """Parameters extracted from room availability requests."""
    
    date: Optional[date] = Field(None, description="Requested check-in date")
    room_count: Optional[int] = Field(None, ge=1, le=10, description="Number of rooms")
    budget: Optional[float] = Field(None, gt=0, description="Budget per room per night")
    view_preference: Optional[str] = Field(None, description="Preferred view type")
    special_requests: Optional[str] = Field(None, description="Special requests or notes")
    
    @validator('date')
    def validate_date_not_past(cls, v):
        """Ensure date is not in the past."""
        if v and v < date.today():
            raise ValueError("Date cannot be in the past")
        return v


class EmailMessage(BaseModel):
    """Parsed email message structure."""
    
    subject: str = Field(..., description="Email subject line")
    body: str = Field(..., description="Cleaned email body text")
    sender: str = Field(..., description="Sender email address")
    received_at: datetime = Field(..., description="When email was received")
    message_id: str = Field(..., description="Unique message identifier")
    
    @validator('body')
    def validate_body_not_empty(cls, v):
        """Ensure email body is not empty after cleaning."""
        if not v.strip():
            raise ValueError("Email body cannot be empty")
        return v.strip()


class IntentClassificationResult(BaseModel):
    """Result of intent classification."""
    
    intent: IntentType = Field(..., description="Classified intent type")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Classification confidence")
    reasoning: Optional[str] = Field(None, description="Explanation of classification")


class ParameterExtractionResult(BaseModel):
    """Result of parameter extraction from email."""
    
    params: RoomRequest = Field(..., description="Extracted parameters")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Extraction confidence")
    missing_fields: List[str] = Field(default_factory=list, description="Required fields that are missing")


class NLPProcessingResult(BaseModel):
    """Complete result of NLP processing pipeline."""
    
    intent: IntentType = Field(..., description="Classified intent")
    params: Optional[RoomRequest] = Field(None, description="Extracted parameters if available")
    confidence: float = Field(..., ge=0.0, le=1.0, description="Overall confidence score")
    next_action: NextAction = Field(..., description="Recommended next action")
    clarification_needed: bool = Field(False, description="Whether clarification is needed")
    clarification_questions: List[str] = Field(default_factory=list, description="Questions to ask for clarification")
    processing_time_ms: float = Field(..., gt=0, description="Processing time in milliseconds")
    
    class Config:
        """Pydantic configuration."""
        use_enum_values = True


class APIAvailabilityRequest(BaseModel):
    """Request format for backend availability API."""
    
    check_in_date: date = Field(..., description="Check-in date")
    room_count: int = Field(1, ge=1, le=10, description="Number of rooms needed")
    max_budget: Optional[float] = Field(None, gt=0, description="Maximum budget per room")
    view_preference: Optional[str] = Field(None, description="Preferred view type")
    
    class Config:
        """Pydantic configuration."""
        json_encoders = {
            date: lambda v: v.isoformat()
        }


class APIAvailabilityResponse(BaseModel):
    """Response format from backend availability API."""
    
    available_rooms: List[Dict[str, Any]] = Field(default_factory=list, description="Available rooms")
    total_count: int = Field(0, ge=0, description="Total number of available rooms")
    suggested_alternatives: List[Dict[str, Any]] = Field(default_factory=list, description="Alternative suggestions")
    message: Optional[str] = Field(None, description="Additional message from API") 