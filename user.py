"""
users table - the base account for every person using the system.
"""
from typing import TYPE_CHECKING
from sqlalchemy.orm import relationship
if TYPE_CHECKING:
    from app.models.patient import Patient
    from app.models.doctor import Doctor
import uuid
from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.database.base import Base

class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name: Mapped[str] = mapped_column(String(150), nullable=False)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    role: Mapped[str] = mapped_column(String(20), nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), server_default=func.now())
    patient: Mapped["Patient"] = relationship(
    "Patient",
    back_populates="user",
    uselist=False
)

    doctor: Mapped["Doctor"] = relationship(
    "Doctor",
    back_populates="user",
    uselist=False
)
    