import asyncio
import time
import statistics

import httpx


BASE_URL = "http://127.0.0.1:8000"

HEADERS = {
    "X-Client-Name": "benchmark"
}

PAYLOAD = {
    "question": "Who is the CEO of XYZ Company?"
}


# =========================================================
# ASYNC REQUEST
# =========================================================

async def send_async_request(
    client,
    endpoint
):

    start = time.perf_counter()

    try:

        response = await client.post(
            BASE_URL + endpoint,
            json=PAYLOAD,
            headers=HEADERS,
            timeout=90
        )

        elapsed = (
            time.perf_counter()
            - start
        )

        return {
            "status": response.status_code,
            "time": elapsed
        }

    except Exception as e:

        return {
            "status": "ERROR",
            "time": None,
            "error": str(e)
        }


# =========================================================
# CONCURRENT BENCHMARK
# =========================================================

async def benchmark(
    endpoint,
    requests=5
):

    print("\n" + "=" * 60)

    print(
        f"Testing: {endpoint}"
    )

    print(
        f"Concurrent requests: {requests}"
    )

    print("=" * 60)

    async with httpx.AsyncClient() as client:

        start = time.perf_counter()

        tasks = [
            send_async_request(
                client,
                endpoint
            )
            for _ in range(requests)
        ]

        results = await asyncio.gather(
            *tasks
        )

        total_time = (
            time.perf_counter()
            - start
        )

    successful = [
        result
        for result in results
        if result["status"] == 200
    ]

    failed = [
        result
        for result in results
        if result["status"] != 200
    ]

    print("\nIndividual Results:")

    for index, result in enumerate(
        results,
        start=1
    ):

        if result["status"] == 200:

            print(
                f"Request {index}: "
                f"{result['time']:.4f}s "
                f"[SUCCESS]"
            )

        else:

            print(
                f"Request {index}: "
                f"FAILED "
                f"[{result['status']}]"
            )

    if not successful:

        print(
            "\nNo successful requests."
        )

        return None

    times = [
        result["time"]
        for result in successful
    ]

    return {

        "successful":
            len(successful),

        "failed":
            len(failed),

        "average":
            statistics.mean(times),

        "minimum":
            min(times),

        "maximum":
            max(times),

        "total":
            total_time
    }


# =========================================================
# MAIN
# =========================================================

async def main():

    print("\n")
    print("=" * 60)
    print(
        "AI RESEARCH ASSISTANT"
    )
    print(
        "CONCURRENT API PERFORMANCE BENCHMARK"
    )
    print("=" * 60)

    # -----------------------------------------------------
    # SYNCHRONOUS ENDPOINT
    # -----------------------------------------------------

    sync_result = await benchmark(
        "/api/v1/sync/ask",
        requests=5
    )

    # -----------------------------------------------------
    # ASYNCHRONOUS ENDPOINT
    # -----------------------------------------------------

    async_result = await benchmark(
        "/api/v1/async/ask",
        requests=5
    )

    # -----------------------------------------------------
    # RESULTS
    # -----------------------------------------------------

    print("\n")
    print("=" * 60)
    print("FINAL PERFORMANCE COMPARISON")
    print("=" * 60)

    if sync_result:

        print("\nSYNCHRONOUS API")

        print(
            f"Successful: "
            f"{sync_result['successful']}"
        )

        print(
            f"Failed: "
            f"{sync_result['failed']}"
        )

        print(
            f"Average request time: "
            f"{sync_result['average']:.4f}s"
        )

        print(
            f"Minimum request time: "
            f"{sync_result['minimum']:.4f}s"
        )

        print(
            f"Maximum request time: "
            f"{sync_result['maximum']:.4f}s"
        )

        print(
            f"Total benchmark time: "
            f"{sync_result['total']:.4f}s"
        )

    if async_result:

        print("\nASYNCHRONOUS API")

        print(
            f"Successful: "
            f"{async_result['successful']}"
        )

        print(
            f"Failed: "
            f"{async_result['failed']}"
        )

        print(
            f"Average request time: "
            f"{async_result['average']:.4f}s"
        )

        print(
            f"Minimum request time: "
            f"{async_result['minimum']:.4f}s"
        )

        print(
            f"Maximum request time: "
            f"{async_result['maximum']:.4f}s"
        )

        print(
            f"Total benchmark time: "
            f"{async_result['total']:.4f}s"
        )

    # -----------------------------------------------------
    # IMPROVEMENT
    # -----------------------------------------------------

    if sync_result and async_result:

        sync_total = sync_result["total"]

        async_total = async_result["total"]

        improvement = (
            (
                sync_total
                - async_total
            )
            / sync_total
        ) * 100

        print("\n")
        print(
            f"Total Time Improvement: "
            f"{improvement:.2f}%"
        )

        if improvement > 0:

            print(
                "Async API completed the "
                "concurrent benchmark faster."
            )

        elif improvement < 0:

            print(
                "Async API was slower in "
                "this benchmark."
            )

            print(
                "This can happen because "
                "of external AI/network latency."
            )

        else:

            print(
                "Both implementations "
                "had similar performance."
            )

    print("=" * 60)


if __name__ == "__main__":

    asyncio.run(main())