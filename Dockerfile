FROM python:3.12.4-slim-bullseye

WORKDIR /app

# Install system dependencies + updated SQLite
RUN apt-get update && \
    apt-get install -y \
        build-essential \
        libpq-dev \
        tesseract-ocr \
        libtesseract-dev \
        libleptonica-dev \
        poppler-utils \
        wget && \
    # Add testing repo for newer SQLite
    echo "deb http://deb.debian.org/debian testing main" > /etc/apt/sources.list.d/testing.list && \
    apt-get update && \
    # Install SQLite from testing - CORRECTED COMMAND
    apt-get install -y -t testing sqlite3 && \
    # Cleanup
    rm -rf /var/lib/apt/lists/* \
        /etc/apt/sources.list.d/testing.list

# Verify SQLite version (optional)
RUN sqlite3 --version

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