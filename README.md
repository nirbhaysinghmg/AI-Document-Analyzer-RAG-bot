# Document Analysis Chatbot

This satisfy all the requirements of the given objective of the chatbot to my best knowledge, If anything is left out, I am so sorry for that
I did not left it intentionally

A powerful document analysis chatbot built with FastAPI and Google's Gemini AI that can process, analyze, and extract themes from various document types.

## Features

- **Multi-Document Support**: Process PDFs, Word documents, text files, and images (with OCR)\
- **Multi-Document Support**: Process PDFs, Word documents, text files, and images (with OCR)
- **Theme Analysis**: Automatically identifies and extracts themes from documents
- **Real-time Chat**: WebSocket support for real-time document analysis and Q&A
- **Session Management**: Maintains separate document collections and chat histories for different sessions
- **Citation Support**: Provides detailed citations for extracted information
- **Document Management**: Upload, list, and delete documents with metadata support
- **Bulk Document Processing**: Supports processing of 75+ documents with optimized chunking and storage

## Document Ingestion Capabilities

The system is designed to handle large document collections with the following features:

### Performance Optimizations

- Efficient document chunking (500 characters per chunk with 50 character overlap)
- Asynchronous document processing
- Session-based document management
- Optimized vector storage using ChromaDB

### Memory Management

- Documents are processed in chunks to manage memory efficiently
- Each document is stored with unique identifiers
- Automatic cleanup of unused sessions
- Efficient retrieval using similarity search

### Limitations and Considerations

- Processing time increases with document size and count
- Memory usage scales with the number of documents and their size
- WebSocket connections may timeout for very large document sets
- Consider implementing pagination for document listing
- Monitor system resources when processing large document sets

### Best Practices for Large Document Sets

1. Process documents in batches
2. Monitor system memory usage
3. Implement proper error handling for failed uploads
4. Use appropriate chunk sizes based on document types
5. Consider implementing a queue system for very large document sets

## Prerequisites

Python 3.8+
Tesseract OCR (for image processing)
Google Gemini API key
fastapi==0.104.1
uvicorn==0.24.0
python-dotenv==1.0.0
langchain==0.0.350
langchain-google-genai==0.0.5
langchain-chroma==0.0.1
chromadb==0.4.18
google-generativeai==0.3.1
pandas==2.1.3
python-multipart==0.0.6
PyPDF2==3.0.1
python-docx==1.0.1
pytesseract==0.3.10
Pillow==10.1.0
mysql-connector-python==8.2.0
websockets==12.0

2. Install dependencies:

```bash
pip install -r requirements.txt
```

3. Install Tesseract OCR:

- Windows: Download and install from [Tesseract GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
- Linux: `sudo apt-get install tesseract-ocr`
- macOS: `brew install tesseract`

4. Create a `.env` file with your configuration:

```env
GEMINI_API_KEY=your_api_key_here
EMBED_MODEL=models/embedding-001
LLM_MODEL=gemini-2.0-flash
PERSIST_DIRECTORY=chroma_db
```

## Usage

1. Start the server:

```bash
python app.py
```

The server will start on `http://0.0.0.0:8008`

### API Endpoints

- `POST /upload/document`: Upload a document for analysis
- `POST /query`: Query the document collection
- `GET /documents`: List all documents in a session
- `DELETE /documents/{document_id}`: Delete a specific document
- `DELETE /session/{session_id}`: Clear a specific session
- `DELETE /sessions/clear`: Clear all sessions
- `WebSocket /ws`: Real-time chat endpoint

### WebSocket Connection

Connect to the WebSocket endpoint for real-time document analysis:

```javascript
const ws = new WebSocket("ws://localhost:8008/ws");
ws.onmessage = (event) => {
  const response = JSON.parse(event.data);
  // Handle response
};
```

## Document Processing

The system supports the following file types:

- PDF (.pdf)
- Word Documents (.docx, .doc)
- Text Files (.txt)
- Images (.jpg, .jpeg, .png) with OCR

## Theme Analysis

The chatbot uses a specialized prompt template to:

1. Analyze document excerpts
2. Identify main themes and patterns
3. Provide synthesized summaries with citations

## Security

- CORS middleware is configured to allow specific origins
- Session-based document management
- Secure WebSocket connections

## Error Handling

The system includes comprehensive error handling for:

- File processing errors
- Invalid file types
- Missing documents
- WebSocket disconnections
- API errors

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
