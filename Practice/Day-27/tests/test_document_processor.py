from document_processor import (
    clean_text,
    chunk_text
)


def test_clean_text():

    text = """
    
    Hello world.
    
    
    This is a test.
    
    """

    result = clean_text(text)

    assert result == (
        "Hello world.\n"
        "This is a test."
    )


def test_chunk_text():

    text = "A" * 1200

    chunks = chunk_text(
        text,
        chunk_size=500
    )

    assert len(chunks) == 3