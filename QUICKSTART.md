# Multi-Session Chat - Quick Start Guide

## What's New?

✨ The application now supports **multiple independent chat sessions**!

- Each session has its own documents, chat history, and context
- Easily switch between sessions
- Scalable architecture for adding new features
- Session management UI with rename/delete capabilities

## Setup & Run

### 1. Backend Setup

```bash
cd backend
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Make sure .env has OPENAI_API_KEY
# Create .env file if it doesn't exist

# Run backend
python main.py
```

**Backend runs at**: http://localhost:8000

### 2. Frontend Setup

```bash
cd frontend

# Install dependencies (if not already done)
npm install

# Run development server
npm run dev
```

**Frontend runs at**: http://localhost:5173

## How to Use

### Creating a Session
1. Enter a name in the "New session name..." input box
2. Click the ➕ button or press Enter
3. New session appears in the left sidebar

### Uploading Documents
1. **Select a session** from the left sidebar
2. **Choose a file** (PDF, TXT, or DOCX)
3. Click **📤 Upload**
4. Document appears in the "Uploaded Documents" section

### Chatting
1. **Select a session** (must have uploaded at least one document)
2. **Type a question** in the message input
3. Press **Enter** or click the **📤** button
4. AI responds with context from your documents

### Managing Sessions
- **Rename**: Click the ✏️ icon and edit the name
- **Delete**: Click the 🗑️ icon to delete (confirmation required)
- **Clear Chat**: Click the 🗑️ Clear button in the chat window

## API Endpoints

### Sessions
- `POST /sessions/create` - Create session
- `GET /sessions/` - List all sessions
- `GET /sessions/{session_id}` - Get session details
- `PUT /sessions/{session_id}` - Update session name
- `DELETE /sessions/{session_id}` - Delete session

### Chat
- `POST /chat/{session_id}/message` - Send message (with query in form data)
- `GET /chat/{session_id}/history` - Get chat history
- `POST /chat/{session_id}/clear` - Clear history

### Documents
- `POST /documents/{session_id}/upload` - Upload document
- `GET /documents/{session_id}/list` - List documents
- `DELETE /documents/{session_id}/documents/{doc_id}` - Delete document

## Example cURL Commands

### Create Session
```bash
curl -X POST http://localhost:8000/sessions/create \
  -H "Content-Type: application/json" \
  -d '{"name": "My Project"}'
```

### Upload Document
```bash
curl -X POST http://localhost:8000/documents/{session_id}/upload \
  -F "file=@document.pdf"
```

### Send Message
```bash
curl -X POST http://localhost:8000/chat/{session_id}/message \
  -F "query=What is in this document?"
```

## Project Structure

```
backend/
├── main.py                 # App initialization & router setup
├── services/               # Business logic
│   ├── session_service.py
│   ├── chat_service.py
│   └── document_service.py
├── routers/                # API endpoints
│   ├── sessions.py
│   ├── chat.py
│   └── documents.py
├── requirements.txt        # Python dependencies
└── sessions_data/          # Persistent session storage

frontend/
├── src/
│   ├── App.jsx            # Main app component
│   ├── components/        # React components
│   │   ├── SessionSidebar.jsx
│   │   ├── ChatWindow.jsx
│   │   └── DocumentUpload.jsx
│   ├── api/
│   │   └── client.js      # API client
│   └── main.jsx           # Entry point
├── package.json
└── vite.config.js
```

## Troubleshooting

### "Please upload a document first"
- Upload a document in the Document section before asking questions

### "Session not found"
- Refresh the page or create a new session

### Backend connection error
- Ensure backend is running on `http://localhost:8000`
- Check that Python and all dependencies are installed

### OPENAI_API_KEY error
- Create `.env` file in backend directory with your key:
  ```
  OPENAI_API_KEY=sk-...
  ```

## Performance Tips

- **Fewer documents = faster responses** - Keep only relevant documents per session
- **Clear chat history** - Reduces memory usage, speeds up queries
- **Chunk size** - Automatically optimized (1000 chars per chunk)

## Next Steps

1. Explore the modular architecture in `backend/services/`
2. Add new features by creating new routers in `backend/routers/`
3. Customize the UI components in `frontend/src/components/`
4. See [ARCHITECTURE.md](ARCHITECTURE.md) for detailed design docs

---

**Need help?** Check the architecture documentation for implementation details.
