from pathlib import Path

from pypdf import PdfReader


def read_file(file_path: str) -> str:
    """
    Read TXT, CSV, PDF and other text-based files.

    Args:
        file_path: Path of the file.

    Returns:
        Extracted file content.
    """

    try:
        path = Path(file_path)

        if not path.exists():
            return f"File Reader error: File not found: {file_path}"

        if path.stat().st_size == 0:
            return "File Reader error: File is empty."

        extension = path.suffix.lower()

        if extension == ".pdf":
            reader = PdfReader(str(path))

            text = []

            for page in reader.pages:
                page_text = page.extract_text()

                if page_text:
                    text.append(page_text)

            if not text:
                return "File Reader error: No readable text found in PDF."

            return "\n".join(text)

        elif extension in [".txt", ".csv", ".md", ".json"]:
            return path.read_text(
                encoding="utf-8",
                errors="replace"
            )

        else:
            return (
                f"File Reader error: Unsupported file format: "
                f"{extension}"
            )

    except Exception as e:
        return f"File Reader error: {e}"
    