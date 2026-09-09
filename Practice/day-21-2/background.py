from datetime import datetime


# =========================================================
# BACKGROUND TASK
# =========================================================

def save_request_log(
    question: str,
    answer: str
):

    timestamp = datetime.now().isoformat()

    with open(
        "api_requests.log",
        "a",
        encoding="utf-8"
    ) as file:

        file.write(
            f"{timestamp} | "
            f"Question: {question} | "
            f"Answer: {answer}\n"
        )