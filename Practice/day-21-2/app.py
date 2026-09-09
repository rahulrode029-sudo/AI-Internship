import time
import asyncio

from fastapi import (
    FastAPI,
    HTTPException,
    BackgroundTasks,
    Depends
)

from pydantic import (
    BaseModel,
    Field
)

from agent import run_agent

from dependencies import (
    get_api_client
)

from middleware import (
    performance_middleware
)

from background import (
    save_request_log
)


# =========================================================
# APPLICATION
# =========================================================

app = FastAPI(

    title="AI Research Assistant Async API",

    description="""
AI Research Assistant API demonstrating:

- Async Programming
- Async/Await
- Middleware
- Background Tasks
- Dependency Injection
- API Versioning
- Validation
- Performance Benchmarking
""",

    version="2.0.0"
)


# =========================================================
# MIDDLEWARE
# =========================================================

app.middleware(
    "http"
)(performance_middleware)


# =========================================================
# REQUEST MODEL
# =========================================================

class QuestionRequest(BaseModel):

    question: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Question for the AI agent"
    )


# =========================================================
# RESPONSE MODEL
# =========================================================

class HealthResponse(BaseModel):

    status: str


# =========================================================
# HOME
# =========================================================

@app.get("/")
async def home():

    return {

        "message":
        "AI Research Assistant Async API",

        "version":
        "2.0.0",

        "documentation":
        "/docs"
    }


# =========================================================
# HEALTH
# =========================================================

@app.get(
    "/health",
    response_model=HealthResponse
)
async def health():

    return {
        "status": "OK"
    }


# =========================================================
# API V1 - SYNCHRONOUS
# =========================================================

@app.post(
    "/api/v1/sync/ask"
)
def sync_ask(
    request: QuestionRequest,
    background_tasks: BackgroundTasks,
    client=Depends(get_api_client)
):

    start = time.perf_counter()

    # Run async agent from sync endpoint
    result = asyncio.run(
        run_agent(
            request.question
        )
    )

    elapsed = (
        time.perf_counter() - start
    )

    background_tasks.add_task(
        save_request_log,
        request.question,
        result["answer"]
    )

    result["performance"] = {
        "type": "synchronous",
        "response_time_seconds":
            round(elapsed, 4)
    }

    result["client"] = client[
        "client"
    ]

    return result


# =========================================================
# API V1 - ASYNCHRONOUS
# =========================================================

@app.post(
    "/api/v1/async/ask"
)
async def async_ask(
    request: QuestionRequest,
    background_tasks: BackgroundTasks,
    client=Depends(get_api_client)
):

    start = time.perf_counter()

    result = await run_agent(
        request.question
    )

    elapsed = (
        time.perf_counter() - start
    )

    background_tasks.add_task(
        save_request_log,
        request.question,
        result["answer"]
    )

    result["performance"] = {
        "type": "asynchronous",
        "response_time_seconds":
            round(elapsed, 4)
    }

    result["client"] = client[
        "client"
    ]

    return result


# =========================================================
# API V1 - SIMPLE ASYNC TEST
# =========================================================

@app.get(
    "/api/v1/async/ping"
)
async def async_ping():

    await asyncio.sleep(0.1)

    return {
        "message": "Async endpoint working"
    }