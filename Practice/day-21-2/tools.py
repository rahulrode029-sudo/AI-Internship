import os
import re


DOCS_FOLDER = "docs"


# =========================================================
# TOOL 1: SEARCH COMPANY DOCUMENTS
# =========================================================

def search_company_documents(query: str):

    if not os.path.exists(DOCS_FOLDER):
        return "Company documents folder does not exist."

    query_words = set(
        re.findall(
            r"\b\w+\b",
            query.lower()
        )
    )

    if not query_words:
        return "No valid search terms were provided."

    results = []

    for filename in os.listdir(DOCS_FOLDER):

        file_path = os.path.join(
            DOCS_FOLDER,
            filename
        )

        if not os.path.isfile(file_path):
            continue

        try:

            with open(
                file_path,
                "r",
                encoding="utf-8"
            ) as file:

                content = file.read()

        except Exception:
            continue

        matched_lines = []

        for line in content.splitlines():

            line_words = set(
                re.findall(
                    r"\b\w+\b",
                    line.lower()
                )
            )

            if query_words.intersection(line_words):

                matched_lines.append(
                    line.strip()
                )

        if matched_lines:

            results.append(
                f"File: {filename}\n"
                + "\n".join(matched_lines)
            )

    if not results:

        return (
            "No relevant information found "
            "in company documents."
        )

    return "\n\n".join(results)


# =========================================================
# TOOL 2: READ COMPANY FILE
# =========================================================

def read_company_file(filename: str):

    file_path = os.path.join(
        DOCS_FOLDER,
        filename
    )

    if not os.path.exists(file_path):

        return (
            f"File '{filename}' was not found."
        )

    try:

        with open(
            file_path,
            "r",
            encoding="utf-8"
        ) as file:

            return file.read()

    except Exception as e:

        return (
            f"Error reading file: {str(e)}"
        )


# =========================================================
# TOOL 3: CALCULATOR
# =========================================================

def calculate(expression: str):

    try:

        allowed = set(
            "0123456789+-*/(). %"
        )

        if not all(
            char in allowed
            for char in expression
        ):

            return (
                "Invalid mathematical expression."
            )

        result = eval(
            expression,
            {
                "__builtins__": {}
            }
        )

        return str(result)

    except Exception as e:

        return (
            f"Calculation error: {str(e)}"
        )


# =========================================================
# TOOL 4: LIST DOCUMENTS
# =========================================================

def list_documents(query: str = ""):

    if not os.path.exists(DOCS_FOLDER):

        return "No documents folder found."

    files = []

    for filename in os.listdir(DOCS_FOLDER):

        file_path = os.path.join(
            DOCS_FOLDER,
            filename
        )

        if os.path.isfile(file_path):

            files.append(filename)

    if not files:

        return "No company documents available."

    return "\n".join(files)