"""
Configuration management for the FastAPI backend.
Loads environment variables and provides settings.
"""
import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    """Application settings loaded from environment variables."""
    
    # API Keys
    GROQ_API_KEY: str
    LANGSMITH_API_KEY: Optional[str] = None
    GOOGLE_SHEETS_CREDENTIALS_PATH: str
    GOOGLE_SHEET_NAME: str = "Copy of PMMPL AI (Prabhat)"
    
    # Database
    DATABASE_URL: str = "sqlite:///./chat_history.db"
    
    # Server Configuration
    HOST: str = "0.0.0.0"
    PORT: int = 8000
    RELOAD: bool = True
    
    # CORS Settings
    CORS_ORIGINS: list = ["http://localhost:3000", "http://127.0.0.1:3000", "http://localhost:5500", "http://127.0.0.1:5500"]
    
    # Refresh Settings
    SHEETS_REFRESH_INTERVAL_MINUTES: int = 10
    
    # LLM Settings
    LLM_MODEL: str = "llama-3.3-70b-versatile"
    LLM_TEMPERATURE: float = 0.0
    
    class Config:
        env_file = ".env"
        case_sensitive = True

# Global settings instance
settings = Settings()
