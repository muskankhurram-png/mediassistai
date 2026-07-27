
"""
Authentication routes: register and login.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database.session import get_db
from app.schemas.user import TokenOut, UserLogin, UserOut, UserRegister
from app.services.auth_service import authenticate_user, issue_token, register_user

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/register", response_model=UserOut, status_code=201)
def register(payload: UserRegister, db: Session = Depends(get_db)):
    try:
        user = register_user(db, payload)
    except ValueError as exc:
        raise HTTPException(status_code=409, detail=str(exc))
    return user


@router.post("/login", response_model=TokenOut)
def login(payload: UserLogin, db: Session = Depends(get_db)):
    try:
        user = authenticate_user(db, payload)
    except ValueError as exc:
        raise HTTPException(status_code=401, detail=str(exc))
    token = issue_token(user)
    return TokenOut(access_token=token)
