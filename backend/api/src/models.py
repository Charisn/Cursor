"""SQLAlchemy database models."""

from datetime import date, datetime
from enum import Enum
from typing import List, Optional

from sqlalchemy import (
    Boolean, Column, Date, DateTime, Float, ForeignKey, 
    Integer, String, Text, Enum as SQLEnum, UniqueConstraint
)
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import sqlalchemy

from .database import Base


class RoomType(str, Enum):
    """Room type enumeration."""
    STANDARD = "standard"
    DELUXE = "deluxe"
    SUITE = "suite"
    PENTHOUSE = "penthouse"


class ViewType(str, Enum):
    """View type enumeration."""
    OCEAN = "ocean"
    CITY = "city"
    GARDEN = "garden"
    POOL = "pool"
    MOUNTAIN = "mountain"


class BookingStatus(str, Enum):
    """Booking status enumeration."""
    PENDING = "pending"
    CONFIRMED = "confirmed"
    CANCELLED = "cancelled"
    COMPLETED = "completed"


class Room(Base):
    """Room model."""
    
    __tablename__ = "rooms"
    
    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(String(10), unique=True, index=True, nullable=False)
    room_type = Column(SQLEnum(RoomType), nullable=False)
    view_type = Column(SQLEnum(ViewType), nullable=False)
    
    # Pricing
    base_price = Column(Float, nullable=False)
    weekend_price = Column(Float, nullable=True)  # Optional weekend pricing
    
    # Capacity and features
    max_occupancy = Column(Integer, nullable=False, default=2)
    bed_count = Column(Integer, nullable=False, default=1)
    bathroom_count = Column(Integer, nullable=False, default=1)
    
    # Room features
    has_balcony = Column(Boolean, default=False)
    has_kitchenette = Column(Boolean, default=False)
    has_jacuzzi = Column(Boolean, default=False)
    square_feet = Column(Integer, nullable=True)
    
    # Amenities (JSON-like string storage)
    amenities = Column(Text, nullable=True)  # Comma-separated amenities
    
    # Description
    description = Column(Text, nullable=True)
    
    # Availability
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    bookings = relationship("Booking", back_populates="room")
    availability = relationship("RoomAvailability", back_populates="room")


class RoomAvailability(Base):
    """Room availability model for specific dates."""
    
    __tablename__ = "room_availability"
    
    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    date = Column(Date, nullable=False, index=True)
    
    # Availability status
    is_available = Column(Boolean, default=True)
    is_maintenance = Column(Boolean, default=False)
    
    # Dynamic pricing
    price_override = Column(Float, nullable=True)  # Override room base price for this date
    
    # Notes
    notes = Column(Text, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    room = relationship("Room", back_populates="availability")
    
    # Unique constraint on room_id and date
    __table_args__ = (
        sqlalchemy.UniqueConstraint('room_id', 'date', name='_room_date_uc'),
    )


class Customer(Base):
    """Customer model."""
    
    __tablename__ = "customers"
    
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    
    # Personal information
    first_name = Column(String(100), nullable=True)
    last_name = Column(String(100), nullable=True)
    phone = Column(String(20), nullable=True)
    
    # Preferences
    preferred_room_type = Column(SQLEnum(RoomType), nullable=True)
    preferred_view_type = Column(SQLEnum(ViewType), nullable=True)
    
    # Customer status
    is_vip = Column(Boolean, default=False)
    is_active = Column(Boolean, default=True)
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    bookings = relationship("Booking", back_populates="customer")


class Booking(Base):
    """Booking model."""
    
    __tablename__ = "bookings"
    
    id = Column(Integer, primary_key=True, index=True)
    confirmation_number = Column(String(20), unique=True, index=True, nullable=False)
    
    # Foreign keys
    customer_id = Column(Integer, ForeignKey("customers.id"), nullable=False)
    room_id = Column(Integer, ForeignKey("rooms.id"), nullable=False)
    
    # Booking details
    check_in_date = Column(Date, nullable=False, index=True)
    check_out_date = Column(Date, nullable=False, index=True)
    guest_count = Column(Integer, nullable=False, default=1)
    
    # Pricing
    total_amount = Column(Float, nullable=False)
    amount_paid = Column(Float, default=0.0)
    
    # Status
    status = Column(SQLEnum(BookingStatus), default=BookingStatus.PENDING)
    
    # Special requests
    special_requests = Column(Text, nullable=True)
    
    # Booking source
    booking_source = Column(String(50), default="email")  # email, website, phone, etc.
    
    # Timestamps
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    cancelled_at = Column(DateTime(timezone=True), nullable=True)
    
    # Relationships
    customer = relationship("Customer", back_populates="bookings")
    room = relationship("Room", back_populates="bookings")


class EmailLog(Base):
    """Email processing log model."""
    
    __tablename__ = "email_logs"
    
    id = Column(Integer, primary_key=True, index=True)
    message_id = Column(String(255), unique=True, index=True, nullable=False)
    
    # Email details
    sender = Column(String(255), nullable=False, index=True)
    subject = Column(String(500), nullable=False)
    body_snippet = Column(Text, nullable=True)  # First 1000 chars
    
    # NLP processing results
    intent = Column(String(50), nullable=True)
    confidence = Column(Float, nullable=True)
    next_action = Column(String(50), nullable=True)
    
    # Extracted parameters (JSON-like storage)
    extracted_date = Column(Date, nullable=True)
    extracted_room_count = Column(Integer, nullable=True)
    extracted_budget = Column(Float, nullable=True)
    extracted_view_preference = Column(String(50), nullable=True)
    extracted_special_requests = Column(Text, nullable=True)
    
    # Processing metadata
    processing_time_ms = Column(Float, nullable=True)
    clarification_needed = Column(Boolean, default=False)
    
    # Response tracking
    response_sent = Column(Boolean, default=False)
    response_type = Column(String(50), nullable=True)  # availability, clarification, generic
    
    # Timestamps
    received_at = Column(DateTime(timezone=True), nullable=False)
    processed_at = Column(DateTime(timezone=True), server_default=func.now())
    responded_at = Column(DateTime(timezone=True), nullable=True) 