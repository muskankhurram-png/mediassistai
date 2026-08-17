"""
Smaller, single-purpose AI features that don't need retrieval (RAG) -
just a direct prompt to Gemini. Reuses the same get_llm() wrapper
from Chunk 15.
"""
from app.ai.llm import invoke_llm

DISCLAIMER = (
    "This is an educational AI-generated explanation, not a medical diagnosis. "
    "Please consult your doctor for confirmation and medical decisions."
)


def summarize_report(extracted_text: str) -> str:
    if not extracted_text or not extracted_text.strip():
        return "No readable text was found in this report to summarize."

    prompt = f"""You are a medical report assistant. Summarize the following medical
report in simple, plain language a patient without medical training can understand.
Mention any values that appear notably high or low, but do not diagnose anything.
Keep it to 3-5 short sentences.

Report text:
{extracted_text[:6000]}

Summary:"""

    return invoke_llm(prompt)


def generate_risk_alerts(extracted_text: str) -> list[str]:
    if not extracted_text or not extracted_text.strip():
        return []

    prompt = f"""Look at the following medical report text. List ONLY values that
appear to fall outside a typical normal reference range, as short flags like
"High blood pressure detected" or "Low hemoglobin observed". If everything looks
normal or you cannot tell, return exactly: None

One flag per line, no numbering, no extra commentary.

Report text:
{extracted_text[:6000]}

Flags:"""

    text = invoke_llm(prompt).strip()
    if not text or text.lower() == "none":
        return []
    return [line.strip("- ").strip() for line in text.split("\n") if line.strip()]


def explain_disease(disease_name: str) -> str:
    prompt = f"""Explain the disease/condition "{disease_name}" to a patient in simple
language. Structure your answer with these short sections: Overview, Symptoms,
Causes, Diagnosis, Treatment, Prevention. Keep each section to 1-2 sentences.

Explanation:"""

    return invoke_llm(prompt)


def explain_medicine(medicine_name: str) -> str:
    prompt = f"""Explain the medicine "{medicine_name}" to a patient in simple language.
Cover: what it is used for, how it works, common side effects, precautions, and
when it's typically taken. Keep it concise and easy to understand.

Explanation:"""

    return invoke_llm(prompt)


def simplify_prescription(medicines: list[dict], notes: str | None) -> str:
    medicine_lines = "\n".join(
        f"- {m.get('name', '')} {m.get('dosage', '')} {m.get('frequency', '')} {m.get('duration', '')}".strip()
        for m in medicines
    )
    notes_line = f"\nDoctor's notes: {notes}" if notes else ""

    prompt = f"""Convert this clinical prescription shorthand into simple,
patient-friendly instructions, as 1-2 short sentences per medicine.

Medicines:
{medicine_lines}
{notes_line}

Patient-friendly instructions:"""

    return invoke_llm(prompt)
