"""Shared state passed between workflow nodes."""

from typing import TypedDict


class WorkflowState(TypedDict):
    """State carried through the sequential workflow.

    Attributes:
        question: The user's original question.
        context: Passages retrieved from the knowledge base.
        answer: The final answer produced by the Report Generator Agent.
    """

    question: str
    context: str
    answer: str
