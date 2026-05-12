"""Shared FastAPI dependencies — re-exports for clean imports in routes."""

from app.core.database import get_db
from app.core.security import get_current_user, get_current_admin

__all__ = ["get_db", "get_current_user", "get_current_admin"]
