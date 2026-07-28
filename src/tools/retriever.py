"""Semantic retrieval tool over the local knowledge base."""

import numpy as np
from langchain.tools import tool

from src.config import KNOWLEDGE_BASE_PATH, TOP_K, build_embeddings
from src.tools.document_loader import load_chunks


def rank_by_similarity(query_vector: np.ndarray, chunk_vectors: np.ndarray) -> np.ndarray:
    """Rank chunks by cosine similarity to the query, most similar first.

    Args:
        query_vector: Embedding of the query, shape ``(dim,)``.
        chunk_vectors: Embeddings of the chunks, shape ``(n_chunks, dim)``.

    Returns:
        Chunk indices ordered by descending cosine similarity.
    """
    normalised_chunks = chunk_vectors / np.linalg.norm(chunk_vectors, axis=1, keepdims=True)
    normalised_query = query_vector / np.linalg.norm(query_vector)
    similarities = normalised_chunks @ normalised_query
    return np.argsort(similarities)[::-1]


@tool
def search_knowledge_base(query: str) -> str:
    """Search the Aurora Dynamics knowledge base for passages relevant to a question.

    Args:
        query: The question to search for.

    Returns:
        The most relevant passages, separated by blank lines.
    """
    embeddings = build_embeddings()
    chunks = load_chunks(KNOWLEDGE_BASE_PATH)
    chunk_vectors = np.array(embeddings.embed_documents(chunks))
    query_vector = np.array(embeddings.embed_query(query))
    ranked = rank_by_similarity(query_vector, chunk_vectors)
    return "\n\n".join(chunks[i] for i in ranked[:TOP_K])
