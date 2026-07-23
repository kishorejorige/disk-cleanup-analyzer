from pathlib import Path

from src.duplicate_detector import calculate_hash, find_duplicates


def test_calculate_hash(tmp_path):
    file1 = tmp_path / "file1.txt"
    file1.write_text("hello duplicate world")

    result = calculate_hash(file1)
    assert result is not None
    file_path_str, hash_val = result
    assert file_path_str == str(file1)
    # Expected SHA256 of "hello duplicate world"
    assert len(hash_val) == 64


def test_calculate_hash_missing():
    assert calculate_hash(Path("non_existent_file.txt")) is None


def test_find_duplicates(tmp_path):
    # Create duplicate files
    file1 = tmp_path / "a_file1.txt"
    file2 = tmp_path / "b_file2.txt"
    file3 = tmp_path / "c_file3.txt"
    file4 = tmp_path / "d_file4.txt"

    content_dup = "duplicate content"
    content_unique = "unique content"

    file1.write_text(content_dup)
    file2.write_text(content_dup)
    file3.write_text(content_dup)
    file4.write_text(content_unique)

    file_paths = [file3, file2, file4, file1]

    duplicates = find_duplicates(file_paths, workers=2)

    # We should have exactly 1 duplicate group
    assert len(duplicates) == 1

    hash_val = next(iter(duplicates))
    matched_files = duplicates[hash_val]

    # Matches must be alphabetically sorted
    assert matched_files == [str(file1), str(file2), str(file3)]


def test_find_duplicates_empty():
    assert find_duplicates([]) == {}
