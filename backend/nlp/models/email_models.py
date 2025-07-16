"""
Pydantic models for email processing
"""
from pydantic import BaseModel, Field, EmailStr, field_validator
from typing import Optional, List, Dict, Any, Literal
from datetime import datetime, date
from enum import Enum

class EmailRequest(BaseModel):
    """Incoming email request model"""
    sender_email: EmailStr
    subject: str
    content: str
    received_at: datetime = Field(default_factory=datetime.now)
    
    @field_validator('content')
    @classmethod
    def validate_content_length(cls, v):
        if len(v) > 10000:
            raise ValueError('Email content too long')
        return v

class BookingParameters(BaseModel):
    """Extracted booking parameters from email"""
    check_in_date: Optional[date] = None
    check_out_date: Optional[date] = None
    guests: Optional[int] = None
    room_type: Optional[str] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    special_requirements: List[str] = Field(default_factory=list)
    location_preferences: List[str] = Field(default_factory=list)
    
    @field_validator('guests')
    @classmethod
    def validate_guests(cls, v):
        if v is not None and v <= 0:
            raise ValueError('Number of guests must be positive')
        return v
    
    @field_validator('check_out_date')
    @classmethod
    def validate_checkout_after_checkin(cls, v, info):
        if v is not None and info.data.get('check_in_date') is not None:
            if v <= info.data['check_in_date']:
                raise ValueError('Check-out date must be after check-in date')
        return v

class ValidationResult(BaseModel):
    """Parameter validation result"""
    is_valid: bool
    confidence: float
    missing_fields: List[str] = Field(default_factory=list)
    invalid_fields: List[str] = Field(default_factory=list)

class ProcessedEmail(BaseModel):
    """Processed email result"""
    intent: Literal["room_availability", "generic", "complaint", "cancellation"]
    extracted_parameters: Dict[str, Any] = Field(default_factory=dict)
    confidence_score: float = Field(ge=0.0, le=1.0)
    requires_clarification: bool = False
    clarification_needed: List[str] = Field(default_factory=list)
    response_type: Literal["availability_check", "clarification_request", "generic_response"]
    
class ResponseTemplate(BaseModel):
    """Email response template"""
    template_type: str
    subject: str
    content: str
    variables: Dict[str, Any] = Field(default_factory=dict)