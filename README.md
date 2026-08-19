# 🩺 MediAssist AI

**An AI-powered healthcare coordination platform** — patients manage appointments, prescriptions, and medical reports in one place, with an AI assistant that answers questions grounded in their own uploaded records.

Built from scratch as a learning project: a FastAPI + PostgreSQL backend, a server-rendered Jinja2 frontend, and a Retrieval-Augmented Generation (RAG) chatbot powered by Google Gemini.

---

## ✨ Features

### For Patients
- Register, log in, and manage a personal health profile (blood group, allergies, emergency contact)
- Browse doctors and request to be added to their care
- Book, view, and cancel appointments
- View prescriptions written by assigned doctors
- Upload medical reports (PDF, JPG, PNG) with automatic text extraction (PyMuPDF + Tesseract OCR)
- **Ask AI** — a chat assistant that answers questions using *only* that patient's own uploaded reports
- One-click AI report summaries and risk-flag detection
- Look up plain-language explanations of diseases and medicines

### For Doctors
- Manage a professional profile (specialization, availability)
- Approve or reject incoming patient assignment requests
- Publish open appointment slots
- Write structured prescriptions with multiple medicines, dosages, and notes
- View assigned patients

### Platform-wide
- JWT-based REST API (for programmatic/API access) **and** session-cookie web pages (for the browser UI) — both backed by the same service layer
- Role-based access control (Patient / Doctor / Admin)
- Per-patient isolated vector stores — the chatbot can *never* retrieve another patient's data, enforced at the storage layer, not just in application logic
- Fully Dockerized: one command sets up the database, runs migrations, and starts the app

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend framework | FastAPI |
| Database | PostgreSQL + SQLAlchemy + Alembic |
| Auth | JWT (API) + signed session cookies (web UI) |
| Frontend | Jinja2 templates, vanilla CSS/JavaScript (no framework) |
| AI / LLM | Google Gemini (`gemini-2.5-flash-lite`) via LangChain |
| Embeddings & Vector Store | Gemini Embeddings + ChromaDB (per-patient collections) |
| Document Processing | PyMuPDF (PDF text) + Tesseract OCR (scanned images) |
| Containerization | Docker + Docker Compose |

---

## 📁 Project Structure

```
mediassistai/
├── app/
│   ├── main.py                    # FastAPI app entrypoint, router wiring
│   ├── core/
│   │   ├── config.py              # Settings loaded from .env
│   │   ├── security.py            # Password hashing, JWT creation/validation
│   │   ├── dependencies.py        # JWT-based auth dependencies (API)
│   │   └── web_auth.py            # Session-cookie auth dependencies (web UI)
│   ├── database/
│   │   ├── base.py                # SQLAlchemy declarative base
│   │   └── session.py             # DB engine/session factory
│   ├── models/                    # SQLAlchemy ORM models (9 tables)
│   ├── schemas/                   # Pydantic request/response schemas
│   ├── services/                  # Business logic layer
│   │   └── (chat, prescription, appointment, report, assignment services...)
│   ├── ai/
│   │   ├── llm.py                 # Gemini chat model wrapper
│   │   ├── vector_store.py        # Per-patient Chroma collections
│   │   ├── rag_engine.py          # Retrieval + answer generation
│   │   ├── ai_features.py         # Summary, risk alerts, explanations
│   │   ├── text_splitter.py       # Chunking for embeddings
│   │   ├── text_extraction.py     # PDF/OCR routing
│   │   ├── pdf_extractor.py       # PyMuPDF text extraction
│   │   └── ocr.py                 # Tesseract OCR
│   └── api/v1/routes/
│       ├── auth.py, patients.py, doctors.py, ...     # JSON API (Swagger)
│       └── web_*.py                                  # Web UI routes (HTML pages)
├── templates/                     # Jinja2 HTML templates
├── static/
│   ├── css/style.css               # Design system (colors, components, animations)
│   └── js/                         # Chat, toast notifications, AI panels
├── alembic/                       # Database migrations
├── uploads/                       # Uploaded report files (gitignored)
├── vectorstore_data/               # Chroma vector DB (gitignored)
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env.example
└── README.md
```

---

## 🚀 Getting Started

### Option A — Docker (recommended)

**Prerequisites:** [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.

```bash
git clone https://github.com/<your-username>/mediassistai.git
cd mediassistai
cp .env.example .env
```

Edit `.env` and fill in:
- `JWT_SECRET_KEY` / `SESSION_SECRET_KEY` — any long random strings
- `GEMINI_API_KEY` — get a free key at [aistudio.google.com/apikey](https://aistudio.google.com/apikey)

Then start everything:

```bash
docker compose up
```

This will:
1. Pull and start a PostgreSQL 16 container
2. Build the app image (installs Python deps + Tesseract OCR)
3. Run all Alembic migrations automatically
4. Start the FastAPI server

Once you see `Application startup complete.`, open:
- **App:** http://localhost:8000
- **API docs (Swagger):** http://localhost:8000/docs

Stop it with `Ctrl+C`, then `docker compose down`.

### Option B — Local (without Docker)

**Prerequisites:** Python 3.12+, PostgreSQL 16, [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki).

```bash
python -m venv .venv
.venv\Scripts\activate          # Windows
# source .venv/bin/activate     # macOS/Linux

pip install -r requirements.txt
cp .env.example .env            # fill in your values
```

Create the database and update `DATABASE_URL` in `.env` to match, then:

```bash
alembic upgrade head
uvicorn app.main:app --reload
```

---

## 🔑 Environment Variables

| Variable | Description |
|---|---|
| `DATABASE_URL` | PostgreSQL connection string |
| `JWT_SECRET_KEY` | Secret used to sign API JWT tokens |
| `SESSION_SECRET_KEY` | Secret used to sign web session cookies |
| `GEMINI_API_KEY` | Google Gemini API key ([free tier available](https://aistudio.google.com/apikey)) |
| `CHAT_MODEL` | Gemini model for chat responses (default: `gemini-2.5-flash-lite`) |
| `EMBEDDING_MODEL` | Gemini model for embeddings (default: `models/gemini-embedding-001`) |
| `UPLOAD_DIR` | Local folder for uploaded report files |
| `VECTOR_STORE_DIR` | Local folder for the Chroma vector database |

See `.env.example` for a template.

---

## 🤖 How the RAG Chatbot Works

1. When a patient uploads a report, its text is extracted (PyMuPDF for native PDFs, Tesseract OCR as a fallback for scanned images)
2. The text is split into overlapping chunks and embedded using Gemini's embedding model
3. Each patient's chunks are stored in a **separate Chroma collection**, keyed by patient ID — there is no code path that opens more than one patient's collection at a time
4. When a patient asks a question, the system retrieves the most relevant chunks from *their own* collection only, and asks Gemini to answer using *only* that retrieved context
5. Every response includes a disclaimer that it is educational information, not a medical diagnosis

This architecture is a deliberate security choice, not just a convenience — it makes it structurally impossible for the chatbot to leak one patient's data into another's conversation.

---
## 🗺️ Possible Future Improvements

- Automated test suite (pytest)
- Rate limiting on AI endpoints
- Doctor-side view of patient-uploaded reports
- Email notifications for appointment reminders
- Deployment guide for Railway / Render / Fly.io

---

## ⚠️ Disclaimer

MediAssist AI is an educational project. All AI-generated content (summaries, risk alerts, explanations, chat answers) is for informational purposes only and is **not a substitute for professional medical advice, diagnosis, or treatment**. Always consult a qualified healthcare provider with any questions about a medical condition.

---

## 📄 License

This project was built for educational purposes. Feel free to fork and adapt it.
