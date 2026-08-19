from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv

from workflow import run_workflow

load_dotenv()

app = FastAPI(
    title="Responsible AI Multi-Agent PoC",
    version="1.0.0",
    description="Day-26 Agent Architecture Proof of Concept"
)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def root():
    return {
        "project": "Responsible AI Multi-Agent PoC",
        "specialization": "Agent Architecture",
        "status": "running"
    }


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }


@app.post("/ask")
async def ask_question(request: QuestionRequest):

    question = request.question.strip()

    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty."
        )

    try:

        result = await run_workflow(question)

        return {
            "question": question,
            "answer": result["answer"],
            "agents_used": result["agents_used"],
            "safety_notes": result["safety_notes"]
        }

    except Exception as e:

        # Print complete error in terminal
        print("\n" + "=" * 70)
        print("ERROR IN /ask")
        print("=" * 70)
        print(type(e).__name__)
        print(str(e))
        print("=" * 70 + "\n")

        raise HTTPException(
            status_code=500,
            detail=f"{type(e).__name__}: {str(e)}"
        )