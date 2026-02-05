import { useState } from 'react';
import SessionSidebar from './components/SessionSidebar';
import ChatWindow from './components/ChatWindow';
import './App.css';

function App() {
  const [activeSessionId, setActiveSessionId] = useState(null);
  const [sessionsUpdated, setSessionsUpdated] = useState(0);

  const handleSessionsChange = () => {
    setSessionsUpdated(prev => prev + 1);
  };

  return (
    <div className="app-container">
      <header className="app-header">
        <h1>🤖 Multi-Session Chat</h1>
        <p>Manage multiple conversations</p>
      </header>

      <div className="app-layout">
        <SessionSidebar
          activeSessionId={activeSessionId}
          onSelectSession={setActiveSessionId}
          onSessionsChange={handleSessionsChange}
        />

        <div className="main-content">
          <div className="right-panel">
            <ChatWindow sessionId={activeSessionId} />
          </div>
        </div>
      </div>
    </div>
  );
}

export default App;