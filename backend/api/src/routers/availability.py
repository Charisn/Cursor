"""Availability API router."""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..schemas import AvailabilityRequest, AvailabilityResponse, ErrorResponse, HotelContextResponse
from ..services import RoomService

router = APIRouter(prefix="/api", tags=["availability"])


@router.post(
    "/availability",
    response_model=AvailabilityResponse,
    responses={
        400: {"model": ErrorResponse, "description": "Invalid request"},
        404: {"model": ErrorResponse, "description": "No availability"},
        500: {"model": ErrorResponse, "description": "Server error"}
    },
    summary="Check Room Availability",
    description="Get available rooms based on customer requirements. This endpoint is used by the NLP service."
)
async def check_availability(
    request: AvailabilityRequest,
    db: Session = Depends(get_db)
):
    """Check room availability based on customer criteria."""
    try:
        room_service = RoomService(db)
        response = room_service.search_available_rooms(request)
        
        if response.total_count == 0:
            raise HTTPException(
                status_code=404,
                detail={
                    "error": "No availability",
                    "details": "No rooms available for the specified criteria"
                }
            )
        
        return response
        
    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail={
                "error": "Invalid request",
                "details": str(e)
            }
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Server error",
                "details": "An unexpected error occurred while checking availability"
            }
        )


@router.get(
    "/rooms/context",
    response_model=HotelContextResponse,
    responses={
        500: {"model": ErrorResponse, "description": "Server error"}
    },
    summary="Get Hotel Context",
    description="Get general information about the hotel for better responses. Used by NLP service."
)
async def get_hotel_context(db: Session = Depends(get_db)):
    """Get hotel context information."""
    try:
        room_service = RoomService(db)
        return room_service.get_hotel_context()
        
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail={
                "error": "Server error",
                "details": "An unexpected error occurred while fetching hotel context"
            }
        ) 