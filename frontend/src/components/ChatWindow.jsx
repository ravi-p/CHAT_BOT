import { useState, useEffect } from 'react';
import axios from 'axios';
import './ChatWindow.css';

function ChatWindow({ sessionId }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);

  const API_BASE_URL = 'http://localhost:8000';

  // Load chat history when session changes
  useEffect(() => {
    const loadHistory = async () => {
      try {
        const response = await axios.get(`${API_BASE_URL}/chat/${sessionId}/history`);
        setMessages(response.data.messages || []);
      } catch (error) {
        console.error('Error loading chat history:', error);
      }
    };

    if (sessionId) {
      loadHistory();
      setMessages([]);
      setInput('');
    }
  }, [sessionId]);

  const handleSendMessage = async () => {
    if (!input.trim() || !sessionId) return;

    const userMessage = { role: 'user', content: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setLoading(true);

    try {
      const formData = new FormData();
      formData.append('query', input);

      const response = await axios.post(
        `${API_BASE_URL}/chat/${sessionId}/message`,
        formData
      );

      const botMessage = {
        role: 'assistant',
        content: response.data.answer || 'No response received',
      };
      setMessages(prev => [...prev, botMessage]);
    } catch (error) {
      console.error('Error sending message:', error);
      const errorMessage = {
        role: 'assistant',
        content: 'Error getting response. Is backend running?',
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setLoading(false);
    }
  };

  const handleClearHistory = async () => {
    try {
      await axios.post(`${API_BASE_URL}/chat/${sessionId}/clear`);
      setMessages([]);
    } catch (error) {
      console.error('Error clearing history:', error);
    }
  };

  if (!sessionId) {
    return (
      <div className="chat-window empty">
        <p>Select a session to start chatting</p>
      </div>
    );
  }

  return (
    <div className="chat-window">
      <div className="chat-header">
        <h3>Chat</h3>
        <button
          className="btn-clear"
          onClick={handleClearHistory}
          title="Clear chat history"
        >
          🗑️ Clear
        </button>
      </div>

      <div className="messages-area">
        {messages.length === 0 && (
          <div className="empty-state">Start a conversation — document upload is optional</div>
        )}
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`message ${msg.role}`}
          >
            <span className={`message-content ${msg.role}`}>
              {msg.content}
            </span>
          </div>
        ))}
        {loading && (
          <div className="message assistant loading">
            <span className="message-content assistant">Thinking...</span>
          </div>
        )}
      </div>

      <div className="input-area">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
          placeholder="Ask a question..."
          disabled={loading}
        />
        <button
          onClick={handleSendMessage}
          disabled={loading || !input.trim()}
          className="btn-send"
        >
          {loading ? '⏳' : '📤'}
        </button>
      </div>
    </div>
  );
}

export default ChatWindow;
