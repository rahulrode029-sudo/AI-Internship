from typing import TypedDict


class AgentState(TypedDict, total=False):

    question: str

    documents: list[str]

    answer: str

    history: list[str]

    error: str