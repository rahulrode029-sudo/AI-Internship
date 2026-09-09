from llm import llm


print("=" * 50)
print("Testing Gemini Model")
print("=" * 50)

try:

    response = llm.invoke(
        "Explain what artificial intelligence is in 3 simple sentences."
    )

    print("\nModel Response:")
    print(response.content)

    print("\nModel test successful!")

except Exception as e:

    print("\nModel test failed!")
    print("Error:", e)