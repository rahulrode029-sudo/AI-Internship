from pathlib import Path

from pypdf import PdfReader


def company_pdf_reader(file_path: str) -> str:
    """
    Read a company PDF document and extract its text.

    Args:
        file_path: Path to company PDF.

    Returns:
        Extracted PDF text.
    """

    try:
        path = Path(file_path)

        if not path.exists():
            return (
                f"Company PDF Reader error: "
                f"File not found: {file_path}"
            )

        if path.suffix.lower() != ".pdf":
            return (
                "Company PDF Reader error: "
                "Only PDF files are supported."
            )

        reader = PdfReader(str(path))

        if len(reader.pages) == 0:
            return (
                "Company PDF Reader error: "
                "PDF contains no pages."
            )

        pages = []

        for page_number, page in enumerate(
            reader.pages,
            start=1
        ):
            text = page.extract_text()

            if text:
                pages.append(
                    f"\n--- Page {page_number} ---\n{text}"
                )

        if not pages:
            return (
                "Company PDF Reader error: "
                "No readable text found."
            )

        return "\n".join(pages)

    except Exception as e:
        return f"Company PDF Reader error: {e}"