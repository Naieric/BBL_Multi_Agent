"""Report Generator Agent: turns retrieved context into a final answer.

This agent summarises and nothing else. It has no access to the knowledge base
or to any retrieval logic — note the absence of any import from ``src.tools``.
"""

from langchain_core.messages import HumanMessage, SystemMessage

from src.config import build_chat_model
from src.graph.state import WorkflowState
from src.prompts.report_generator import REPORT_GENERATOR_SYSTEM_PROMPT

NO_CONTEXT_ANSWER = "No context was retrieved for this question."


def generate_report(state: WorkflowState) -> dict[str, str]:
    """Answer the question using only the retrieved context.

    Args:
        state: Workflow state containing the question and retrieved context.

    Returns:
        A state update containing the final answer.
    """
    context = state["context"].strip()
    if not context:
        return {"answer": NO_CONTEXT_ANSWER}

    response = build_chat_model().invoke(
        [
            SystemMessage(content=REPORT_GENERATOR_SYSTEM_PROMPT),
            HumanMessage(
                content=f"Context:\n{context}\n\nQuestion: {state['question']}"
            ),
        ]
    )

    answer = response.text.strip()
    return {"answer": answer or NO_CONTEXT_ANSWER}
