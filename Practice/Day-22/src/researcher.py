from .state import ResearchState
from .llm import llm


def researcher(state: ResearchState):

    query = state["user_query"]
    plan = state["research_plan"]

    prompt = f"""
You are the Research Agent in a multi-agent AI research system.

User Query:
{query}

Research Plan:
{plan}

Your job is to collect useful and factual information
related to the user's question.

Provide:
1. Important facts
2. Key concepts
3. Examples
4. Advantages or benefits
5. Challenges or limitations
6. Relevant context

Do not write the final answer.

Return detailed research notes for the Analyzer.
"""

    response = llm.invoke(prompt)

    return {
        "research_results": response.content,
        "workflow_status": "Research completed"
    }