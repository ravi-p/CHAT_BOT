# Adding New Features: Step-by-Step Guide

This guide demonstrates how to add new features to the multi-session chat application.

## Example 1: Add a Statistics/Analytics Feature

### Step 1: Create the Service

Create `backend/services/analytics_service.py`:

```python
from datetime import datetime
from typing import Dict, List

class AnalyticsService:
    """Service for tracking analytics per session"""
    
    def __init__(self):
        self.analytics: Dict[str, dict] = {}
    
    def track_message(self, session_id: str, is_user: bool, content_length: int):
        """Track a message"""
        if session_id not in self.analytics:
            self.analytics[session_id] = {
                "messages_count": 0,
                "total_characters": 0,
                "created_at": datetime.utcnow().isoformat(),
            }
        
        analytics = self.analytics[session_id]
        analytics["messages_count"] += 1
        analytics["total_characters"] += content_length
        analytics["last_message_at"] = datetime.utcnow().isoformat()
        
        return analytics
    
    def get_analytics(self, session_id: str) -> dict:
        """Get analytics for a session"""
        return self.analytics.get(session_id, {})
    
    def delete_session(self, session_id: str):
        """Clean up analytics when session is deleted"""
        if session_id in self.analytics:
            del self.analytics[session_id]
```

### Step 2: Create the Router

Create `backend/routers/analytics.py`:

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/analytics", tags=["analytics"])

# Service will be injected at app level
analytics_service = None

def set_analytics_service(service):
    """Inject analytics service at app startup"""
    global analytics_service
    analytics_service = service

class AnalyticsResponse(BaseModel):
    messages_count: int
    total_characters: int
    created_at: str
    last_message_at: str = None

@router.get("/{session_id}", response_model=dict)
async def get_session_analytics(session_id: str):
    """Get analytics for a session"""
    if not analytics_service:
        raise HTTPException(status_code=500, detail="Service not initialized")
    
    analytics = analytics_service.get_analytics(session_id)
    if not analytics:
        raise HTTPException(status_code=404, detail="No analytics found")
    
    return analytics
```

### Step 3: Update main.py

Add to `backend/main.py`:

```python
# At the top with other imports
from services.analytics_service import AnalyticsService
from routers import analytics

# In lifespan function
global analytics_service
analytics_service = AnalyticsService()
analytics.set_analytics_service(analytics_service)

# Include router
app.include_router(analytics.router)
```

### Step 4: Integrate with Chat Service

Update `backend/services/chat_service.py` to track analytics:

```python
# In process_query method, after processing:
if analytics_service:
    analytics_service.track_message(session_id, False, len(answer))

# Inject reference to chat service
self.analytics_service = None

def set_analytics_service(self, service):
    self.analytics_service = service
```

### Step 5: Frontend Component (Optional)

Create `frontend/src/components/Analytics.jsx`:

```jsx
import { useState, useEffect } from 'react';
import axios from 'axios';

function Analytics({ sessionId }) {
  const [analytics, setAnalytics] = useState(null);

  const API_BASE_URL = 'http://localhost:8000';

  useEffect(() => {
    if (!sessionId) return;

    const loadAnalytics = async () => {
      try {
        const response = await axios.get(
          `${API_BASE_URL}/analytics/${sessionId}`
        );
        setAnalytics(response.data);
      } catch (error) {
        console.error('Error loading analytics:', error);
      }
    };

    loadAnalytics();
  }, [sessionId]);

  if (!analytics) return null;

  return (
    <div className="analytics">
      <h4>Session Stats</h4>
      <p>Messages: {analytics.messages_count}</p>
      <p>Characters: {analytics.total_characters}</p>
    </div>
  );
}

export default Analytics;
```

## Example 2: Add a Session Export Feature

### Step 1: Create Export Service

Create `backend/services/export_service.py`:

```python
import json
from datetime import datetime
from typing import Dict

