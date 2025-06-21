FROM python:3.11-slim-bullseye

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    tesseract-ocr \
    libtesseract-dev \
    libleptonica-dev \
    poppler-utils \
    && rm -rf /var/lib/apt/lists/*

# Set pip environment variables
ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

COPY requirements.txt .

# Install dependencies in optimal order
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir \
    googleapis-common-protos \
    google-api-core \
    google-ai-generativelanguage \
    grpcio-status
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN mkdir -p chroma_db

EXPOSE 8008

ENV PYTHONUNBUFFERED=1
ENV PORT=8008

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8008"]