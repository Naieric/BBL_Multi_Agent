# DECISIONS.md

Architecture Decision Record log for this repository. Each entry captures a decision, why it was made, and what alternatives were rejected. New entries go at the top.

Entries below marked **[seeded]** were already decided in `PROJECT_CONTEXT.md` prior to this log's creation and are recorded here for traceability, not re-decided.

---

## Template for new entries

```
## YYYY-MM-DD — <short title>

**Decision:** what was decided.
**Why:** the reasoning / constraint that drove it.
**Rejected alternatives:** what else was considered and why it lost.
```

---

## 2026-07-26 — Mixed pinning strategy in requirements.txt

**Decision:** Pin the LangChain stack exactly (`langgraph==1.2.9`, `langchain==1.3.14`, `langchain-google-genai==4.3.1`); use lower bounds only for the stable utilities (`numpy>=1.26`, `python-dotenv>=1.0`, `pytest>=8.0`).
**Why:** The two risks pull in opposite directions. The LangChain stack genuinely broke across recent majors, so the exact verified combination is worth freezing. But hard-pinning utilities actively breaks reviewers: the current `numpy` (2.5.1) requires Python 3.12+, so pinning it would fail to install on this project's declared 3.10+ floor. Lower bounds let pip resolve whatever fits the reviewer's interpreter.
**Rejected alternatives:** Pin everything — breaks on Python 3.10/3.11 via numpy; pin nothing — leaves the code exposed to the exact API churn that motivated the research step.

## 2026-07-26 — Target Python 3.10+ rather than 3.11+

**Decision:** Lower the declared Python requirement in `PROJECT_CONTEXT.md` from 3.11+ to 3.10+.
**Why:** The development machine has only Python 3.10.0, and every dependency supports `>=3.10`. Nothing in this codebase uses a 3.11-only feature. Declaring 3.11+ while only ever testing on 3.10 would put an untested claim in the README of a submission repo.
**Rejected alternatives:** Installing 3.11+ — fine, but buys nothing here; keeping the 3.11+ claim untested — rejected as dishonest documentation.

## 2026-07-26 — Pinned library and model versions (verified against upstream docs)

**Decision:** Target `langgraph` 1.2.9, `langchain-core` 1.5.1, `langchain-google-genai` 4.3.1. Chat model `gemini-3.6-flash`; embedding model `gemini-embedding-001`. Both model IDs live as constants in `src/config.py`, changeable in one line.
**Why:** These are all major versions ahead of what a model would produce from memory (LangGraph was 0.2.x, langchain-core 0.3.x, and `langchain-google-genai` 4.0 consolidated onto the `google-genai` SDK with breaking changes). Writing code from memory would have produced a stale, non-working API. Verified against PyPI and `docs.langchain.com` on 2026-07-26.
**Rejected alternatives:** `gemini-2.0-flash` / `gemini-3.5-flash` — superseded; `gemini-3.5-flash-lite` is cheaper but the workload here is two calls per run, so cost is irrelevant and answer quality is what a reviewer sees.

## 2026-07-26 — Use the GA embedding model, not the preview one

**Decision:** Use `gemini-embedding-001` (generally available, text-only) rather than `gemini-embedding-2-preview`, even though current LangChain docs use the preview model in their examples.
**Why:** This is a submission repo that must still run when a reviewer clones it. A preview model can change or be withdrawn without notice. `gemini-embedding-2-preview`'s only advantage is multimodality (image/video/audio/PDF), and our corpus is a single plain-text file — so we would be taking on preview risk for a capability we never use.
**Rejected alternatives:** `gemini-embedding-2-preview` — rejected per above. Note the two models' embedding spaces are incompatible, so this is not a drop-in swap later; it would require re-embedding, which is cheap here since embeddings are computed per run.

## 2026-07-26 — Pass no sampling parameters to the chat model

