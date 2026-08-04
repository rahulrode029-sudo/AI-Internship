from langchain_core.prompts import PromptTemplate
from output_parser import parser


support_prompt = PromptTemplate(
    input_variables=["query", "chat_history"],
    partial_variables={
        "format_instructions": parser.get_format_instructions()
    },
    template="""
You are a professional AI Support Assistant.

Here is the recent conversation history (may be empty if this is the first message):
{chat_history}

Analyze the user's new problem below and provide a helpful solution.
Use the conversation history for context if the new query refers to something said earlier.

User Query:
{query}

Return the response only in this JSON format:
{format_instructions}
"""
)