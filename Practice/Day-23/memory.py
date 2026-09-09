conversation_history = []


def save_memory(question, answer):

    conversation_history.append(
        f"User: {question}"
    )

    conversation_history.append(
        f"Assistant: {answer}"
    )


def get_memory():

    return conversation_history