**Decision:** Construct the chat model with no `temperature` argument.
**Why:** An earlier version of this entry called for `temperature=0`, reasoning that the client defaults to 1.0 for Gemini 3.0+ models. That reasoning does not apply to the model actually chosen: `gemini-3.6-flash` is on the client's fixed-sampling list, so `temperature` is stripped from the request and a `UserWarning` is emitted on every call. Passing it bought nothing and put a warning into every terminal screenshot. Grounding is enforced by the prompts, which is where it belongs.
**Rejected alternatives:** Keeping `temperature=0` — silently ignored, and the warning pollutes output; switching to a model that honours sampling parameters — trades away the current model choice for a parameter that adds little on top of an explicit prompt; suppressing the warning — hides real warnings too.
**Note:** Caught in review after the code was written. Recorded rather than quietly edited, because the original reasoning was plausible and would otherwise be repeated.

## 2026-07-26 — Retriever Agent uses real LLM tool-calling, single turn

**Decision:** The Retriever Agent binds the retrieval tool to the model via `bind_tools()`, takes exactly one tool-calling turn, executes the returned tool call, and stops. No loop.
**Why:** The Definition of Done requires "the Retriever uses a tool," and `PROJECT_CONTEXT.md` cites Gemini's reliable tool calling as a selection reason. A single bounded turn satisfies this genuinely while respecting the explicit ban on loops.
**Rejected alternatives:** Calling the tool function directly from the node — simpler, but then no agent is actually "using a tool" and the DoD item is only nominally met. LangGraph's prebuilt ReAct agent — rejected outright: it introduces an iteration loop, which `PROJECT_CONTEXT.md` bans.

## 2026-07-26 — No `task_type` on embeddings

**Decision:** Use one embeddings client with no `task_type` argument, for both documents and the query.
**Why:** `GoogleGenerativeAIEmbeddings` supports `task_type="RETRIEVAL_DOCUMENT"` / `"RETRIEVAL_QUERY"`, which would marginally improve retrieval quality — but it requires two separately-configured clients for a corpus of a few dozen paragraphs. Not worth the extra moving part at this scale.
**Rejected alternatives:** Two task-typed clients — correct at production scale, disproportionate here.

---

## [seeded] Exactly two runtime agents, sequential workflow

**Decision:** The application contains exactly two runtime agents — Retriever and Report Generator — wired as sequential LangGraph nodes. No loops, reflection, planning agent, or reviewer agent inside the application.
**Why:** The assignment requires a minimal Agentic AI workflow; the objective is a clean, understandable implementation, not a production-grade system.
**Rejected alternatives:** Adding a planning/reflection loop or a third orchestration agent — rejected as unnecessary complexity beyond assignment scope.

## [seeded] LangGraph + LangChain for orchestration

**Decision:** Use LangGraph for the workflow graph and LangChain for supporting integrations.
**Why:** LangGraph demonstrates agent orchestration clearly while staying simple enough for a sequential-node workflow.
**Rejected alternatives:** Hand-rolled orchestration (no framework) — would show less familiarity with standard agentic tooling; more complex frameworks — unnecessary for a sequential, two-node graph.

## [seeded] Gemini as the LLM provider

**Decision:** Use Gemini (Google AI), abstracted so another provider could be swapped in later.
**Why:** Easy API access, good LangChain integration, reliable tool calling, cost effective.
**Rejected alternatives:** Not specified in `PROJECT_CONTEXT.md`; provider abstraction is kept so this could change without touching agent logic.

## [seeded] Embedding-based retrieval, no vector database

**Decision:** Split `knowledge_base.txt` into paragraph chunks, embed them, compute semantic similarity, return top-k chunks. No reranking, no hybrid search, no vector DB (ChromaDB/Pinecone/FAISS/Elasticsearch all explicitly excluded).
**Why:** Embedding retrieval better demonstrates practical RAG knowledge than plain keyword search while staying lightweight; the assignment explicitly asks for a simple local knowledge base.
**Rejected alternatives:** Keyword search (accepted by the assignment but demonstrates less RAG understanding); a vector database (explicitly excluded — unnecessary for a single local text file).

## [seeded] Single local knowledge source: knowledge_base.txt

**Decision:** Only `knowledge_base.txt` is used as the knowledge source. No PDFs, no external storage.
**Why:** The assignment explicitly asks for a simple local knowledge base.
**Rejected alternatives:** Multi-format ingestion (PDF, external stores) — out of scope.
