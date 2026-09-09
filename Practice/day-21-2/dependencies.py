from fastapi import Header, HTTPException


# =========================================================
# DEPENDENCY
# =========================================================

def get_api_client(
    x_client_name: str | None = Header(
        default=None
    )
):

    if not x_client_name:

        raise HTTPException(
            status_code=400,
            detail=(
                "X-Client-Name header is required."
            )
        )

    return {
        "client": x_client_name
    }