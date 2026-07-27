"""
Doctor profile routes.
"""
import uuid

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.dependencies import require_roles
from app.database.session import get_db
from app.models.user import User
from app.schemas.doctor import DoctorCreate, DoctorOut, DoctorUpdate
from app.services.doctor_service import (
    create_doctor_profile,
    get_doctor_by_id,
    list_all_doctors,
    update_doctor_profile,
)

router = APIRouter(prefix="/doctors", tags=["Doctors"])


@router.post("", response_model=DoctorOut, status_code=201)
def create_doctor(
    payload: DoctorCreate,
    current_user: User = Depends(require_roles("doctor")),
    db: Session = Depends(get_db),
):
    try:
        doctor = create_doctor_profile(db, current_user, payload)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    return doctor


@router.get("", response_model=list[DoctorOut])
def get_doctors(db: Session = Depends(get_db)):
    return list_all_doctors(db)


@router.get("/{doctor_id}", response_model=DoctorOut)
def get_doctor(doctor_id: uuid.UUID, db: Session = Depends(get_db)):
    doctor = get_doctor_by_id(db, doctor_id)
    if doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


@router.put("/{doctor_id}", response_model=DoctorOut)
def update_doctor(
    doctor_id: uuid.UUID,
    payload: DoctorUpdate,
    current_user: User = Depends(require_roles("doctor")),
    db: Session = Depends(get_db),
):
    doctor = get_doctor_by_id(db, doctor_id)
    if doctor is None:
        raise HTTPException(status_code=404, detail="Doctor not found")
    if doctor.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="You can only update your own doctor record")
    return update_doctor_profile(db, doctor, payload)
