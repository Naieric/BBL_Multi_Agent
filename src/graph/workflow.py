"""Sequential LangGraph workflow wiring the two agents together."""

from langgraph.graph import END, START, StateGraph
from langgraph.graph.state import CompiledStateGraph

from src.agents.report_generator_agent import generate_report
from src.agents.retriever_agent import retrieve
from src.graph.state import WorkflowState


def build_workflow() -> CompiledStateGraph:
    """Build the compiled question-answering workflow.

    The graph is strictly linear: retrieve, then report.

    Returns:
        The compiled graph, ready to invoke.
    """
    graph = StateGraph(WorkflowState)
    graph.add_node("retriever", retrieve)
    graph.add_node("report_generator", generate_report)

    graph.add_edge(START, "retriever")
    graph.add_edge("retriever", "report_generator")
    graph.add_edge("report_generator", END)

    return graph.compile()
