"""
Health check and system information endpoints.
"""
from __future__ import annotations

import sys
from datetime import datetime

from fastapi import APIRouter

router = APIRouter(tags=["health"])


@router.get("/health")
def health_check():
    """Basic health check endpoint."""
    return {
        "status": "ok",
        "timestamp": datetime.utcnow().isoformat(),
    }


@router.get("/")
def root():
    """Root endpoint with API information."""
    return {
        "name": "Portfolio Analysis API",
        "version": "1.0.0",
        "description": "API for analyzing and managing student portfolios",
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
        "endpoints": {
            "health": "/health",
            "docs": "/docs",
            "insights": "/insights",
            "projects": "/projects",
            "privacy_consent": "/privacy-consent",
        }
    }

