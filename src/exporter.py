import csv
from pathlib import Path


def export_file_report(
    records: list[dict],
    output_file: str | Path,
) -> None:
    """Export the list of scanned file records to a CSV file."""
    out_path = Path(output_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "Path",
                "Type",
                "Size_MB",
                "File_Created",
                "Last_Modified",
            ]
        )

        for record in records:
            writer.writerow(
                [
                    record["path"],
                    record["type"],
                    record["size_mb"],
                    record["file_created"],
                    record["last_modified"],
                ]
            )


def export_duplicate_report(
    duplicates: dict[str, list[str]],
    output_file: str | Path,
) -> None:
    """Export groups of duplicate files (mapping hash -> lists of file paths) to a CSV file."""
    out_path = Path(output_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(["Hash", "File_Path"])

        for hash_value, files in duplicates.items():
            for file_path in files:
                writer.writerow([hash_value, file_path])


def export_folder_report(
    folder_records: list[dict],
    output_file: str | Path,
) -> None:
    """Export the folder size analysis records to a CSV file."""
    out_path = Path(output_file)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    with open(out_path, "w", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow(
            [
                "Path",
                "Type",
                "Size_MB",
                "File_Created",
                "Last_Modified",
            ]
        )

        for record in folder_records:
            writer.writerow(
                [
                    record["path"],
                    record["type"],
                    record["size_mb"],
                    record["file_created"],
                    record["last_modified"],
                ]
            )
