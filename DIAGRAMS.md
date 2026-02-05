# System Architecture Diagrams

## High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    MULTI-SESSION CHAT APP                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              FRONTEND (React/Vite)                   │  │
│  │  ┌──────────────┐  ┌──────────────┐  ┌────────────┐ │  │
│  │  │SessionSidebar│  │ ChatWindow   │  │Document    │ │  │
│  │  │  Component   │  │  Component   │  │Upload Comp │ │  │
│  │  └──────────────┘  └──────────────┘  └────────────┘ │  │
│  │         │                  │                 │       │  │
│  │         └──────────────────┴─────────────────┘       │  │
│  │                    ↓                                  │  │
│  │         ┌──────────────────────────┐                │  │
│  │         │   API Client (client.js) │                │  │
│  │         └──────────────────────────┘                │  │
│  └──────────────┬───────────────────────────────────────┘  │
│                 │ HTTP/REST (axios)                        │
│                 ↓                                           │
│  ┌──────────────────────────────────────────────────────┐  │
│  │            BACKEND (FastAPI/Python)                 │  │
│  │                                                      │  │
│  │  Routers Layer:                                     │  │
│  │  ┌─────────┐  ┌──────┐  ┌───────────┐             │  │
│  │  │Sessions │  │Chat  │  │Documents  │             │  │
│  │  │ Router  │  │Router│  │ Router    │             │  │
│  │  └────┬────┘  └──┬───┘  └────┬──────┘             │  │
│  │       │          │           │                     │  │
│  │  ┌────┴──────────┴───────────┴──┐                 │  │
│  │  │   Service Layer              │                 │  │
│  │  │ ┌──────┐ ┌────┐ ┌─────────┐ │                 │  │
│  │  │ │Sesn. │ │Chat│ │Document │ │                 │  │
│  │  │ │Serv. │ │Srv.│ │Service  │ │                 │  │
│  │  │ └──────┘ └────┘ └─────────┘ │                 │  │
│  │  └──────────────────────────────┘                 │  │
│  │                 ↓                                  │  │
│  │  External Services:                               │  │
│  │  ┌─────────────────────────────────────────────┐  │  │
│  │  │ OpenAI LLM (gpt-4o-mini)                   │  │  │
│  │  │ FAISS Vector Store                        │  │  │
│  │  │ Embeddings (OpenAI)                       │  │  │
│  │  └─────────────────────────────────────────────┘  │  │
│  │                                                      │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
│  ┌──────────────────────────────────────────────────────┐  │
│  │         PERSISTENT STORAGE                          │  │
│  │  ┌──────────────┐      ┌──────────────────┐        │  │
│  │  │sessions_data │      │documents_data    │        │  │
│  │  │   /{id}.json │      │/{session_id}/... │        │  │
│  │  └──────────────┘      └──────────────────┘        │  │
│  └──────────────────────────────────────────────────────┘  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Request/Response Flow Diagram

### Creating a Session

```
┌─────────────┐                           ┌─────────────┐
│   User      │                           │   Backend   │
│  Browser    │                           │   (FastAPI) │
└──────┬──────┘                           └──────┬──────┘
       │                                          │
       │  1. Click "Create Session"               │
       ├─────────────────────────────────────────→│
       │  (SessionSidebar component)              │
       │                                          │
       │  2. axios.post(/sessions/create)        │
       ├─────────────────────────────────────────→│ SessionRouter
       │  {name: "Project Alpha"}                │
       │                                          │
       │                                    SessionService
       │                                    │
       │                                    ├─ Generate UUID
       │                                    ├─ Create metadata
       │                                    └─ Save to JSON
       │                                          │
       │  3. Response (SessionResponse)          │
       │  {session_id, name, created_at...}      │
       │←─────────────────────────────────────────┤
       │                                          │
       │  4. Update UI with new session           │
       │                                          │
```

### Uploading a Document

```
┌─────────────┐                           ┌─────────────┐
│   User      │                           │   Backend   │
│  Browser    │                           │   (FastAPI) │
└──────┬──────┘                           └──────┬──────┘
       │                                          │
       │  1. Select file + Click Upload           │
       ├─────────────────────────────────────────→│
       │  (DocumentUpload component)              │
       │  FormData: {file, session_id}            │
       │                                          │
       │  2. POST /documents/{session_id}/upload │
       ├─────────────────────────────────────────→│ DocumentRouter
       │                                          │
       │                                    DocumentService
       │                                    │
       │                                    ├─ Validate file
       │                                    ├─ Load documents
       │                                    ├─ Split text
       │                                    ├─ Create embeddings
       │                                    ├─ FAISS vectorstore
       │                                    └─ Save to disk
       │                                          │
       │  3. Response {message, chunks...}       │
       │←─────────────────────────────────────────┤
       │                                          │
       │  4. Show in DocumentUpload component     │
       │                                          │
```

