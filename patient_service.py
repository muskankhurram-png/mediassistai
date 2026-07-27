"""
Business logic for patient profiles.
"""
import uuid

from sqlalchemy.orm import Session

from app.models.patient import Patient
from app.models.user import User
from app.schemas.patient import PatientCreate, PatientUpdate


def create_patient_profile(db: Session, user: User, payload: PatientCreate) -> Patient:
    existing = db.query(Patient).filter(Patient.user_id == user.id).first()
    if existing:
        raise ValueError("Patient profile already exists for this account")

    patient = Patient(user_id=user.id, **payload.model_dump())
    db.add(patient)
    db.commit()
    db.refresh(patient)
    return patient


def get_patient_by_id(db: Session, patient_id: uuid.UUID) -> Patient | None:
    return db.query(Patient).filter(Patient.id == patient_id).first()


def update_patient_profile(db: Session, patient: Patient, payload: PatientUpdate) -> Patient:
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(patient, field, value)
    db.commit()
    db.refresh(patient)
    return patient


def list_all_patients(db: Session) -> list[Patient]:
    return db.query(Patient).all()
