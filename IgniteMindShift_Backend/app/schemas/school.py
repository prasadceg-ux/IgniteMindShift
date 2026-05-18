"""Pydantic schemas for school endpoints."""

from typing import List, Optional
from pydantic import BaseModel


class SchoolOut(BaseModel):
    id: str
    name: str
    district_id: str

    model_config = {"from_attributes": True}


class SchoolListResponse(BaseModel):
    schools: List[SchoolOut]
    total: int
