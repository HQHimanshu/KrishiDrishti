from pydantic_settings import BaseSettings
from typing import List
import json


class Settings(BaseSettings):
    # App
    APP_ENV: str = "development"
    SECRET_KEY: str = "your_jwt_secret_key_change_in_production"
    CORS_ORIGINS: str = '["http://localhost:5173", "http://localhost:3000"]'
    
    # Database
    DATABASE_URL: str = "sqlite+aiosqlite:///./krishidrishti.db"
    
    # AI
    OLLAMA_BASE_URL: str = "http://localhost:11434"
    OLLAMA_MODEL: str = "qwen2.5:1.5b"
    RAG_COLLECTION_NAME: str = "crop_knowledge_maharashtra"
    
    # APIs
    OPENWEATHER_API_KEY: str = ""
    TWILIO_ACCOUNT_SID: str = ""
    TWILIO_AUTH_TOKEN: str = ""
    TWILIO_WHATSAPP_NUMBER: str = "+14155238886"
    SMTP_EMAIL: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_SERVER: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    
    # Notifications
    DEFAULT_LANGUAGE: str = "hi"
    VOICE_ALERT_ENABLED: bool = True
    
    # Resource Budgets
    WATER_BUDGET_LITERS_PER_ACRE: float = 10000
    FERTILIZER_BUDGET_GRAMS_PER_ACRE: float = 5000
    
    # OTP Settings (Mock for dev)
    OTP_SECRET: str = "123456"  # Fixed OTP for development
    OTP_EXPIRY_MINUTES: int = 5
    
    @property
    def cors_origins(self) -> List[str]:
        try:
            return json.loads(self.CORS_ORIGINS)
        except:
            return ["http://localhost:5173"]
    
    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
