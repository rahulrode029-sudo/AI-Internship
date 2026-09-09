import sqlite3
from pathlib import Path


DATABASE_PATH = Path("database/company.db")


def database_query(query: str) -> str:
    """
    Execute a read-only SQL query on the company database.

    Args:
        query: SQL SELECT query.

    Returns:
        Query results.
    """

    try:
        query = query.strip()

        if not query:
            return "Database error: Query cannot be empty."

        if not query.lower().startswith("select"):
            return "Database error: Only SELECT queries are allowed."

        connection = sqlite3.connect(DATABASE_PATH)
        cursor = connection.cursor()

        cursor.execute(query)

        rows = cursor.fetchall()
        columns = [description[0] for description in cursor.description]

        connection.close()

        if not rows:
            return "No records found."

        result = []

        result.append(" | ".join(columns))
        result.append("-" * 60)

        for row in rows:
            result.append(
                " | ".join(str(value) for value in row)
            )

        return "\n".join(result)

    except sqlite3.Error as e:
        return f"Database error: {e}"

    except Exception as e:
        return f"Unexpected database error: {e}"