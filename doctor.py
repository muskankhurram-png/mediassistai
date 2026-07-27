"""
Request/response schemas for doctor profiles.
"""
import uuid
from pydantic import BaseModel, Field


class DoctorCreate(BaseModel):
    specialization: str | None = Field(default=None, max_length=150)
    availability: str | None = Field(default=None, max_length=255)


class DoctorUpdate(BaseModel):
    specialization: str | None = None
    availability: str | None = None


class DoctorOut(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    specialization: str | None
    availability: str | None

    model_config = {"from_attributes": True}
