"""Comprehensive API tests for all endpoints and scenarios."""

import pytest
from datetime import date, timedelta
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app
from src.database import get_db, Base
from src.utils.seed_data import initialize_sample_data

# Create test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    """Override database dependency for testing."""
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

# Create test client
client = TestClient(app)


@pytest.fixture(scope="module")
def setup_database():
    """Set up test database."""
    Base.metadata.create_all(bind=engine)
    
    # Initialize test data
    db = TestingSessionLocal()
    try:
        initialize_sample_data()
    finally:
        db.close()
    
    yield
    
    Base.metadata.drop_all(bind=engine)


class TestHealthEndpoints:
    """Test health and root endpoints."""
    
    def test_root_endpoint(self, setup_database):
        """Test root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["service"] == "Staydesk API"
        assert data["version"] == "1.0.0"
        assert "endpoints" in data
    
    def test_health_endpoint(self, setup_database):
        """Test health check endpoint."""
        response = client.get("/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data


class TestAvailabilityEndpoints:
    """Test availability-related endpoints."""
    
    def test_check_availability_valid_request(self, setup_database):
        """Test availability check with valid request."""
        future_date = (date.today() + timedelta(days=30)).isoformat()
        
        request_data = {
            "check_in_date": future_date,
            "room_count": 1,
            "max_budget": 200.0,
            "view_preference": "ocean"
        }
        
        response = client.post("/api/availability", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "available_rooms" in data
        assert "total_count" in data
        assert "message" in data
        assert isinstance(data["available_rooms"], list)
        assert isinstance(data["total_count"], int)
        
        # Should have ocean view rooms within budget
        if data["available_rooms"]:
            room = data["available_rooms"][0]
            assert "room_id" in room
            assert "price_per_night" in room
            assert room["price_per_night"] <= 200.0
            assert room["view_type"] == "ocean"
    
    def test_check_availability_multiple_rooms(self, setup_database):
        """Test availability check for multiple rooms."""
        future_date = (date.today() + timedelta(days=30)).isoformat()
        
        request_data = {
            "check_in_date": future_date,
            "room_count": 3,
            "max_budget": 150.0
        }
        
        response = client.post("/api/availability", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["total_count"] >= 0
        
        # If not enough rooms, should suggest alternatives
        if data["total_count"] < 3:
            assert "suggested_alternatives" in data
    
    def test_check_availability_high_budget_luxury(self, setup_database):
        """Test availability for luxury rooms with high budget."""
        future_date = (date.today() + timedelta(days=30)).isoformat()
        
        request_data = {
            "check_in_date": future_date,
            "room_count": 1,
            "max_budget": 500.0
        }
        
        response = client.post("/api/availability", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        # Should include penthouse and suites
        assert data["total_count"] > 0
    
    def test_check_availability_low_budget(self, setup_database):
        """Test availability with very low budget."""
        future_date = (date.today() + timedelta(days=30)).isoformat()
        
        request_data = {
            "check_in_date": future_date,
            "room_count": 1,
            "max_budget": 50.0
        }
        
        response = client.post("/api/availability", json=request_data)
        
        # Might be 404 if no rooms in budget, or 200 with empty results
        assert response.status_code in [200, 404]
        
        if response.status_code == 200:
            data = response.json()
            assert data["total_count"] == 0
    
    def test_check_availability_past_date(self, setup_database):
        """Test availability check with past date."""
        past_date = (date.today() - timedelta(days=1)).isoformat()
        
        request_data = {
            "check_in_date": past_date,
            "room_count": 1
        }
        
        response = client.post("/api/availability", json=request_data)
        assert response.status_code == 422  # Validation error
    
    def test_check_availability_invalid_room_count(self, setup_database):
        """Test availability check with invalid room count."""
        future_date = (date.today() + timedelta(days=30)).isoformat()
        
        request_data = {
            "check_in_date": future_date,
            "room_count": 0  # Invalid
        }
        
        response = client.post("/api/availability", json=request_data)
        assert response.status_code == 422  # Validation error
    
    def test_get_hotel_context(self, setup_database):
        """Test hotel context endpoint."""
        response = client.get("/api/rooms/context")
        assert response.status_code == 200
        
        data = response.json()
        assert "hotel_name" in data
        assert "location" in data
        assert "amenities" in data
        assert "room_types" in data
        assert "policies" in data
        
        assert data["hotel_name"] == "Staydesk Resort"
        assert isinstance(data["amenities"], list)
        assert isinstance(data["room_types"], list)
        
        # Check room types structure
        if data["room_types"]:
            room_type = data["room_types"][0]
            assert "type" in room_type
            assert "base_price_range" in room_type
            assert "capacity" in room_type


class TestBookingEndpoints:
    """Test booking-related endpoints."""
    
    def test_create_booking_valid(self, setup_database):
        """Test creating a valid booking."""
        future_date = date.today() + timedelta(days=30)
        checkout_date = future_date + timedelta(days=2)
        
        request_data = {
            "customer_email": "test.booking@example.com",
            "room_id": 1,  # Ocean suite
            "check_in_date": future_date.isoformat(),
            "check_out_date": checkout_date.isoformat(),
            "guest_count": 2,
            "special_requests": "Late check-in requested"
        }
        
        response = client.post("/api/bookings", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        assert "booking_id" in data
        assert "confirmation_number" in data
        assert data["customer_email"] == "test.booking@example.com"
        assert data["status"] == "confirmed"
        assert data["total_amount"] > 0
    
    def test_create_booking_nonexistent_room(self, setup_database):
        """Test creating booking for non-existent room."""
        future_date = date.today() + timedelta(days=30)
        checkout_date = future_date + timedelta(days=2)
        
        request_data = {
            "customer_email": "test@example.com",
            "room_id": 999,  # Non-existent
            "check_in_date": future_date.isoformat(),
            "check_out_date": checkout_date.isoformat(),
            "guest_count": 2
        }
        
        response = client.post("/api/bookings", json=request_data)
        assert response.status_code == 404
    
    def test_create_booking_invalid_dates(self, setup_database):
        """Test creating booking with invalid dates."""
        future_date = date.today() + timedelta(days=30)
        
        request_data = {
            "customer_email": "test@example.com",
            "room_id": 1,
            "check_in_date": future_date.isoformat(),
            "check_out_date": future_date.isoformat(),  # Same date
            "guest_count": 2
        }
        
        response = client.post("/api/bookings", json=request_data)
        assert response.status_code == 422  # Validation error


class TestEdgeCases:
    """Test edge cases and error handling."""
    
    def test_nonexistent_endpoint(self, setup_database):
        """Test accessing non-existent endpoint."""
        response = client.get("/api/nonexistent")
        assert response.status_code == 404
    
    def test_malformed_json(self, setup_database):
        """Test sending malformed JSON."""
        response = client.post(
            "/api/availability",
            data="invalid json",
            headers={"Content-Type": "application/json"}
        )
        assert response.status_code == 422
    
    def test_missing_required_fields(self, setup_database):
        """Test request with missing required fields."""
        request_data = {
            "room_count": 1
            # Missing check_in_date
        }
        
        response = client.post("/api/availability", json=request_data)
        assert response.status_code == 422
    
    def test_cors_headers(self, setup_database):
        """Test CORS headers are present."""
        response = client.options("/api/availability")
        # CORS headers should be present due to middleware
        assert response.status_code in [200, 405]  # Some implementations return 405


class TestIntegrationScenarios:
    """Test real-world integration scenarios."""
    
    def test_nlp_to_api_flow_basic(self, setup_database):
        """Test basic NLP to API integration flow."""
        # Simulate NLP service calling availability
        future_date = (date.today() + timedelta(days=15)).isoformat()
        
        # 1. NLP extracts parameters and calls availability
        availability_request = {
            "check_in_date": future_date,
            "room_count": 1,
            "max_budget": 150.0,
            "view_preference": "ocean"
        }
        
        availability_response = client.post("/api/availability", json=availability_request)
        assert availability_response.status_code == 200
        
        availability_data = availability_response.json()
        assert availability_data["total_count"] > 0
        
        # 2. If customer wants to book, create booking
        if availability_data["available_rooms"]:
            first_room = availability_data["available_rooms"][0]
            room_id = int(first_room["room_id"])
            
            booking_request = {
                "customer_email": "nlp.customer@example.com",
                "room_id": room_id,
                "check_in_date": future_date,
                "check_out_date": (date.today() + timedelta(days=17)).isoformat(),
                "guest_count": 2,
                "special_requests": "Extracted from NLP: Ocean view preferred"
            }
            
            booking_response = client.post("/api/bookings", json=booking_request)
            assert booking_response.status_code == 200
            
            booking_data = booking_response.json()
            assert booking_data["confirmation_number"].startswith("STD-")
    
    def test_multi_room_family_scenario(self, setup_database):
        """Test multi-room family booking scenario."""
        future_date = (date.today() + timedelta(days=20)).isoformat()
        
        # Family needs 3 rooms
        request_data = {
            "check_in_date": future_date,
            "room_count": 3,
            "max_budget": 150.0
        }
        
        response = client.post("/api/availability", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        
        # Should provide alternatives if not enough rooms
        if data["total_count"] < 3:
            assert len(data["suggested_alternatives"]) > 0
            
            # Check alternative dates
            alternative = data["suggested_alternatives"][0]
            assert "check_in_date" in alternative
            assert alternative["available_rooms"] >= 3
    
    def test_luxury_penthouse_scenario(self, setup_database):
        """Test luxury penthouse booking scenario."""
        future_date = (date.today() + timedelta(days=25)).isoformat()
        
        # High budget for luxury accommodation
        request_data = {
            "check_in_date": future_date,
            "room_count": 1,
            "max_budget": 600.0,
            "view_preference": "ocean"
        }
        
        response = client.post("/api/availability", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        assert data["total_count"] > 0
        
        # Should include penthouse in results
        penthouse_found = False
        for room in data["available_rooms"]:
            if "penthouse" in room["room_type"].lower():
                penthouse_found = True
                assert room["price_per_night"] > 300  # Luxury pricing
                break
        
        # Penthouse should be available for high budget
        assert penthouse_found
    
    def test_budget_conscious_scenario(self, setup_database):
        """Test budget-conscious customer scenario."""
        future_date = (date.today() + timedelta(days=10)).isoformat()
        
        # Low budget request
        request_data = {
            "check_in_date": future_date,
            "room_count": 1,
            "max_budget": 100.0,
            "view_preference": "garden"
        }
        
        response = client.post("/api/availability", json=request_data)
        
        if response.status_code == 200:
            data = response.json()
            
            # All returned rooms should be within budget
            for room in data["available_rooms"]:
                assert room["price_per_night"] <= 100.0
                
            # Should prefer garden view rooms
            garden_rooms = [r for r in data["available_rooms"] if r["view_type"] == "garden"]
            assert len(garden_rooms) > 0


class TestResponseFormats:
    """Test response format compliance with NLP expectations."""
    
    def test_availability_response_format(self, setup_database):
        """Test availability response matches expected format."""
        future_date = (date.today() + timedelta(days=30)).isoformat()
        
        request_data = {
            "check_in_date": future_date,
            "room_count": 1,
            "max_budget": 200.0
        }
        
        response = client.post("/api/availability", json=request_data)
        assert response.status_code == 200
        
        data = response.json()
        
        # Check required fields
        required_fields = ["available_rooms", "total_count", "suggested_alternatives", "message"]
        for field in required_fields:
            assert field in data
        
        # Check room format
        if data["available_rooms"]:
            room = data["available_rooms"][0]
            room_required_fields = [
                "room_id", "room_type", "price_per_night", "view_type",
                "amenities", "availability_date", "description"
            ]
            for field in room_required_fields:
                assert field in room
            
            assert isinstance(room["amenities"], list)
            assert isinstance(room["price_per_night"], (int, float))
    
    def test_hotel_context_response_format(self, setup_database):
        """Test hotel context response format."""
        response = client.get("/api/rooms/context")
        assert response.status_code == 200
        
        data = response.json()
        
        # Check required fields
        required_fields = ["hotel_name", "location", "amenities", "room_types", "policies"]
        for field in required_fields:
            assert field in data
        
        # Check policies format
        policies = data["policies"]
        policy_fields = ["check_in_time", "check_out_time", "cancellation_policy"]
        for field in policy_fields:
            assert field in policies 