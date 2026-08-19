from pathlib import Path


def read_document(file_path: str) -> str:
    """
    Read a text document from disk.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Document not found: {file_path}"
        )

    return path.read_text(
        encoding="utf-8"
    )


def clean_text(text: str) -> str:
    """
    Basic text cleaning.
    """

    lines = []

    for line in text.splitlines():

        line = line.strip()

        if line:
            lines.append(line)

    return "\n".join(lines)


def chunk_text(
    text: str,
    chunk_size: int = 500
) -> list[str]:
    """
    Split text into fixed-size chunks.
    """

    text = clean_text(text)

    if not text:
        return []

    chunks = []

    for start in range(
        0,
        len(text),
        chunk_size
    ):
        chunk = text[
            start:start + chunk_size
        ]

        if chunk.strip():
            chunks.append(chunk.strip())

    return chunks