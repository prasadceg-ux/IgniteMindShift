"""SchoolDistrict model."""

import uuid
from sqlalchemy import String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


def _new_uuid():
    return str(uuid.uuid4())


class SchoolDistrict(Base):
    __tablename__ = "school_districts"

    id: Mapped[str] = mapped_column(String(36), primary_key=True, default=_new_uuid)
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    state: Mapped[str | None] = mapped_column(String(2), nullable=True)
    is_active: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)

    users: Mapped[list["User"]] = relationship(back_populates="district")  # type: ignore[name-defined]
    schools: Mapped[list["School"]] = relationship(back_populates="district")  # type: ignore[name-defined]
