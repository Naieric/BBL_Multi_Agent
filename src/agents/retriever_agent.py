"""Retriever Agent: turns a question into retrieved context.

This agent retrieves and nothing else. It never answers the user, and it never
summarises what it retrieved.
"""

from langchain_core.messages import HumanMessage, SystemMessage

from src.config import build_chat_model
from src.graph.state import WorkflowState
from src.prompts.retriever import RETRIEVER_SYSTEM_PROMPT
from src.tools.retriever import search_knowledge_base


def retrieve(state: WorkflowState) -> dict[str, str]:
    """Invoke the retrieval tool for the user's question.

    The model takes a single turn and is required to call the tool, so retrieval
    always happens. There is no loop.

    Args:
        state: Workflow state containing the user's question.

    Returns:
        A state update containing the retrieved context.
    """
    model = build_chat_model().bind_tools([search_knowledge_base], tool_choice="any")
    response = model.invoke(
        [
            SystemMessage(content=RETRIEVER_SYSTEM_PROMPT),
            HumanMessage(content=state["question"]),
        ]
    )

    if not response.tool_calls:
        return {"context": ""}

    return {"context": search_knowledge_base.invoke(response.tool_calls[0]["args"])}
