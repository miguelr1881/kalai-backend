from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
import os

from app.config import settings
from app.routes import public, admin
from app.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Initialize database connection on startup"""
    await init_db()
    yield
    # Cleanup on shutdown


app = FastAPI(
    title="Kalai Medical Center API",
    description="API para la gestión de productos y servicios de Kalai Medical Center",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(public.router, prefix="/api/public", tags=["Public"])
app.include_router(admin.router, prefix="/api/admin", tags=["Admin"])


@app.get("/")
async def root():
    return {
        "message": "Kalai Medical Center API",
        "status": "active",
        "version": "1.0.0"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
