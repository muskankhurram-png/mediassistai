"""
Wraps Gemini embeddings + a per-patient Chroma vector store collection.
Keeping one collection per patient is what guarantees the chatbot can
never accidentally retrieve a different patient's data.
"""
import uuid

from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

from app.core.config import settings

_embeddings = GoogleGenerativeAIEmbeddings(
    model=settings.EMBEDDING_MODEL,
    google_api_key=settings.GEMINI_API_KEY,
)


def get_patient_vector_store(patient_id: uuid.UUID) -> Chroma:
    collection_name = f"patient_{patient_id}"
    return Chroma(
        collection_name=collection_name,
        embedding_function=_embeddings,
        persist_directory=settings.VECTOR_STORE_DIR,
    )


def add_report_chunks(patient_id: uuid.UUID, report_id: uuid.UUID, chunks: list[str]) -> list[str]:
    if not chunks:
        return []

    store = get_patient_vector_store(patient_id)
    ids = [f"{report_id}_{i}" for i in range(len(chunks))]
    metadatas = [{"report_id": str(report_id), "chunk_index": i} for i in range(len(chunks))]

    store.add_texts(texts=chunks, metadatas=metadatas, ids=ids)
    return ids
