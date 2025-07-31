"""
Mrs-Unkwn Configuration Settings
"""
import os
from typing import Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Application
    app_name: str = "Mrs-Unkwn"
    app_version: str = "1.0.0"
    debug: bool = False
    
    # Database
    database_url: str = "postgresql://user:password@localhost/mrsunkwn"
    database_echo: bool = False
    
    # Redis
    redis_url: str = "redis://localhost:6379"
    
    # OpenAI API
    openai_api_key: Optional[str] = None
    openai_model: str = "gpt-4-turbo-preview"
    
    # GitHub Integration
    github_token: Optional[str] = None
    github_repo_owner: str = "meinzeug-cloud"
    github_repo_name: str = "mrsunkwn"
    
    # Security
    secret_key: str = "dev-secret-key-change-in-production"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    
    # API Configuration
    api_host: str = "127.0.0.1"
    api_port: int = 8000
    api_workers: int = 1
    
    # Mrs-Unkwn Specific
    max_session_duration_minutes: int = 120
    default_difficulty_level: int = 5
    max_hint_count: int = 3
    socratic_response_max_tokens: int = 1000
    
    # Monitoring & Analytics
    enable_monitoring: bool = True
    enable_analytics: bool = True
    analytics_retention_days: int = 365
    
    # Anti-Cheat Settings
    suspicion_threshold: float = 0.7
    ai_detection_enabled: bool = True
    browser_monitoring_enabled: bool = True
    clipboard_monitoring_enabled: bool = True
    
    # Parental Controls
    default_time_limit_minutes: int = 60
    enable_content_filtering: bool = True
    default_allowed_subjects: list = ["math", "science", "english", "history"]
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

# Global settings instance
settings = Settings()