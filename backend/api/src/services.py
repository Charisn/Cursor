"""Business logic services for room availability and bookings."""

import random
import string
from datetime import date, datetime, timedelta
from typing import List, Optional, Tuple

from sqlalchemy.orm import Session
from sqlalchemy import and_, or_, func

from .models import Room, RoomAvailability, Booking, Customer, RoomType, ViewType, BookingStatus
from .schemas import (
    AvailabilityRequest, AvailabilityResponse, RoomResponse, 
    AlternativeDateResponse, CreateBookingRequest, BookingResponse,
    HotelContextResponse, RoomTypeInfo, HotelPolicies
)
from .config import get_settings

settings = get_settings()


class RoomService:
    """Service for room-related operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def search_available_rooms(self, request: AvailabilityRequest) -> AvailabilityResponse:
        """Search for available rooms based on criteria."""
        
        # Base query for available rooms
        query = (
            self.db.query(Room)
            .filter(Room.is_active == True)
        )
        
        # Filter by view preference if specified
        if request.view_preference:
            view_preference_lower = request.view_preference.lower()
            # Map common view preferences to our enum values
            view_mapping = {
                'ocean': ViewType.OCEAN,
                'sea': ViewType.OCEAN,
                'water': ViewType.OCEAN,
                'city': ViewType.CITY,
                'garden': ViewType.GARDEN,
                'pool': ViewType.POOL,
                'mountain': ViewType.MOUNTAIN,
            }
            
            if view_preference_lower in view_mapping:
                query = query.filter(Room.view_type == view_mapping[view_preference_lower])
        
        # Filter by budget if specified
        if request.max_budget:
            query = query.filter(
                or_(
                    Room.base_price <= request.max_budget,
                    Room.weekend_price <= request.max_budget
                )
            )
        
        # Check availability for the specific date
        available_rooms = []
        for room in query.all():
            if self._is_room_available(room.id, request.check_in_date):
                # Calculate price for the date
                price = self._calculate_room_price(room, request.check_in_date)
                
                # Apply budget filter to calculated price
                if request.max_budget and price > request.max_budget:
                    continue
                
                # Convert to response format
                room_response = self._room_to_response(room, request.check_in_date, price)
                available_rooms.append(room_response)
        
        # Sort by price and limit results
        available_rooms.sort(key=lambda r: r.price_per_night)
        total_count = len(available_rooms)
        
        # Return top 10 rooms for the requested count
        if request.room_count > 1:
            # For multi-room requests, ensure we have enough rooms
            available_rooms = available_rooms[:min(10, request.room_count * 2)]
        else:
            available_rooms = available_rooms[:10]
        
        # Generate suggested alternatives if limited availability
        suggested_alternatives = []
        if total_count < request.room_count:
            suggested_alternatives = self._get_alternative_dates(request, days_ahead=7)
        
        # Generate response message
        if total_count == 0:
            message = "No rooms available for the specified criteria"
        elif total_count < request.room_count:
            message = f"Found {total_count} available rooms (requested {request.room_count})"
        else:
            message = f"Found {total_count} available rooms matching your criteria"
        
        return AvailabilityResponse(
            available_rooms=available_rooms,
            total_count=total_count,
            suggested_alternatives=suggested_alternatives,
            message=message
        )
    
    def _is_room_available(self, room_id: int, check_date: date) -> bool:
        """Check if a room is available on a specific date."""
        
        # Check for existing bookings
        existing_booking = (
            self.db.query(Booking)
            .filter(
                and_(
                    Booking.room_id == room_id,
                    Booking.check_in_date <= check_date,
                    Booking.check_out_date > check_date,
                    Booking.status.in_([BookingStatus.CONFIRMED, BookingStatus.PENDING])
                )
            )
            .first()
        )
        
        if existing_booking:
            return False
        
        # Check room availability settings
        availability = (
            self.db.query(RoomAvailability)
            .filter(
                and_(
                    RoomAvailability.room_id == room_id,
                    RoomAvailability.date == check_date
                )
            )
            .first()
        )
        
        if availability:
            return availability.is_available and not availability.is_maintenance
        
        # Default to available if no specific availability record
        return True
    
    def _calculate_room_price(self, room: Room, check_date: date) -> float:
        """Calculate room price for a specific date."""
        
        # Check for price override
        availability = (
            self.db.query(RoomAvailability)
            .filter(
                and_(
                    RoomAvailability.room_id == room.id,
                    RoomAvailability.date == check_date
                )
            )
            .first()
        )
        
        if availability and availability.price_override:
            return availability.price_override
        
        # Use weekend pricing if applicable and available
        if check_date.weekday() >= 5 and room.weekend_price:  # Saturday or Sunday
            return room.weekend_price
        
        return room.base_price
    
    def _room_to_response(self, room: Room, availability_date: date, price: float) -> RoomResponse:
        """Convert Room model to RoomResponse schema."""
        
        # Parse amenities from string
        amenities = []
        if room.amenities:
            amenities = [a.strip() for a in room.amenities.split(',') if a.strip()]
        
        # Format room type for display
        room_type_display = room.room_type.value.replace('_', ' ').title()
        
        return RoomResponse(
            room_id=str(room.room_number),
            room_type=room_type_display,
            price_per_night=price,
            view_type=room.view_type.value,
            amenities=amenities,
            availability_date=availability_date,
            description=room.description or f"{room_type_display} with {room.view_type.value} view",
            max_occupancy=room.max_occupancy,
            square_feet=room.square_feet,
            has_balcony=room.has_balcony,
            has_kitchenette=room.has_kitchenette,
            has_jacuzzi=room.has_jacuzzi
        )
    
    def _get_alternative_dates(self, request: AvailabilityRequest, days_ahead: int = 7) -> List[AlternativeDateResponse]:
        """Get alternative dates with better availability."""
        alternatives = []
        
        for days_offset in range(1, days_ahead + 1):
            alt_date = request.check_in_date + timedelta(days=days_offset)
            
            # Create a new request for the alternative date
            alt_request = AvailabilityRequest(
                check_in_date=alt_date,
                room_count=request.room_count,
                max_budget=request.max_budget,
                view_preference=request.view_preference
            )
            
            # Get available rooms for this date
            alt_response = self.search_available_rooms(alt_request)
            
            if alt_response.total_count >= request.room_count:
                message = f"Better availability on {alt_date.strftime('%B %d')}"
                if alt_response.total_count > request.room_count * 2:
                    message = f"Excellent availability on {alt_date.strftime('%B %d')}"
                
                alternatives.append(AlternativeDateResponse(
                    check_in_date=alt_date,
                    available_rooms=alt_response.total_count,
                    message=message
                ))
                
                # Return max 3 alternatives
                if len(alternatives) >= 3:
                    break
        
        return alternatives
    
    def get_hotel_context(self) -> HotelContextResponse:
        """Get hotel context information."""
        
        # Get room type statistics
        room_types = []
        for room_type in RoomType:
            rooms = (
                self.db.query(Room)
                .filter(
                    and_(
                        Room.room_type == room_type,
                        Room.is_active == True
                    )
                )
                .all()
            )
            
            if rooms:
                prices = [room.base_price for room in rooms]
                room_types.append(RoomTypeInfo(
                    type=room_type.value.replace('_', ' ').title(),
                    base_price_range=[min(prices), max(prices)],
                    capacity=max(room.max_occupancy for room in rooms)
                ))
        
        # Hotel amenities
        amenities = [
            "Pool", "Spa", "Restaurant", "Gym", "Beach Access",
            "WiFi", "Room Service", "Concierge", "Business Center",
            "Parking", "Pet Friendly"
        ]
        
        # Policies
        policies = HotelPolicies(
            check_in_time=settings.default_check_in_time,
            check_out_time=settings.default_check_out_time,
            cancellation_policy=f"Free cancellation up to {settings.cancellation_hours} hours before check-in"
        )
        
        return HotelContextResponse(
            hotel_name=settings.hotel_name,
            location=settings.hotel_location,
            amenities=amenities,
            room_types=room_types,
            policies=policies
        )


class BookingService:
    """Service for booking-related operations."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def create_booking(self, request: CreateBookingRequest) -> BookingResponse:
        """Create a new booking."""
        
        # Get or create customer
        customer = self._get_or_create_customer(request.customer_email)
        
        # Validate room exists and is available
        room = self.db.query(Room).filter(Room.id == request.room_id).first()
        if not room:
            raise ValueError(f"Room with ID {request.room_id} not found")
        
        # Check availability for all nights
        nights = (request.check_out_date - request.check_in_date).days
        if nights <= 0:
            raise ValueError("Check-out date must be after check-in date")
        
        for night in range(nights):
            check_date = request.check_in_date + timedelta(days=night)
            room_service = RoomService(self.db)
            if not room_service._is_room_available(room.id, check_date):
                raise ValueError(f"Room is not available on {check_date}")
        
        # Calculate total amount
        total_amount = 0.0
        room_service = RoomService(self.db)
        for night in range(nights):
            check_date = request.check_in_date + timedelta(days=night)
            price = room_service._calculate_room_price(room, check_date)
            total_amount += price
        
        # Generate confirmation number
        confirmation_number = self._generate_confirmation_number()
        
        # Create booking
        booking = Booking(
            confirmation_number=confirmation_number,
            customer_id=customer.id,
            room_id=room.id,
            check_in_date=request.check_in_date,
            check_out_date=request.check_out_date,
            guest_count=request.guest_count,
            total_amount=total_amount,
            status=BookingStatus.CONFIRMED,
            special_requests=request.special_requests,
            booking_source="api"
        )
        
        self.db.add(booking)
        self.db.commit()
        self.db.refresh(booking)
        
        return BookingResponse(
            booking_id=booking.id,
            confirmation_number=booking.confirmation_number,
            customer_email=customer.email,
            room_number=room.room_number,
            check_in_date=booking.check_in_date,
            check_out_date=booking.check_out_date,
            guest_count=booking.guest_count,
            total_amount=booking.total_amount,
            status=booking.status.value,
            special_requests=booking.special_requests,
            created_at=booking.created_at
        )
    
    def _get_or_create_customer(self, email: str) -> Customer:
        """Get existing customer or create new one."""
        customer = self.db.query(Customer).filter(Customer.email == email).first()
        
        if not customer:
            customer = Customer(email=email)
            self.db.add(customer)
            self.db.commit()
            self.db.refresh(customer)
        
        return customer
    
    def _generate_confirmation_number(self) -> str:
        """Generate unique confirmation number."""
        while True:
            # Format: STD-YYYY-XXX (STD = Staydesk)
            year = datetime.now().year
            suffix = ''.join(random.choices(string.digits, k=3))
            confirmation_number = f"STD-{year}-{suffix}"
            
            # Check if it already exists
            existing = (
                self.db.query(Booking)
                .filter(Booking.confirmation_number == confirmation_number)
                .first()
            )
            
            if not existing:
                return confirmation_number 