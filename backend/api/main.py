"""Main FastAPI application for Staydesk API."""

import time
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.config import get_settings
from src.database import create_tables
from src.routers import availability, bookings

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events."""
    # Startup
    print("🏨 Starting Staydesk API...")
    
    # Create database tables
    create_tables()
    print("✅ Database initialized")
    
    # Initialize sample data
    from src.utils.seed_data import initialize_sample_data
    initialize_sample_data()
    print("✅ Sample data initialized")
    
    print("🚀 Staydesk API is ready!")
    
    yield
    
    # Shutdown
    print("⏹️ Shutting down Staydesk API...")


# Create FastAPI application
app = FastAPI(
    title="Staydesk API",
    description="Backend API for Staydesk hotel booking system with email intelligence",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Add timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next):
    """Add processing time header to responses."""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Include routers
app.include_router(availability.router)
app.include_router(bookings.router)


# Root endpoints
@app.get("/")
async def root():
    """Root endpoint."""
    return {
        "service": "Staydesk API",
        "version": "1.0.0",
        "status": "running",
        "hotel": settings.hotel_name,
        "location": settings.hotel_location,
        "endpoints": {
            "availability": "/api/availability",
            "hotel_context": "/api/rooms/context",
            "bookings": "/api/bookings",
            "health": "/health",
            "docs": "/docs"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "timestamp": time.time(),
        "service": "staydesk-api",
        "version": "1.0.0"
    }


# Custom exception handlers
@app.exception_handler(404)
async def not_found_handler(request: Request, exc):
    """Handle 404 errors."""
    return JSONResponse(
        status_code=404,
        content={
            "error": "Not found",
            "details": f"The requested endpoint {request.url.path} was not found"
        }
    )


@app.exception_handler(500)
async def internal_error_handler(request: Request, exc):
    """Handle 500 errors."""
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "details": "An unexpected error occurred"
        }
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app, 
        host=settings.api_host, 
        port=settings.api_port, 
        reload=settings.api_reload
    ) 