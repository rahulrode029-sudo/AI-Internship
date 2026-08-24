from document_processor import (
    DocumentChunk,
)

from retriever import (
    DocumentRetriever,
)


def test_retriever_initialization():

    documents = [
        DocumentChunk(
            text="Python is a programming language.",
            metadata={
                "chunk_index": 0
            }
        ),
        DocumentChunk(
            text="FastAPI is a Python web framework.",
            metadata={
                "chunk_index": 1
            }
        ),
    ]

    retriever = DocumentRetriever(
        documents
    )

    assert retriever.documents == documents

    assert retriever.matrix is not None


def test_empty_retriever():

    retriever = DocumentRetriever([])

    results = retriever.search(
        "Python"
    )

    assert results == []


def test_retriever_search():

    documents = [
        DocumentChunk(
            text=(
                "Python is a programming language."
            ),
            metadata={
                "chunk_index": 0
            }
        ),
        DocumentChunk(
            text=(
                "FastAPI is used to build APIs."
            ),
            metadata={
                "chunk_index": 1
            }
        ),
        DocumentChunk(
            text=(
                "Machine learning uses data "
                "to train models."
            ),
            metadata={
                "chunk_index": 2
            }
        ),
    ]

    retriever = DocumentRetriever(
        documents
    )

    results = retriever.search(
        "Python programming"
    )

    assert len(results) > 0

    assert "text" in results[0]

    assert "score" in results[0]

    assert "metadata" in results[0]


def test_retriever_result_metadata():

    documents = [
        DocumentChunk(
            text=(
                "Python is a programming language."
            ),
            metadata={
                "chunk_index": 5
            }
        )
    ]

    retriever = DocumentRetriever(
        documents
    )

    results = retriever.search(
        "Python programming"
    )

    assert len(results) > 0

    assert (
        results[0]["metadata"]["chunk_index"]
        == 5
    )


def test_top_k():

    documents = [
        DocumentChunk(
            text="Python programming language.",
            metadata={
                "chunk_index": 0
            }
        ),
        DocumentChunk(
            text="Python web development.",
            metadata={
                "chunk_index": 1
            }
        ),
        DocumentChunk(
            text="Python machine learning.",
            metadata={
                "chunk_index": 2
            }
        ),
    ]

    retriever = DocumentRetriever(
        documents
    )

    results = retriever.search(
        "Python",
        top_k=2,
        min_score=0.0
    )

    assert len(results) <= 2