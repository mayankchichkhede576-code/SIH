from fastapi import APIRouter
from .health import router as health_router
from .investigations import router as investigations_router
api_router = APIRouter()
api_router.include_router(health_router)
api_router.include_router(investigations_router)
