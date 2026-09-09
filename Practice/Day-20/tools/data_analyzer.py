from pathlib import Path

import pandas as pd


def analyze_data(file_path: str) -> str:
    """
    Analyze a CSV file using pandas.

    Args:
        file_path: Path to CSV file.

    Returns:
        Dataset analysis.
    """

    try:
        path = Path(file_path)

        if not path.exists():
            return f"Data Analyzer error: File not found: {file_path}"

        if path.stat().st_size == 0:
            return "Data Analyzer error: File is empty."

        if path.suffix.lower() != ".csv":
            return "Data Analyzer error: Only CSV files are supported."

        dataframe = pd.read_csv(path)

        if dataframe.empty:
            return "Data Analyzer error: CSV contains no records."

        result = []

        result.append("DATASET ANALYSIS")
        result.append("=" * 50)

        result.append(
            f"Rows: {dataframe.shape[0]}"
        )

        result.append(
            f"Columns: {dataframe.shape[1]}"
        )

        result.append(
            f"Column names: {', '.join(dataframe.columns)}"
        )

        result.append("\nMissing Values:")

        missing = dataframe.isnull().sum()

        for column, count in missing.items():
            result.append(
                f"{column}: {count}"
            )

        numeric_columns = dataframe.select_dtypes(
            include="number"
        ).columns

        if len(numeric_columns) > 0:

            result.append("\nNumeric Statistics:")

            for column in numeric_columns:

                result.append(
                    f"\n{column}:"
                )

                result.append(
                    f"  Average: {dataframe[column].mean():.2f}"
                )

                result.append(
                    f"  Minimum: {dataframe[column].min()}"
                )

                result.append(
                    f"  Maximum: {dataframe[column].max()}"
                )

        return "\n".join(result)

    except Exception as e:
        return f"Data Analyzer error: {e}"