from .state import ResearchState
from .llm import llm, get_text


def critic(state: ResearchState):

    query = state["user_query"]
    analysis = state["analysis"]

    prompt = f"""
You are the Critic Agent in a multi-agent research system.

User Query:
{query}

Analysis:
{analysis}

Evaluate the analysis carefully.

Check:

1. Relevance
2. Logical consistency
3. Completeness
4. Possible factual problems
5. Missing information
6. Unsupported claims
7. Overall quality

At the end, provide exactly one decision:

DECISION: APPROVE

or

DECISION: REVISE

If revision is required, clearly explain what must be improved.

Keep your response concise.
"""

    response = llm.invoke(prompt)

    # Convert Gemini response into a string
    feedback = get_text(response)

    # Extra safety: guarantee that feedback is a string
    if not isinstance(feedback, str):
        feedback = str(feedback)

    return {
        "critic_feedback": feedback,
        "workflow_status": "Analysis reviewed"
    }