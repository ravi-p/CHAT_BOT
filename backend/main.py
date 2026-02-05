from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from dotenv import load_dotenv
import os
import sys

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Load environment variables from .env file
load_dotenv()

# Configure LangSmith tracing if enabled
if os.getenv("LANGSMITH_API_KEY"):
    os.environ["LANGCHAIN_TRACING_V2"] = os.getenv("LANGSMITH_TRACING_V2", "true")
    os.environ["LANGCHAIN_ENDPOINT"] = os.getenv("LANGSMITH_ENDPOINT", "https://api.smith.langchain.com")
    os.environ["LANGCHAIN_API_KEY"] = os.getenv("LANGSMITH_API_KEY")
    os.environ["LANGCHAIN_PROJECT"] = os.getenv("LANGSMITH_PROJECT", "chat-bot-project")
    print("✓ LangSmith tracing enabled")

# Import services
from services.session_service import SessionService
from services.chat_service import ChatService

# Import routers
from routers import sessions, chat

# Global service instances
session_service = None
chat_service = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle management"""
    global session_service, chat_service
    
    # Initialize services
    session_service = SessionService()
    chat_service = ChatService()
    
    # Inject services into routers
    sessions.set_session_service(session_service)
    chat.set_chat_service(chat_service)
    
    yield
    
    # Cleanup can go here
    pass

app = FastAPI(
    title="Multi-Session Chat API",
    description="Chat application with support for multiple sessions",
    version="2.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(sessions.router)
app.include_router(chat.router)

@app.get("/")
async def root():
    """API health check"""
    return {
        "message": "Multi-Session Chat API",
        "version": "2.0.0",
        "status": "running"
    }

@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
