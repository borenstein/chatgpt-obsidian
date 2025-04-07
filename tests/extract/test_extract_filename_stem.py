from pathlib import Path

from importer.extract import extract_filename_relative_path


def test_extract_filename_relative_path_returns_expected_value() -> None:
    conversation = {
        "title": "Sample Conversation",
        "create_time": 1680816000
    }
    expected = Path("2023") / "04" / "06" / "2023-04-06 Sample Conversation.md"
    result = extract_filename_relative_path(conversation)
    assert result == expected
