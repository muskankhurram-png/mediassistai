"""
Patient profile routes.
"""
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user, require_roles
from app.database.session import get_db
from app.models.user import User
from app.schemas.patient import PatientCreate, PatientOut, PatientUpdate
from app.services.patient_service import (
    create_patient_profile,
    get_patient_by_id,
    list_all_patients,
    update_patient_profile,
)

router = APIRouter(prefix="/patients", tags=["Patients"])


@router.post("", response_model=PatientOut, status_code=201)
def create_patient(
    payload: PatientCreate,
    current_user: User = Depends(require_roles("patient")),
    db: Session = Depends(get_db),
):
    try:
        patient = create_patient_profile(db, current_user, payload)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    return patient


@router.get("", response_model=list[PatientOut])
def get_patients(
    _: User = Depends(require_roles("doctor", "admin")),
    db: Session = Depends(get_db),
):
    return list_all_patients(db)


@router.get("/{patient_id}", response_model=PatientOut)
def get_patient(
    patient_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    patient = get_patient_by_id(db, patient_id)
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    if current_user.role == "patient" and patient.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only view your own patient record")
    return patient


@router.put("/{patient_id}", response_model=PatientOut)
def update_patient(
    patient_id: uuid.UUID,
    payload: PatientUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    patient = get_patient_by_id(db, patient_id)
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    if current_user.role == "patient" and patient.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only update your own patient record")
    return update_patient_profile(db, patient, payload)
