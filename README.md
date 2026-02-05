# Chat Bot - RAG (Retrieval-Augmented Generation) Application

A full-stack web application that enables document upload and intelligent question-answering using LLM-powered retrieval-augmented generation (RAG). Built with FastAPI backend, React frontend, and FAISS vector store.

## Features

- **Document Upload**: Upload PDF and TXT files for processing
- **RAG Pipeline**: Uses OpenAI embeddings and LLM models for intelligent Q&A
- **Vector Store**: FAISS for efficient similarity search and retrieval
- **Conversation Memory**: Token-limited memory (max 400 tokens) for multi-turn conversations
- **Real-time Chat**: Ask questions about uploaded documents and get contextual answers
- **Memory Management**: Clear conversation history on new uploads or via `/clear-memory` endpoint
- **RESTful API**: Clean FastAPI endpoints for all operations
- **Modern UI**: React-based frontend with responsive design

## Project Structure

```
chat_bot/
├── backend/
│   ├── main.py              # FastAPI application
│   └── requirements.txt      # Python dependencies
├── frontend/
│   ├── src/                 # React components
│   ├── package.json         # Node.js dependencies
│   ├── vite.config.js       # Vite configuration
│   └── index.html           # HTML entry point
└── README.md
```

## Prerequisites

### Backend
- Python 3.10 or higher (tested with Python 3.14)
- pip or poetry for package management
- OpenAI API key (for embeddings and LLM)

### Frontend
- Node.js 18+ and npm
- Modern web browser

## Installation

### Backend Setup

1. **Clone the repository:**
   ```bash
   cd chat_bot/backend
   ```

2. **Create virtual environment:**
   ```bash
   python -m venv ../my_venv
   ```

3. **Activate virtual environment:**
   - Windows:
     ```bash
     ..\my_venv\Scripts\activate
     ```
   - macOS/Linux:
     ```bash
     source ../my_venv/bin/activate
     ```

4. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

5. **Create `.env` file with your OpenAI API key:**
   
   Create a file named `.env` in the `backend` directory:
   ```
   OPENAI_API_KEY=your-api-key-here
   ```
   
   The application will automatically load this file on startup.

### Frontend Setup

1. **Navigate to frontend directory:**
   ```bash
   cd chat_bot/frontend
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

## Running the Application

### Start Backend Server

```bash
cd backend
python main.py
```

The API will be available at `http://localhost:8000`

### Start Frontend Development Server

```bash
cd frontend
npm run dev
```

The UI will be available at `http://localhost:5173`

## API Endpoints

### POST `/upload`
Upload a document for processing.

**Request:**
- Content-Type: `multipart/form-data`
- Body: `file` (PDF or TXT file)

**Response:**
```json
{
  "message": "File processed successfully",
  "filename": "document.pdf"
}
```

### POST `/chat`
Send a query and get an answer based on uploaded documents and conversation history.

**Request:**
- Content-Type: `application/x-www-form-urlencoded`
- Body: `query` (question text)

**Response:**
```json
{
  "answer": "The answer based on the retrieved context and recent conversation history."
}
```

### POST `/clear-memory`
Clear the conversation memory to start fresh.

**Request:** No body required

**Response:**
```json
{
  "message": "Conversation memory cleared"
}
```

## How It Works

1. **Document Upload & Processing**:
   - User uploads a PDF or TXT file
   - Document is loaded and split into chunks (1000 chars, 200 overlap)
   - Text is embedded using OpenAI Embeddings API
   - Vectors are stored in FAISS index for efficient retrieval
   - **Conversation memory is cleared** to start fresh with new document

2. **Question Answering (Hybrid RAG + Memory)**:
   - User submits a question
   - Query is embedded using the same embedding model
   - FAISS retrieves top-3 similar document chunks (k=3 retrieval)
   - **Recent conversation history is loaded** from token-limited memory (max 400 tokens)
   - Retrieved context + chat history is passed to GPT-4o-mini
   - LLM generates contextual answer using the RAG prompt
   - **Interaction is saved to memory** for next turn context (token-limited)

3. **Conversation Memory (Hybrid Optimization)**:
   - Uses `ConversationTokenBufferMemory` with max 400 tokens
   - Stores recent Q&A exchanges automatically
   - Older exchanges are dropped when token limit is exceeded
   - Reduces API costs while maintaining conversation context
   - Cleared on new document upload or via `/clear-memory` endpoint

