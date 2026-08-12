from typing import TypedDict


class AgentState(TypedDict, total=False):

    # User input
    question: str

    # Conversation memory
    history: list[str]

    # Coordinator output
    coordinator_plan: str

    # Research Agent output
    documents: list[str]
    research: str

    # Writer Agent output
    answer: str

    # Error handling
    error: str

    # Communication log
    communication_log: list[str]