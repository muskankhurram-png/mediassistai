from fastapi import FastAPI

from app.api.v1.routes import auth, doctors, patients
from app.core.config import settings
from app.database.session import engine
from app.database.base import Base
import app.models.user
import app.models.patient
import app.models.doctor
# Ensure the User model is imported so that its relationships are registered
Base.metadata.create_all(bind=engine)
app = FastAPI(title=settings.APP_NAME)

app.include_router(auth.router, prefix="/api/v1")
app.include_router(patients.router, prefix="/api/v1")
app.include_router(doctors.router, prefix="/api/v1")


@app.get("/health")
def health_check():
    return {
        "success": True,
        "status": "ok",
        "app_name": settings.APP_NAME,
        "environment": settings.ENVIRONMENT,
    }
