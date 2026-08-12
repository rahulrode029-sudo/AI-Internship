
import os
import logging

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

from workflow import execute_workflow


# =========================================================
# LOAD ENVIRONMENT VARIABLES
# =========================================================

load_dotenv()

logger = logging.getLogger(__name__)


# =========================================================
# AGENT
# =========================================================

async def run_agent(question: str):

    try:

        # =================================================
        # CHECK API KEY
        # =================================================

        api_key = os.getenv("GOOGLE_API_KEY")

        if not api_key:
            raise ValueError(
                "GOOGLE_API_KEY is not configured in the .env file."
            )

        # =================================================
        # RUN AGENT WORKFLOW
        # =================================================

        logger.info(
            "Starting workflow for question: %s",
            question
        )

        workflow_result = await execute_workflow(
            question
        )

        logger.info(
            "Workflow completed successfully"
        )

        # =================================================
        # GET OBSERVATION
        # =================================================

        observation = workflow_result.get(
            "observation",
            ""
        )

        # =================================================
        # CREATE LLM
        # =================================================

        llm = ChatGoogleGenerativeAI(
            model="gemini-flash-latest",
            temperature=0,
            google_api_key=api_key
        )

        # =================================================
        # FINAL RESPONSE PROMPT
        # =================================================

        prompt = f"""
You are an AI Research Assistant.

User Question:
{question}

Information retrieved by the agent:
{observation}

Answer the user's question using the retrieved information.

Rules:

- Do not invent information.
- If information is unavailable, say so.
- Give a clear and concise answer.
"""

        # =================================================
        # CALL GEMINI
        # =================================================

        logger.info(
            "Calling Gemini model"
        )

        response = await llm.ainvoke(
            [
                HumanMessage(
                    content=prompt
                )
            ]
        )

        # =================================================
        # RETURN RESULT
        # =================================================

        return {
            "question": question,

            "plan": {
                "reason": workflow_result.get(
                    "reason",
                    ""
                ),

                "tool": workflow_result.get(
                    "tool",
                    ""
                ),

                "input": workflow_result.get(
                    "tool_input",
                    ""
                )
            },

            "observation": observation,

            "answer": response.content
        }

    except Exception as e:

        logger.exception(
            "Error while running AI agent"
        )

        raise
