from graph import graph
from memory import get_memory


print("=" * 50)
print("       Day-19 LangGraph RAG Assistant")
print("=" * 50)

while True:

    question = input("\nAsk Question: ")

    if question.lower() in ["exit", "quit"]:

        print("\nGoodbye!")
        break

    if not question.strip():

        print("Please enter a question.")
        continue

    result = graph.invoke({
        "question": question,
        "history": get_memory()
    })

    print("\nAnswer:")
    print(result.get("answer", "No answer generated."))