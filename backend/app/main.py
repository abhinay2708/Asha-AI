"""
Asha AI - Rural Healthcare Screening System
FastAPI Backend Entry Point
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


from .config import get_settings
from .database import Database
from .routers import triage, screenings, clinics


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan: connect DB on startup, disconnect on shutdown."""
    await Database.connect()
    yield
    await Database.disconnect()


app = FastAPI(
    title="Asha AI API",
    description="Rural Healthcare Screening System - Voice-to-AI Triage",
    version="1.0.0",
    lifespan=lifespan,
)

settings = get_settings()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(triage.router)
app.include_router(screenings.router)
app.include_router(clinics.router)


@app.get("/")
async def root():
    """Root health check."""
    return {
        "app": "Asha AI",
        "status": "running",
        "docs": "/docs",
    }


@app.get("/health")
async def health():
    """Health check for deployment platforms."""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
