from pathlib import Path

from src.folder_analyzer import calculate_folder_sizes


def test_calculate_folder_sizes_complex_hierarchy(tmp_path):
    # Setup folders:
    # tmp_path
    #  ├── dir1 (empty folder)
    #  └── dir2
    #       ├── file1.txt (1 MB)
    #       └── subdir3
    #            └── file2.txt (2 MB)

    dir1 = tmp_path / "dir1"
    dir2 = tmp_path / "dir2"
    subdir3 = dir2 / "subdir3"

    dir1.mkdir()
    dir2.mkdir()
    subdir3.mkdir()

    file1 = dir2 / "file1.txt"
    file2 = subdir3 / "file2.txt"

    # 1 MB = 1,048,576 bytes
    file1.write_bytes(b"\0" * 1024 * 1024)
    # 2 MB = 2,097,152 bytes
    file2.write_bytes(b"\0" * 2 * 1024 * 1024)

    folder_records = calculate_folder_sizes(tmp_path)

    # We should have records for dir1, dir2, subdir3.
    # Note that folder_records should be sorted by size descending.
    # Expected sizes:
    # dir2: file1 (1MB) + subdir3/file2 (2MB) = 3MB
    # subdir3: file2 (2MB) = 2MB
    # dir1: 0MB

    # Let's clean paths to make assertions relative/easy
    records_by_name = {Path(r["path"]).name: r for r in folder_records}

    assert "dir2" in records_by_name
    assert "subdir3" in records_by_name
    assert "dir1" in records_by_name

    assert records_by_name["dir2"]["size_mb"] == 3.0
    assert records_by_name["subdir3"]["size_mb"] == 2.0
    assert records_by_name["dir1"]["size_mb"] == 0.0
    assert records_by_name["dir2"]["type"] == "Folder"

    # Check sorting: dir2 should be before subdir3, which is before dir1
    assert folder_records[0]["path"] == str(dir2)
    assert folder_records[1]["path"] == str(subdir3)
    assert folder_records[2]["path"] == str(dir1)


def test_calculate_folder_sizes_empty(tmp_path):
    folder_records = calculate_folder_sizes(tmp_path)
    assert len(folder_records) == 0
