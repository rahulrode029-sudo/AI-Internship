from io import BytesIO
from pathlib import Path

from fastapi.testclient import TestClient

from app import app


client = TestClient(app)


# ==========================================================
# ROOT
# ==========================================================

def test_root():

    response = client.get("/")

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "running"


# ==========================================================
# HEALTH
# ==========================================================

def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "healthy"


# ==========================================================
# GET DOCUMENTS
# ==========================================================

def test_get_documents():

    response = client.get(
        "/documents"
    )

    assert response.status_code == 200

    data = response.json()

    assert "total_documents" in data

    assert "documents" in data

    assert "total_chunks" in data

    assert isinstance(
        data["documents"],
        list
    )


# ==========================================================
# UPLOAD TXT
# ==========================================================

def test_upload_txt():

    content = (
        b"Python is a programming language. "
        b"FastAPI is a web framework."
    )

    response = client.post(
        "/upload",
        files={
            "file": (
                "test_api.txt",
                BytesIO(content),
                "text/plain"
            )
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["filename"]
        == "test_api.txt"
    )

    assert (
        data["file_type"]
        == ".txt"
    )

    assert (
        data["size_bytes"]
        == len(content)
    )

    assert (
        data["chunks_created"] > 0
    )


# ==========================================================
# GET DOCUMENTS AFTER UPLOAD
# ==========================================================

def test_get_documents_after_upload():

    content = (
        b"Python is a programming language."
    )

    upload_response = client.post(
        "/upload",
        files={
            "file": (
                "content_test.txt",
                BytesIO(content),
                "text/plain"
            )
        }
    )

    assert (
        upload_response.status_code
        == 200
    )

    response = client.get(
        "/documents"
    )

    assert response.status_code == 200

    data = response.json()

    assert (
        data["total_documents"]
        >= 1
    )

    filenames = [
        document["filename"]
        for document in data["documents"]
    ]

    assert (
        "content_test.txt"
        in filenames
    )


# ==========================================================
# CHECK ACTUAL DOCUMENT CONTENT
# ==========================================================

def test_get_document_content():

    document_content = (
        "Rahul is learning Python and FastAPI."
    )

    response = client.post(
        "/upload",
        files={
            "file": (
                "content_check.txt",
                BytesIO(
                    document_content.encode(
                        "utf-8"
                    )
                ),
                "text/plain"
            )
        }
    )

    assert response.status_code == 200

    response = client.get(
        "/documents"
    )

    assert response.status_code == 200

    data = response.json()

    matching_documents = [
        document
        for document in data["documents"]
        if document["filename"]
        == "content_check.txt"
    ]

    assert len(
        matching_documents
    ) == 1

    document = matching_documents[0]

    assert (
        document["file_type"]
        == ".txt"
    )

    assert (
        document["size_bytes"]
        > 0
    )

    assert (
        document["content"]
        == document_content
    )


# ==========================================================
# EMPTY QUESTION
# ==========================================================

def test_empty_question():

    response = client.post(
        "/ask",
        json={
            "question": ""
        }
    )

    assert response.status_code == 400


# ==========================================================
# INVALID FILE
# ==========================================================

def test_invalid_file():

    response = client.post(
        "/upload",
        files={
            "file": (
                "malicious.exe",
                BytesIO(
                    b"fake executable"
                ),
                "application/octet-stream"
            )
        }
    )

    assert response.status_code == 400

    data = response.json()

    assert (
        "Unsupported file type"
        in data["detail"]
    )


# ==========================================================
# EMPTY FILE
# ==========================================================

def test_empty_file():

    response = client.post(
        "/upload",
        files={
            "file": (
                "empty.txt",
                BytesIO(b""),
                "text/plain"
            )
        }
    )

    assert response.status_code == 400

    data = response.json()

    assert (
        data["detail"]
        == "Uploaded file is empty."
    )