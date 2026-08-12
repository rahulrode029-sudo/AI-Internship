import asyncio

from planner import create_plan

from tools import (
    search_company_documents,
    read_company_file,
    calculate,
    list_documents
)


# =========================================================
# ASYNC TOOL EXECUTION
# =========================================================

async def execute_tool(
    tool_name: str,
    tool_input: str
):

    if tool_name == "search_company_documents":

        return await asyncio.to_thread(
            search_company_documents,
            tool_input
        )

    elif tool_name == "read_company_file":

        return await asyncio.to_thread(
            read_company_file,
            tool_input
        )

    elif tool_name == "calculate":

        return await asyncio.to_thread(
            calculate,
            tool_input
        )

    elif tool_name == "list_documents":

        return await asyncio.to_thread(
            list_documents,
            tool_input
        )

    return f"Unknown tool: {tool_name}"


# =========================================================
# ASYNC WORKFLOW
# =========================================================

async def execute_workflow(question: str):

    # Step 1: Planning

    plan = await create_plan(
        question
    )

    reason = plan.get(
        "reason",
        ""
    )

    tool = plan.get(
        "tool",
        ""
    )

    tool_input = plan.get(
        "tool_input",
        question
    )

    # Step 2: Tool execution

    observation = await execute_tool(
        tool,
        tool_input
    )

    # Step 3: Return result

    return {

        "reason": reason,

        "tool": tool,

        "tool_input": tool_input,

        "observation": observation
    }