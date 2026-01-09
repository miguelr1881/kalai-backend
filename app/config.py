from pydantic_settings import BaseSettings
from typing import List


class Settings(BaseSettings):
    # Supabase Configuration
    SUPABASE_URL: str
    SUPABASE_KEY: str
    SUPABASE_SERVICE_KEY: str
    
    # Database
    DATABASE_URL: str
    
    # Security
    SECRET_KEY: str = "kalai-medical-center-secret-key-change-in-production"
    ADMIN_USERNAME: str = "admin"
    ADMIN_PASSWORD: str = "kalai2026"
    
    # CORS
    ALLOWED_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:5173",
        "https://silkskincr.com",
        "https://www.silkskincr.com"
    ]
    
    # WhatsApp
    WHATSAPP_NUMBER: str = "+50688926754"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
