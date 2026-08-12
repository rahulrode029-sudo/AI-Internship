from .state import ResearchState
from .llm import llm


def coordinator(state: ResearchState):

    query = state["user_query"]

    prompt = f"""
You are the Coordinator of a multi-agent research system.

User Query:
{query}

Create a clear research plan for the other AI agents.

The plan should contain 3 to 5 specific research steps.

Return ONLY the numbered research plan.
"""

    response = llm.invoke(prompt)

    # LangChain/Gemini may return content as either
    # a string or a list of content blocks.
    if isinstance(response.content, list):
        plan_text = "\n".join(
            str(item.get("text", item))
            if isinstance(item, dict)
            else str(item)
            for item in response.content
        )
    else:
        plan_text = str(response.content)

    plan = [
        line.strip()
        for line in plan_text.splitlines()
        if line.strip()
    ]

    return {
        "research_plan": plan,
        "workflow_status": "Research plan created"
    }