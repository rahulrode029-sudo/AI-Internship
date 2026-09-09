from .state import ResearchState
from .llm import llm


def writer(state: ResearchState):

    query = state["user_query"]
    analysis = state["analysis"]
    feedback = state["critic_feedback"]

    prompt = f"""
You are the Writer Agent.

User Query:
{query}

Approved Analysis:
{analysis}

Critic Feedback:
{feedback}

Write the final answer for the user.

Requirements:

- Answer the user's question directly.
- Use clear headings where useful.
- Use bullet points when appropriate.
- Be accurate and easy to understand.
- Do not mention the internal AI agents.
- Do not mention the workflow.
- Do not mention the critic.
- Do not invent facts.

Return only the final answer.
"""

    response = llm.invoke(prompt)

    return {
        "final_answer": response.content,
        "workflow_status": "Final answer generated"
    }