from app.api.system.health import router as health_router
from app.api.system.status import router as status_router
from app.api.system.root import router as root_router

__all__ = [
    "health_router",
    "status_router",
    "root_router"
]