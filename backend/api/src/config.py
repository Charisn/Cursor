"""Configuration management for API service."""

import os
from typing import List

from pydantic import Field
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # Database Configuration
    database_url: str = Field("sqlite:///./staydesk.db", env="DATABASE_URL")
    
    # API Configuration
    api_host: str = Field("0.0.0.0", env="API_HOST")
    api_port: int = Field(8000, env="API_PORT")
    api_reload: bool = Field(True, env="API_RELOAD")
    
    # Hotel Configuration
    hotel_name: str = Field("Staydesk Resort", env="HOTEL_NAME")
    hotel_location: str = Field("Miami Beach, FL", env="HOTEL_LOCATION")
    hotel_timezone: str = Field("America/New_York", env="HOTEL_TIMEZONE")
    
    # NLP Service Integration
    nlp_service_url: str = Field("http://nlp-service:8001", env="NLP_SERVICE_URL")
    nlp_timeout: int = Field(30, env="NLP_TIMEOUT")
    
    # Security
    secret_key: str = Field("your-secret-key-here", env="SECRET_KEY")
    cors_origins: str = Field("http://localhost:3000,http://localhost:8001", env="CORS_ORIGINS")
    
    # Logging
    log_level: str = Field("INFO", env="LOG_LEVEL")
    log_format: str = Field("json", env="LOG_FORMAT")
    
    # Email Testing (MailHog)
    smtp_host: str = Field("mailhog", env="SMTP_HOST")
    smtp_port: int = Field(1025, env="SMTP_PORT")
    smtp_username: str = Field("", env="SMTP_USERNAME")
    smtp_password: str = Field("", env="SMTP_PASSWORD")
    
    # Business Rules
    default_check_in_time: str = Field("15:00", env="DEFAULT_CHECK_IN_TIME")
    default_check_out_time: str = Field("11:00", env="DEFAULT_CHECK_OUT_TIME")
    max_advance_booking_days: int = Field(365, env="MAX_ADVANCE_BOOKING_DAYS")
    max_rooms_per_booking: int = Field(10, env="MAX_ROOMS_PER_BOOKING")
    cancellation_hours: int = Field(24, env="CANCELLATION_HOURS")
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Get CORS origins as a list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    class Config:
        """Pydantic configuration."""
        env_file = ".env"
        case_sensitive = False


# Global settings instance
settings = Settings()


def get_settings() -> Settings:
    """Get application settings."""
    return settings 