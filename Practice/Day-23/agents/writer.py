from llm import llm, extract_text


def writer_agent(state):

    question = state["question"]

    research = state.get(
        "research",
        ""
    )

    history = state.get(
        "history",
        []
    )

    conversation = "\n".join(history)

    # ==========================================
    # WRITER PROMPT
    # ==========================================

    prompt = f"""
You are the Writer Agent in a multi-agent AI system.

Your responsibility is to create the final answer
using the research provided by the Research Agent.

Do not invent information.

If the research does not contain enough information,
clearly say that the answer could not be found
in the provided company documents.

Previous Conversation:
{conversation}

User Question:
{question}

Research from Research Agent:
{research}

Write a clear, accurate and concise final answer.

Final Answer:
"""

    response = llm.invoke(prompt)

    # Convert Gemini response into a normal string
    answer = extract_text(response)

    if not answer.strip():
        raise ValueError(
            "Writer Agent generated an empty answer."
        )

    return {
        "answer": answer,
        "communication_log": [
            "Writer Agent received the Research Agent's findings.",
            "Writer Agent generated the final answer."
        ]
    }