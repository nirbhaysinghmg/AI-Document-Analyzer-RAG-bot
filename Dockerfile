# Use Python 3.11 slim image with Debian Bullseye for stability
FROM python:3.11-slim-bullseye

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    tesseract-ocr \
    libtesseract-dev \
    libleptonica-dev \
    poppler-utils \  # Required for PDF processing
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for better dependency resolution
ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_RESOLVER=backtracking

# Copy requirements first for better caching
COPY requirements.txt .

# Upgrade pip and install Python dependencies in two stages
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-cache-dir \
    googleapis-common-protos \
    google-api-core \
    google-ai-generativelanguage \
    grpcio-status && \
    pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Create directory for ChromaDB
RUN mkdir -p chroma_db

# Expose port
EXPOSE 8008

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8008

# Run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8008"]