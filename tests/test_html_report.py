from src.html_report import generate_html_report


def test_generate_html_report(tmp_path):
    report_file = tmp_path / "disk_report.html"

    records = [
        {
            "path": "/path/to/file1.txt",
            "size_bytes": 100,
            "last_modified": "2026-07-23 12:00:00",
        },
        {
            "path": "/path/to/file2.txt",
            "size_bytes": 500,
            "last_modified": "2026-07-23 13:00:00",
        }
    ]

    generate_html_report(records, report_file)

    assert report_file.exists()

    html_content = report_file.read_text(encoding="utf-8")

    # Verify sorting (file2.txt (500) should come before file1.txt (100) in the rows)
    index_file2 = html_content.find("file2.txt")
    index_file1 = html_content.find("file1.txt")

    assert index_file2 != -1
    assert index_file1 != -1
    assert index_file2 < index_file1

    assert "Disk Cleanup Analyzer Report" in html_content
    assert "file1.txt" in html_content
    assert "file2.txt" in html_content
