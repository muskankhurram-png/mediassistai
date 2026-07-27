"""
Request/response schemas for patient profiles.
"""
import uuid
from pydantic import BaseModel, Field


class PatientCreate(BaseModel):
    blood_group: str | None = Field(default=None, max_length=5)
    allergies: str | None = None
    emergency_contact: str | None = Field(default=None, max_length=50)


class PatientUpdate(BaseModel):
    blood_group: str | None = None
    allergies: str | None = None
    emergency_contact: str | None = None


class PatientOut(BaseModel):
    id: uuid.UUID
    user_id: uuid.UUID
    blood_group: str | None
    allergies: str | None
    emergency_contact: str | None

    model_config = {"from_attributes": True}
