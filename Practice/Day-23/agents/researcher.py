from retriever import retriever
from llm import llm


def research_agent(state):

    question = state["question"]

    plan = state.get(
        "coordinator_plan",
        ""
    )

    # Retrieve relevant documents
    results = retriever.invoke(question)

    documents = [
        doc.page_content
        for doc in results
    ]

    if not documents:
        raise ValueError(
            "No relevant documents were found."
        )

    context = "\n\n".join(documents)

    prompt = f"""
You are the Research Agent in a multi-agent AI system.

Your job is to analyze the provided company documents
and extract the information needed to answer the user's question.

Coordinator's Research Plan:
{plan}

User Question:
{question}

Retrieved Documents:
{context}

Do not create a polished final answer.

Instead, provide factual research findings that
the Writer Agent can use.

Research Findings:
"""

    response = llm.invoke(prompt)

    research = response.content

    return {
        "documents": documents,
        "research": research,
        "communication_log": [
            f"Research Agent received the Coordinator's plan.",
            f"Research Agent retrieved {len(documents)} document chunks.",
            f"Research Agent completed the research."
        ]
    }