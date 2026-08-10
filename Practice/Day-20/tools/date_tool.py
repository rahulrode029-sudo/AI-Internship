from datetime import datetime


def date_tool(
    operation: str,
    date1: str = "",
    date2: str = ""
) -> str:
    """
    Perform date operations.

    Operations:
    - today
    - difference

    Args:
        operation: Date operation.
        date1: First date in YYYY-MM-DD format.
        date2: Second date in YYYY-MM-DD format.

    Returns:
        Date result.
    """

    try:
        if operation.lower() == "today":
            today = datetime.now().strftime("%Y-%m-%d")

            return f"Today's date is {today}"

        if operation.lower() == "difference":

            if not date1 or not date2:
                return (
                    "Date error: date1 and date2 "
                    "are required."
                )

            first = datetime.strptime(
                date1,
                "%Y-%m-%d"
            )

            second = datetime.strptime(
                date2,
                "%Y-%m-%d"
            )

            difference = abs((second - first).days)

            return (
                f"Difference between {date1} and {date2}: "
                f"{difference} days"
            )

        return (
            "Date error: Unsupported operation. "
            "Use 'today' or 'difference'."
        )

    except ValueError:
        return (
            "Date error: Dates must use YYYY-MM-DD format."
        )

    except Exception as e:
        return f"Date error: {e}"