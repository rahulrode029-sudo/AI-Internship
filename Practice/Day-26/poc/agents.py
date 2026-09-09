import os

from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage


load_dotenv()


API_KEY = os.getenv("GOOGLE_API_KEY")

MODEL_NAME = os.getenv(
    "MODEL_NAME",
    "gemini-2.5-flash"
)


if not API_KEY:
    raise RuntimeError(
        "GOOGLE_API_KEY is missing. "
        "Please add it to your .env file."
    )


llm = ChatGoogleGenerativeAI(
    model=MODEL_NAME,
    google_api_key=API_KEY,
    temperature=0.2
)


def call_llm(prompt: str) -> str:

    response = llm.invoke(
        [
            HumanMessage(
                content=prompt
            )
        ]
    )

    return response.content


# ============================================================
# COORDINATOR AGENT
# ============================================================

def coordinator_agent(question: str) -> str:

    prompt = f"""
You are the Coordinator Agent in a multi-agent AI system.

User Question:
{question}

Your responsibility is to create a simple execution plan.

The plan should contain:

1. Research the question.
2. Analyze the information.
3. Prepare a final answer.

Do NOT answer the user's question yet.

Only create the execution plan.
"""

    return call_llm(prompt)


# ============================================================
# RESEARCH AGENT
# ============================================================

def research_agent(
    question: str,
    plan: str
) -> str:

    prompt = f"""
You are the Research Agent.

User Question:
{question}

Coordinator Plan:
{plan}

Your task is to provide useful factual background
for answering the user's question.

Responsible AI requirements:

- Do not invent facts.
- Do not create fake sources.
- Clearly mention uncertainty.
- Do not expose private information.
- Do not present guesses as facts.

Provide concise research information.
"""

    return call_llm(prompt)


# ============================================================
# ANALYSIS AGENT
# ============================================================

def analysis_agent(
    question: str,
    research: str
) -> str:

    prompt = f"""
You are the Analysis Agent.

User Question:
{question}

Research Information:
{research}

Analyze the research.

Your responsibilities:

1. Identify the important information.
2. Identify possible assumptions.
3. Identify uncertain information.
4. Identify possible hallucinations.
5. Prepare useful conclusions.

Do not introduce unsupported facts.
"""

    return call_llm(prompt)


# ============================================================
# WRITER AGENT
# ============================================================

def writer_agent(
    question: str,
    analysis: str
) -> str:

    prompt = f"""
You are the Writer Agent.

User Question:
{question}

Analysis:
{analysis}

Write the final response for the user.

Requirements:

- Answer the question directly.
- Use clear language.
- Do not invent information.
- Do not create fake citations.
- Mention uncertainty when necessary.
- Do not present speculation as fact.
- Keep the response concise and useful.
"""

    return call_llm(prompt)