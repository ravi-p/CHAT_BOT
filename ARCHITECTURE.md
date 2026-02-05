# Multi-Session Chat Application - Architecture Guide

## Overview
The chat application has been refactored to support **multiple independent chat sessions** with a scalable, modular architecture. Each session has its own document context, chat history, and memory management.

## Backend Architecture

### 🏗️ Modular Design

#### 1. **Services Layer** (`backend/services/`)
Independent, reusable business logic components:

- **`SessionService`** - Manages session lifecycle and metadata
  - Create/read/update/delete sessions
  - Track documents per session
  - Persistent session storage (JSON-based)

- **`ChatService`** - Handles LLM interactions per session
  - Session-specific memory management
  - Query processing with RAG (Retrieval Augmented Generation)
  - Chat history tracking per session

- **`DocumentService`** - Manages document uploads and processing
  - File upload and validation
  - FAISS vectorstore management per session
  - Document chunking and embedding

#### 2. **Routers Layer** (`backend/routers/`)
RESTful API endpoints organized by feature:

- **`/sessions/`** - Session management
  - `POST /sessions/create` - Create new session
  - `GET /sessions/` - List all sessions
  - `GET /sessions/{session_id}` - Get session details
  - `PUT /sessions/{session_id}` - Rename session
  - `DELETE /sessions/{session_id}` - Delete session

- **`/chat/`** - Chat operations
  - `POST /chat/{session_id}/message` - Send message
  - `GET /chat/{session_id}/history` - Get chat history
  - `POST /chat/{session_id}/clear` - Clear history

- **`/documents/`** - Document management
  - `POST /documents/{session_id}/upload` - Upload document
  - `GET /documents/{session_id}/list` - List documents
  - `DELETE /documents/{session_id}/documents/{doc_id}` - Delete document

### 🔄 Data Flow

```
User Request
    ↓
Router (API endpoint)
    ↓
Service (business logic)
    ↓
LLM/Vector Store (external services)
    ↓
Response
```

### 💾 Storage Structure
```
backend/
├── sessions_data/
│   └── {session_id}.json          # Session metadata
├── documents_data/
│   └── {session_id}/
│       └── vectorstore/           # FAISS index per session
```

## Frontend Architecture

### 🎨 Component Structure

#### Main Components

1. **`App.jsx`** - Root component
   - Manages active session state
   - Orchestrates component communication

2. **`SessionSidebar`** - Session management UI
   - Create new sessions
   - List and select sessions
   - Edit/delete sessions
   - Shows document count

3. **`DocumentUpload`** - Document management
   - File upload interface
   - Supported formats: PDF, TXT, DOCX
   - Lists uploaded documents
   - Delete documents

4. **`ChatWindow`** - Chat interface
   - Message display
   - User input
   - Auto-load session history
   - Clear history button

### 📡 API Client (`api/client.js`)
Centralized API communication with organized endpoints:
```javascript
sessionAPI, chatAPI, documentAPI
```

### 🎯 Layout Structure
```
┌─────────────────────────────────────┐
│        App Header                   │
├──────────────────┬──────────────────┤
│                  │  Document Upload │
│  Sessions        ├──────────────────┤
│  Sidebar         │  Chat Window     │
│                  │                  │
└──────────────────┴──────────────────┘
```

## Scalability Features

### ✨ Easy to Add New Features

1. **New Router** - Create `backend/routers/new_feature.py`
   ```python
   from fastapi import APIRouter
   router = APIRouter(prefix="/feature", tags=["feature"])
   
   @router.get("/endpoint")
   async def new_endpoint():
       ...
   ```

2. **Include in main.py**
   ```python
   from routers import new_feature
   app.include_router(new_feature.router)
   ```

3. **New Service** - Create `backend/services/new_service.py`
   - Inject in `lifespan` event

### 🔌 Benefits

- **Session Isolation** - Each session has independent state
- **Modular Services** - Easy to test and maintain
- **Scalable API** - Router-based endpoint organization
- **No Global State** - Services are injected and session-specific
- **Persistent Storage** - Sessions survive application restarts
- **Component Reusability** - Frontend components accept `sessionId` prop

## Configuration

### Environment Variables
Required in `.env`:
```
OPENAI_API_KEY=your_key_here
```

### Dependencies

**Backend** (add to requirements.txt):
- FastAPI 0.128.0+
- langchain & ecosystem packages
- FAISS (vector store)
- pydantic (data validation)

**Frontend** (installed via npm):
- React 19+
- Axios (HTTP client)
- React Router 6+ (for future routing features)

## Running the Application

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
python main.py
```

Server runs at `http://localhost:8000`

### Frontend
```bash
cd frontend
npm install
npm run dev
```

App runs at `http://localhost:5173`

## Future Enhancements

1. **User Authentication** - Add login/multi-user support
2. **Session Sharing** - Share sessions with other users
3. **Advanced Search** - Full-text search across documents
4. **Analytics** - Track usage patterns
5. **Custom Models** - Support multiple LLM providers
6. **File Export** - Export chat/documents
7. **Real-time Updates** - WebSocket for live chat
8. **Database Integration** - Replace JSON with PostgreSQL

## Error Handling

- **400 Bad Request** - Invalid input or unsupported file type
- **404 Not Found** - Session/document not found
- **500 Internal Error** - Service initialization issues

Check backend logs for detailed error messages.

## Performance Considerations

- **Token Limiting** - Chat memory capped at 400 tokens
- **Document Chunking** - 1000-char chunks with 200-char overlap
- **Vector Retrieval** - Top-3 most relevant chunks
- **Session Cleanup** - Delete unused sessions to free resources

---

**Version**: 2.0.0  
**Last Updated**: February 2026
