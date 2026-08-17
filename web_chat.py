"""
Web page + AJAX routes for the patient-facing chat interface.
Uses session-cookie auth (like every other web_*.py route), not the
JWT-based JSON API - so the browser doesn't need a separate token.
"""
from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.core.web_auth import get_current_user_web
from app.database.session import SessionLocal
from app.models.patient import Patient
from app.services.chat_service import ask_question, list_chat_history

router = APIRouter(tags=["Web - Chat"])
templates = Jinja2Templates(directory="templates")


@router.get("/chat")
def chat_page(request: Request):
    user = get_current_user_web(request)
    if user is None or user.role != "patient":
        return RedirectResponse(url="/login", status_code=303)

    db = SessionLocal()
    try:
        patient = db.query(Patient).filter(Patient.user_id == user.id).first()
        if patient is None:
            return RedirectResponse(url="/dashboard?error=Complete+your+patient+profile+first", status_code=303)

        history = list_chat_history(db, patient.id)
        history = list(reversed(history))  # oldest first, so it reads top-to-bottom

        return templates.TemplateResponse(request, "chat.html", {
            "user": user,
            "history": history,
        })
    finally:
        db.close()


@router.post("/chat/ask")
async def chat_ask(request: Request):
    user = get_current_user_web(request)
    if user is None or user.role != "patient":
        return JSONResponse(status_code=401, content={"detail": "Please log in again."})

    body = await request.json()
    question = (body.get("question") or "").strip()
    if not question:
        return JSONResponse(status_code=400, content={"detail": "Please enter a question."})

    db = SessionLocal()
    try:
        patient = db.query(Patient).filter(Patient.user_id == user.id).first()
        if patient is None:
            return JSONResponse(status_code=400, content={"detail": "Complete your patient profile first."})

        try:
            entry = ask_question(db, patient.id, question)
        except Exception:
            return JSONResponse(
                status_code=500,
                content={"detail": "Something went wrong generating an answer. Please try again in a moment."},
            )

        sources = entry.sources.split("\n") if entry.sources else []
        return JSONResponse(content={"answer": entry.answer, "sources": sources})
    finally:
        db.close()
