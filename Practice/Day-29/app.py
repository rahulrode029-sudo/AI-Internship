import logging
from pathlib import Path

from fastapi import FastAPI, HTTPException, UploadFile, File

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
        "AI-powered document research assistant "
        "using PDF, TXT and DOCX documents."
    )
)


# ==========================================================
# GLOBAL DOCUMENT STORAGE
# ==========================================================

document_chunks: list[str] = []

retriever = DocumentRetriever(
    document_chunks
)


# ==========================================================
# ROOT
# ==========================================================

@app.get("/")
def root():

    return {
        "message": APP_NAME,
        "version": APP_VERSION,
        "status": "running"
    }


# ==========================================================
# HEALTH
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
# UPLOAD DOCUMENT
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

    # ------------------------------------------------------
    # Check filename
    # ------------------------------------------------------

    if not file.filename:

        raise HTTPException(
            status_code=400,
            detail="Filename is required."
        )

    # ------------------------------------------------------
    # Allowed extensions
    # ------------------------------------------------------

    allowed_extensions = {
        ".txt",
        ".pdf",
        ".docx"
    }

    extension = Path(
        file.filename
    ).suffix.lower()

    if extension not in allowed_extensions:

        raise HTTPException(
            status_code=400,
            detail=(
                "Only .txt, .pdf and .docx "
                "files are supported."
            )
        )

    # ------------------------------------------------------
    # Create documents directory
    # ------------------------------------------------------

    upload_dir = Path(
        "documents"
    )

    upload_dir.mkdir(
        exist_ok=True
    )

    # ------------------------------------------------------
    # Prevent unsafe file paths
    # ------------------------------------------------------

    safe_filename = Path(
        file.filename
    ).name

    file_path = (
        upload_dir /
        safe_filename
    )

    # ------------------------------------------------------
    # Read uploaded file
    # ------------------------------------------------------

    try:

        content = await file.read()

    except Exception as error:

        logger.exception(
            "Could not read uploaded file."
        )

        raise HTTPException(
            status_code=400,
            detail=(
                f"Could not read file: {error}"
            )
        )

    # ------------------------------------------------------
    # Empty file check
    # ------------------------------------------------------

    if not content:

        raise HTTPException(
            status_code=400,
            detail="Uploaded file is empty."
        )

    # ------------------------------------------------------
    # Save file
    # ------------------------------------------------------

    try:

        file_path.write_bytes(
            content
        )

    except Exception as error:

        logger.exception(
            "Could not save uploaded file."
        )

        raise HTTPException(
            status_code=500,
            detail=(
                f"Could not save file: {error}"
            )
        )

    # ------------------------------------------------------
    # Extract text and create chunks
    # ------------------------------------------------------

    try:

        text = read_document(
            str(file_path)
        )

        if not text or not text.strip():

            file_path.unlink(
                missing_ok=True
            )

            raise HTTPException(
                status_code=400,
                detail=(
                    "No readable text was found "
                    "in the document."
                )
            )

        chunks = chunk_text(
            text
        )

        if not chunks:

            file_path.unlink(
                missing_ok=True
            )

            raise HTTPException(
                status_code=400,
                detail="Document is empty."
            )

        # --------------------------------------------------
        # Add chunks to global collection
        # --------------------------------------------------

        document_chunks.extend(
            chunks
        )

        # --------------------------------------------------
        # Rebuild retriever
        # --------------------------------------------------

        retriever = DocumentRetriever(
            document_chunks
        )

        logger.info(
            "Document processed successfully: %s chunks",
            len(chunks)
        )

        # --------------------------------------------------
        # Return upload result
        # --------------------------------------------------

        return {
            "message": (
                "Document uploaded successfully."
            ),
            "filename": safe_filename,
            "file_type": extension,
            "size_bytes": len(content),
            "chunks_created": len(chunks),
            "total_chunks": len(
                document_chunks
            )
        }

    except HTTPException:

        raise

    except Exception as error:

        logger.exception(
            "Document processing failed."
        )

        file_path.unlink(
            missing_ok=True
        )

        raise HTTPException(
            status_code=500,
            detail=str(error)
        )


