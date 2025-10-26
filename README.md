# Cognitive Memory Architecture

A modular memory system for AI agents that combines short-term, episodic, and semantic memory to enable coherent long-term conversations — even with small models and limited context windows (e.g., Ollama, LocalAI, or LLaMA.cpp).

---

## Overview

This project provides a three-layered memory design inspired by human cognition:

| Memory Type | Storage | Purpose |
|--------------|----------|----------|
| Short-Term Memory | Redis | Keeps recent messages for active conversation context |
| Episodic Memory | PostgreSQL | Stores summarized conversation episodes once a context window limit is reached |
| Semantic (Knowledge) Memory | Vector Database (e.g. FAISS, Qdrant, Chroma) | Retains facts, summaries, and documents for retrieval and reasoning |

Each layer plays a specific role in maintaining context, learning from prior interactions, and providing user-specific knowledge recall.

---

## Memory Layers

### 1. Short-Term Memory (Conversational Memory)

The Short-Term Memory stores the most recent chat messages in a fast cache (Redis). 
It allows the model to maintain continuity during a session.

**Schema:**
```
session_id   # unique UUID for the chat session
role         # "human" or "ai"
message      # chat content
token_count  # running token total for this session
```

**Trigger:** 
When the token count reaches approximately 80% of the model’s context window, the conversation is summarized and offloaded to long-term memory.

---

### 2. Long-Term Memory (Episodic Memory)

The Episodic Memory stores high-level summaries of conversations in a relational database (PostgreSQL). 
Each record represents a complete episode of interaction — what the user asked, how the AI responded, and a combined summary for context restoration.

**Schema:**
```
session_id
human_summary
ai_summary
combined_summary
timestamp
```

After saving a summary, the model receives the combined summary as the new context, allowing it to continue the conversation seamlessly.

---

### 3. Semantic Memory (Knowledge Memory)

The Semantic Memory is a vector-based knowledge store that contains embeddings of:
- past conversation summaries 
- user-uploaded documents 
- extracted facts and relations 

This allows semantic search and knowledge grounding across sessions. 
It is user-dependent, meaning each user can recall and query their own history and knowledge base.

**Example:**
> “Remind me how we configured Redis last week.” 
> The system retrieves the relevant episodic summary via vector similarity.

---

## Architecture Summary

```
           ┌────────────────────────┐
           │   User Interaction     │
           └────────────┬───────────┘
                        │
                        ▼
             ┌────────────────────┐
             │ Short-Term Memory  │  ← Redis (recent chat)
             └────────┬───────────┘
                      │  summarize when ~80% context used
                      ▼
             ┌────────────────────┐
             │ Episodic Memory    │  ← PostgreSQL (summaries)
             └────────┬───────────┘
                      │  embed summaries
                      ▼
             ┌────────────────────┐
             │ Knowledge Memory   │  ← Vector DB (facts, embeddings)
             └────────────────────┘
```

---

## Goals

- Enable context continuity beyond small model limits 
- Support memory persistence between sessions 
- Provide semantic recall across conversations 
- Build foundation for fine-tuning datasets (from episodic memory)

---

## Tech Stack

| Component | Technology |
|------------|-------------|
| Cache | Redis |
| Database | PostgreSQL / SQLModel |
| Vector Store | FAISS / Milvus |
| Language Models | Ollama / LocalAI / LLaMA.cpp |
| API Layer | Flask / FastAPI|

---

## Example Workflow

1. User starts a chat → new session_id (UUID)
2. Messages are stored in Short-Term Memory (Redis)
3. On each new user/assistant message: check token usage
4. If ~80% context is reached:  
    * Generate human_summary, ai_summary, combined_summary
    * Persist to Episodic Memory (SQL)
    * Write combined_summary back into Redis as a context snapshot (e.g., a system/memory message) and optionally prune old turns
    * Continue the same turn: build the prompt from the snapshot + recent tail and answer the user’s message based on that
5. Optionally (async): embed the combined_summary and index it in Knowledge Memory (VectorDB) for later recall

---

## Future Enhancements

- Add procedural memory for tool use and agent behavior patterns 
- Implement memory pruning and relevance scoring 
- Integrate LangGraph for agent orchestration 
- Enable user-personalized knowledge graphs 

---

## License

MIT License © 2025 [Christopher Abanilla @ Evolvingstack]  
