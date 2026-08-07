from fastapi import FastAPI

from pydantic import BaseModel

from agent import run_agent


app = FastAPI(
    title="AI Research Assistant Agent"
)



class Query(BaseModel):

    question:str



@app.get("/")
def home():

    return {

        "message":
        "AI Research Assistant Agent Running"

    }



@app.post("/ask")
def ask_agent(data:Query):


    answer = run_agent(data.question)


    return {

        "question":data.question,

        "answer":answer

    }