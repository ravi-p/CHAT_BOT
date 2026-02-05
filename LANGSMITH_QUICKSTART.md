# LangSmith Quick Start

## 🚀 Getting Started

### 1. Already Configured ✓
Your environment is already set up! No additional setup needed.

### 2. Verify LangSmith is Active
When you start the backend:
```bash
cd backend
python main.py
```

You should see:
```
✓ LangSmith tracing enabled
```

### 3. Monitor in Real-Time
1. Open https://smith.langchain.com
2. Go to Projects → **chat-bot-project**
3. Send a message via the chat UI
4. See the trace appear instantly in LangSmith dashboard

## 📝 What's Traced

| Operation | Details Captured |
|-----------|-----------------|
| User Query | Input text, session ID |
| LLM Call | Model, tokens, latency, output |
| RAG Retrieval | Documents retrieved, similarity scores |
| Memory | Conversation history managed |
| Errors | Full error traces with context |

## 🔧 Common Tasks

### View All Traces
Dashboard → Projects → chat-bot-project → Traces (tab)

### Search Traces
Filter by:
- Session ID: `session:abc123...`
- Query type: `chat-query` or `general-qa`
- Timeframe: Last hour/day/week

### Compare Traces
- Select 2+ traces
- Click "Compare"
- See side-by-side differences

### Create Test Dataset
1. Right-click a trace
2. Select "Add to Dataset"
3. Use for evaluation later

## 🚨 Troubleshooting

**No traces showing?**
- Check backend logs for "✓ LangSmith tracing enabled"
- Verify LANGSMITH_API_KEY in .env is not commented out
- Ensure you're in correct project (chat-bot-project)

**Want to disable temporarily?**
- Comment out `LANGSMITH_API_KEY` in .env
- Restart backend
- Tracing will auto-disable

## 📊 Key Metrics Available

- **Latency**: Response time per query
- **Tokens**: Prompt + completion token counts
- **Cost**: Estimated API costs (if configured)
- **Errors**: Failed queries with full stack traces
- **Success Rate**: Percentage of successful traces

## 💡 Pro Tips

1. **Use tags**: Filter traces by session or query type
2. **Check costs**: Monitor token usage in production
3. **Debug errors**: Click trace → "Inspect" to see full context
4. **Compare performance**: RAG traces vs. general QA traces

## 📚 Learn More

- Full docs: [LANGSMITH_INTEGRATION.md](LANGSMITH_INTEGRATION.md)
- LangSmith docs: https://docs.smith.langchain.com/
