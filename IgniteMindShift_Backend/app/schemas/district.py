"""Pydantic schemas for school district endpoints."""

from typing import Optional, List
from pydantic import BaseModel


class DistrictOut(BaseModel):
    id: str
    name: str
    state: Optional[str] = None

    model_config = {"from_attributes": True}


class DistrictListResponse(BaseModel):
    districts: List[DistrictOut]
    total: int
