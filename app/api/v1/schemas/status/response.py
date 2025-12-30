"""
        return {
        "application": {
            "name": config.APP_NAME,
            "version": config.APP_VERSION,
            "environment": config.ENVIRONMENT,
            "debug": config.DEBUG,
        },
        "runtime": {
            "uptime_seconds": int(time()),
        },
        "features": {
            "authentication": True,
            "database": True,
        }
    }
"""
from pydantic import BaseModel

class ApplicationStatus(BaseModel):
    name: str
    version: str
    environment: str
    debug: bool


class RuntimeStatus(BaseModel):
    uptime_seconds: int


class FeaturesStatus(BaseModel):
    authentication: bool
    database: bool

class StatusResponse(BaseModel):
    application: ApplicationStatus
    runtime: RuntimeStatus
    features: FeaturesStatus