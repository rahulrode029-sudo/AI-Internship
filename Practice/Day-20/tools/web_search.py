from duckduckgo_search import DDGS


def web_search(query: str) -> str:
    """
    Search the web using DuckDuckGo.

    Args:
        query: Search query.

    Returns:
        Search results.
    """

    try:
        if not query.strip():
            return "Web search error: Search query cannot be empty."

        results = []

        with DDGS() as ddgs:
            search_results = ddgs.text(
                query,
                max_results=5
            )

            for result in search_results:
                results.append(
                    f"Title: {result.get('title', 'N/A')}\n"
                    f"URL: {result.get('href', 'N/A')}\n"
                    f"Description: {result.get('body', 'N/A')}"
                )

        if not results:
            return "No search results found."

        return "\n\n".join(results)

    except Exception as e:
        return f"Web search error: {e}"