"""
Configuration settings for NLP service
"""
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings"""
    
    # Service configuration
    service_name: str = "nlp-service"
    debug: bool = False
    log_level: str = "INFO"
    
    # API configuration
    backend_api_url: str = "http://backend:8000"
    api_key: Optional[str] = None
    
    # Redis configuration
    redis_url: str = "redis://redis:6379"
    
    # Model configuration
    openai_api_key: Optional[str] = None
    model_name: str = "gpt-3.5-turbo"
    
    # Processing configuration
    max_email_length: int = 10000
    confidence_threshold: float = 0.7
    
    class Config:
        env_file = ".env"
        env_prefix = "NLP_"