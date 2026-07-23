import csv

from src.exporter import (
    export_duplicate_report,
    export_file_report,
    export_folder_report,
)


def test_export_file_report(tmp_path):
    report_file = tmp_path / "subdir" / "file_report.csv"

    records = [
        {
            "path": "/path/to/file1.txt",
            "type": "File",
            "size_mb": 10.5,
            "file_created": "2026-07-23 00:00:00",
            "last_modified": "2026-07-23 12:00:00",
        }
    ]

    export_file_report(records, report_file)

    assert report_file.exists()

    with open(report_file, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert rows[0] == ["Path", "Type", "Size_MB", "File_Created", "Last_Modified"]
    assert rows[1] == ["/path/to/file1.txt", "File", "10.5", "2026-07-23 00:00:00", "2026-07-23 12:00:00"]


def test_export_duplicate_report(tmp_path):
    report_file = tmp_path / "dup_report.csv"

    duplicates = {
        "hash123": ["/path/to/file1.txt", "/path/to/file2.txt"]
    }

    export_duplicate_report(duplicates, report_file)

    assert report_file.exists()

    with open(report_file, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert rows[0] == ["Hash", "File_Path"]
    assert rows[1] == ["hash123", "/path/to/file1.txt"]
    assert rows[2] == ["hash123", "/path/to/file2.txt"]


def test_export_folder_report(tmp_path):
    report_file = tmp_path / "folder_report.csv"

    folder_records = [
        {
            "path": "/path/to/dir",
            "type": "Folder",
            "size_mb": 100.25,
            "file_created": "2026-07-20 08:00:00",
            "last_modified": "2026-07-23 10:00:00",
        }
    ]

    export_folder_report(folder_records, report_file)

    assert report_file.exists()

    with open(report_file, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        rows = list(reader)

    assert rows[0] == ["Path", "Type", "Size_MB", "File_Created", "Last_Modified"]
    assert rows[1] == ["/path/to/dir", "Folder", "100.25", "2026-07-20 08:00:00", "2026-07-23 10:00:00"]
