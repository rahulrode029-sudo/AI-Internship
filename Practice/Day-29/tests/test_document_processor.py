from pathlib import Path

from document_processor import (
    DocumentChunk,
    read_document,
    clean_text,
    chunk_text,
)


def test_clean_text():
    text = """
    
    Hello World
    
    This is a test.
    
    """

    result = clean_text(text)

    assert result == "Hello World\nThis is a test."


def test_chunk_text_returns_document_chunks():

    text = (
        "Python is a programming language. "
        "FastAPI is a Python framework. "
        "Machine learning is useful."
    )

    chunks = chunk_text(
        text,
        chunk_size=30
    )

    assert len(chunks) > 0

    assert all(
        isinstance(chunk, DocumentChunk)
        for chunk in chunks
    )


def test_chunk_contains_text():

    text = (
        "Python is easy to learn."
    )

    chunks = chunk_text(
        text,
        chunk_size=500
    )

    assert len(chunks) == 1

    assert (
        "Python is easy to learn."
        in chunks[0].text
    )


def test_chunk_metadata():

    text = (
        "This is a test document."
    )

    chunks = chunk_text(
        text,
        chunk_size=500
    )

    assert len(chunks) == 1

    assert "chunk_index" in (
        chunks[0].metadata
    )

    assert (
        chunks[0].metadata["chunk_index"]
        == 0
    )


def test_empty_text_returns_empty_list():

    chunks = chunk_text("")

    assert chunks == []


def test_read_txt_document(tmp_path):

    file_path = (
        tmp_path / "test.txt"
    )

    file_path.write_text(
        "This is a test TXT document.",
        encoding="utf-8"
    )

    result = read_document(
        str(file_path)
    )

    assert (
        result
        == "This is a test TXT document."
    )


def test_unsupported_document():

    file_path = (
        Path("test.exe")
    )

    file_path.write_bytes(
        b"fake file"
    )

    try:

        read_document(
            str(file_path)
        )

        assert False

    except ValueError as error:

        assert (
            "Unsupported document type"
            in str(error)
        )

    finally:

        if file_path.exists():
            file_path.unlink()