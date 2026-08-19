import time

from agents import (
    coordinator_agent,
    research_agent,
    analysis_agent,
    writer_agent
)


async def run_workflow(question: str) -> dict:

    workflow_start = time.time()

    print("\n" + "=" * 60)
    print("WORKFLOW STARTED")
    print("=" * 60)

    # ---------------------------------------------------------
    # Step 1: Coordinator
    # ---------------------------------------------------------

    print("\n[1/4] Coordinator Agent started...")

    start = time.time()

    plan = coordinator_agent(question)

    print(
        f"[1/4] Coordinator completed "
        f"in {time.time() - start:.2f} seconds"
    )

    # ---------------------------------------------------------
    # Step 2: Research
    # ---------------------------------------------------------

    print("\n[2/4] Research Agent started...")

    start = time.time()

    research = research_agent(
        question,
        plan
    )

    print(
        f"[2/4] Research completed "
        f"in {time.time() - start:.2f} seconds"
    )

    # ---------------------------------------------------------
    # Step 3: Analysis
    # ---------------------------------------------------------

    print("\n[3/4] Analysis Agent started...")

    start = time.time()

    analysis = analysis_agent(
        question,
        research
    )

    print(
        f"[3/4] Analysis completed "
        f"in {time.time() - start:.2f} seconds"
    )

    # ---------------------------------------------------------
    # Step 4: Writer
    # ---------------------------------------------------------

    print("\n[4/4] Writer Agent started...")

    start = time.time()

    answer = writer_agent(
        question,
        analysis
    )

    print(
        f"[4/4] Writer completed "
        f"in {time.time() - start:.2f} seconds"
    )

    total_time = time.time() - workflow_start

    print("\n" + "=" * 60)
    print(f"TOTAL WORKFLOW TIME: {total_time:.2f} seconds")
    print("=" * 60)

    return {

        "answer": answer,

        "agents_used": [
            "Coordinator Agent",
            "Research Agent",
            "Analysis Agent",
            "Writer Agent"
        ],

        "safety_notes": [
            "Generated information should be verified.",
            "The system should not expose private information.",
            "Important decisions require human review.",
            "The model should not treat speculation as fact."
        ]
    }