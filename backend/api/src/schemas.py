"""Pydantic schemas for API requests and responses."""

from datetime import date, datetime
from typing import List, Optional, Dict, Any
from enum import Enum

from pydantic import BaseModel, Field, validator

from .models import RoomType, ViewType, BookingStatus


# Request schemas (matching NLP expectations)
class AvailabilityRequest(BaseModel):
    """Room availability request schema."""
    
    check_in_date: date = Field(..., description="Check-in date in YYYY-MM-DD format")
    room_count: int = Field(..., ge=1, le=10, description="Number of rooms needed")
    max_budget: Optional[float] = Field(None, gt=0, description="Maximum budget per room per night")
    view_preference: Optional[str] = Field(None, description="Preferred view type")
    
    @validator('check_in_date')
    def validate_check_in_date(cls, v):
        """Validate check-in date is not in the past."""
        if v < date.today():
            raise ValueError("Check-in date cannot be in the past")
        return v
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "check_in_date": "2025-08-15",
                "room_count": 2,
                "max_budget": 150.0,
                "view_preference": "ocean"
            }
        }


# Response schemas
class RoomResponse(BaseModel):
    """Individual room response schema."""
    
    room_id: str = Field(..., description="Unique room identifier")
    room_type: str = Field(..., description="Type of room")
    price_per_night: float = Field(..., description="Price per night in USD")
    view_type: str = Field(..., description="View type")
    amenities: List[str] = Field(default_factory=list, description="List of amenities")
    availability_date: date = Field(..., description="Date this room is available")
    description: str = Field(..., description="Room description")
    
    # Additional details
    max_occupancy: Optional[int] = Field(None, description="Maximum occupancy")
    square_feet: Optional[int] = Field(None, description="Room size in square feet")
    has_balcony: Optional[bool] = Field(None, description="Has balcony")
    has_kitchenette: Optional[bool] = Field(None, description="Has kitchenette")
    has_jacuzzi: Optional[bool] = Field(None, description="Has jacuzzi")
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "room_id": "101",
                "room_type": "Ocean View Suite",
                "price_per_night": 120.0,
                "view_type": "ocean",
                "amenities": ["WiFi", "Air Conditioning", "Mini Bar"],
                "availability_date": "2025-08-15",
                "description": "Spacious suite with panoramic ocean views",
                "max_occupancy": 4,
                "square_feet": 450,
                "has_balcony": True,
                "has_kitchenette": False,
                "has_jacuzzi": True
            }
        }


class AlternativeDateResponse(BaseModel):
    """Alternative date suggestion schema."""
    
    check_in_date: date = Field(..., description="Alternative check-in date")
    available_rooms: int = Field(..., description="Number of available rooms on this date")
    message: str = Field(..., description="Message about this alternative")
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "check_in_date": "2025-08-16",
                "available_rooms": 12,
                "message": "More rooms available the next day"
            }
        }


class AvailabilityResponse(BaseModel):
    """Room availability response schema (matching NLP expectations)."""
    
    available_rooms: List[RoomResponse] = Field(default_factory=list, description="Available rooms")
    total_count: int = Field(..., ge=0, description="Total number of available rooms")
    suggested_alternatives: List[AlternativeDateResponse] = Field(
        default_factory=list, 
        description="Alternative dates/options if limited availability"
    )
    message: Optional[str] = Field(None, description="Additional message about availability")
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "available_rooms": [
                    {
                        "room_id": "101",
                        "room_type": "Ocean View Suite",
                        "price_per_night": 120.0,
                        "view_type": "ocean",
                        "amenities": ["WiFi", "Air Conditioning", "Mini Bar"],
                        "availability_date": "2025-08-15",
                        "description": "Spacious suite with panoramic ocean views"
                    }
                ],
                "total_count": 8,
                "suggested_alternatives": [
                    {
                        "check_in_date": "2025-08-16",
                        "available_rooms": 12,
                        "message": "More rooms available the next day"
                    }
                ],
                "message": "Found 8 available rooms matching your criteria"
            }
        }


class RoomTypeInfo(BaseModel):
    """Room type information schema."""
    
    type: str = Field(..., description="Room type name")
    base_price_range: List[float] = Field(..., description="[min_price, max_price] range")
    capacity: int = Field(..., description="Maximum capacity")
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "type": "Ocean View Suite",
                "base_price_range": [150, 250],
                "capacity": 4
            }
        }


