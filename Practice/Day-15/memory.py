from langchain.memory import ConversationBufferMemory


def get_memory():
    """
    Creates a simple in-memory conversation buffer.
    Stores the last few turns of the conversation so the assistant
    can refer back to earlier messages in the same session.
    """
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=False,  # False -> gives a plain string, easier to drop into a PromptTemplate
    )
    return memory