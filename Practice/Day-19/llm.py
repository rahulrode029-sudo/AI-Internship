import os
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI

load_dotenv()

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError(
        "GOOGLE_API_KEY not found in .env file."
    )

llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    google_api_key=api_key,
    temperature=0.2
)


def generate_answer(state):

    question = state["question"]
    documents = state.get("documents", [])
    history = state.get("history", [])

    context = "\n\n".join(documents)

    conversation = "\n".join(history)

    prompt = f"""
You are a helpful AI research assistant.

Answer the user's question using the provided documents.

If the answer is not available in the documents, say:
"I could not find the answer in the provided documents."

Previous conversation:
{conversation}

Documents:
{context}

User Question:
{question}

Answer:
"""

    response = llm.invoke(prompt)

    return {
        "answer": response.content
    }