from typing import List, Optional, ClassVar
import os
from typing import Optional
from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings

load_dotenv()

class Config(BaseSettings):
    APP_NAME: str = Field(default = "Catalogo peliculas API", env="APP_NAME")
    APP_VERSION: str = Field(default = "1.0.0", env="APP_VERSION")
    APP_DESCRIPTION: str = Field(default = "Api un catalogo de peliculas", env="APP_DESCRIPTION")
    ENVIRONMENT: str = Field(default=None, env="ENVIRONMENT")
    DEBUG: bool = Field(default=False)

    # Base de datos
    DB_USER: str = Field(default="root", env="DB_USER")
    DB_PASSWORD: str = Field(default="", env="DB_PASSWORD")
    DB_HOST: str = Field(default="localhost", env="DB_HOST")
    DB_PORT: str = Field(default="3306", env="DB_PORT")
    DB_NAME: str = Field(default="catalogfilms", env="DB_NAME")

    AUTH_EXCLUDED_PATHS: List[str] = [
        "/docs",
        "/redoc",
        "/openapi.json",
        "/api/v1/auth/login",
        "/api/v1/auth/register",
        "/health",
        "/favicon.ico",
    ]

    PROTECTED_PATH_PREFIXES: List[str] = [
        "/api/v1/user",
        "/api/v1/admin",
    ]


    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    LOG_FILE: Optional[str] = Field(default=None)


    PERSIST_PATH: str = Field(default=None, env="PERSIST_PATH")


    @property 
    def is_development(self) -> bool:
        return self.ENVIRONMENT.lower() == "develop"
    
    @property
    def is_production(self) -> bool:
        return self.ENVIRONMENT.lower() == "production"
    
    @property
    def is_testing(self) -> bool:
        return self.ENVIRONMENT.lower() == "testing"

    class Config:
        env_file = ".env"
        case_sensitive = True


class DevelopmentConfig(Config):
    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"
    LOG_FILE: Optional[str] = "/var/log/app_dev.log"

class TestingConfig(Config):
    DEBUG: bool = True
    LOG_LEVEL: str = "INFO"
    LOG_FILE: Optional[str] = "/var/log/app_test.log"


class ProductionConfig(Config):
    DEBUG: bool = False
    LOG_LEVEL: str = "ERROR"
    LOG_FILE: Optional[str] = "/var/log/app.log"

    

def get_config() -> Config:

    environment = os.getenv("ENVIRONMENT", "develop").lower()
    
    if environment == "production":
        return ProductionConfig()
    elif environment == "testing":
        return TestingConfig()
    else:
        return DevelopmentConfig()


config = get_config()