# ==========================================================
# ASK QUESTION
# ==========================================================

@app.post(
    "/ask",
    response_model=QuestionResponse
)
def ask_question(
    request: QuestionRequest
):

    logger.info(
        "RUNNING CURRENT ASK FUNCTION"
    )

    logger.info(
        "Question received: %s",
        request.question
    )


    # ------------------------------------------------------
    # Validate question
    # ------------------------------------------------------

    question = request.question.strip()

    if not question:

        return QuestionResponse(
            question=request.question,
            answer="Please enter a question.",
            sources=[]
        )

    # ------------------------------------------------------
    # Check documents
    # ------------------------------------------------------

    if not document_chunks:

        return QuestionResponse(
            question=question,
            answer=(
                "I am sorry, but no document "
                "has been uploaded yet."
            ),
            sources=[]
        )

    # ------------------------------------------------------
    # Check retriever
    # ------------------------------------------------------

    if retriever is None:

        return QuestionResponse(
            question=question,
            answer=(
                "I am sorry, but the document "
                "search system is not ready."
            ),
            sources=[]
        )

    # ------------------------------------------------------
    # Search documents
    # ------------------------------------------------------

    try:

        results = retriever.search(
            question
        )

    except Exception as error:

        logger.exception(
            "Retriever search failed."
        )

        return QuestionResponse(
            question=question,
            answer=(
                "I am sorry, but I could not "
                "search the uploaded document."
            ),
            sources=[]
        )

    # ------------------------------------------------------
    # No results
    # ------------------------------------------------------

    if not results:

        return QuestionResponse(
            question=question,
            answer=(
                "I am sorry, but I could not find "
                "the answer in the uploaded documents."
            ),
            sources=[]
        )

    # ------------------------------------------------------
    # Generate answer
    # ------------------------------------------------------

    try:

        answer = generate_answer(
            question,
            results
        )

    except Exception as error:

        logger.exception(
            "Answer generation failed."
        )

        return QuestionResponse(
            question=question,
            answer=(
                "I am sorry, but I could not "
                "generate an answer."
            ),
            sources=[]
        )

    # ------------------------------------------------------
    # Check generated answer
    # ------------------------------------------------------

    if answer is None:

        return QuestionResponse(
            question=question,
            answer=(
                "I am sorry, but I could not find "
                "the answer in the uploaded documents."
            ),
            sources=[]
        )

    # ------------------------------------------------------
    # Convert answer to string
    # ------------------------------------------------------

    answer = str(
        answer
    ).strip()

    if not answer:

        answer = (
            "I am sorry, but I could not find "
            "the answer in the uploaded documents."
        )

    # ------------------------------------------------------
    # Build sources
    # ------------------------------------------------------

    sources = []

    for result in results:

        # Dictionary result
        if isinstance(
            result,
            dict
        ):

            source_text = (
                result.get("text")
                or result.get("content")
                or result.get("chunk")
            )

            if source_text:

                sources.append(
                    str(source_text)
                )

        # Object result
        elif hasattr(
            result,
            "text"
        ):

            source_text = getattr(
                result,
                "text",
                None
            )

            if source_text:

                sources.append(
                    str(source_text)
                )

        # String result
        else:

            sources.append(
                str(result)
            )

    # ------------------------------------------------------
    # Remove duplicate sources
    # ------------------------------------------------------

    sources = list(
        dict.fromkeys(
            sources
        )
    )

    # ------------------------------------------------------
    # FINAL RESPONSE
    # ------------------------------------------------------

    response = QuestionResponse(
        question=question,
        answer=answer,
        sources=sources
    )

    logger.info(
        "Question answered successfully."
    )

    return response


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


# ==========================================================
# CLEAR DOCUMENTS
# ==========================================================

@app.delete("/documents")
def clear_documents():

    global document_chunks
    global retriever

    document_chunks.clear()

    retriever = DocumentRetriever(
        document_chunks
    )

    logger.info(
        "All document chunks cleared."
    )

    return {
        "message": (
            "All document data cleared successfully."
        ),
        "total_chunks": 0
    }