class HotelPolicies(BaseModel):
    """Hotel policies schema."""
    
    check_in_time: str = Field(..., description="Check-in time")
    check_out_time: str = Field(..., description="Check-out time")
    cancellation_policy: str = Field(..., description="Cancellation policy description")
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "check_in_time": "15:00",
                "check_out_time": "11:00",
                "cancellation_policy": "Free cancellation up to 24 hours before check-in"
            }
        }


class HotelContextResponse(BaseModel):
    """Hotel context response schema (matching NLP expectations)."""
    
    hotel_name: str = Field(..., description="Hotel name")
    location: str = Field(..., description="Hotel location")
    amenities: List[str] = Field(default_factory=list, description="Hotel amenities")
    room_types: List[RoomTypeInfo] = Field(default_factory=list, description="Available room types")
    policies: HotelPolicies = Field(..., description="Hotel policies")
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "hotel_name": "Staydesk Resort",
                "location": "Miami Beach, FL",
                "amenities": ["Pool", "Spa", "Restaurant", "Gym", "Beach Access"],
                "room_types": [
                    {
                        "type": "Standard Room",
                        "base_price_range": [80, 120],
                        "capacity": 2
                    },
                    {
                        "type": "Ocean View Suite",
                        "base_price_range": [150, 250],
                        "capacity": 4
                    }
                ],
                "policies": {
                    "check_in_time": "15:00",
                    "check_out_time": "11:00",
                    "cancellation_policy": "Free cancellation up to 24 hours before check-in"
                }
            }
        }


# Error response schemas
class ErrorResponse(BaseModel):
    """Error response schema."""
    
    error: str = Field(..., description="Error type or title")
    details: str = Field(..., description="Detailed error message")
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "error": "Invalid request",
                "details": "check_in_date must be in future"
            }
        }


# Booking schemas
class CreateBookingRequest(BaseModel):
    """Create booking request schema."""
    
    customer_email: str = Field(..., description="Customer email address")
    room_id: int = Field(..., description="Room ID to book")
    check_in_date: date = Field(..., description="Check-in date")
    check_out_date: date = Field(..., description="Check-out date")
    guest_count: int = Field(1, ge=1, le=10, description="Number of guests")
    special_requests: Optional[str] = Field(None, description="Special requests")
    
    @validator('check_out_date')
    def validate_check_out_after_check_in(cls, v, values):
        """Validate check-out date is after check-in date."""
        if 'check_in_date' in values and v <= values['check_in_date']:
            raise ValueError("Check-out date must be after check-in date")
        return v
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "customer_email": "john.doe@example.com",
                "room_id": 101,
                "check_in_date": "2025-08-15",
                "check_out_date": "2025-08-17",
                "guest_count": 2,
                "special_requests": "Ocean view room preferred"
            }
        }


class BookingResponse(BaseModel):
    """Booking response schema."""
    
    booking_id: int = Field(..., description="Booking ID")
    confirmation_number: str = Field(..., description="Booking confirmation number")
    customer_email: str = Field(..., description="Customer email")
    room_number: str = Field(..., description="Room number")
    check_in_date: date = Field(..., description="Check-in date")
    check_out_date: date = Field(..., description="Check-out date")
    guest_count: int = Field(..., description="Number of guests")
    total_amount: float = Field(..., description="Total booking amount")
    status: str = Field(..., description="Booking status")
    special_requests: Optional[str] = Field(None, description="Special requests")
    created_at: datetime = Field(..., description="Booking creation timestamp")
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "booking_id": 123,
                "confirmation_number": "STD-2024-001",
                "customer_email": "john.doe@example.com",
                "room_number": "101",
                "check_in_date": "2025-08-15",
                "check_out_date": "2025-08-17",
                "guest_count": 2,
                "total_amount": 240.0,
                "status": "confirmed",
                "special_requests": "Ocean view room preferred",
                "created_at": "2024-01-15T10:30:00Z"
            }
        }


# Statistics and monitoring schemas
class APIStatsResponse(BaseModel):
    """API statistics response schema."""
    
    total_requests: int = Field(..., description="Total API requests")
    availability_requests: int = Field(..., description="Availability requests count")
    booking_requests: int = Field(..., description="Booking requests count")
    error_rate: float = Field(..., description="Error rate percentage")
    average_response_time_ms: float = Field(..., description="Average response time in milliseconds")
    
    class Config:
        """Pydantic configuration."""
        schema_extra = {
            "example": {
                "total_requests": 1250,
                "availability_requests": 890,
                "booking_requests": 123,
                "error_rate": 2.5,
                "average_response_time_ms": 85.3
            }
        } 