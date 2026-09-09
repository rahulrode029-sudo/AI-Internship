from graph import graph
from memory import get_memory


print("=" * 60)
print("          MULTI-AGENT AI RESEARCH ASSISTANT")
print("=" * 60)

print("\nAgents:")
print("1. Coordinator Agent")
print("2. Research Agent")
print("3. Writer Agent")

print("\nType 'exit' or 'quit' to stop.")


while True:

    question = input("\nAsk Question: ")

    if question.lower() in ["exit", "quit"]:

        print("\nGoodbye!")
        break

    if not question.strip():

        print("Please enter a question.")
        continue

    try:

        result = graph.invoke({

            "question": question,

            "history": get_memory(),

            "communication_log": []

        })

        print("\n" + "=" * 60)
        print("AGENT COMMUNICATION LOG")
        print("=" * 60)

        for log in result.get(
            "communication_log",
            []
        ):

            print(f"→ {log}")

        print("\n" + "=" * 60)
        print("FINAL ANSWER")
        print("=" * 60)

        print(
            result.get(
                "answer",
                "No answer generated."
            )
        )

    except Exception as e:

        print("\nSystem Error:")
        print(str(e))