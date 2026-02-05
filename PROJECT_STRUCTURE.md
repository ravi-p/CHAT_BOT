# Project Structure Overview

## Directory Tree

```
chat_bot/
├── README.md                      # Original project README
├── QUICKSTART.md                  # Quick start guide ✨ NEW
├── ARCHITECTURE.md                # System design documentation ✨ NEW
├── IMPLEMENTATION_SUMMARY.md      # What changed summary ✨ NEW
├── ADDING_FEATURES.md            # How to extend the system ✨ NEW
├── test_file.txt                 # Test file
│
├── backend/                       # Python FastAPI backend
│   ├── main.py                   # 🔄 REFACTORED - Main app with routers
│   ├── requirements.txt          # Python dependencies
│   ├── smoke_test.py            # Testing utility
│   │
│   ├── services/                 # 📦 NEW - Business logic layer
│   │   ├── __init__.py
│   │   ├── session_service.py   # Session lifecycle management
│   │   ├── chat_service.py      # LLM & chat operations
│   │   └── document_service.py  # Document upload & processing
│   │
│   ├── routers/                  # 📦 NEW - API endpoints
│   │   ├── __init__.py
│   │   ├── sessions.py          # Session CRUD endpoints
│   │   ├── chat.py              # Chat message endpoints
│   │   └── documents.py         # Document management endpoints
│   │
│   ├── faiss_index/             # Vector store (existing)
│   │   └── index.faiss
│   │
│   ├── sessions_data/           # 📦 NEW - Session persistence
│   │   └── {session_id}.json    # One file per session
│   │
│   ├── documents_data/          # 📦 NEW - Document storage
│   │   └── {session_id}/
│   │       └── vectorstore/     # FAISS index per session
│   │
│   └── __pycache__/             # Python cache
│
├── frontend/                      # React + Vite frontend
│   ├── package.json             # 🔄 UPDATED - Added react-router-dom
│   ├── vite.config.js           # Vite configuration
│   ├── index.html               # HTML entry point
│   ├── eslint.config.js         # Linting rules
│   │
│   ├── public/                  # Static assets
│   │
│   ├── src/
│   │   ├── main.jsx             # React entry point
│   │   ├── App.jsx              # 🔄 REFACTORED - Main app component
│   │   ├── App.css              # 🔄 UPDATED - New styling
│   │   ├── index.css            # Global styles
│   │   │
│   │   ├── api/                 # 📦 NEW - API communication
│   │   │   └── client.js        # Centralized API client
│   │   │
│   │   ├── components/          # 📦 NEW - React components
│   │   │   ├── SessionSidebar.jsx      # Session management UI
│   │   │   ├── SessionSidebar.css      # Sidebar styling
│   │   │   ├── ChatWindow.jsx          # Chat interface
│   │   │   ├── ChatWindow.css          # Chat styling
│   │   │   ├── DocumentUpload.jsx      # Document upload UI
│   │   │   └── DocumentUpload.css      # Upload styling
│   │   │
│   │   └── assets/              # App assets
│   │
│   └── node_modules/            # NPM dependencies
│
├── my_venv/                       # Python virtual environment
│   ├── pyvenv.cfg
│   ├── Scripts/                 # Executables
│   ├── Lib/                     # Python packages
│   └── Include/                 # Header files
│
└── .gitignore                     # Git configuration
```

## File Changes Summary

### ✨ NEW Files (14 files)

**Backend Services:**
- `backend/services/__init__.py`
- `backend/services/session_service.py`
- `backend/services/chat_service.py`
- `backend/services/document_service.py`

**Backend Routers:**
- `backend/routers/__init__.py`
- `backend/routers/sessions.py`
- `backend/routers/chat.py`
- `backend/routers/documents.py`

**Frontend Components:**
- `frontend/src/api/client.js`
- `frontend/src/components/SessionSidebar.jsx`
- `frontend/src/components/SessionSidebar.css`
- `frontend/src/components/ChatWindow.jsx`
- `frontend/src/components/ChatWindow.css`
- `frontend/src/components/DocumentUpload.jsx`
- `frontend/src/components/DocumentUpload.css`

**Documentation:**
- `QUICKSTART.md`
- `ARCHITECTURE.md`
- `IMPLEMENTATION_SUMMARY.md`
- `ADDING_FEATURES.md`

### 🔄 REFACTORED Files (3 files)

- `backend/main.py` - Complete restructuring
- `frontend/src/App.jsx` - Multi-session support
- `frontend/src/App.css` - Modern layout

### 📦 UPDATED Files (1 file)

- `frontend/package.json` - Added react-router-dom

### 📂 NEW Directories

- `backend/services/` - Service layer
- `backend/routers/` - Router layer
- `backend/sessions_data/` - Session persistence
- `backend/documents_data/` - Document storage
- `frontend/src/api/` - API client
- `frontend/src/components/` - React components

---

## Layer Architecture

