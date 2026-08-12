from langgraph.graph import StateGraph, START, END

from state import AgentState
from agents.coordinator import coordinator_agent
from agents.researcher import research_agent
from agents.writer import writer_agent
from memory import save_memory


# ============================================================
# COORDINATOR NODE
# ============================================================

def coordinator_node(state):

    try:

        result = coordinator_agent(state)

        return result

    except Exception as e:

        return {
            "error": f"Coordinator Agent error: {str(e)}",
            "communication_log": [
                f"Coordinator Agent failed: {str(e)}"
            ]
        }


# ============================================================
# RESEARCH NODE
# ============================================================

def researcher_node(state):

    try:

        result = research_agent(state)

        return result

    except Exception as e:

        return {
            "error": f"Research Agent error: {str(e)}",
            "communication_log": [
                f"Research Agent failed: {str(e)}"
            ]
        }


# ============================================================
# WRITER NODE
# ============================================================

def writer_node(state):

    try:

        result = writer_agent(state)

        return result

    except Exception as e:

        return {
            "error": f"Writer Agent error: {str(e)}",
            "communication_log": [
                f"Writer Agent failed: {str(e)}"
            ]
        }


# ============================================================
# MEMORY NODE
# ============================================================

def memory_node(state):

    save_memory(
        state["question"],
        state.get("answer", "")
    )

    return {
        "communication_log": [
            "Conversation saved to memory."
        ]
    }


# ============================================================
# ERROR NODE
# ============================================================

def error_node(state):

    error_message = state.get(
        "error",
        "Unknown error occurred."
    )

    return {
        "answer": (
            "Sorry, I could not complete the request.\n\n"
            f"Reason: {error_message}"
        ),
        "communication_log": [
            f"Workflow stopped because of an error: {error_message}"
        ]
    }


# ============================================================
# ROUTING FUNCTIONS
# ============================================================

def check_coordinator(state):

    if state.get("error"):
        return "error"

    if not state.get("coordinator_plan"):
        return "error"

    return "research"


def check_research(state):

    if state.get("error"):
        return "error"

    if not state.get("research"):
        return "error"

    return "writer"


def check_writer(state):

    if state.get("error"):
        return "error"

    if not state.get("answer"):
        return "error"

    return "memory"


# ============================================================
# CREATE LANGGRAPH
# ============================================================

builder = StateGraph(AgentState)


# Add agent nodes
builder.add_node(
    "coordinator",
    coordinator_node
)

builder.add_node(
    "researcher",
    researcher_node
)

builder.add_node(
    "writer",
    writer_node
)

builder.add_node(
    "memory",
    memory_node
)

builder.add_node(
    "error",
    error_node
)


# ============================================================
# WORKFLOW
# ============================================================

# START → COORDINATOR
builder.add_edge(
    START,
    "coordinator"
)


# COORDINATOR → RESEARCHER / ERROR
builder.add_conditional_edges(
    "coordinator",
    check_coordinator,
    {
        "research": "researcher",
        "error": "error"
    }
)


# RESEARCHER → WRITER / ERROR
builder.add_conditional_edges(
    "researcher",
    check_research,
    {
        "writer": "writer",
        "error": "error"
    }
)


# WRITER → MEMORY / ERROR
builder.add_conditional_edges(
    "writer",
    check_writer,
    {
        "memory": "memory",
        "error": "error"
    }
)


# MEMORY → END
builder.add_edge(
    "memory",
    END
)


# ERROR → END
builder.add_edge(
    "error",
    END
)


# Compile
graph = builder.compile()