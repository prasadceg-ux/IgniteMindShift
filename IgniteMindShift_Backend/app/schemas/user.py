"""Pydantic schemas for user profile endpoints."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field


class DistrictInfo(BaseModel):
    id: str
    name: str
    state: Optional[str] = None

    model_config = {"from_attributes": True}


class UserProfile(BaseModel):
    """Full profile returned to the authenticated user."""
    id: str
    email: EmailStr
    name: str
    avatar_url: Optional[str] = None
    bio: Optional[str] = None
    role: str
    district_id: Optional[str] = None
    district: Optional[DistrictInfo] = None
    xp_points: int
    level: int
    streak_count: int
    longest_streak: int
    dark_mode: bool
    locale: str
    is_active: bool
    created_at: datetime
    last_active: Optional[datetime] = None

    model_config = {"from_attributes": True}


class UserPublic(BaseModel):
    """Public-facing user info (leaderboard, feed authors)."""
    id: str
    name: str
    avatar_url: Optional[str] = None
    xp_points: int
    level: int
    streak_count: int

    model_config = {"from_attributes": True}


class UserUpdate(BaseModel):
    """Fields the user can update on their own profile."""
    name: Optional[str] = Field(None, min_length=2, max_length=150)
    bio: Optional[str] = Field(None, max_length=500)
    avatar_url: Optional[str] = None
    dark_mode: Optional[bool] = None
    locale: Optional[str] = Field(None, max_length=10)
    district_id: Optional[str] = None
