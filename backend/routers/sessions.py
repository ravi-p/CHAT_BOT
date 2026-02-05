"""
Session Management Router
Handles all session-related operations
"""

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Optional
import uuid
from datetime import datetime
from services.session_service import SessionService

router = APIRouter(prefix="/sessions", tags=["sessions"])

# Pydantic models
class SessionCreate(BaseModel):
    name: Optional[str] = None

class SessionUpdate(BaseModel):
    name: str

class SessionResponse(BaseModel):
    session_id: str
    name: str
    created_at: str
    updated_at: str
    document_count: int

# Service instance (will be managed at app level)
session_service = None

def set_session_service(service: SessionService):
    """Inject session service at app startup"""
    global session_service
    session_service = service

@router.post("/create", response_model=SessionResponse)
async def create_session(data: SessionCreate):
    """Create a new chat session"""
    if not session_service:
        raise HTTPException(status_code=500, detail="Service not initialized")
    
    session = session_service.create_session(data.name)
    return session

@router.get("/{session_id}", response_model=SessionResponse)
async def get_session(session_id: str):
    """Get session details"""
    if not session_service:
        raise HTTPException(status_code=500, detail="Service not initialized")
    
    session = session_service.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return session

@router.get("/")
async def list_sessions():
    """List all sessions"""
    if not session_service:
        raise HTTPException(status_code=500, detail="Service not initialized")
    
    sessions = session_service.list_sessions()
    return {"sessions": sessions}

@router.put("/{session_id}", response_model=SessionResponse)
async def update_session(session_id: str, data: SessionUpdate):
    """Update session name"""
    if not session_service:
        raise HTTPException(status_code=500, detail="Service not initialized")
    
    session = session_service.update_session(session_id, data.name)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return session

@router.delete("/{session_id}")
async def delete_session(session_id: str):
    """Delete a session"""
    if not session_service:
        raise HTTPException(status_code=500, detail="Service not initialized")
    
    success = session_service.delete_session(session_id)
    if not success:
        raise HTTPException(status_code=404, detail="Session not found")
    
    return {"message": "Session deleted successfully"}
