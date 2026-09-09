from pathlib import Path

def document_search(query):
    file_path = Path("docs/company_policy.txt")

    if not file_path.exists():
        return "Document not found."

    return file_path.read_text(encoding="utf-8")



def calculator(expression):

    try:
        result = eval(expression)
        return str(result)

    except:
        return "Calculation error"
