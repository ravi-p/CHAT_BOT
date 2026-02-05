"""
Chat Service
Manages chat interactions and LLM operations per session
Integrated with LangSmith for tracing and monitoring
"""

from typing import Dict, Optional, List
import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores.faiss import FAISS
from langchain_classic.chains import create_retrieval_chain
from langchain_classic.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.memory import ConversationTokenBufferMemory
from langsmith.run_trees import RunTree

class ChatService:
    """Service for managing chat operations per session"""
    
    def __init__(self):
        """Initialize chat service"""
        # Initialize LLM and embeddings (shared across sessions)
        # LangSmith tracing is automatically enabled via environment variables
        self.llm = ChatOpenAI(
            model="gpt-4o-mini",
            temperature=0,
            tags=["chat-service"]  # Tag for LangSmith tracing
        )
        self.embeddings = OpenAIEmbeddings()
        
        # Session-specific storage
        self.vectorstores: Dict[str, FAISS] = {}
        self.memories: Dict[str, ConversationTokenBufferMemory] = {}
        self.chat_history: Dict[str, List[dict]] = {}
        
        # LangSmith tracing enabled flag
        self.langsmith_enabled = bool(os.getenv("LANGSMITH_API_KEY"))
    
    def _get_or_create_memory(self, session_id: str) -> ConversationTokenBufferMemory:
        """Get or create memory for a session"""
        if session_id not in self.memories:
            self.memories[session_id] = ConversationTokenBufferMemory(
                llm=self.llm,
                memory_key="chat_history",
                max_token_limit=400,
                return_messages=False,
            )
        return self.memories[session_id]
    
    def _get_vectorstore(self, session_id: str) -> Optional[FAISS]:
        """Get vectorstore for a session"""
        return self.vectorstores.get(session_id)
    
    def set_vectorstore(self, session_id: str, vectorstore: FAISS):
        """Set vectorstore for a session"""
        self.vectorstores[session_id] = vectorstore
        if session_id not in self.chat_history:
            self.chat_history[session_id] = []
    
    async def process_query(self, session_id: str, query: str) -> dict:
        """Process a query in a chat session"""
        vectorstore = self._get_vectorstore(session_id)
        # Allow chatting without any uploaded documents: fall back to general LLM
        try:
            memory = self._get_or_create_memory(session_id)
            
            # Create a custom trace for this query interaction in LangSmith
            trace_metadata = {
                "session_id": session_id,
                "has_vectorstore": bool(vectorstore),
                "query_length": len(query),
            }
            tags = ["chat-query", f"session:{session_id}"]
            if vectorstore:
                tags.append("with-rag")
            else:
                tags.append("general-qa")

            # Load recent token-limited chat history (string)
            chat_history_str = memory.load_memory_variables({}).get("chat_history", "")

            # If we have a vectorstore for the session, use RAG as before.
            if vectorstore:
                retriever = vectorstore.as_retriever(search_kwargs={"k": 3})

                # RAG Prompt including recent chat history and retrieved context
                system_prompt = (
                    "You are an assistant for question-answering tasks. "
                    "Use the following recent chat history and retrieved context to answer "
                    "the question. If you don't know the answer, say that you "
                    "don't know. Use three sentences maximum and keep the "
                    "answer concise."
                    "\n\nRecent chat history:\n{chat_history}\n\nContext:\n{context}"
                )

                prompt = ChatPromptTemplate.from_messages([
                    ("system", system_prompt),
                    ("human", "{input}"),
                ])

                # Create chains and perform retrieval-augmented generation
                question_answer_chain = create_stuff_documents_chain(self.llm, prompt)
                rag_chain = create_retrieval_chain(retriever, question_answer_chain)

                response = rag_chain.invoke({
                    "input": query,
                    "chat_history": chat_history_str,
                })

                answer = response.get("answer") if isinstance(response, dict) else response

            else:
                # No document context: use general LLM prompt (fallback)
                system_prompt = (
                    "You are a helpful general-purpose assistant. "
                    "Answer the user's question concisely and clearly. "
                    "If you don't know the answer, say so. Use at most three sentences."
                    "\n\nRecent chat history:\n{chat_history}\n\nContext:\n{context}"
                )

                prompt = ChatPromptTemplate.from_messages([
                    ("system", system_prompt),
                    ("human", "{input}"),
                ])

                # Create a simple QA chain (no retriever) and invoke it with empty context
                question_answer_chain = create_stuff_documents_chain(self.llm, prompt)
                response = question_answer_chain.invoke({
                    "input": query,
                    "chat_history": chat_history_str,
                    "context": "",
                })

                answer = response.get("answer") if isinstance(response, dict) else response

            # Save the interaction to token-limited memory
            try:
                memory.save_context({"input": query}, {"output": answer})
            except Exception as e:
                print(f"Error saving to memory: {e}")

            # Track in chat history
            if session_id not in self.chat_history:
                self.chat_history[session_id] = []
            self.chat_history[session_id].append({"role": "user", "content": query})
            self.chat_history[session_id].append({"role": "assistant", "content": answer})

            return {"answer": answer, "context": []}

        except Exception as e:
            return {"error": str(e)}
    
    def get_history(self, session_id: str) -> List[dict]:
        """Get chat history for a session"""
        return self.chat_history.get(session_id, [])
    
    def clear_history(self, session_id: str):
        """Clear chat history for a session"""
        memory = self._get_or_create_memory(session_id)
        try:
            memory.clear()
        except Exception:
            pass
        
        self.chat_history[session_id] = []
    
    def delete_session(self, session_id: str):
        """Clean up session data"""
        if session_id in self.vectorstores:
            del self.vectorstores[session_id]
        if session_id in self.memories:
            del self.memories[session_id]
        if session_id in self.chat_history:
            del self.chat_history[session_id]
