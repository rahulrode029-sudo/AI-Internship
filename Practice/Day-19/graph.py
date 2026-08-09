from langgraph.graph import StateGraph, START, END

from state import AgentState
from retriever import retrieve_documents
from llm import generate_answer
from memory import save_memory


def retrieve_node(state):
    try:
        return retrieve_documents(state)

    except Exception as e:
        return {
            "documents": [],
            "error": f"Retriever error: {str(e)}"
        }


def generate_node(state):
    try:
        return generate_answer(state)

    except Exception as e:
        return {
            "answer": "",
            "error": f"LLM error: {str(e)}"
        }


def memory_node(state):
    save_memory(
        state["question"],
        state.get("answer", "")
    )

    return {}


def check_retrieval(state):

    if state.get("error"):
        return "error"

    if not state.get("documents"):
        return "error"

    return "generate"


def check_generation(state):

    if state.get("error"):
        return "error"

    if not state.get("answer"):
        return "error"

    return "memory"


def error_node(state):

    error_message = state.get(
        "error",
        "Unknown error occurred."
    )

    return {
        "answer": (
            "Sorry, I could not complete the request.\n\n"
            f"Reason: {error_message}"
        )
    }


# Create graph
builder = StateGraph(AgentState)


# Add nodes
builder.add_node("retrieve", retrieve_node)
builder.add_node("generate", generate_node)
builder.add_node("memory", memory_node)
builder.add_node("error", error_node)


# Start → Retriever
builder.add_edge(START, "retrieve")


# Conditional routing after retrieval
builder.add_conditional_edges(
    "retrieve",
    check_retrieval,
    {
        "generate": "generate",
        "error": "error"
    }
)


# Conditional routing after generation
builder.add_conditional_edges(
    "generate",
    check_generation,
    {
        "memory": "memory",
        "error": "error"
    }
)


# Memory → End
builder.add_edge("memory", END)

# Error → End
builder.add_edge("error", END)


# Compile
graph = builder.compile()