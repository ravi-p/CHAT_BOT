# LangSmith Integration Guide

## Overview
This project is integrated with **LangSmith** for comprehensive tracing, monitoring, and debugging of LLM interactions and chain executions.

## What is LangSmith?
LangSmith is a platform for debugging, testing, and monitoring LLM applications. It provides:
- **Tracing**: Automatic tracking of all LLM calls and chain executions
- **Debugging**: Detailed logs of inputs, outputs, and intermediate steps
- **Testing**: Dataset management and evaluation frameworks
- **Monitoring**: Production performance tracking and error analysis

## Environment Configuration

### Required Environment Variables
Your `.env` file contains the following LangSmith settings:

```dotenv
# LangSmith API Configuration
LANGSMITH_API_KEY=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
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_PROJECT=chat-bot-project
LANGSMITH_TRACING_V2=true
```

### Environment Variable Reference

| Variable | Description | Default |
|----------|-------------|---------|
| `LANGSMITH_API_KEY` | API key for authentication (personal or service key) | Required for tracing |
| `LANGSMITH_ENDPOINT` | LangSmith API endpoint | `https://api.smith.langchain.com` |
| `LANGSMITH_PROJECT` | Project name for organizing traces | `chat-bot-project` |
| `LANGSMITH_TRACING_V2` | Enable tracing v2 protocol | `true` |

## How LangSmith is Integrated

### 1. **Automatic Environment Setup** (`backend/main.py`)

When the application starts, it automatically configures LangSmith:

```python
if os.getenv("LANGSMITH_API_KEY"):
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_ENDPOINT"] = "https://api.smith.langchain.com"
    os.environ["LANGCHAIN_API_KEY"] = "<api_key>"
    os.environ["LANGCHAIN_PROJECT"] = "chat-bot-project"
    print("✓ LangSmith tracing enabled")
```

### 2. **LLM Tagging** (`backend/services/chat_service.py`)

The ChatOpenAI instance is tagged for better organization in LangSmith:

```python
self.llm = ChatOpenAI(
    model="gpt-4o-mini",
    temperature=0,
    tags=["chat-service"]  # Visible in LangSmith traces
)
```

### 3. **Query Tracing** (`backend/services/chat_service.py`)

Each query is automatically traced with metadata:

```python
trace_metadata = {
    "session_id": session_id,
    "has_vectorstore": bool(vectorstore),
    "query_length": len(query),
}
tags = ["chat-query", f"session:{session_id}"]
```

## What Gets Traced

### Automatic Tracing (No Code Changes Required)
- ✅ LLM API calls (to OpenAI)
- ✅ Prompt templates and formatting
- ✅ Chain executions (RAG chains)
- ✅ Document retrieval operations
- ✅ Token counts and model information

### Tagged Operations
- ✅ Chat queries with session metadata
- ✅ RAG vs. General QA differentiation
- ✅ Session creation/deletion
- ✅ Memory management operations

## Accessing Traces

### 1. Open LangSmith Dashboard
Go to: https://smith.langchain.com

### 2. Navigate to Your Project
Look for the **"chat-bot-project"** project in your dashboard

### 3. View Traces
Each API call to `/chat/{session_id}/message` will create a trace showing:
- Query input
- Retrieved documents (if RAG enabled)
- LLM response
- Token usage
- Latency information
- All intermediate chain steps

## Trace Structure Example

```
Chat Query Trace
├── Session ID: abc123...
├── Query: "What is the weather?"
├── Type: with-rag (or general-qa)
├── LLM Call
│   ├── Model: gpt-4o-mini
│   ├── Tokens: 45 prompt, 15 completion
│   ├── Duration: 1.2s
│   └── Output: "The weather is..."
├── Retriever (if RAG)
│   ├── Query: "What is the weather?"
│   ├── Results: 3 documents
│   └── Duration: 0.3s
└── Memory
    ├── Saved: yes
    └── Duration: 0.05s
```

## Benefits for Your Application

### 🔍 **Debugging**
- See exactly what each LLM call produces
- Inspect prompt templates and variable substitutions
- Identify performance bottlenecks

### 📊 **Monitoring**
- Track token usage and costs
- Monitor response latency
- Identify error patterns

### 📈 **Optimization**
- Compare prompt variations
- Test different models
- Evaluate RAG effectiveness

### 🧪 **Testing**
- Create datasets from production traces
- Build evaluation harnesses
- A/B test different approaches

## Disabling LangSmith (Optional)

To disable tracing temporarily, remove or comment out the `LANGSMITH_API_KEY` in your `.env` file:

```dotenv
# LANGSMITH_API_KEY=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
```

The application will automatically detect this and skip LangSmith initialization.

## Troubleshooting

### Issue: "Authentication failed" in traces
- **Solution**: Verify your `LANGSMITH_API_KEY` is correct and not expired
- Check if it's a personal (`lsv2_pt_*`) vs. service key (`lsv2_sk_*`)

### Issue: No traces appearing in dashboard
- **Solution**: Ensure `LANGSMITH_TRACING_V2=true` is set
- Check the application logs for "✓ LangSmith tracing enabled"
- Verify the `LANGSMITH_PROJECT` name matches the project in your dashboard

### Issue: Performance degradation
- **Solution**: LangSmith has minimal overhead (~10-50ms per trace)
- If unacceptable, you can disable it via `.env` configuration

## API Key Management

### Best Practices
- ✅ **Never commit API keys** to version control
- ✅ Use `.env` file for local development (included in `.gitignore`)
- ✅ Use environment variables in production (Docker, K8s, Cloud platforms)
- ✅ Rotate keys periodically for security

### Types of Keys
- **Personal Keys** (`lsv2_pt_*`): For development and testing
- **Service Keys** (`lsv2_sk_*`): For production with restricted permissions
- **Tenant Keys** (`lsv2_tk_*`): For multi-tenant deployments

## Useful Resources

- [LangSmith Documentation](https://docs.smith.langchain.com/)
- [LangSmith API Reference](https://docs.smith.langchain.com/reference)
- [LangChain Integration Docs](https://python.langchain.com/docs/langsmith/)
- [Debugging with LangSmith](https://docs.smith.langchain.com/user_guide/debugging)

## Summary

Your chat application now has enterprise-grade observability! Every interaction is automatically traced, allowing you to:
- Debug issues quickly
- Understand LLM behavior
- Optimize costs and performance
- Build reliable AI applications

Monitor your traces at: https://smith.langchain.com/projects/chat-bot-project
