from fastapi import FastAPI, Request
from fastapi.exceptions import HTTPException
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.sessions import SessionMiddleware

from app.api.v1.routes import (
    ai,
    appointments,
    assignments,
    auth,
    chat,
    doctors,
    patients,
    prescriptions,
    reports,
    web_ai_features,
    web_appointments,
    web_auth,
    web_chat,
    web_dashboard,
    web_doctor_dashboard,
    web_doctor_slots,
    web_doctors,
    web_prescriptions,
    web_profile_setup,
    web_reports,
)
from app.core.config import settings
from app.core.web_auth import get_current_user_web

app = FastAPI(title=settings.APP_NAME)

app.add_middleware(SessionMiddleware, secret_key=settings.SESSION_SECRET_KEY)

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

app.include_router(auth.router, prefix="/api/v1")
app.include_router(patients.router, prefix="/api/v1")
app.include_router(doctors.router, prefix="/api/v1")
app.include_router(assignments.router, prefix="/api/v1")
app.include_router(appointments.router, prefix="/api/v1")
app.include_router(prescriptions.router, prefix="/api/v1")
app.include_router(reports.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")
app.include_router(ai.router, prefix="/api/v1")
app.include_router(web_auth.router)
app.include_router(web_dashboard.router)
app.include_router(web_doctor_dashboard.router)
app.include_router(web_doctors.router)
app.include_router(web_appointments.router)
app.include_router(web_prescriptions.router)
app.include_router(web_reports.router)
app.include_router(web_doctor_slots.router)
app.include_router(web_profile_setup.router)
app.include_router(web_chat.router)
app.include_router(web_ai_features.router)


@app.exception_handler(404)
async def custom_404_handler(request: Request, exc: HTTPException):
    if request.url.path.startswith("/api/"):
        return JSONResponse(status_code=404, content={"detail": exc.detail})

    user = get_current_user_web(request)
    return templates.TemplateResponse(
        request, "404.html", {"user": user}, status_code=404
    )


@app.get("/health")
def health_check():
    return {
        "success": True,
        "status": "ok",
        "app_name": settings.APP_NAME,
        "environment": settings.ENVIRONMENT,
    }


@app.get("/")
def home_page(request: Request):
    user = get_current_user_web(request)
    return templates.TemplateResponse(request, "home.html", {"user": user})
