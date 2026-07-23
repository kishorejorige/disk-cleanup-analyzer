from src.utils import format_timestamp, readable_size


def test_readable_size():
    assert readable_size(100) == "100.00 B"
    assert readable_size(1024) == "1.00 KB"
    assert readable_size(1024 * 1024) == "1.00 MB"
    assert readable_size(1.5 * 1024 * 1024 * 1024) == "1.50 GB"
    assert readable_size(1024 * 1024 * 1024 * 1024 * 1024) == "1.00 PB"


def test_format_timestamp():
    # 0 unix timestamp = 1970-01-01 (in UTC; local time zone can affect this)
    # Let's test with a known timestamp and check formatting matches YYYY-MM-DD HH:MM:SS format length
    ts = 1718919600  # Friday, June 21, 2024 12:20:00 AM UTC
    fmt = format_timestamp(ts)
    assert len(fmt) == 19
    assert fmt[4] == "-"
    assert fmt[7] == "-"
    assert fmt[10] == " "
    assert fmt[13] == ":"
    assert fmt[16] == ":"
