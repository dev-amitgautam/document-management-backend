import os
from pydantic_settings import BaseSettings
from typing import Optional, Dict, Any, List

class Settings(BaseSettings):
    PROJECT_NAME: str = "Document Management System"
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = os.getenv("SECRET_KEY", "your-secret-key-for-jwt")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:4200", "http://localhost:3000"]
    
    # Database
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "document_management")
    SQLALCHEMY_DATABASE_URI: Optional[str] = None
    
    # File storage
    MAX_CONTENT_LENGTH: int = 5 * 1024 * 1024  # 5MB
    
    # Legacy Dropbox settings - ignored but included to prevent validation errors
    # when environment variables are present
    DROPBOX_ACCESS_TOKEN: Optional[str] = None
    DROPBOX_ROOT_PATH: Optional[str] = None
    DROPBOX_REFRESH_TOKEN: Optional[str] = None
    DROPBOX_APP_KEY: Optional[str] = None
    DROPBOX_APP_SECRET: Optional[str] = None
    
    class Config:
        case_sensitive = True
        env_file = ".env"

    def __init__(self, **data: Any):
        super().__init__(**data)
        self.SQLALCHEMY_DATABASE_URI = f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_SERVER}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

settings = Settings() 