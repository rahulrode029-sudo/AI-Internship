import logging
from pathlib import Path

from fastapi import (
    FastAPI,
    HTTPException,
    UploadFile,
    File
)

from config import (
    APP_NAME,
    APP_VERSION,
    LOG_LEVEL
)

from models import (
    QuestionRequest,
    QuestionResponse,
    HealthResponse
)

from document_processor import (
    read_document,
    chunk_text
)

from retriever import DocumentRetriever

from ai_service import generate_answer


# ==========================================================
# LOGGING
# ==========================================================

Path("logs").mkdir(
    exist_ok=True
)

logging.basicConfig(
    level=getattr(
        logging,
        LOG_LEVEL.upper(),
        logging.INFO
    ),
    format=(
        "%(asctime)s - "
        "%(levelname)s - "
        "%(message)s"
    ),
    handlers=[
        logging.FileHandler(
            "logs/app.log"
        ),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)


# ==========================================================
# FASTAPI
# ==========================================================

app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description=(
        "AI-powered document research "
        "assistant using retrieval."
    )
)


# ==========================================================
# GLOBAL DOCUMENT STORAGE
# ==========================================================

document_chunks: list[str] = []

retriever = DocumentRetriever([])


# ==========================================================
# ROOT ENDPOINT
# ==========================================================

@app.get("/")
def root():

    return {
        "message": APP_NAME,
        "version": APP_VERSION,
        "status": "running"
    }


# ==========================================================
# HEALTH ENDPOINT
# ==========================================================

@app.get(
    "/health",
    response_model=HealthResponse
)
def health():

    return {
        "status": "healthy",
        "version": APP_VERSION
    }


# ==========================================================
# DOCUMENT UPLOAD
# ==========================================================

@app.post("/upload")
async def upload_document(
    file: UploadFile = File(...)
):

    global document_chunks
    global retriever

    logger.info(
        "Document upload started: %s",
        file.filename
    )

    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required."
        )

    allowed_extensions = {
        ".txt"
    }

    extension = Path(
        file.filename
    ).suffix.lower()

    if extension not in allowed_extensions:

        raise HTTPException(
            status_code=400,
            detail=(
                "Only .txt files are supported "
                "in this demo."
            )
        )

    upload_dir = Path("documents")

    upload_dir.mkdir(
        exist_ok=True
    )

    file_path = (
        upload_dir /
        file.filename
    )

    content = await file.read()

    file_path.write_bytes(content)

    try:

        text = read_document(
            str(file_path)
        )

        chunks = chunk_text(
            text
        )

        if not chunks:

            raise HTTPException(
                status_code=400,
                detail="Document is empty."
            )

        document_chunks.extend(
            chunks
        )

        retriever = DocumentRetriever(
            document_chunks
        )

        logger.info(
            "Document processed successfully: %s chunks",
            len(chunks)
        )

        return {
            "message": "Document uploaded successfully",
            "filename": file.filename,
            "chunks_created": len(chunks)
        }

    except HTTPException:
        raise

    except Exception as error:

        logger.exception(
            "Document processing failed"
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# ==========================================================
# QUESTION ANSWERING
# ==========================================================

@app.post(
    "/ask",
    response_model=QuestionResponse
)
def ask_question(
    request: QuestionRequest
):

    global retriever

    question = request.question.strip()

    if not question:

        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    logger.info(
        "Question received: %s",
        question
    )

    results = retriever.search(
        question,
        top_k=3
    )

    contexts = [
        result[0]
        for result in results
    ]

    answer = generate_answer(
        question,
        contexts
    )

    sources = [
        f"chunk_{index + 1}"
        for index in range(
            len(contexts)
        )
    ]

    logger.info(
        "Question processed successfully"
    )

    return {
        "question": question,
        "answer": answer,
        "sources": sources
    }


# ==========================================================
# DOCUMENT STATUS
# ==========================================================

@app.get("/documents")
def document_status():

    return {
        "total_chunks": len(
            document_chunks
        ),
        "status": (
            "documents available"
            if document_chunks
            else "no documents uploaded"
        )
    }