### Sending a Message

```
┌─────────────┐                           ┌─────────────┐
│   User      │                           │   Backend   │
│  Browser    │                           │   (FastAPI) │
└──────┬──────┘                           └──────┬──────┘
       │                                          │
       │  1. Type message + Press Enter           │
       ├─────────────────────────────────────────→│
       │  (ChatWindow component)                  │
       │                                          │
       │  2. POST /chat/{session_id}/message     │
       ├─────────────────────────────────────────→│ ChatRouter
       │  FormData: {query: "..."}                │
       │                                          │
       │                                    ChatService
       │                                    │
       │                    ┌───────────────┴────────────┐
       │                    │                            │
       │              Get Vectorstore          Get Memory
       │              (session-specific)    (session-specific)
       │                    │                            │
       │                    └────────────┬────────────────┘
       │                                 │
       │                           RAG Chain:
       │                           │
       │                           ├─ Retrieve (top-3)
       │                           ├─ Create prompt
       │                           └─ Call OpenAI LLM
       │                                 │
       │                        Save to memory
       │                                 │
       │  3. Response {answer: "..."}   │
       │←─────────────────────────────────┤
       │                                          │
       │  4. Display in ChatWindow                │
       │                                          │
```

---

## Data Structure Diagram

### Session Storage

```
sessions_data/
├── session-uuid-1.json
│   {
│     "session_id": "uuid-1",
│     "name": "Project Alpha",
│     "created_at": "2026-02-01T10:00:00",
│     "updated_at": "2026-02-01T11:00:00",
│     "document_count": 2,
│     "documents": [
│       {
│         "doc_id": "doc-uuid-1",
│         "filename": "report.pdf",
│         "uploaded_at": "2026-02-01T10:15:00"
│       },
│       {
│         "doc_id": "doc-uuid-2",
│         "filename": "notes.txt",
│         "uploaded_at": "2026-02-01T10:20:00"
│       }
│     ]
│   }
│
├── session-uuid-2.json
│   { ... }
│
└── session-uuid-3.json
    { ... }
```

### Document Storage

```
documents_data/
├── session-uuid-1/
│   ├── vectorstore/
│   │   ├── index.faiss          (FAISS index binary)
│   │   ├── index.pkl            (pickle file)
│   │   ├── docstore.pkl         (documents)
│   │   └── index_to_docstore.json
│   │
│   └── metadata.json            (optional)
│
├── session-uuid-2/
│   ├── vectorstore/
│   │   ├── index.faiss
│   │   ├── index.pkl
│   │   ├── docstore.pkl
│   │   └── index_to_docstore.json
│   
└── session-uuid-3/
    └── vectorstore/
        └── ...
```

---

## Service Interaction Diagram

```
                        ┌─────────────┐
                        │  MainApp    │
                        │  (main.py)  │
                        └──────┬──────┘
                               │
        ┌──────────────────────┼──────────────────────┐
        │                      │                      │
        ↓                      ↓                      ↓
┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐
│ SessionService   │  │  ChatService     │  │ DocumentService  │
├──────────────────┤  ├──────────────────┤  ├──────────────────┤
│ - Sessions       │  │ - Memory (LM)    │  │ - Embeddings     │
│ - Persistence    │  │ - Chat history   │  │ - Vectorstores   │
│ - Metadata       │  │ - RAG chains     │  │ - Text splitting │
└────────┬─────────┘  └────────┬─────────┘  └────────┬─────────┘
         │                     │                     │
         │ Uses                │ Uses                │ Uses
         │                     │                     │
         └─────────────────────┼─────────────────────┘
                               │
                    ┌──────────┴──────────┐
                    │                     │
                    ↓                     ↓
            ┌─────────────────┐   ┌──────────────┐
            │  OpenAI APIs    │   │ FAISS Vector │
            │  (LLM+Embed)    │   │     Store    │
            └─────────────────┘   └──────────────┘
```

---

## Component Hierarchy Diagram

### Frontend Components

