def generate_answer(
    question: str,
    contexts: list[str]
) -> str:

    if not contexts:
        return (
            "I could not find relevant information "
            "in the uploaded documents."
        )

    context_text = "\n\n".join(contexts)

    answer = (
        f"Based on the available documents, "
        f"the relevant information for your question "
        f"'{question}' is:\n\n"
        f"{context_text}"
    )

    return answer