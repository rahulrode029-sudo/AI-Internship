import os
import json

from dotenv import load_dotenv

from langchain_google_genai import (
    ChatGoogleGenerativeAI
)


# =========================================================
# ENVIRONMENT
# =========================================================

load_dotenv()

API_KEY = os.getenv(
    "GOOGLE_API_KEY"
)

if not API_KEY:

    raise ValueError(
        "GOOGLE_API_KEY was not found in .env"
    )


# =========================================================
# GEMINI
# =========================================================

llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    temperature=0,
    google_api_key=API_KEY
)


# =========================================================
# ASYNC PLANNER
# =========================================================

async def create_plan(question: str):

    prompt = f"""
You are an AI Agent Planner.

Your job is to decide which tool should be used
to answer the user's question.

Available tools:

1. search_company_documents
2. read_company_file
3. calculate
4. list_documents

User Question:

{question}

Return ONLY valid JSON.

Format:

{{
    "reason": "short explanation",
    "tool": "tool name",
    "tool_input": "input for the tool"
}}

Rules:

- Select only one tool.
- Do not invent tools.
- Mathematical questions -> calculate
- Company information -> search_company_documents
- Specific filename -> read_company_file
- Document listing -> list_documents
"""

    response = await llm.ainvoke(prompt)

    content = response.content

    if isinstance(content, list):

        content = "".join(
            str(item)
            for item in content
        )

    content = str(content).strip()

    if content.startswith("```"):

        content = content.replace(
            "```json",
            ""
        )

        content = content.replace(
            "```",
            ""
        )

        content = content.strip()

    try:

        return json.loads(content)

    except json.JSONDecodeError:

        return {
            "reason":
                "Planner returned invalid JSON.",

            "tool":
                "search_company_documents",

            "tool_input":
                question
        }