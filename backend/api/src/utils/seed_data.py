"""Seed data utility for populating the database with sample data."""

from datetime import date, datetime, timedelta
from sqlalchemy.orm import sessionmaker

from ..database import engine, get_db
from ..models import Room, RoomType, ViewType, Customer, RoomAvailability

# Create a session for seeding
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def initialize_sample_data():
    """Initialize the database with sample rooms and data."""
    
    db = SessionLocal()
    try:
        # Check if data already exists
        existing_rooms = db.query(Room).first()
        if existing_rooms:
            print("📊 Sample data already exists, skipping initialization")
            return
        
        print("📊 Creating sample room data...")
        
        # Create sample rooms
        sample_rooms = [
            # Ocean View Suites
            Room(
                room_number="101",
                room_type=RoomType.SUITE,
                view_type=ViewType.OCEAN,
                base_price=180.0,
                weekend_price=220.0,
                max_occupancy=4,
                bed_count=2,
                bathroom_count=2,
                has_balcony=True,
                has_jacuzzi=True,
                square_feet=450,
                amenities="WiFi,Air Conditioning,Mini Bar,Ocean View,Balcony,Jacuzzi",
                description="Luxurious suite with panoramic ocean views and private balcony"
            ),
            Room(
                room_number="102",
                room_type=RoomType.SUITE,
                view_type=ViewType.OCEAN,
                base_price=180.0,
                weekend_price=220.0,
                max_occupancy=4,
                bed_count=2,
                bathroom_count=2,
                has_balcony=True,
                has_jacuzzi=True,
                square_feet=450,
                amenities="WiFi,Air Conditioning,Mini Bar,Ocean View,Balcony,Jacuzzi",
                description="Luxurious suite with panoramic ocean views and private balcony"
            ),
            Room(
                room_number="201",
                room_type=RoomType.SUITE,
                view_type=ViewType.OCEAN,
                base_price=200.0,
                weekend_price=250.0,
                max_occupancy=4,
                bed_count=2,
                bathroom_count=2,
                has_balcony=True,
                has_jacuzzi=True,
                square_feet=500,
                amenities="WiFi,Air Conditioning,Mini Bar,Ocean View,Balcony,Jacuzzi,Room Service",
                description="Premium ocean suite with enhanced amenities"
            ),
            
            # City View Deluxe Rooms
            Room(
                room_number="103",
                room_type=RoomType.DELUXE,
                view_type=ViewType.CITY,
                base_price=120.0,
                weekend_price=140.0,
                max_occupancy=2,
                bed_count=1,
                bathroom_count=1,
                has_balcony=True,
                square_feet=300,
                amenities="WiFi,Air Conditioning,Mini Bar,City View,Balcony",
                description="Deluxe room with stunning city skyline views"
            ),
            Room(
                room_number="104",
                room_type=RoomType.DELUXE,
                view_type=ViewType.CITY,
                base_price=120.0,
                weekend_price=140.0,
                max_occupancy=2,
                bed_count=1,
                bathroom_count=1,
                has_balcony=True,
                square_feet=300,
                amenities="WiFi,Air Conditioning,Mini Bar,City View,Balcony",
                description="Deluxe room with stunning city skyline views"
            ),
            Room(
                room_number="203",
                room_type=RoomType.DELUXE,
                view_type=ViewType.CITY,
                base_price=130.0,
                weekend_price=150.0,
                max_occupancy=3,
                bed_count=1,
                bathroom_count=1,
                has_balcony=True,
                square_feet=320,
                amenities="WiFi,Air Conditioning,Mini Bar,City View,Balcony,Work Desk",
                description="Spacious deluxe room perfect for business travelers"
            ),
            
            # Garden View Standard Rooms
            Room(
                room_number="105",
                room_type=RoomType.STANDARD,
                view_type=ViewType.GARDEN,
                base_price=80.0,
                weekend_price=95.0,
                max_occupancy=2,
                bed_count=1,
                bathroom_count=1,
                square_feet=250,
                amenities="WiFi,Air Conditioning,Garden View",
                description="Comfortable standard room overlooking the hotel gardens"
            ),
            Room(
                room_number="106",
                room_type=RoomType.STANDARD,
                view_type=ViewType.GARDEN,
                base_price=80.0,
                weekend_price=95.0,
                max_occupancy=2,
                bed_count=1,
                bathroom_count=1,
                square_feet=250,
                amenities="WiFi,Air Conditioning,Garden View",
                description="Comfortable standard room overlooking the hotel gardens"
            ),
            Room(
                room_number="204",
                room_type=RoomType.STANDARD,
                view_type=ViewType.GARDEN,
                base_price=85.0,
                weekend_price=100.0,
                max_occupancy=2,
                bed_count=1,
                bathroom_count=1,
                square_feet=260,
                amenities="WiFi,Air Conditioning,Garden View,Mini Fridge",
                description="Cozy standard room with garden views and modern amenities"
            ),
            
            # Pool View Rooms
            Room(
                room_number="107",
                room_type=RoomType.DELUXE,
                view_type=ViewType.POOL,
                base_price=110.0,
                weekend_price=130.0,
                max_occupancy=2,
                bed_count=1,
                bathroom_count=1,
                has_balcony=True,
                square_feet=280,
                amenities="WiFi,Air Conditioning,Mini Bar,Pool View,Balcony",
                description="Deluxe room with direct pool and recreation area views"
            ),
            Room(
                room_number="108",
                room_type=RoomType.DELUXE,
                view_type=ViewType.POOL,
                base_price=110.0,
                weekend_price=130.0,
                max_occupancy=2,
                bed_count=1,
                bathroom_count=1,
                has_balcony=True,
                square_feet=280,
                amenities="WiFi,Air Conditioning,Mini Bar,Pool View,Balcony",
                description="Deluxe room with direct pool and recreation area views"
            ),
            
            # Penthouse
            Room(
                room_number="301",
                room_type=RoomType.PENTHOUSE,
                view_type=ViewType.OCEAN,
                base_price=350.0,
                weekend_price=450.0,
                max_occupancy=6,
                bed_count=3,
                bathroom_count=3,
                has_balcony=True,
                has_kitchenette=True,
                has_jacuzzi=True,
                square_feet=800,
                amenities="WiFi,Air Conditioning,Full Kitchen,Ocean View,Private Terrace,Jacuzzi,Butler Service",
                description="Exclusive penthouse with panoramic ocean views and luxury amenities"
            ),
        ]
        
        # Add rooms to database
        for room in sample_rooms:
            db.add(room)
        
        # Create some sample customers
        sample_customers = [
            Customer(
                email="john.doe@example.com",
                first_name="John",
                last_name="Doe",
                preferred_room_type=RoomType.DELUXE,
                preferred_view_type=ViewType.OCEAN
            ),
            Customer(
                email="jane.smith@example.com",
                first_name="Jane",
                last_name="Smith",
                preferred_room_type=RoomType.SUITE,
                preferred_view_type=ViewType.CITY
            ),
            Customer(
                email="test@example.com",
                first_name="Test",
                last_name="User"
            )
        ]
        
        for customer in sample_customers:
            db.add(customer)
        
        # Create some availability overrides for testing
        today = date.today()
        
        # Make room 101 unavailable for maintenance next week
        maintenance_date = today + timedelta(days=7)
        maintenance_availability = RoomAvailability(
            room_id=1,  # Room 101
            date=maintenance_date,
            is_available=False,
            is_maintenance=True,
            notes="Scheduled maintenance"
        )
        db.add(maintenance_availability)
        
        # Add special pricing for holiday period
        holiday_dates = [today + timedelta(days=i) for i in range(14, 21)]  # Week starting 2 weeks from now
        for holiday_date in holiday_dates:
            for room_id in [1, 2, 3]:  # Ocean view suites
                holiday_pricing = RoomAvailability(
                    room_id=room_id,
                    date=holiday_date,
                    is_available=True,
                    price_override=300.0,  # Holiday pricing
                    notes="Holiday special pricing"
                )
                db.add(holiday_pricing)
        
        db.commit()
        print(f"✅ Created {len(sample_rooms)} sample rooms")
        print(f"✅ Created {len(sample_customers)} sample customers")
        print("✅ Created availability overrides for testing")
        
    except Exception as e:
        print(f"❌ Error initializing sample data: {e}")
        db.rollback()
    finally:
        db.close()


def reset_database():
    """Reset the database by dropping and recreating all tables."""
    from ..database import drop_tables, create_tables
    
    print("⚠️  Resetting database...")
    drop_tables()
    create_tables()
    initialize_sample_data()
    print("✅ Database reset complete")


if __name__ == "__main__":
    # Allow running this script directly for testing
    initialize_sample_data() 