import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

// Session API calls
export const sessionAPI = {
  createSession: (name) => 
    axios.post(`${API_BASE_URL}/sessions/create`, { name }),
  
  listSessions: () => 
    axios.get(`${API_BASE_URL}/sessions/`),
  
  getSession: (sessionId) => 
    axios.get(`${API_BASE_URL}/sessions/${sessionId}`),
  
  updateSession: (sessionId, name) => 
    axios.put(`${API_BASE_URL}/sessions/${sessionId}`, { name }),
  
  deleteSession: (sessionId) => 
    axios.delete(`${API_BASE_URL}/sessions/${sessionId}`),
};

// Chat API calls
export const chatAPI = {
  sendMessage: (sessionId, query) => {
    const formData = new FormData();
    formData.append('query', query);
    return axios.post(`${API_BASE_URL}/chat/${sessionId}/message`, formData);
  },
  
  getHistory: (sessionId) => 
    axios.get(`${API_BASE_URL}/chat/${sessionId}/history`),
  
  clearHistory: (sessionId) => 
    axios.post(`${API_BASE_URL}/chat/${sessionId}/clear`),
};

// Document API calls
export const documentAPI = {
  uploadDocument: (sessionId, file) => {
    const formData = new FormData();
    formData.append('file', file);
    return axios.post(`${API_BASE_URL}/documents/${sessionId}/upload`, formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    });
  },
  
  listDocuments: (sessionId) => 
    axios.get(`${API_BASE_URL}/documents/${sessionId}/list`),
  
  deleteDocument: (sessionId, docId) => 
    axios.delete(`${API_BASE_URL}/documents/${sessionId}/documents/${docId}`),
};

export default {
  sessionAPI,
  chatAPI,
  documentAPI,
};
