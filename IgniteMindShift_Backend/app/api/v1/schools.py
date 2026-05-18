"""
Schools API routes.

GET /schools?district_id=<id>&search=   → Schools for a district (autocomplete)
"""

from typing import Optional

from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.deps import get_db
from app.models.school import School
from app.models.district import SchoolDistrict
from app.schemas.school import SchoolOut, SchoolListResponse

router = APIRouter()


@router.get("/schools", response_model=SchoolListResponse)
async def list_schools(
    district_id: str = Query(..., description="Filter schools by district"),
    search: Optional[str] = Query(None, max_length=100),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """Return active schools for a given district. Pass ?search= to filter by name."""
    # Verify district exists
    district = (await db.execute(
        select(SchoolDistrict).where(SchoolDistrict.id == district_id)
    )).scalar_one_or_none()
    if not district:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="District not found")

    base_filter = (School.district_id == district_id) & (School.is_active == True)  # noqa: E712

    query = select(School).where(base_filter)
    count_query = select(func.count()).select_from(School).where(base_filter)

    if search:
        like = f"%{search}%"
        query = query.where(School.name.ilike(like))
        count_query = count_query.where(School.name.ilike(like))

    query = query.order_by(School.name).limit(limit)

    schools = (await db.execute(query)).scalars().all()
    total = (await db.execute(count_query)).scalar()

    return SchoolListResponse(schools=schools, total=total)
