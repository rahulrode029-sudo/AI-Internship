from langgraph.graph import StateGraph, START, END

from .state import ResearchState
from .coordinator import coordinator
from .researcher import researcher
from .analyzer import analyzer
from .critic import critic
from .writer import writer


def critic_router(state: ResearchState):

    feedback = state.get("critic_feedback", "")

    # Make absolutely sure feedback is a string
    if isinstance(feedback, list):

        text_parts = []

        for item in feedback:

            if isinstance(item, dict):

                if "text" in item:
                    text_parts.append(str(item["text"]))

            else:
                text_parts.append(str(item))

        feedback = "\n".join(text_parts)

    elif not isinstance(feedback, str):

        feedback = str(feedback)

    feedback_upper = feedback.upper()

    revision_count = state.get("revision_count", 0)

    # Critic approved the analysis
    if "DECISION: APPROVE" in feedback_upper:
        return "writer"

    # Prevent infinite revision loop
    if revision_count >= 3:
        return "writer"

    # Critic wants revision
    return "analyzer"


def build_graph():

    workflow = StateGraph(ResearchState)

    # Add agents
    workflow.add_node("coordinator", coordinator)
    workflow.add_node("researcher", researcher)
    workflow.add_node("analyzer", analyzer)
    workflow.add_node("critic", critic)
    workflow.add_node("writer", writer)

    # Start
    workflow.add_edge(START, "coordinator")

    # Coordinator → Researcher
    workflow.add_edge("coordinator", "researcher")

    # Researcher → Analyzer
    workflow.add_edge("researcher", "analyzer")

    # Analyzer → Critic
    workflow.add_edge("analyzer", "critic")

    # Critic → Writer OR Analyzer
    workflow.add_conditional_edges(
        "critic",
        critic_router,
        {
            "writer": "writer",
            "analyzer": "analyzer"
        }
    )

    # Writer → End
    workflow.add_edge("writer", END)

    return workflow.compile()