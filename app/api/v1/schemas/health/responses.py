from pydantic import BaseModel


"""
        "status": "ok",
        "timestamp": int(time()),
        "service": config.APP_NAME,
        "version": config.APP_VERSION,
        "components": {
            "api": "up",
            "database": "up"
        }    
"""
class HealthResponse(BaseModel):
    status: str
    timestamp: int
    service: str
    version: str
    components: dict

    model_config = {
        "from_attributes": True
    }