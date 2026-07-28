"""Application configuration and model factories.

This module is the single place where model identifiers, retrieval settings, and
credentials are resolved. Swapping to a different LLM provider means changing
only the two factory functions below.
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings

load_dotenv()

KNOWLEDGE_BASE_PATH = Path(__file__).resolve().parent.parent / "knowledge_base.txt"

CHAT_MODEL = "gemini-3.6-flash"
EMBEDDING_MODEL = "gemini-embedding-001"

# Number of knowledge base chunks the retriever returns per question.
TOP_K = 3

_MISSING_KEY_MESSAGE = (
    "GOOGLE_API_KEY is not set. Copy .env.example to .env and add your key "
    "from https://aistudio.google.com/apikey."
)


def _require_api_key() -> None:
    """Fail early with a readable message if the API key is absent.

    The LangChain clients read ``GOOGLE_API_KEY`` from the environment
    themselves; this only turns a confusing downstream error into a clear one.

    Raises:
        RuntimeError: If ``GOOGLE_API_KEY`` is not set.
    """
    if not os.getenv("GOOGLE_API_KEY"):
        raise RuntimeError(_MISSING_KEY_MESSAGE)


def build_chat_model() -> ChatGoogleGenerativeAI:
    """Create the chat model used by both agents.

    Returns:
        A Gemini chat client.
    """
    _require_api_key()
    # No sampling parameters: gemini-3.6-flash uses fixed sampling defaults and
    # ignores temperature. Grounding is enforced by the prompts instead.
    return ChatGoogleGenerativeAI(model=CHAT_MODEL)


def build_embeddings() -> GoogleGenerativeAIEmbeddings:
    """Create the embeddings client used by the retrieval tool.

    Returns:
        A Gemini embeddings client.
    """
    _require_api_key()
    return GoogleGenerativeAIEmbeddings(model=EMBEDDING_MODEL)
