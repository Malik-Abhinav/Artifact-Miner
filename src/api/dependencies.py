"""
Shared dependencies for FastAPI endpoints.
"""
from __future__ import annotations

import os
from typing import Optional

from insights.storage import ProjectInsightsStore, DEFAULT_DB_PATH
from insights.user_role_store import ProjectRoleStore


def resolve_db_path(db_url: Optional[str] = None) -> str:
    """Resolve database path from URL or environment variable."""
    env_url = os.getenv("DATABASE_URL")
    effective = db_url or env_url or f"sqlite:///{DEFAULT_DB_PATH}"
    return effective.replace("sqlite:///", "")


def get_insights_store(db_url: Optional[str] = None) -> ProjectInsightsStore:
    """Dependency for getting ProjectInsightsStore instance."""
    db_path = resolve_db_path(db_url)
    return ProjectInsightsStore(db_path=db_path)


def get_role_store(db_url: Optional[str] = None) -> ProjectRoleStore:
    """Dependency for getting ProjectRoleStore instance."""
    db_path = resolve_db_path(db_url)
    return ProjectRoleStore(db_path=db_path)