```
┌─────────────────────────────────────────────┐
│         Frontend (React Components)         │
│  ┌────────────────┬────────────────────────┐ │
│  │  SessionBar    │  ChatWindow            │ │
│  │  DocumentUp    │  (session-specific)    │ │
│  └────────────────┴────────────────────────┘ │
└──────────────────────┬──────────────────────┘
                       │ API Calls
                       ↓
┌─────────────────────────────────────────────┐
│    API Layer (FastAPI Routers)              │
│  ┌──────┬──────────┬────────────────────┐   │
│  │/sess │/chat     │/documents          │   │
│  └──────┴──────────┴────────────────────┘   │
└──────────────────────┬──────────────────────┘
                       │ Delegates to
                       ↓
┌─────────────────────────────────────────────┐
│  Service Layer (Business Logic)             │
│  ┌──────┬──────────┬────────────────────┐   │
│  │Sesn. │Chat      │Document            │   │
│  │Srv   │Service   │Service             │   │
│  └──────┴──────────┴────────────────────┘   │
└──────────────────────┬──────────────────────┘
                       │ Uses
                       ↓
┌─────────────────────────────────────────────┐
│  External Services (LLM, Vector DB)         │
│  ┌──────────┬──────────────────────────┐    │
│  │OpenAI    │FAISS Vector Store        │    │
│  └──────────┴──────────────────────────┘    │
└─────────────────────────────────────────────┘
```

---

## Data Flow Diagram

### Creating a Session

```
User Input (Frontend)
    ↓
SessionSidebar Component
    ↓
sessionAPI.createSession()
    ↓
POST /sessions/create (Router)
    ↓
SessionService.create_session()
    ↓
Generate UUID + Metadata
    ↓
Save to sessions_data/{id}.json
    ↓
Return SessionResponse
    ↓
Frontend Updates UI
```

### Uploading a Document

```
File Selection (Frontend)
    ↓
DocumentUpload Component
    ↓
documentAPI.uploadDocument()
    ↓
POST /documents/{session_id}/upload (Router)
    ↓
DocumentService.upload_and_process()
    ↓
Load File → Split Text → Create Embeddings
    ↓
FAISS.from_documents() / Add to existing
    ↓
Save to documents_data/{session_id}/vectorstore/
    ↓
Return Success Response
    ↓
Frontend Shows Confirmation
```

### Sending a Message

```
User Text Input (Frontend)
    ↓
ChatWindow Component
    ↓
chatAPI.sendMessage()
    ↓
POST /chat/{session_id}/message (Router)
    ↓
ChatService.process_query()
    ↓
Get Session Vectorstore + Memory
    ↓
RAG Chain: Query → Retrieve → Generate
    ↓
LLM Response
    ↓
Save to Session Memory + History
    ↓
Return ChatResponse
    ↓
Frontend Displays Message
```

---

## Dependency Graph

### Backend Dependencies
```
main.py
├── services/
│   ├── session_service.py
│   ├── chat_service.py (imports: langchain, faiss)
│   └── document_service.py (imports: langchain, faiss)
├── routers/
│   ├── sessions.py (uses: SessionService)
│   ├── chat.py (uses: ChatService)
│   └── documents.py (uses: DocumentService)
└── Third-party
    ├── FastAPI
    ├── Langchain
    ├── FAISS
    └── OpenAI
```

### Frontend Dependencies
```
App.jsx
├── SessionSidebar.jsx (uses: sessionAPI)
├── ChatWindow.jsx (uses: chatAPI)
├── DocumentUpload.jsx (uses: documentAPI)
├── api/client.js (uses: axios)
└── Third-party
    ├── React
    ├── React Router
    └── Axios
```

---

## Environment Configuration

### Backend `.env`
```
OPENAI_API_KEY=sk-your-key-here
```

### Frontend `.env` (optional)
```
VITE_API_URL=http://localhost:8000
```

---

## Build & Deploy Structure

### Development
```
Local Machine
├── Backend (localhost:8000)
├── Frontend (localhost:5173)
└── Shared: .env
```

### Production
```
Docker Containers
├── Backend Service (Port 8000)
│   ├── services/
│   ├── routers/
│   └── Data: PostgreSQL + Redis
├── Frontend Build (Static files)
│   └── Served by Nginx
└── Volumes
    ├── /sessions_data/
    └── /documents_data/
```

---

## Configuration Files

### Backend
- `.env` - Environment variables
- `requirements.txt` - Python dependencies
- `main.py` - Application config

### Frontend
- `package.json` - NPM dependencies
- `vite.config.js` - Build configuration
- `.env` - Frontend config (optional)

---

## Quick Reference

| Component | Purpose | Location |
|-----------|---------|----------|
| SessionService | Session CRUD | `backend/services/session_service.py` |
| ChatService | Chat logic | `backend/services/chat_service.py` |
| DocumentService | File handling | `backend/services/document_service.py` |
| SessionRouter | Session API | `backend/routers/sessions.py` |
| ChatRouter | Chat API | `backend/routers/chat.py` |
| DocumentRouter | Document API | `backend/routers/documents.py` |
| SessionSidebar | Session UI | `frontend/src/components/SessionSidebar.jsx` |
| ChatWindow | Chat UI | `frontend/src/components/ChatWindow.jsx` |
| DocumentUpload | Upload UI | `frontend/src/components/DocumentUpload.jsx` |
| API Client | HTTP calls | `frontend/src/api/client.js` |

---

**Total New Lines of Code**: ~2,000+  
**Backend Services**: 3  
**API Routers**: 3  
**Frontend Components**: 3  
**Documentation Files**: 4
