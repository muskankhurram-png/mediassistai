"""
Business logic for doctor profiles.
"""
import uuid

from sqlalchemy.orm import Session

from app.models.doctor import Doctor
from app.models.user import User
from app.schemas.doctor import DoctorCreate, DoctorUpdate


def create_doctor_profile(db: Session, user: User, payload: DoctorCreate) -> Doctor:
    existing = db.query(Doctor).filter(Doctor.user_id == user.id).first()
    if existing:
        raise ValueError("Doctor profile already exists for this account")

    doctor = Doctor(user_id=user.id, **payload.model_dump())
    db.add(doctor)
    db.commit()
    db.refresh(doctor)
    return doctor


def get_doctor_by_id(db: Session, doctor_id: uuid.UUID) -> Doctor | None:
    return db.query(Doctor).filter(Doctor.id == doctor_id).first()


def update_doctor_profile(db: Session, doctor: Doctor, payload: DoctorUpdate) -> Doctor:
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(doctor, field, value)
    db.commit()
    db.refresh(doctor)
    return doctor


def list_all_doctors(db: Session) -> list[Doctor]:
    return db.query(Doctor).all()
