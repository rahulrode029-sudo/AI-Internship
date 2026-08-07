import os

from fastapi import FastAPI, UploadFile, File, HTTPException

from pydantic import BaseModel

from rag import process_pdf, ask_question



app = FastAPI(
    title="RAG Document Assistant API",
    version="1.0"
)



UPLOAD_FOLDER = "uploads"


os.makedirs(
    UPLOAD_FOLDER,
    exist_ok=True
)



# -----------------------------
# Home
# -----------------------------

@app.get("/")
def home():

    return {
        "message": "RAG API is running"
    }



# -----------------------------
# Upload PDF
# -----------------------------

@app.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):

    try:


        if not file.filename.endswith(".pdf"):

            raise HTTPException(
                status_code=400,
                detail="Only PDF files allowed"
            )



        file_path = os.path.join(
            UPLOAD_FOLDER,
            file.filename
        )



        content = await file.read()



        if len(content) == 0:

            raise HTTPException(
                status_code=400,
                detail="Empty file"
            )



        with open(
            file_path,
            "wb"
        ) as f:

            f.write(content)



        chunks = process_pdf(
            file_path
        )



        return {

            "message": "PDF uploaded successfully",

            "filename": file.filename,

            "chunks_created": chunks

        }



    except Exception as e:


        raise HTTPException(

            status_code=500,

            detail=str(e)

        )





# -----------------------------
# Ask Question
# -----------------------------


class QuestionRequest(BaseModel):

    question: str





@app.post("/ask")
def ask(
    request: QuestionRequest
):

    try:


        answer = ask_question(
            request.question
        )


        return {


            "question": request.question,


            "answer": answer


        }


    except Exception as e:


        raise HTTPException(

            status_code=500,

            detail=str(e)

        )




# -----------------------------
# Health Check
# -----------------------------


@app.get("/health")
def health():

    return {

        "status": "OK"

    }
    