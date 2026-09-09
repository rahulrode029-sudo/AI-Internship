from typing import TypedDict, List


class ResearchState(TypedDict, total=False):

    user_query: str

    research_plan: List[str]

    research_results: str

    analysis: str

    critic_feedback: str

    revision_count: int

    final_answer: str

    workflow_status: str