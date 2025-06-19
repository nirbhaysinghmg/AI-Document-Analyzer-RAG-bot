# Stage 1: Frontend Build
FROM node:18-alpine as frontend-build

# Set working directory
WORKDIR /app/frontend

# Copy frontend package files
COPY frontend/package*.json ./

# Install frontend dependencies
RUN npm install

# Copy frontend source code
COPY frontend/ ./

# Build frontend
RUN npm run build

# Stage 2: Backend Build
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    tesseract-ocr \
    && rm -rf /var/lib/apt/lists/*

# Copy backend requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend source code
COPY app.py .
COPY .env .

# Copy built frontend files from previous stage
COPY --from=frontend-build /app/frontend/dist /app/static

# Create directory for ChromaDB
RUN mkdir -p chroma_db

# Expose port
EXPOSE 8008

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PORT=8008

# Run the application
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8008"] 