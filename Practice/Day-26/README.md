# Day-26 - Advanced AI and Responsible AI

## Selected Specialization

Agent Architecture

## Project

Responsible AI Multi-Agent Research Assistant

## Objective

The objective of this project is to build a Proof of Concept
demonstrating multi-agent architecture while applying basic
Responsible AI principles.

## Architecture

User
  |
  v
FastAPI
  |
  v
Coordinator Agent
  |
  v
Research Agent
  |
  v
Analysis Agent
  |
  v
Writer Agent
  |
  v
Final Answer

## Technologies

- Python
- FastAPI
- LangChain
- LangChain Google GenAI
- Gemini
- Pydantic
- Pytest

## Setup

Create virtual environment:

python -m venv venv

Activate on Windows:

.\venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Create `.env`:

GOOGLE_API_KEY=YOUR_GOOGLE_API_KEY
MODEL_NAME=gemini-2.5-flash

## Run Application

uvicorn app:app --reload

Open:

http://127.0.0.1:8000/docs

## Test

pytest -v

## API Endpoint

POST /ask

Example:

{
    "question": "What is Responsible AI?"
}

## Responsible AI Features

- Input validation
- Hallucination awareness
- Uncertainty handling
- Privacy awareness
- Human oversight
- Error handling
- No intentionally fabricated citations

## Case Study

Amazon AI Recruiting Bias

## Mini Practical

Company Responsible AI Guidelines covering:

- Fairness
- Bias
- Privacy
- Hallucination
- Human oversight
- Transparency
- Security
- Monitoring
- Accountability