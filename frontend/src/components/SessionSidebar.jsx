import { useState, useEffect } from 'react';
import axios from 'axios';
import './SessionSidebar.css';

function SessionSidebar({ activeSessionId, onSelectSession, onSessionsChange }) {
  const [sessions, setSessions] = useState([]);
  const [newSessionName, setNewSessionName] = useState('');
  const [loading, setLoading] = useState(false);
  const [editingId, setEditingId] = useState(null);
  const [editingName, setEditingName] = useState('');

  const API_BASE_URL = 'http://localhost:8000';

  // Load sessions on mount
  useEffect(() => {
    loadSessions();
  }, []);

  const loadSessions = async () => {
    try {
      const response = await axios.get(`${API_BASE_URL}/sessions/`);
      setSessions(response.data.sessions || []);
    } catch (error) {
      console.error('Error loading sessions:', error);
    }
  };

  const handleCreateSession = async () => {
    if (!newSessionName.trim()) return;

    setLoading(true);
    try {
      const response = await axios.post(`${API_BASE_URL}/sessions/create`, {
        name: newSessionName,
      });

      setSessions([response.data, ...sessions]);
      onSelectSession(response.data.session_id);
      setNewSessionName('');
      onSessionsChange?.();
    } catch (error) {
      console.error('Error creating session:', error);
      alert('Failed to create session');
    } finally {
      setLoading(false);
    }
  };

  const handleDeleteSession = async (sessionId) => {
    if (!window.confirm('Delete this session?')) return;

    try {
      await axios.delete(`${API_BASE_URL}/sessions/${sessionId}`);
      setSessions(sessions.filter(s => s.session_id !== sessionId));
      
      if (activeSessionId === sessionId) {
        onSelectSession(null);
      }
      onSessionsChange?.();
    } catch (error) {
      console.error('Error deleting session:', error);
      alert('Failed to delete session');
    }
  };

  const handleUpdateSession = async (sessionId) => {
    if (!editingName.trim()) return;

    try {
      const response = await axios.put(
        `${API_BASE_URL}/sessions/${sessionId}`,
        { name: editingName }
      );

      setSessions(sessions.map(s =>
        s.session_id === sessionId ? response.data : s
      ));
      setEditingId(null);
      setEditingName('');
      onSessionsChange?.();
    } catch (error) {
      console.error('Error updating session:', error);
      alert('Failed to update session');
    }
  };

  return (
    <div className="sidebar">
      <div className="sidebar-header">
        <h2>💬 Sessions</h2>
      </div>

      <div className="new-session">
        <input
          type="text"
          value={newSessionName}
          onChange={(e) => setNewSessionName(e.target.value)}
          placeholder="New session name..."
          onKeyPress={(e) => e.key === 'Enter' && handleCreateSession()}
        />
        <button
          onClick={handleCreateSession}
          disabled={loading || !newSessionName.trim()}
        >
          {loading ? '⏳' : '➕'}
        </button>
      </div>

      <div className="sessions-list">
        {sessions.length === 0 ? (
          <div className="no-sessions">No sessions yet</div>
        ) : (
          sessions.map(session => (
            <div
              key={session.session_id}
              className={`session-item ${
                activeSessionId === session.session_id ? 'active' : ''
              }`}
            >
              {editingId === session.session_id ? (
                <div className="edit-session">
                  <input
                    autoFocus
                    type="text"
                    value={editingName}
                    onChange={(e) => setEditingName(e.target.value)}
                    onBlur={() => handleUpdateSession(session.session_id)}
                    onKeyPress={(e) => {
                      if (e.key === 'Enter') {
                        handleUpdateSession(session.session_id);
                      }
                    }}
                  />
                </div>
              ) : (
                <>
                  <div
                    className="session-content"
                    onClick={() => onSelectSession(session.session_id)}
                  >
                    <div className="session-name">{session.name}</div>
                    <div className="session-meta">
                      {session.document_count} document{session.document_count !== 1 ? 's' : ''}
                    </div>
                  </div>
                  <div className="session-actions">
                    <button
                      className="btn-icon"
                      onClick={() => {
                        setEditingId(session.session_id);
                        setEditingName(session.name);
                      }}
                      title="Edit"
                    >
                      ✏️
                    </button>
                    <button
                      className="btn-icon delete"
                      onClick={() => handleDeleteSession(session.session_id)}
                      title="Delete"
                    >
                      🗑️
                    </button>
                  </div>
                </>
              )}
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default SessionSidebar;
