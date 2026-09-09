def create_plan(query):

    plan = []

    query_lower = query.lower()

    plan.append("Understand user query")

    if "company" in query_lower or "policy" in query_lower:
        plan.append("Search company documents")

    elif "latest" in query_lower:
        plan.append("Search external information")

    else:
        plan.append("Use AI knowledge")

    plan.append("Analyze information")
    plan.append("Generate final response")


    return plan