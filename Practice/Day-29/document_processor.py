from pathlib import Path
from dataclasses import dataclass, field

from pypdf import PdfReader
from docx import Document


@dataclass
class DocumentChunk:
    text: str
    metadata: dict = field(default_factory=dict)


def read_document(file_path: str) -> str:
    """
    Extract text from TXT, PDF, or DOCX documents.
    """

    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(
            f"Document not found: {file_path}"
        )

    extension = path.suffix.lower()

    if extension == ".txt":
        return path.read_text(
            encoding="utf-8"
        )

    if extension == ".pdf":
        return read_pdf(path)

    if extension == ".docx":
        return read_docx(path)

    raise ValueError(
        f"Unsupported document type: {extension}"
    )


def read_pdf(path: Path) -> str:
    """
    Extract text from a PDF document.
    """

    reader = PdfReader(str(path))

    pages = []

    for page in reader.pages:

        text = page.extract_text()

        if text:
            pages.append(text)

    return "\n".join(pages)


def read_docx(path: Path) -> str:
    """
    Extract text from a DOCX document.
    """

    document = Document(str(path))

    paragraphs = []

    for paragraph in document.paragraphs:

        if paragraph.text.strip():
            paragraphs.append(
                paragraph.text
            )

    return "\n".join(paragraphs)


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
) -> list[DocumentChunk]:
    """
    Split text into fixed-size DocumentChunk objects.
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

            chunks.append(
                DocumentChunk(
                    text=chunk.strip(),
                    metadata={
                        "chunk_index": len(chunks)
                    }
                )
            )

    return chunks