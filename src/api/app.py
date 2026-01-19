"""
Main FastAPI application for portfolio analysis system.
"""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from api.routers import health, insights, projects, consent

# Create FastAPI app
app = FastAPI(
    title="Portfolio Analysis API",
    description="API for analyzing and managing student portfolios and projects",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure appropriately for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router)
app.include_router(insights.router)
app.include_router(projects.router)
app.include_router(consent.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

