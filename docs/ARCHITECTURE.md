# ARCHITECTURE.md

This document organizes the architecture that is already decided in [`PROJECT_CONTEXT.md`](./PROJECT_CONTEXT.md) into one reference. It does not introduce new decisions — see `PROJECT_CONTEXT.md` for the full rationale behind each choice, and `DECISIONS.md` for the decision log.

---

## Workflow

```
User
  ↓
Retriever Agent
  ↓
Retriever Tool
  ↓
knowledge_base.txt
  ↓
Retriever Agent
  ↓
Report Generator Agent
  ↓
Final Answer
```

Sequential LangGraph nodes only. No loops, no reflection, no planning agent, no reviewer agent inside the application, no autonomous decision making.

---

## Runtime agents (exactly two)

### Retriever Agent

| | |
|---|---|
| May | call the retrieval tool |
| May NOT | summarize, answer the user, generate reports |

Receives the user's question, invokes the retrieval tool against `knowledge_base.txt`, and returns only the relevant retrieved context. Never answers the user directly.

### Report Generator Agent

| | |
|---|---|
| May | summarize retrieved context |
| May NOT | search documents, call retrieval logic |

Receives retrieved context and generates a concise response using only that context. Never invents information, never retrieves documents.

This boundary (retrieval vs. generation) is the core architectural constraint of the assignment and must not be blurred by any implementation task.

---

## Framework & model choices

- **Orchestration:** LangGraph + LangChain — sequential nodes, no complex graph logic needed.
- **LLM:** Gemini (Google AI) — abstracted behind the implementation so another provider could be swapped in later.
- **Retrieval:** Embedding-based semantic search over paragraph chunks of `knowledge_base.txt`. Top-k relevant chunks only — no reranking, no hybrid search, no vector database (no ChromaDB/Pinecone/FAISS/Elasticsearch).

---

## Folder responsibilities

```
src/
  agents/    Agent implementations
  tools/     Retrieval tools
  graph/     LangGraph workflow (sequential node wiring)
  prompts/   Prompts used by agents
```

No business logic outside `src/`.

---

## Non-goals

Explicitly out of scope for this assignment (see `PROJECT_CONTEXT.md` for full list): production-grade RAG, vector databases, reranking, hybrid search, additional runtime agents, memory, planning loops, reflection.
