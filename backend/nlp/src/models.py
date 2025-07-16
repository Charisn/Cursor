"""Data models for NLP data structures using dataclasses."""

from dataclasses import dataclass, field
from datetime import date, datetime
from enum import Enum
from typing import Any, Dict, List, Optional


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


@dataclass
class RoomRequest:
    """Parameters extracted from room availability requests."""
    
    date: Optional[date] = None
    room_count: Optional[int] = None
    budget: Optional[float] = None
    view_preference: Optional[str] = None
    special_requests: Optional[str] = None


@dataclass
class EmailMessage:
    """Parsed email message structure."""
    
    subject: str
    body: str
    sender: str
    received_at: datetime
    message_id: str


@dataclass
class IntentClassificationResult:
    """Result of intent classification."""
    
    intent: str
    confidence: float
    reasoning: Optional[str] = None


@dataclass
class ParameterExtractionResult:
    """Result of parameter extraction from email."""
    
    params: RoomRequest
    confidence: float
    missing_fields: List[str] = field(default_factory=list)


@dataclass
class NLPProcessingResult:
    """Complete result of NLP processing pipeline."""
    
    intent: str
    confidence: float
    next_action: str
    processing_time_ms: float
    params: Optional[RoomRequest] = None
    clarification_needed: bool = False
    clarification_questions: List[str] = field(default_factory=list)


@dataclass
class APIAvailabilityRequest:
    """Request format for backend availability API."""
    
    check_in_date: date
    room_count: int = 1
    max_budget: Optional[float] = None
    view_preference: Optional[str] = None


@dataclass
class APIAvailabilityResponse:
    """Response format from backend availability API."""
    
    available_rooms: List[Dict[str, Any]] = field(default_factory=list)
    total_count: int = 0
    suggested_alternatives: List[Dict[str, Any]] = field(default_factory=list)
    message: Optional[str] = None 