4. **Vector Store Persistence**:
   - FAISS (Facebook AI Similarity Search) for in-memory vector indexing
   - **Persists to `backend/faiss_index`** directory for durability across restarts
   - Supports fast similarity search with minimal overhead
   - New index created on each document upload

## Technologies Used

### Backend
- **FastAPI**: Modern Python web framework for building APIs
- **LangChain**: LLM orchestration and RAG pipeline
- **OpenAI API**: Embeddings and chat models
- **FAISS**: Vector similarity search library
- **Uvicorn**: ASGI server for FastAPI
- **pydantic**: Data validation and settings management

### Frontend
- **React**: UI library for building interactive components
- **Vite**: Fast build tool and dev server
- **Axios**: HTTP client for API calls
- **Vite React Plugin**: Optimized React integration

### Data & Vector Storage
- **FAISS**: In-memory vector database for fast similarity search
- **PyPDF**: PDF text extraction
- **Sentence Transformers**: Pre-trained embedding models (via LangChain)

## Configuration

### Environment Variables

Create a `.env` file in the `backend` directory:

```
OPENAI_API_KEY=your-api-key-here
```

This file is automatically loaded on application startup using `python-dotenv`. **Do not commit `.env` to version control** — add it to `.gitignore`.

### Customizable Parameters in `backend/main.py`

- **Chunk size**: Line 92 (`chunk_size=1000`) — size of document chunks for embedding
- **Chunk overlap**: Line 92 (`chunk_overlap=200`) — overlap between chunks for context continuity
- **LLM model**: Line 49 (`model="gpt-4o-mini"`) — OpenAI model for chat/answer generation
- **LLM temperature**: Line 49 (`temperature=0`) — controls randomness (0=deterministic)
- **Memory token limit**: Line 51 (`max_token_limit=400`) — max tokens for conversation history
- **Retrieval k**: Line 129 (`search_kwargs={"k": 3}`) — number of document chunks to retrieve
- **Max answer length**: System prompt (currently 3 sentences max)
- **Persist directory**: Line 44 (`PERSIST_DIR=os.path.join(...)`) — where FAISS index is saved

## Troubleshooting

### FAISS Import Error
If you get "Could not import faiss", install it explicitly:
```bash
pip install faiss-cpu
```
For GPU support (CUDA):
```bash
pip install faiss-gpu
```

### OpenAI API Key Error
- Verify API key is valid at https://platform.openai.com/account/api-keys
- Check billing is enabled on your OpenAI account
- Ensure key has sufficient quota/credits

### Port Already in Use
If port 8000 is already in use:
```bash
# Windows: Find and kill process using port 8000
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# macOS/Linux: Find and kill process
lsof -ti:8000 | xargs kill -9
```

## Performance Notes

- **First upload**: may take 30-60 seconds (model downloading)
- **Memory efficiency**: Token-limited memory (400 tokens) keeps conversation context small and API costs low
- **FAISS index**: persists to disk (`backend/faiss_index`) so it survives server restarts
- **Retrieval**: k=3 chunks retrieved per query; adjust for speed vs. accuracy tradeoff
- **Large-scale production**: FAISS is in-memory; for multi-user/large docs, consider persistent vector DB (Pinecone, Weaviate, Qdrant)
- **Embeddings**: cached in FAISS index; new upload rebuilds the index

## Future Enhancements

- [ ] Persistent vector database integration (Pinecone, Weaviate, Qdrant)
- [ ] Multi-user session management & per-user memory isolation
- [ ] Batch document processing and index merging
- [ ] Export conversation history to JSON/CSV
- [ ] Support for more document formats (DOCX, PPT, Excel, Images)
- [ ] Advanced RAG techniques (HyDE, Chain-of-Thought, multi-query)
- [ ] Cost tracking and usage analytics per session
- [ ] Docker containerization with docker-compose
- [ ] LangSmith integration for observability & debugging
- [ ] Hybrid memory: summarization for older conversations
- [ ] Semantic search over memory (retrieve relevant past conversations)
- [ ] Web UI for memory management and conversation export

## License

MIT

## Support

For issues or questions, please open an issue in the repository.
