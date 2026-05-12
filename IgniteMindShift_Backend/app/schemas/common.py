"""Shared schemas used across multiple endpoints."""

from typing import Optional, Generic, TypeVar, List
from pydantic import BaseModel

T = TypeVar("T")


class HealthCheck(BaseModel):
    status: str = "ok"
    app: str
    environment: str


class PaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    total: int
    page: int
    page_size: int
    has_next: bool


class CursorPaginatedResponse(BaseModel, Generic[T]):
    items: List[T]
    next_cursor: Optional[str] = None
    has_next: bool
