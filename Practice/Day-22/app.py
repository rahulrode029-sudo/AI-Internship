from src.graph import build_graph


def main():

    print("=" * 70)
    print("MULTI-AGENT AI RESEARCH ASSISTANT")
    print("=" * 70)

    query = input("\nEnter your research question: ").strip()

    if not query:
        print("Please enter a question.")
        return

    graph = build_graph()

    initial_state = {
        "user_query": query,
        "research_plan": [],
        "research_results": "",
        "analysis": "",
        "critic_feedback": "",
        "revision_count": 0,
        "final_answer": "",
        "workflow_status": "Started"
    }

    print("\nStarting multi-agent workflow...\n")

    final_state = graph.invoke(initial_state)

    print("\n" + "=" * 70)
    print("FINAL ANSWER")
    print("=" * 70)

    print(final_state["final_answer"])

    print("\n" + "=" * 70)
    print("WORKFLOW INFORMATION")
    print("=" * 70)

    print("Status:", final_state["workflow_status"])
    print("Revisions:", final_state["revision_count"])


if __name__ == "__main__":
    main()