```
App.jsx (Root)
│
├── Header (UI only)
│   └── Title + Description
│
├── Layout Container
│   │
│   ├── SessionSidebar
│   │   ├── Header
│   │   ├── New Session Input
│   │   │   ├── Input field
│   │   │   └── Create button
│   │   │
│   │   └── Sessions List
│   │       └── SessionItem × N
│   │           ├── Session name (clickable)
│   │           ├── Document count
│   │           ├── Edit button
│   │           └── Delete button
│   │
│   └── RightPanel
│       │
│       ├── DocumentUpload
│       │   ├── Header
│       │   ├── Upload Form
│       │   │   ├── File input
│       │   │   └── Upload button
│       │   │
│       │   └── Documents List
│       │       └── DocumentItem × N
│       │           ├── Document name
│       │           ├── Chunk count
│       │           └── Delete button
│       │
│       └── ChatWindow
│           ├── Header
│           │   └── Clear button
│           │
│           ├── Messages Area
│           │   └── Message × N
│           │       ├── User message bubble
│           │       └── Assistant message bubble
│           │
│           └── Input Area
│               ├── Text input
│               └── Send button
```

---

## Data Flow: Multi-Session Isolation

```
Memory (RAM)
├── Session 1 ID
│   ├── Vectorstore (FAISS) → Documents A, B
│   ├── Memory (LLM) → chat history
│   └── Chat History → messages
│
├── Session 2 ID
│   ├── Vectorstore (FAISS) → Documents C, D
│   ├── Memory (LLM) → chat history
│   └── Chat History → messages
│
└── Session 3 ID
    ├── Vectorstore (FAISS) → Documents E
    ├── Memory (LLM) → chat history
    └── Chat History → messages

Persistent Storage
├── sessions_data/
│   ├── session-1.json → metadata
│   ├── session-2.json → metadata
│   └── session-3.json → metadata
│
└── documents_data/
    ├── session-1/vectorstore/ → FAISS index
    ├── session-2/vectorstore/ → FAISS index
    └── session-3/vectorstore/ → FAISS index
```

---

## API Endpoint Organization

```
FastAPI App
│
├── /                                    [Health check]
│
├── /sessions/                           [SessionRouter]
│   ├── POST   /create                   [Create new session]
│   ├── GET    /                         [List all sessions]
│   ├── GET    /{session_id}            [Get session details]
│   ├── PUT    /{session_id}            [Update session]
│   └── DELETE /{session_id}            [Delete session]
│
├── /chat/                               [ChatRouter]
│   ├── POST   /{session_id}/message     [Send message]
│   ├── GET    /{session_id}/history     [Get chat history]
│   └── POST   /{session_id}/clear       [Clear history]
│
├── /documents/                          [DocumentRouter]
│   ├── POST   /{session_id}/upload      [Upload document]
│   ├── GET    /{session_id}/list        [List documents]
│   └── DELETE /{session_id}/documents/{doc_id} [Delete doc]
│
└── Future Expansion Points
    ├── /analytics/
    ├── /export/
    ├── /search/
    ├── /users/
    └── /settings/
```

---

## Scalability Architecture

```
Current (Single Instance)
┌────────────────┐
│  FastAPI App   │
├────────────────┤
│ Services       │
│ - Session      │
│ - Chat         │
│ - Document     │
├────────────────┤
│ Storage        │
│ - JSON files   │
│ - FAISS index  │
└────────────────┘

Future (Horizontally Scalable)
┌──────────────────────────────────────────┐
│           Load Balancer                  │
└───────┬──────────────────────┬───────────┘
        │                      │
   ┌────▼─────┐          ┌──────▼────┐
   │FastAPI   │          │FastAPI    │
   │Instance1 │          │Instance2  │
   └────┬─────┘          └──────┬────┘
        │                       │
   ┌────▼───────────────────────▼────┐
   │   Shared Services Layer         │
   ├─────────────────────────────────┤
   │ - Redis (session cache)         │
   │ - PostgreSQL (persistence)      │
   │ - Message Queue (async)         │
   └─────────────────────────────────┘
```

---

## Error Handling Flow

```
API Request
│
├── Router Receives Request
│   │
│   └─→ Try:
│       │
│       ├─→ Validate Input (Pydantic)
│       │   ├─→ Valid? Continue ✓
│       │   └─→ Invalid? → 400 Bad Request ✗
│       │
│       ├─→ Service Call
│       │   ├─→ Session not found? → 404 Not Found ✗
│       │   ├─→ LLM error? → 500 Internal Error ✗
│       │   └─→ Success? → Process ✓
│       │
│       └─→ Return Response
│           ├─→ Success → 200 + Data
│           └─→ Error → Error Code + Message
│
└── Except:
    └─→ 500 Internal Server Error
        ├─→ Log error
        └─→ Return error message
```

---

These diagrams illustrate the complete architecture of your multi-session chat application!
