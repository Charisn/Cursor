"""Bookings API router."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import CreateBookingRequest, BookingResponse, ErrorResponse
from ..services import BookingService

router = APIRouter(prefix="/api", tags=["bookings"])


@router.post(
    "/bookings",
    response_model=BookingResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request"},
        404: {"model": ErrorResponse, "description": "Room not found"},
        409: {"model": ErrorResponse, "description": "Room not available"},
        500: {"model": ErrorResponse, "description": "Server error"}
    },
    summary="Create Booking",
    description="Create a new booking for a customer."
)
async def create_booking(
    request: CreateBookingRequest,
    db: Session = Depends(get_db)
):
    """Create a new booking."""
    try:
        booking_service = BookingService(db)
        return booking_service.create_booking(request)
        
    except ValueError as e:
        error_msg = str(e)
        
        if "not found" in error_msg:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "Room not found",
                    "details": error_msg
                }
            )
        elif "not available" in error_msg:
            raise HTTPException(
                status_code=409,
                detail={
                    "error": "Room not available",
                    "details": error_msg
                }
            )
        else:
            raise HTTPException(
                status_code=400,
                detail={
                    "error": "Invalid request",
                    "details": error_msg
                }
            )
            
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Server error",
                "details": "An unexpected error occurred while creating the booking"
            }
        ) 