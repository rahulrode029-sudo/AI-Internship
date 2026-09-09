from llm import llm


def coordinator_agent(state):

    question = state["question"]

    history = state.get("history", [])

    conversation = "\n".join(history)

    prompt = f"""
You are the Coordinator Agent in a multi-agent AI research system.

Your responsibility is to analyze the user's question and create
a clear research plan for the Research Agent.

Do not answer the user's question directly.

Determine:
1. What information needs to be found?
2. What should the Research Agent look for?
3. What should the Writer Agent focus on?

Previous conversation:
{conversation}

User Question:
{question}

Provide a short and clear research plan.
"""

    response = llm.invoke(prompt)

    plan = response.content

    return {
        "coordinator_plan": plan,
        "communication_log": [
            f"Coordinator Agent received the question: {question}",
            f"Coordinator Agent created the research plan: {plan}"
        ]
    }