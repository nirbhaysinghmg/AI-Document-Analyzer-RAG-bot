# Document Analysis Chatbot - Development Brief

# Summary:

The frontend is a basic react app that is connected through the websocket to the backend app.py, The app is designed such that the user have to upload their document before proceeding with the query, The user can upload their document, There is a UI to track and select their document, The user can ask the question about their document and it will answer accordingly with the citations.

For each session their is a session id is created and for that session id the document are processed
The citation table format is created using react to show the citations and page number and lines.

## Project Overview

This project implements an intelligent document analysis chatbot capable of processing various document formats and providing context-aware responses to user queries. The system leverages modern AI technologies and natural language processing to deliver meaningful insights from document content.

## Technical Approach

### Core Technology Stack

- **Backend Framework**: FastAPI

  - Chosen for its high performance, async support, and modern Python features
  - Provides excellent WebSocket support for real-time communication
  - Built-in API documentation and validation

- **AI & NLP Components**:

  - Google's Gemini AI for embeddings and chat capabilities
  - LangChain for document processing and AI interactions
  - ChromaDB for vector storage and efficient document retrieval

- **Document Processing**:
  - Tesseract OCR for image text extraction
  - PyPDF2 for PDF processing
  - python-docx for Word document handling

### Architecture Design

#### 1. Document Processing Pipeline

- Implemented a modular pipeline for handling multiple file formats
- Created a chunking system to break documents into manageable pieces
- Added metadata tracking for better document organization
- Implemented background processing for large documents

#### 2. Session Management

- Developed a session-based architecture for multi-user support
- Implemented WebSocket connections for real-time communication
- Created a robust connection manager with proper cleanup
- Added session persistence and state management

#### 3. AI Integration

- Integrated Google's Gemini AI for document analysis
- Implemented theme analysis system for topic identification
- Created citation system for information tracking
- Built context-aware chat history system

## Methodology

### 1. Development Approach

- Used an iterative development methodology
- Implemented features incrementally
- Focused on modularity and maintainability
- Prioritized user experience and performance

### 2. Key Features Implementation

- **Document Processing**:

  - Unified processing pipeline for multiple formats
  - Efficient text extraction and chunking
  - Metadata preservation and tracking

- **Real-time Communication**:

  - WebSocket implementation for instant updates
  - Background task processing
  - Progress tracking and status updates

- **AI Analysis**:
  - Theme identification and extraction
  - Context-aware responses
  - Citation and source tracking

### 3. Performance Considerations

- Implemented async processing for better scalability
- Used background tasks for heavy operations
- Optimized document chunking and storage
- Implemented efficient vector search

## Challenges and Solutions

### 1. Document Processing

**Challenge**: Handling diverse file formats while maintaining context
**Solution**: Created a unified processing pipeline with format-specific handlers

### 2. Real-time Communication

**Challenge**: Managing WebSocket connections and session state
**Solution**: Implemented a robust connection manager with proper cleanup

### 3. Performance

**Challenge**: Processing large documents efficiently
**Solution**: Implemented chunking and background processing

### 4. Document Text Storage

**Challenge**: Maintaining page and paragraph structure while processing documents
**Solution**: Implemented a structured storage approach using arrays to store page texts and paragraph texts separately, ensuring proper document structure preservation and easier navigation

### 5. Deployment

**Challenge**: First-time deployment on Render platform with complex dependencies and environment setup
**Solution**: Implemented a keep-alive mechanism, proper environment variable management, and configured the application for cloud deployment with appropriate timeout settings and worker configurations

## Future Enhancements

1. Support for additional document formats
2. Implementation of caching mechanisms
3. User authentication and authorization
4. Enhanced theme analysis capabilities
5. Document versioning support

## Implementation Details

### Document Processing System

#### File Type Handlers

- **PDF Processing**:

  - Implemented page-by-page text extraction
  - Maintained page numbers and line numbers
  - Preserved document structure in metadata

- **DOCX Processing**:

  - Paragraph-level text extraction
  - Maintained paragraph numbering
  - Converted paragraphs to line-based format for consistency

- **Text File Processing**:

  - Direct UTF-8 text extraction
  - Simple and efficient processing

- **Image Processing**:
  - OCR implementation using Tesseract
  - Error handling for image processing failures

#### Document Storage and Retrieval

- Implemented chunking system with:
  - 500-character chunk size
  - 50-character overlap
  - Line-based separation
- Maintained detailed metadata for each chunk:
  - Source file information
  - Page/line numbers
  - Chunk indices
  - Original file references

### Query Processing System

#### Query Handling

- Session-based query management
- Chat history maintenance (limited to 10 interactions)
- Context-aware responses using previous interactions

#### Response Generation

- Implemented theme extraction from responses
- Citation tracking with:
  - Page numbers
  - Line ranges
  - Chunk references
- Structured response format with:
  - Main answer
  - Individual document answers
  - Theme analysis
  - Source citations

#### Error Handling

- Comprehensive error management for:
  - File processing failures
  - Invalid file types
  - Empty documents
  - Processing errors
- Detailed error messages for debugging
- HTTP status code mapping

### Session Management System

#### Session Handling

- Implemented session-based architecture for multi-user support
- Unique session ID generation for each user
- Separate storage for:
  - Chat histories
  - Document collections
  - Original file metadata

#### Session Cleanup

- Individual session cleanup functionality:
  - Removes chat history
  - Clears document collections
  - Deletes original file records
  - Removes ChromaDB session directory
- Global session management:
  - Bulk session clearing capability
  - Complete system reset functionality
  - Automatic cleanup of all session directories

#### Resource Management

- Efficient memory management through session cleanup
- Automatic removal of temporary files
- Prevention of resource leaks
- Maintained system performance through proper cleanup

### Bulk Processing System

#### Background Processing

- Implemented asynchronous document processing
- Concurrent file handling using asyncio
- Background task management for large uploads
- Progress tracking and status updates

#### Processing Pipeline

- File type detection and validation
- Parallel processing of multiple documents
- Metadata preservation and tracking
- Error handling and recovery mechanisms

#### Status Management

- Real-time progress monitoring
- Detailed status tracking:
  - Total files
  - Processed files
  - Failed files
  - Completion percentage
- Session-based status updates

### Server Configuration

#### Performance Optimization

- Single worker configuration for stability
- Optimized keep-alive timeout settings
- Environment-based port configuration
- Graceful shutdown handling

#### Signal Handling

- SIGTERM signal management
- Graceful shutdown implementation
- Resource cleanup on termination
- Process state preservation

#### Deployment Settings

- Configurable port through environment variables
- Host binding to all interfaces (0.0.0.0)
- Log level configuration
- Worker process management

## Conclusion

The document analysis chatbot successfully combines modern AI capabilities with robust document processing to provide a powerful tool for document analysis. The system's architecture allows for easy scaling and future enhancements while maintaining good performance and user experience.

This project demonstrates the practical application of AI and natural language processing in document analysis, providing valuable insights and information extraction capabilities to users.
