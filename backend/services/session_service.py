"""
Session Service
Manages chat session lifecycle and metadata
Integrated with LangSmith for session tracking and monitoring
"""

from typing import Dict, Optional, List
from datetime import datetime
import uuid
import json
import os
from pathlib import Path
import logging

# Configure logging for session operations (tracked by LangSmith)
logger = logging.getLogger(__name__)

class SessionService:
    """Service for managing chat sessions"""
    
    def __init__(self, storage_path: str = None):
        """Initialize session service with persistent storage"""
        self.storage_path = storage_path or os.path.join(
            os.path.dirname(__file__), "..", "sessions_data"
        )
        os.makedirs(self.storage_path, exist_ok=True)
        self.sessions: Dict[str, dict] = self._load_sessions()
    
    def _get_session_file(self, session_id: str) -> str:
        """Get the file path for a session"""
        return os.path.join(self.storage_path, f"{session_id}.json")
    
    def _load_sessions(self) -> Dict[str, dict]:
        """Load all sessions from disk"""
        sessions = {}
        for file in os.listdir(self.storage_path):
            if file.endswith(".json"):
                try:
                    with open(os.path.join(self.storage_path, file), "r") as f:
                        session_data = json.load(f)
                        sessions[session_data["session_id"]] = session_data
                except Exception as e:
                    print(f"Error loading session {file}: {e}")
        return sessions
    
    def _save_session(self, session: dict):
        """Save session to disk"""
        try:
            file_path = self._get_session_file(session["session_id"])
            with open(file_path, "w") as f:
                json.dump(session, f, indent=2)
        except Exception as e:
            print(f"Error saving session: {e}")
    
    def create_session(self, name: Optional[str] = None) -> dict:
        """Create a new chat session"""
        session_id = str(uuid.uuid4())
        now = datetime.utcnow().isoformat()
        
        session = {
            "session_id": session_id,
            "name": name or f"Chat {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            "created_at": now,
            "updated_at": now,
            "document_count": 0,
            "documents": []
        }
        
        self.sessions[session_id] = session
        self._save_session(session)
        
        return session
    
    def get_session(self, session_id: str) -> Optional[dict]:
        """Get session details"""
        return self.sessions.get(session_id)
    
    def list_sessions(self) -> List[dict]:
        """List all sessions sorted by update time"""
        sessions = list(self.sessions.values())
        sessions.sort(key=lambda x: x["updated_at"], reverse=True)
        return sessions
    
    def update_session(self, session_id: str, name: str) -> Optional[dict]:
        """Update session name"""
        if session_id not in self.sessions:
            return None
        
        session = self.sessions[session_id]
        session["name"] = name
        session["updated_at"] = datetime.utcnow().isoformat()
        self._save_session(session)
        
        return session
    
    def delete_session(self, session_id: str) -> bool:
        """Delete a session and its data"""
        if session_id not in self.sessions:
            return False
        
        del self.sessions[session_id]
        
        # Delete session file
        try:
            file_path = self._get_session_file(session_id)
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception as e:
            print(f"Error deleting session file: {e}")
        
        return True
    
    def add_document(self, session_id: str, doc_id: str, filename: str) -> bool:
        """Track a document in a session"""
        if session_id not in self.sessions:
            return False
        
        session = self.sessions[session_id]
        session["documents"].append({
            "doc_id": doc_id,
            "filename": filename,
            "uploaded_at": datetime.utcnow().isoformat()
        })
        session["document_count"] = len(session["documents"])
        session["updated_at"] = datetime.utcnow().isoformat()
        self._save_session(session)
        
        return True
    
    def remove_document(self, session_id: str, doc_id: str) -> bool:
        """Remove a document from a session"""
        if session_id not in self.sessions:
            return False
        
        session = self.sessions[session_id]
        session["documents"] = [d for d in session["documents"] if d["doc_id"] != doc_id]
        session["document_count"] = len(session["documents"])
        session["updated_at"] = datetime.utcnow().isoformat()
        self._save_session(session)
        
        return True
