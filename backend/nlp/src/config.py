"""Configuration management for NLP service."""

import os
from typing import Optional

from pydantic import BaseSettings, Field


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Google Cloud Configuration
    google_cloud_project: str = Field(..., env="GOOGLE_CLOUD_PROJECT")
    google_application_credentials: str = Field(..., env="GOOGLE_APPLICATION_CREDENTIALS")
    vertex_ai_location: str = Field("us-central1", env="VERTEX_AI_LOCATION")
    
    # Email Configuration
    imap_server: str = Field("localhost", env="IMAP_SERVER")
    imap_port: int = Field(1143, env="IMAP_PORT")
    imap_username: str = Field(..., env="IMAP_USERNAME")
    imap_password: str = Field(..., env="IMAP_PASSWORD")
    imap_use_tls: bool = Field(False, env="IMAP_USE_TLS")
    
    # NLP Configuration
    confidence_threshold: float = Field(0.85, env="CONFIDENCE_THRESHOLD", ge=0.0, le=1.0)
    max_processing_time: int = Field(300, env="MAX_PROCESSING_TIME", gt=0)
    gemini_model: str = Field("gemini-2.0-flash-exp", env="GEMINI_MODEL")
    
    # API Integration
    backend_api_base_url: str = Field("http://localhost:8000/api", env="BACKEND_API_BASE_URL")
    api_timeout: int = Field(30, env="API_TIMEOUT", gt=0)
    
    # Logging
    log_level: str = Field("INFO", env="LOG_LEVEL")
    log_format: str = Field("json", env="LOG_FORMAT")
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings."""
    return settings 