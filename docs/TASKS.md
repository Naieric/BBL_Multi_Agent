# TASKS.md

Implementation plan approved on 2026-07-26.

**Ordering principle:** bottom-up by hard dependency (config → data → tool → prompts → state → agents → graph → entrypoint), then verification, then submission artifacts. Nothing needing a live API key sits before the code that uses it; nothing needing a working app (screenshots, README examples) sits before the app runs.

Decisions resolved before implementation:
- Knowledge base: fictional company internal FAQ — a reviewer can tell instantly that answers came from retrieval and not from model pretraining.
- Language: English throughout (KB, prompts, output, code, docs).
- Tests: minimal `pytest` covering pure functions only (chunking, cosine similarity) — no API key, no mocks, fast.
- Git: initialised and pushed on 2026-07-28, closing the Definition of Done item "repository ready for GitHub submission". `.env` is gitignored and has never been committed.
- App invocation: question as CLI argument, falling back to a single `input()` prompt. No interactive loop (would invite conversation memory, which is banned).
- Retrieval: real LLM tool-calling, single bounded turn. See `DECISIONS.md`.

---

## Phase 1 — Foundation (no API key needed)

- [x] **1. Package skeleton** — `src/__init__.py` plus `src/agents/`, `src/tools/`, `src/graph/`, `src/prompts/`, each with `__init__.py`.
- [x] **2. Dependencies and environment template** — `requirements.txt` (`langgraph`, `langchain`, `langchain-google-genai`, `python-dotenv`, `numpy`, `pytest`) and `.env.example` declaring `GOOGLE_API_KEY`. Verify a clean install succeeds. Pinned versions per `DECISIONS.md`.
- [x] **3. Author `knowledge_base.txt`** — repo root, blank-line-separated paragraphs, 15–30 of them, each self-contained enough to answer a question alone. Fictional company FAQ.
- [x] **4. Configuration and model factories** — `src/config.py`: load `.env`, expose API key, chat model ID, embedding model ID, `TOP_K`, KB path as module constants; plus two small factory functions returning the configured chat and embeddings clients. These two factories **are** the "swappable provider" requirement — nothing more.

## Phase 2 — Retrieval

- [x] **5. Knowledge base loader** — `src/tools/document_loader.py`: read file, split on blank lines, strip empties, clear error if missing. Pure, no LLM, no network. *(If this lands under ~10 lines, fold it into the retriever rather than preserving the split for its own sake.)*
- [x] **6. Retrieval tool** — `src/tools/retriever.py`: embed chunks, embed query, cosine similarity, return top-k. Exposed as a real LangChain `@tool` — the DoD requires the Retriever to *use a tool*, so the tool object must genuinely exist. **First task requiring a live API key.**

## Phase 3 — Agents and orchestration

- [x] **7. Prompts** — `src/prompts/`: one short deterministic system prompt per agent. Retriever: call the tool, return context only, never answer. Report: answer only from supplied context, say so plainly when context doesn't cover the question, never invent.
- [x] **8. Graph state** — `src/graph/state.py`: `TypedDict` with `question`, `context`, `answer`.
- [x] **9. Retriever Agent** — `src/agents/retriever_agent.py`: node taking `question`, invoking the tool-bound model, executing the tool call, writing `context`. Single turn, no loop. No prose output.
- [x] **10. Report Generator Agent** — `src/agents/report_generator_agent.py`: node taking `context`, writing `answer`. Handles empty context by saying the KB has no relevant information. **Must contain no import from `src/tools`** — that absent import is the enforceable form of the architectural boundary, and a reviewer will check for it.
- [x] **11. Sequential workflow** — `src/graph/workflow.py`: `StateGraph`, two nodes, `START → retriever → report_generator → END`, compiled by a small builder function.

## Phase 4 — Runnable application

- [x] **12. Entry point** — `main.py` at repo root. Thin: read question, invoke graph, print retrieved context then final answer. Printing the context makes the two-agent separation visible in screenshots for ~3 lines of cost.
- [x] **13. Error-handling pass** — one focused sweep for the four cases in `PROJECT_CONTEXT.md`: missing `knowledge_base.txt`, empty retrieval, missing/invalid API key, unexpected LLM response. Messages surfaced at the `main.py` boundary, non-zero exit on fatal errors.
- [x] **14. Minimal tests** — one `pytest` file covering chunking and cosine similarity. Pure functions only; no API key, no mocks.
- [x] **15. End-to-end verification** — clean install, real key, 3–5 sample questions including one deliberately not covered by the KB. Walk the Definition of Done item by item.

## Phase 5 — Submission artifacts

- [x] **16. README** — written, including a worked example from a real verified run. Full transcripts in `docs/example_run.md`.
- [x] **17. Example screenshots** — three captured from real runs into `docs/screenshots/` and embedded in the README. Rendered from genuine terminal output; no API key or personal path visible in any frame.

---

## Deliberately excluded (do not quietly reintroduce)

None of these earn a Definition-of-Done checkmark:

- Persisted/on-disk embedding cache or incremental re-indexing.
- `pydantic-settings` or a `Settings` class — plain module constants suffice for five values.
- An abstract `LLMProvider` base class, `Protocol`, or provider registry — two factory functions satisfy "swappable provider"; more is speculative generality.
- A custom exception hierarchy — built-in exceptions with clear messages, caught at the `main.py` boundary.
- Structured logging or a logging config module — plain prints in the entry point.
- Chunk overlap, token-aware splitting, recursive character splitters — paragraph splitting is the specified strategy.
- Reranking, hybrid/keyword fusion, query rewriting, MMR — explicitly excluded by `PROJECT_CONTEXT.md`.
- `typer`/`click` — `sys.argv` is enough for one argument.
- Pydantic models for graph state — `TypedDict` is idiomatic for LangGraph and smaller.
- Streaming output, retry/backoff wrappers, Docker, CI, pre-commit hooks, evaluation harnesses.
- A `src/utils.py` junk drawer — every helper here has an obvious owning module.

## Review findings resolved (independent review, 2026-07-26)

- **Provider errors were uncaught.** An invalid key produced a ~40-line traceback. `main.py` now catches provider/transport failures at the boundary. The Definition of Done names "invalid API key" explicitly; task 13 had claimed this was covered and it was not.
- **`temperature=0` was silently ignored.** `gemini-3.6-flash` uses fixed sampling, so the parameter was stripped and a `UserWarning` printed twice per run — into the very output the screenshots capture. Removed, and the ADR corrected. See `DECISIONS.md`.
- **The tool call was not forced.** With `tool_choice` at auto the model could skip retrieval, and the user would then be told the knowledge base lacked the answer when it had never been searched. Now `tool_choice="any"`.
- **The embedding cache never hit.** `main.py` answers one question and exits, so the module-level `_index` global could not pay for itself. Deleted, along with a provider-specific import it had leaked into `retriever.py`.
- **Smaller fixes:** `.text()` → `.text` (deprecated call form), `EOFError` guard on the interactive prompt, an early knowledge-base existence check so that failure costs nothing, and return type hints on the tests.

## Open risks

- **Embeddings recomputed every run.** Accepted: correct simple choice at this corpus size. Costs one API call and a second or two per run. Do not "fix" with a cache.
- ~~**Model ID drift.**~~ Retired: `gemini-3.6-flash` and `gemini-embedding-001` both resolved and answered correctly on live runs.
- ~~**API key required.**~~ Retired: key supplied, all LLM paths exercised.
