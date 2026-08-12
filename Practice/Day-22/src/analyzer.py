from .state import ResearchState
from .llm import llm


def analyzer(state: ResearchState):

    query = state["user_query"]
    research = state["research_results"]
    feedback = state.get("critic_feedback", "")

    prompt = f"""
You are the Analyzer Agent.

User Query:
{query}

Research Results:
{research}

Previous Critic Feedback:
{feedback}

Analyze and organize the research.

Your analysis must:

1. Identify the most important information.
2. Remove irrelevant information.
3. Organize the information logically.
4. Identify important advantages and disadvantages.
5. Identify possible contradictions or unsupported claims.
6. Improve the analysis based on the critic feedback if available.

Do NOT write the final user response.

Return a structured analysis for the Critic Agent.
"""

    response = llm.invoke(prompt)

    revision_count = state.get("revision_count", 0)

    return {
        "analysis": response.content,
        "revision_count": revision_count + 1,
        "workflow_status": "Analysis completed"
    }