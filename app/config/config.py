from typing import List, Optional, ClassVar
import os
from typing import Optional
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()

class Config(BaseSettings):
    APP_NAME: str = "Catalogo peliculas API"
    APP_VERSION: str = "1.0.0"
    APP_DESCRIPTION: str = "Api un catalogo de peliculas"

    ENVIRONMENT: str = "develop"
    DEBUG: bool = False

    DB_USER: str = "root"
    DB_PASSWORD: str = ""
    DB_HOST: str = "localhost"
    DB_PORT: str = "3306"
    DB_NAME: str = "catalogfilms"

    LOG_LEVEL: str = "INFO"
    LOG_FILE: str | None = None

    PERSIST_PATH: str | None = None

    AUTH_EXCLUDED_PATHS: list[str] = [
        "/docs",
        "/redoc",
        "/openapi.json",
        "/api/v1/auth/login",
        "/api/v1/auth/register",
        "/health",
        "/status",
        "/favicon.ico",
    ]

    PROTECTED_PATH_PREFIXES: list[str] = [
        "/api/v1/user",
        "/api/v1/admin",
    ]

    model_config = SettingsConfigDict(
        env_file=".env",
        case_sensitive=True
    )


    @property 
    def is_development(self) -> bool:
        return self.ENVIRONMENT.lower() == "develop"
    
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() == "production"
    
    @property
    def is_testing(self) -> bool:
        return self.ENVIRONMENT.lower() == "testing"


class DevelopmentConfig(Config):
    DEBUG: bool = True
    ENVIRONMENT: str = "develop"
    LOG_LEVEL: str = "DEBUG"
    LOG_FILE: Optional[str] = "/var/log/app_dev.log"

class TestingConfig(Config):
    DEBUG: bool = True
    ENVIRONMENT: str = "testing"
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Optional[str] = "/var/log/app_test.log"


class ProductionConfig(Config):
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    LOG_LEVEL: str = "ERROR"
    LOG_FILE: Optional[str] = "/var/log/app.log"

    

def get_config() -> Config:

    env = os.getenv("ENVIRONMENT", "develop").lower()

    match env:
        case "production":
            return ProductionConfig()
        case "testing":
            return TestingConfig()
        case _:
            return DevelopmentConfig()


config = get_config()