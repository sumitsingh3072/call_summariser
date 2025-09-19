import csv
from pathlib import Path
from typing import Union, Any, Optional


def save_to_csv(analysis_result: Any, filename: Optional[Union[str, Path]] = None):
    """Save the analysis result to a CSV file."""

    repo_backend = Path(__file__).resolve().parent.parent
    csv_path = Path(filename) if filename else repo_backend / "call_analysis.csv"

    if hasattr(analysis_result, "dict"):
        row = analysis_result.dict()
    elif isinstance(analysis_result, dict):
        row = analysis_result
    else:
        row = {
            "transcript": getattr(analysis_result, "transcript", ""),
            "summary": getattr(analysis_result, "summary", ""),
            "sentiment": getattr(analysis_result, "sentiment", ""),
        }

    fieldnames = ["transcript", "summary", "sentiment"]
    file_exists = csv_path.is_file()
    csv_path.parent.mkdir(parents=True, exist_ok=True)

    with open(csv_path, mode="a", newline="", encoding="utf-8") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, quoting=csv.QUOTE_ALL)
        if not file_exists:
            writer.writeheader()
        writer.writerow({k: row.get(k, "") for k in fieldnames})
