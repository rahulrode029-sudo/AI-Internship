import os

from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI

from planner import create_plan
from tools import document_search, calculator


load_dotenv()


llm = ChatGoogleGenerativeAI(
    model="models/gemini-3.5-flash",
    temperature=0
)

def run_agent(query):

    print("\n--- Agent Planning ---")

    plan = create_plan(query)

    for step in plan:
        print(step)


    context = ""


    if "company" in query.lower() or "policy" in query.lower():

        context = document_search(query)


    elif any(char.isdigit() for char in query):

        context = calculator(query)



    prompt = f"""

You are an AI Research Assistant.

User Question:
{query}


Available Information:
{context}


Provide a clear answer.

"""


    response = llm.invoke(prompt)


    return response.content