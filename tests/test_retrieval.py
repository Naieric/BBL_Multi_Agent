"""Tests for the pure parts of retrieval: chunking and similarity ranking.

These cover the logic that does not depend on the LLM, so they run without an
API key and without network access.
"""

import numpy as np

from src.tools.document_loader import split_into_chunks
from src.tools.retriever import rank_by_similarity


def test_split_into_chunks_separates_on_blank_lines() -> None:
    assert split_into_chunks("first para\n\nsecond para") == ["first para", "second para"]


def test_split_into_chunks_ignores_extra_blank_lines_and_whitespace() -> None:
    assert split_into_chunks("\n\n  first  \n\n\n\n second \n\n") == ["first", "second"]


def test_split_into_chunks_returns_empty_list_for_blank_text() -> None:
    assert split_into_chunks("   \n\n  \n") == []


def test_rank_by_similarity_orders_most_similar_first() -> None:
    chunk_vectors = np.array([[0.0, 1.0], [1.0, 0.0], [0.7, 0.7]])
    query_vector = np.array([1.0, 0.0])

    ranked = rank_by_similarity(query_vector, chunk_vectors)

    assert list(ranked) == [1, 2, 0]


def test_rank_by_similarity_ignores_vector_magnitude() -> None:
    chunk_vectors = np.array([[0.0, 5.0], [0.1, 0.0]])
    query_vector = np.array([9.0, 0.0])

    ranked = rank_by_similarity(query_vector, chunk_vectors)

    assert ranked[0] == 1
