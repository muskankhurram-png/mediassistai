"""
Module 6 (Resume AI Chat equivalent) - RAG chatbot routes.
"""
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_patient_profile
from app.database.session import get_db
from app.schemas.chat import ChatHistoryOut, ChatRequest, ChatResponse
from app.services.chat_service import ask_question, list_chat_history

router = APIRouter(prefix="/chat", tags=["AI Chat"])


@router.post("", response_model=ChatResponse)
def chat(
    payload: ChatRequest,
    patient=Depends(get_current_patient_profile),
    db: Session = Depends(get_db),
):
    entry = ask_question(db, patient.id, payload.question)
    sources = entry.sources.split("\n") if entry.sources else []
    return ChatResponse(answer=entry.answer, sources=sources)


@router.get("/history", response_model=list[ChatHistoryOut])
def chat_history(
    patient=Depends(get_current_patient_profile),
    db: Session = Depends(get_db),
):
    return list_chat_history(db, patient.id)
