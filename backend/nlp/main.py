"""
NLP Service for Hotel Room Availability Email Processing
"""
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime, date
import re
from loguru import logger

from .services.email_processor import EmailProcessor
from .services.parameter_extractor import ParameterExtractor
from .services.response_generator import ResponseGenerator
from .models.email_models import EmailRequest, ProcessedEmail
from .config import Settings

# Initialize settings
settings = Settings()

# Initialize FastAPI app
app = FastAPI(
    title="NLP Service",
    description="Email processing service for hotel room availability inquiries",
    version="1.0.0"
)

# Initialize services
email_processor = EmailProcessor()
parameter_extractor = ParameterExtractor()
response_generator = ResponseGenerator()

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "nlp"}

@app.post("/process-email", response_model=ProcessedEmail)
async def process_email(email_request: EmailRequest):
    """
    Main endpoint to process incoming emails and extract room availability parameters
    """
    try:
        logger.info(f"Processing email from: {email_request.sender_email}")
        
        # Step 1: Clean and preprocess email content
        cleaned_content = email_processor.clean_email_content(email_request.content)
        
        # Step 2: Classify email intent
        intent = email_processor.classify_intent(cleaned_content)
        
        # Step 3: Extract parameters based on intent
        if intent == "room_availability":
            extracted_params = parameter_extractor.extract_booking_parameters(cleaned_content)
            
            # Validate extracted parameters
            validation_result = parameter_extractor.validate_parameters(extracted_params)
            
            if validation_result.is_valid:
                return ProcessedEmail(
                    intent=intent,
                    extracted_parameters=extracted_params,
                    confidence_score=validation_result.confidence,
                    requires_clarification=False,
                    response_type="availability_check"
                )
            else:
                return ProcessedEmail(
                    intent=intent,
                    extracted_parameters=extracted_params,
                    confidence_score=validation_result.confidence,
                    requires_clarification=True,
                    clarification_needed=validation_result.missing_fields,
                    response_type="clarification_request"
                )
        
        else:
            # Generic response for non-availability requests
            return ProcessedEmail(
                intent="generic",
                extracted_parameters={},
                confidence_score=0.9,
                requires_clarification=False,
                response_type="generic_response"
            )
            
    except Exception as e:
        logger.error(f"Error processing email: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

@app.post("/generate-response")
async def generate_response(processed_email: ProcessedEmail, booking_data: Optional[Dict[str, Any]] = None):
    """
    Generate appropriate response based on processed email data
    """
    try:
        response = await response_generator.generate_response(
            processed_email=processed_email,
            booking_data=booking_data
        )
        
        return {"response": response}
        
    except Exception as e:
        logger.error(f"Error generating response: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal server error")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)