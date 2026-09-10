from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.db.session import Base, engine
from app.models.investigation import Investigation  # noqa: F401
from app.api.v1.router import api_router

Base.metadata.create_all(bind=engine)
app = FastAPI(title=settings.app_name, version="1.0.0", docs_url="/docs", redoc_url="/redoc")
app.add_middleware(CORSMiddleware, allow_origins=settings.cors_origin_list, allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
app.include_router(api_router, prefix=settings.api_v1_prefix)
@app.get("/", tags=["System"])
def root(): return {"name": settings.app_name, "docs": "/docs", "health": f"{settings.api_v1_prefix}/health"}