class ExportService:
    """Service for exporting session data"""
    
    def export_session_json(self, session: dict, chat_history: list, documents: list) -> str:
        """Export session as JSON"""
        export_data = {
            "session": session,
            "chat_history": chat_history,
            "documents": documents,
            "exported_at": datetime.utcnow().isoformat()
        }
        return json.dumps(export_data, indent=2)
    
    def export_session_markdown(self, session: dict, chat_history: list) -> str:
        """Export session as Markdown"""
        md = f"# {session['name']}\n\n"
        md += f"Created: {session['created_at']}\n\n"
        md += "## Chat History\n\n"
        
        for msg in chat_history:
            role = "**User**" if msg['role'] == 'user' else "**Assistant**"
            md += f"{role}: {msg['content']}\n\n"
        
        return md
```

### Step 2: Create Export Router

Create `backend/routers/export.py`:

```python
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
import io

router = APIRouter(prefix="/export", tags=["export"])

export_service = None
session_service = None
chat_service = None

def set_services(export_svc, session_svc, chat_svc):
    global export_service, session_service, chat_service
    export_service = export_svc
    session_service = session_svc
    chat_service = chat_svc

@router.get("/{session_id}/json")
async def export_session_json(session_id: str):
    """Export session as JSON"""
    session = session_service.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    history = chat_service.get_history(session_id)
    json_data = export_service.export_session_json(session, history, session['documents'])
    
    return StreamingResponse(
        io.BytesIO(json_data.encode()),
        media_type="application/json",
        headers={"Content-Disposition": "attachment; filename=session.json"}
    )

@router.get("/{session_id}/markdown")
async def export_session_markdown(session_id: str):
    """Export session as Markdown"""
    session = session_service.get_session(session_id)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    history = chat_service.get_history(session_id)
    md_data = export_service.export_session_markdown(session, history)
    
    return StreamingResponse(
        io.BytesIO(md_data.encode()),
        media_type="text/markdown",
        headers={"Content-Disposition": "attachment; filename=session.md"}
    )
```

### Step 3: Integrate in main.py

```python
from services.export_service import ExportService
from routers import export

# In lifespan
export_service = ExportService()
export.set_services(export_service, session_service, chat_service)

# Include router
app.include_router(export.router)
```

---

## Example 3: Add a Search Feature

### Router (`backend/routers/search.py`)

```python
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/search", tags=["search"])

chat_service = None

def set_chat_service(service):
    global chat_service
    chat_service = service

@router.get("/{session_id}")
async def search_chat(session_id: str, query: str):
    """Search in chat history"""
    if not chat_service:
        raise HTTPException(status_code=500, detail="Service not initialized")
    
    history = chat_service.get_history(session_id)
    
    # Simple search implementation
    results = [
        msg for msg in history
        if query.lower() in msg['content'].lower()
    ]
    
    return {"results": results, "count": len(results)}
```

---

## Pattern Summary

### To Add Any New Feature:

1. **Create Service** (`backend/services/feature_service.py`)
   - Contains business logic
   - Independent, testable
   - Per-session or global

2. **Create Router** (`backend/routers/feature.py`)
   - Exposes API endpoints
   - Delegates to service
   - Handles HTTP concerns

3. **Integrate in main.py**
   - Instantiate service
   - Inject into router
   - Include router in app

4. **Optional: Frontend Component**
   - React component (`frontend/src/components/Feature.jsx`)
   - Calls API client
   - Integrates with existing UI

---

## Best Practices

✅ **DO**
- Keep services focused and single-purpose
- Use dependency injection
- Make services session-aware when needed
- Document service contracts
- Write unit tests for services

❌ **DON'T**
- Use global variables
- Make routers do business logic
- Hardcode session IDs
- Skip error handling
- Mix concerns in one file

---

## Testing Your New Feature

```bash
# Test service directly
python -c "
from backend.services.analytics_service import AnalyticsService
service = AnalyticsService()
analytics = service.track_message('session-1', False, 100)
print(analytics)
"

# Test router
curl http://localhost:8000/analytics/session-1
```

---

## Deployment Considerations

When deploying the multi-instance setup:

1. **Move session storage to database**
   - Replace JSON with PostgreSQL
   - Add connection pooling

2. **Use Redis for chat cache**
   - Store recent messages
   - Cache vectorstore references

3. **Load balancing**
   - Route same session_id to same instance
   - Or use distributed session store

4. **Monitoring**
   - Track errors per session
   - Monitor memory usage
   - Alert on failed exports

---

This modular pattern ensures your application stays maintainable and scalable!
