from retriever import DocumentRetriever


def test_retriever():

    documents = [
        "Python is a programming language.",
        "Artificial intelligence is used in business.",
        "Git is used for source code collaboration."
    ]

    retriever = DocumentRetriever(
        documents
    )

    results = retriever.search(
        "artificial intelligence",
        top_k=2
    )

    assert len(results) > 0

    assert (
        "artificial intelligence"
        in results[0][0].lower()
    )