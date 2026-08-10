import os

from dotenv import load_dotenv
from google import genai

from tools.calculator import calculator
from tools.web_search import web_search
from tools.database_tool import database_query
from tools.file_reader import read_file
from tools.weather_tool import get_weather
from tools.email_tool import send_email
from tools.date_tool import date_tool
from tools.data_analyzer import analyze_data
from project_tool.pdf_reader_tool import company_pdf_reader


load_dotenv()


API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise ValueError(
        "GEMINI_API_KEY is missing. "
        "Add it to your .env file."
    )


client = genai.Client(
    api_key=API_KEY
)


SYSTEM_INSTRUCTION = """
You are a company AI assistant.

You have access to several tools.

Choose a tool whenever the user's request requires
calculation, web information, database information,
file information, weather information, email processing,
date operations, data analysis, or company PDF information.

Available tools:

1. calculator
2. web_search
3. database_query
4. read_file
5. get_weather
6. send_email
7. date_tool
8. analyze_data
9. company_pdf_reader

Important rules:

- Use calculator for mathematical calculations.
- Use web_search for current web information.
- Use database_query for company employee database questions.
- Use read_file for reading text, CSV or PDF files.
- Use get_weather for weather requests.
- Use send_email for email requests.
- Use date_tool for date calculations.
- Use analyze_data for CSV analysis.
- Use company_pdf_reader for company PDF documents.

You may call multiple tools when necessary.

For example:
If the user asks for the average salary of IT employees,
first use the database tool to retrieve the data and
then use calculation logic if necessary.

Always explain the final answer clearly.

If a tool returns an error, explain the error instead
of inventing information.
"""


TOOLS = [
    calculator,
    web_search,
    database_query,
    read_file,
    get_weather,
    send_email,
    date_tool,
    analyze_data,
    company_pdf_reader,
]


def ask_agent(user_question: str) -> str:

    try:

        response = client.models.generate_content(
            model="models/gemini-3.5-flash",
            contents=user_question,
            config={
                "system_instruction": SYSTEM_INSTRUCTION,
                "tools": TOOLS,
                "temperature": 0.2,
            },
        )

        return response.text

    except Exception as e:
        return f"Agent error: {e}"


def main():

    print("=" * 70)
    print("AI TOOL-CALLING ASSISTANT")
    print("=" * 70)

    print("\nAvailable tools:")
    print("1. Calculator")
    print("2. Web Search")
    print("3. Database")
    print("4. File Reader")
    print("5. Weather")
    print("6. Email")
    print("7. Date")
    print("8. Data Analyzer")
    print("9. Company PDF Reader")

    print("\nType 'exit' to stop.")

    while True:

        question = input("\nYou: ").strip()

        if question.lower() == "exit":
            print("Goodbye!")
            break

        if not question:
            print("Please enter a question.")
            continue

        print("\nAI is processing...\n")

        answer = ask_agent(question)

        print("AI:", answer)


if __name__ == "__main__":
    main()