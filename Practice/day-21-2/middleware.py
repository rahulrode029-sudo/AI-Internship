import time

from fastapi import Request


# =========================================================
# PERFORMANCE MIDDLEWARE
# =========================================================

async def performance_middleware(
    request: Request,
    call_next
):

    start_time = time.perf_counter()

    response = await call_next(
        request
    )

    end_time = time.perf_counter()

    process_time = (
        end_time - start_time
    )

    response.headers[
        "X-Process-Time"
    ] = f"{process_time:.4f}"

    print(
        f"{request.method} "
        f"{request.url.path} "
        f"-> {process_time:.4f}s"
    )

    return response