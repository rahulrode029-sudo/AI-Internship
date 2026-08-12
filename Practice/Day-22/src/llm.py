import os
from pathlib import Path

from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI


BASE_DIR = Path(__file__).resolve().parent.parent

env_file = BASE_DIR / ".env"
load_dotenv(env_file)

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError(
        f"GOOGLE_API_KEY not found.\n"
        f"Please check your .env file at:\n{env_file}"
    )


llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    temperature=0.2,
    max_retries=5
)


def get_text(response):
    """
    Convert Gemini/LangChain response content
    into a normal Python string.
    """

    content = response.content

    if isinstance(content, str):
        return content

    if isinstance(content, list):

        text_parts = []

        for item in content:

            if isinstance(item, dict):

                if "text" in item:
                    text_parts.append(str(item["text"]))

            else:
                text_parts.append(str(item))

        return "\n".join(text_parts)

    return str(content)