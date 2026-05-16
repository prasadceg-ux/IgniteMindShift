"""
District API routes.

GET /districts   → List / search school districts for autocomplete
"""

from typing import Optional

from fastapi import APIRouter, Depends, Query
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.models.district import SchoolDistrict
from app.schemas.district import DistrictOut, DistrictListResponse

router = APIRouter()


@router.get("/districts", response_model=DistrictListResponse)
async def list_districts(
    search: Optional[str] = Query(None, max_length=100),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Return active school districts. Pass ?search= to filter by name (autocomplete)."""
    base_filter = SchoolDistrict.is_active == True  # noqa: E712

    query = select(SchoolDistrict).where(base_filter)
    count_query = select(func.count()).select_from(SchoolDistrict).where(base_filter)

    if search:
        like = f"%{search}%"
        query = query.where(SchoolDistrict.name.ilike(like))
        count_query = count_query.where(SchoolDistrict.name.ilike(like))

    query = query.order_by(SchoolDistrict.name).limit(limit)

    districts = (await db.execute(query)).scalars().all()
    total = (await db.execute(count_query)).scalar()

    return DistrictListResponse(districts=districts, total=total)
