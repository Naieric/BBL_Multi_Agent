# PROJECT_CONTEXT.md

# AI Engineer Programming Test — Project Context

## Purpose

This document defines the overall project context for this repository.

Every future implementation, architectural decision, and code modification must follow this document unless the assignment requirements explicitly state otherwise.

This file acts as the primary source of truth for the project.

---

# Project Goal

Build a simple Agentic AI application that demonstrates an understanding of:

* Agent-based system design
* Retrieval-Augmented Generation (RAG)
* Tool usage
* Agent orchestration
* Clean software architecture

The objective is **NOT** to build a production-grade RAG system.

The objective is to produce a clean, understandable, maintainable implementation that satisfies the programming assignment.

---

# Assignment Scope

The assignment requires a minimal Agentic AI workflow.

The system must contain exactly two agents.

## Agent 1

Data Retriever Agent

Responsibilities

* Receive the user's question.
* Invoke a retrieval tool.
* Search information inside `knowledge_base.txt`.
* Return only the relevant retrieved context.
* Never answer the user directly.

This agent is responsible only for retrieval.

---

## Agent 2

Report Generator Agent

Responsibilities

* Receive retrieved context.
* Generate a concise response using only the retrieved information.
* Never invent information.
* Never retrieve documents directly.

This agent is responsible only for report generation.

---

# Overall Workflow

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

The workflow is intentionally simple.

No loops.

No reflection.

No planning agent.

No reviewer agent inside the application.

No autonomous decision making.

---

# Framework Choice

This project uses:

* LangGraph
* LangChain

Reasoning

LangGraph clearly demonstrates agent orchestration while remaining simple enough for the assignment.

The workflow consists of sequential nodes.

No complex graph logic is required.

---

# LLM

Gemini (Google AI)

Reason

* Easy API access
* Good LangChain integration
* Reliable tool calling
* Cost effective

The implementation should abstract the model so another provider can be swapped later if needed.

---

# Retrieval Strategy

This project intentionally uses embedding-based semantic retrieval.

Reason

Although the assignment accepts keyword search, embedding retrieval better demonstrates practical RAG knowledge while remaining lightweight.

Implementation principles

* Split the knowledge base into paragraph chunks.
* Generate embeddings.
* Compute semantic similarity.
* Return only the top relevant chunks.
* Do not perform reranking.
* Do not implement hybrid search.

Keep retrieval simple.

---

# Knowledge Base

The knowledge source is

knowledge_base.txt

Only this file is used.

No PDFs.

No Vector Database.

No ChromaDB.

No Pinecone.

No FAISS.

No Elasticsearch.

No external storage.

The assignment explicitly asks for a simple local knowledge base.

---

# Architecture Principles

The project should prioritize

* Simplicity
* Readability
* Maintainability

Avoid unnecessary abstraction.

Avoid premature optimization.

Avoid enterprise patterns.

The repository should be understandable within a few minutes by an interviewer.

---

# Coding Principles

Python version

3.10+

Guidelines

* Type hints
* Small functions
* Clear naming
* Single Responsibility Principle
* Minimal dependencies
* Meaningful comments only
* Google-style docstrings

Every module should have one clear responsibility.

---

# Folder Responsibilities

src/

Contains all production code.

agents/

Contains Agent implementations.

tools/

Contains retrieval tools.

graph/

Contains LangGraph workflow.

prompts/

Contains prompts used by agents.

No business logic should exist outside src.

---

# Agent Responsibilities

Retriever Agent

May

* call retrieval tool

May NOT

* summarize
* answer user
* generate reports

Report Generator

May

* summarize retrieved context

May NOT

* search documents
* call retrieval logic

---

# Prompt Philosophy

Prompts should be

* short
* explicit
* deterministic

Avoid unnecessary prompt engineering.

The assignment evaluates engineering, not prompt complexity.

---

# Error Handling

Gracefully handle

* empty retrieval
* missing files
* invalid API key
* unexpected LLM responses

Return meaningful error messages.

Never crash unnecessarily.

---

# Definition of Done

The project is complete when

✓ The system runs successfully.

✓ Two agents are implemented.

✓ The Retriever uses a tool.

✓ The Report Generator does not retrieve documents.

✓ Sequential LangGraph workflow works correctly.

✓ knowledge_base.txt is used.

✓ README explains setup and execution.

✓ requirements.txt is complete.

✓ Example screenshots are prepared.

✓ Repository is ready for GitHub submission.

---

# Engineering Philosophy

This repository is an interview assignment.

The goal is not to impress reviewers with complexity.

The goal is to demonstrate engineering judgment.

Whenever there are multiple valid implementations,

prefer the simplest solution that completely satisfies the assignment.

If a feature is not required,

do not implement it.

If an abstraction is unnecessary,

remove it.

Readable code is more valuable than clever code.

The reviewer should understand the entire architecture quickly without additional explanation.

This principle should guide every future decision made in this repository.
