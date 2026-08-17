"""
The core RAG pipeline: given a patient and a question, retrieve the
most relevant chunks from that patient's own vector store, then ask
the LLM to answer using only that retrieved context.
"""
import uuid

from app.ai.llm import invoke_llm
from app.ai.vector_store import get_patient_vector_store

SYSTEM_PROMPT = """You are a medical report assistant helping a patient understand their own health records.

Rules you must follow:
- Answer ONLY using the information in the provided context below.
- If the context doesn't contain enough information to answer, say so clearly instead of guessing.
- Keep answers clear, simple, and free of unnecessary jargon.
- You are not a doctor. Do not provide a diagnosis or tell the patient what to do medically.
- Remind the patient to consult their doctor for any medical decisions.

Context from the patient's medical records:
{context}

Patient's question: {question}

Answer:"""


def answer_patient_question(patient_id: uuid.UUID, question: str, top_k: int = 4) -> dict:
    store = get_patient_vector_store(patient_id)
    results = store.similarity_search(question, k=top_k)

    if not results:
        return {
            "answer": (
                "I couldn't find anything in your uploaded reports related to that question. "
                "Try uploading the relevant report first, or ask your doctor directly."
            ),
            "sources": [],
        }

    context = "\n\n---\n\n".join(r.page_content for r in results)
    prompt = SYSTEM_PROMPT.format(context=context, question=question)

    answer = invoke_llm(prompt)

    sources = [
        f"Report chunk {r.metadata.get('chunk_index', '?')} (report {r.metadata.get('report_id', 'unknown')})"
        for r in results
    ]

    return {
        "answer": answer,
        "sources": sources,
    }
