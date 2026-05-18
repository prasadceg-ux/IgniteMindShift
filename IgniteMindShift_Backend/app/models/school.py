"""School model."""

import uuid
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


def _new_uuid():
    return str(uuid.uuid4())


class School(Base):
    __tablename__ = "schools"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    district_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("school_districts.id"), nullable=False, index=True
    )
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    district: Mapped["SchoolDistrict"] = relationship(  # type: ignore[name-defined]
        "SchoolDistrict", back_populates="schools"
    )
    users: Mapped[list["User"]] = relationship(back_populates="school")  # type: ignore[name-defined]
