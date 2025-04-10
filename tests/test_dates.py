from importer.dates import *

def test_epoch_to_dt() -> None:
    dt = epoch_to_dt(1000000000.0)
    assert dt.year == 2001
    assert dt.month == 9
    assert dt.day == 9
    assert dt.tzinfo is not None

def test_epoch_to_date() -> None:
    assert epoch_to_date(1000000000.0) == "2001-09-09"

def test_epoch_to_human_timestamp() -> None:
    expected = "Sunday, September 9, 2001 01:46:40 UTC"
    assert epoch_to_human_timestamp(1000000000.0) == expected