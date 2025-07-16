from datetime import date
from pydantic import BaseModel, Field, field_validator

class SimpleRoomRequest(BaseModel):
    """Simple test model to identify the Pydantic issue."""
    
    date: date | None = Field(default=None, description="Requested check-in date")
    room_count: int | None = Field(default=None, description="Number of rooms")
    
    @field_validator('date')
    @classmethod
    def validate_date_not_past(cls, v):
        """Ensure date is not in the past."""
        if v and v < date.today():
            raise ValueError("Date cannot be in the past")
        return v

if __name__ == "__main__":
    # Test the model
    request = SimpleRoomRequest()
    print("Model created successfully!")
    print(request) 