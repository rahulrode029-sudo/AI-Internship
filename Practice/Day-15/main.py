import os
from dotenv import load_dotenv

from langchain_google_genai import ChatGoogleGenerativeAI

from prompts import support_prompt
from output_parser import parser
from memory import get_memory


# Load environment variables from .env
load_dotenv()

# Get Gemini API Key
api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    raise ValueError(
        "GOOGLE_API_KEY not found. Create a .env file (see .env.example) "
        "and add your key from https://aistudio.google.com/apikey"
    )

# Create Memory
memory = get_memory()

# Gemini Model
llm = ChatGoogleGenerativeAI(
    model="gemini-flash-latest",
    google_api_key=api_key,
    temperature=0.7,
)

# Build the Sequential Chain: Prompt -> LLM -> Output Parser
chain = support_prompt | llm | parser


print("=" * 50)
print("AI SUPPORT ASSISTANT (Gemini)")
print("=" * 50)

while True:
    user_query = input("\nEnter your query (type exit to quit): ")

    if user_query.lower() == "exit":
        print("Goodbye!")
        break

    try:
        # Load prior conversation as plain text for the prompt
        history = memory.load_memory_variables({}).get("chat_history", "")

        result = chain.invoke(
            {
                "query": user_query,
                "chat_history": history,
            }
        )

        # Save this turn into memory AFTER getting the result
        memory.save_context(
            {"input": user_query},
            {"output": str(result)},
        )

        print("\nStructured Response")
        print("-" * 50)
        print(result)

        print("\nConversation History")
        print("-" * 50)
        print(memory.load_memory_variables({}))

    except Exception as e:
        print("\nError:")
        print(e)