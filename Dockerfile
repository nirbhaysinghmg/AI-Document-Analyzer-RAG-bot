FROM python:3.12.4-slim-bullseye

WORKDIR /app

# Install system dependencies
RUN apt-get update && \
    apt-get install -y \
        build-essential \
        libpq-dev \
        tesseract-ocr \
        libtesseract-dev \
        libleptonica-dev \
        poppler-utils \
        wget \
        tcl-dev \
        tk-dev \
        && rm -rf /var/lib/apt/lists/*

# Install latest SQLite from source
RUN wget https://www.sqlite.org/2024/sqlite-autoconf-3450200.tar.gz && \
    tar xvfz sqlite-autoconf-3450200.tar.gz && \
    cd sqlite-autoconf-3450200 && \
    ./configure --prefix=/usr/local && \
    make && \
    make install && \
    cd .. && \
    rm -rf sqlite-autoconf-3450200*

# Set environment variables to use the new sqlite3
ENV LD_LIBRARY_PATH=/usr/local/lib:$LD_LIBRARY_PATH
ENV PATH=/usr/local/bin:$PATH

# Rebuild Python's sqlite3 module with the new sqlite3
RUN python -m pip install --upgrade pip setuptools wheel && \
    python -c "import sqlite3; print('SQLite version:', sqlite3.sqlite_version)" && \
    python -m pip install --force-reinstall --no-cache-dir pysqlite3-binary

# Verify SQLite version
RUN sqlite3 --version

COPY requirements.txt .

# Install dependencies
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