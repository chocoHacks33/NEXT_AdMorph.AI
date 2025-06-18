"""
Application settings and configuration
"""

import os
from typing import List, Optional
from functools import lru_cache
try:
    from pydantic_settings import BaseSettings
    from pydantic import validator
except ImportError:
    from pydantic import BaseSettings, validator


class Settings(BaseSettings):
    """Application settings"""
    
    # Server configuration
    host: str = "0.0.0.0"
    port: int = 8000
    environment: str = "development"
    log_level: str = "INFO"
    
    # CORS settings
    allowed_origins: List[str] = ["http://localhost:3000", "http://localhost:3001"]
    
    # OpenAI configuration
    openai_api_key: str
    openai_model: str = "gpt-4"
    openai_max_tokens: int = 2000
    openai_temperature: float = 0.7
    openai_timeout: int = 30
    
    # Meta API configuration
    meta_access_token: Optional[str] = None
    meta_app_id: Optional[str] = None
    meta_app_secret: Optional[str] = None
    meta_ad_account_id: Optional[str] = None
    
    # Database configuration (for future use)
    database_url: Optional[str] = None
    redis_url: Optional[str] = None
    
    # File storage
    upload_dir: str = "uploads"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    allowed_file_types: List[str] = ["image/jpeg", "image/png", "image/gif", "image/webp"]
    
    # Rate limiting
    rate_limit_requests: int = 100
    rate_limit_window: int = 60  # seconds
    
    # Background job configuration
    job_timeout: int = 300  # 5 minutes
    max_concurrent_jobs: int = 10
    
    # Monitoring and logging
    enable_metrics: bool = True
    metrics_port: int = 9090
    log_format: str = "json"
    
    @validator("allowed_origins", pre=True)
    def parse_cors_origins(cls, v):
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v
    
    @validator("allowed_file_types", pre=True)
    def parse_file_types(cls, v):
        if isinstance(v, str):
            return [file_type.strip() for file_type in v.split(",")]
        return v
    
    @validator("environment")
    def validate_environment(cls, v):
        allowed_envs = ["development", "staging", "production"]
        if v not in allowed_envs:
            raise ValueError(f"Environment must be one of: {allowed_envs}")
        return v
    
    @validator("log_level")
    def validate_log_level(cls, v):
        allowed_levels = ["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"]
        if v.upper() not in allowed_levels:
            raise ValueError(f"Log level must be one of: {allowed_levels}")
        return v.upper()
    
    def is_production(self) -> bool:
        """Check if running in production"""
        return self.environment == "production"
    
    def is_development(self) -> bool:
        """Check if running in development"""
        return self.environment == "development"
    
    def get_openai_config(self) -> dict:
        """Get OpenAI configuration"""
        return {
            "api_key": self.openai_api_key,
            "model": self.openai_model,
            "max_tokens": self.openai_max_tokens,
            "temperature": self.openai_temperature,
            "timeout": self.openai_timeout
        }
    
    def get_meta_config(self) -> dict:
        """Get Meta API configuration"""
        return {
            "access_token": self.meta_access_token,
            "app_id": self.meta_app_id,
            "app_secret": self.meta_app_secret,
            "ad_account_id": self.meta_ad_account_id
        }
    
    def has_meta_config(self) -> bool:
        """Check if Meta API is configured"""
        return all([
            self.meta_access_token,
            self.meta_app_id,
            self.meta_app_secret,
            self.meta_ad_account_id
        ])
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = False
        
        # Environment variable prefixes
        env_prefix = "ADMORPH_"
        
        # Field aliases for common environment variable names
        fields = {
            "openai_api_key": {"env": ["OPENAI_API_KEY", "ADMORPH_OPENAI_API_KEY"]},
            "meta_access_token": {"env": ["META_ACCESS_TOKEN", "ADMORPH_META_ACCESS_TOKEN"]},
            "meta_app_id": {"env": ["META_APP_ID", "ADMORPH_META_APP_ID"]},
            "meta_app_secret": {"env": ["META_APP_SECRET", "ADMORPH_META_APP_SECRET"]},
            "meta_ad_account_id": {"env": ["META_AD_ACCOUNT_ID", "ADMORPH_META_AD_ACCOUNT_ID"]},
            "database_url": {"env": ["DATABASE_URL", "ADMORPH_DATABASE_URL"]},
            "redis_url": {"env": ["REDIS_URL", "ADMORPH_REDIS_URL"]}
        }


@lru_cache()
def get_settings() -> Settings:
    """Get cached settings instance"""
    return Settings()
