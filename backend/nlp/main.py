"""FastAPI application for NLP service."""

import time
from contextlib import asynccontextmanager
from typing import Dict, List

from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from src.agent_workflow import NLPWorkflow
from src.models import NLPProcessingResult


# Global workflow instance
workflow: NLPWorkflow = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    global workflow
    
    # Startup
    workflow = NLPWorkflow()
    print("NLP service started successfully")
    
    yield
    
    # Shutdown
    print("NLP service shutting down")


# Create FastAPI application
app = FastAPI(
    title="Staydesk NLP Service",
    description="Email intelligence layer for automated room booking responses",
    version="1.0.0",
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request/Response models
class EmailProcessingRequest(BaseModel):
    subject: str
    body: str
    sender: str = "unknown@example.com"


class ProcessingCycleResponse(BaseModel):
    status: str
    stats: Dict
    results: List[NLPProcessingResult] = []
    error: str = None


class HealthResponse(BaseModel):
    healthy: bool
    timestamp: float
    settings: Dict


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check endpoint."""
    try:
        health_result = workflow.health_check()
        return HealthResponse(**health_result)
    except Exception as e:
        return HealthResponse(
            healthy=False,
            timestamp=time.time(),
            settings={},
        )


@app.post("/process-email", response_model=NLPProcessingResult)
async def process_single_email(request: EmailProcessingRequest):
    """Process a single email and return NLP results."""
    try:
        result = workflow.process_single_email_text(
            subject=request.subject,
            body=request.body,
            sender=request.sender
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")


@app.post("/process-cycle", response_model=ProcessingCycleResponse)
async def run_processing_cycle():
    """Run a complete email processing cycle."""
    try:
        cycle_result = workflow.run_email_processing_cycle()
        return ProcessingCycleResponse(**cycle_result)
    except Exception as e:
        return ProcessingCycleResponse(
            status="error",
            stats={},
            error=str(e)
        )


@app.post("/process-cycle-background")
async def run_processing_cycle_background(background_tasks: BackgroundTasks):
    """Run email processing cycle in background."""
    
    def run_cycle():
        try:
            workflow.run_email_processing_cycle()
        except Exception as e:
            print(f"Background processing failed: {e}")
    
    background_tasks.add_task(run_cycle)
    return {"message": "Processing cycle started in background"}


@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "Staydesk NLP",
        "version": "1.0.0",
        "status": "running",
        "endpoints": {
            "health": "/health",
            "process_email": "/process-email",
            "process_cycle": "/process-cycle",
            "docs": "/docs"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001, reload=True) 