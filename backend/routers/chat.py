"""
Chat Router
Handles all chat-related operations
"""

from fastapi import APIRouter, Form, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter(prefix="/chat", tags=["chat"])

# Pydantic models
class ChatMessage(BaseModel):
    role: str
    content: str

class ChatRequest(BaseModel):
    query: str

class ChatResponse(BaseModel):
    answer: str
    context: List[str] = []

# Service will be injected at app level
chat_service = None

def set_chat_service(service):
    """Inject chat service at app startup"""
    global chat_service
    chat_service = service

@router.post("/{session_id}/message", response_model=ChatResponse)
async def send_message(session_id: str, query: str = Form(...)):
    """Send a message in a chat session"""
    if not chat_service:
        raise HTTPException(status_code=500, detail="Service not initialized")
    
    response = await chat_service.process_query(session_id, query)
    if isinstance(response, dict) and "error" in response:
        raise HTTPException(status_code=400, detail=response["error"])
    
    return response

@router.get("/{session_id}/history")
async def get_chat_history(session_id: str):
    """Get chat history for a session"""
    if not chat_service:
        raise HTTPException(status_code=500, detail="Service not initialized")
    
    history = chat_service.get_history(session_id)
    return {"messages": history}

@router.post("/{session_id}/clear")
async def clear_chat_history(session_id: str):
    """Clear chat history for a session"""
    if not chat_service:
        raise HTTPException(status_code=500, detail="Service not initialized")
    
    chat_service.clear_history(session_id)
    return {"message": "Chat history cleared"}
