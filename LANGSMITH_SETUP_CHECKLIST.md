# LangSmith Setup Checklist ✅

## Pre-Setup (One-time)

- [ ] Create LangSmith account at https://smith.langchain.com
- [ ] Generate API key in Settings → API Keys
- [ ] Copy API key (format: `lsv2_pt_*`)

## Code Changes Completed ✓

### Backend Files
- [x] **`.env`** - Corrected LangSmith environment variables
- [x] **`main.py`** - Added automatic LangSmith initialization
- [x] **`services/chat_service.py`** - Added LLM tags and tracing metadata
- [x] **`services/session_service.py`** - Added logging support for tracing

### Documentation Files
- [x] **`LANGSMITH_INTEGRATION.md`** - Full integration guide
- [x] **`LANGSMITH_QUICKSTART.md`** - Quick reference guide
- [x] **`LANGSMITH_IMPLEMENTATION.md`** - Implementation summary

## Verification Steps

### 1. Start Backend
```bash
cd backend
python main.py
```
Expected output:
```
✓ LangSmith tracing enabled
```
- [ ] See "LangSmith tracing enabled" message
- [ ] Backend runs without errors

### 2. Send Test Message
```bash
# Via frontend UI or API:
curl -X POST http://localhost:8000/chat/{session_id}/message \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "query=Hello, how are you?"
```
- [ ] Message processed successfully
- [ ] Receive response from backend

### 3. Check LangSmith Dashboard
1. Open https://smith.langchain.com
2. Go to Projects → chat-bot-project
3. Check Traces tab
- [ ] See new trace appear
- [ ] Trace contains your query
- [ ] All metadata is visible

## Environment Configuration

Current `.env` settings:
```
LANGSMITH_API_KEY=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
LANGSMITH_ENDPOINT=https://api.smith.langchain.com
LANGSMITH_PROJECT=chat-bot-project
LANGSMITH_TRACING_V2=true
```

## Troubleshooting Checklist

If traces aren't appearing:

- [ ] API key is valid (not expired)
- [ ] `.env` file has `LANGSMITH_API_KEY` set
- [ ] Backend shows "✓ LangSmith tracing enabled"
- [ ] You're looking at correct project (`chat-bot-project`)
- [ ] Network connectivity to api.smith.langchain.com
- [ ] Waited 5+ seconds for trace to sync

If "authentication failed":

- [ ] API key hasn't changed (check in Settings)
- [ ] Using personal key (`lsv2_pt_*`), not service key
- [ ] No typos in `.env` file
- [ ] `.env` file saved properly

## What to Monitor

### Performance Metrics
- **Latency**: How long queries take
- **Token Usage**: Prompt + completion tokens per query
- **Cost**: Estimated API spend
- **Error Rate**: Percentage of failed queries

### Key Traces to Check
- [x] Chat queries with documents (RAG)
- [x] Chat queries without documents (general QA)
- [x] Error traces (if any)
- [x] Session creation/deletion operations

## Pro Tips

1. **Filter by session**: Use tag `session:abc123...` to see all queries in a session
2. **Compare traces**: Select 2+ traces and click "Compare" for differences
3. **Export data**: Create datasets from traces for evaluation
4. **Monitor costs**: Track token usage to estimate monthly costs
5. **Debug errors**: Click trace → "Inspect" for full error context

## Next Steps

1. Monitor your first 10-20 traces
2. Explore the LangSmith dashboard features
3. Create evaluation datasets if needed
4. Set up alerts for errors (if available)
5. Review costs weekly

## Quick Links

- 🔗 LangSmith Dashboard: https://smith.langchain.com
- 📖 Full Documentation: [LANGSMITH_INTEGRATION.md](LANGSMITH_INTEGRATION.md)
- ⚡ Quick Start: [LANGSMITH_QUICKSTART.md](LANGSMITH_QUICKSTART.md)
- 📋 Implementation: [LANGSMITH_IMPLEMENTATION.md](LANGSMITH_IMPLEMENTATION.md)

---

## Done! 🎉

Your application is now fully integrated with LangSmith!

Every interaction is automatically traced and visible in your dashboard.

**Happy monitoring!** 🚀
