FROM python:3.12-slim

# System dependencies:
# - tesseract-ocr: needed for OCR text extraction (Chunk 13)
# - libpq-dev, gcc: needed to build psycopg2-binary correctly on some platforms
RUN apt-get update && apt-get install -y --no-install-recommends \
    tesseract-ocr \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p uploads vectorstore_data

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
