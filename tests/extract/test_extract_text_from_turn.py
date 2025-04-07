from typing import Any
from importer.extract import extract_text_from_turn

class TestExtractTextFromTurn:
    def test_returns_none_when_turn_lacks_message_field(self) -> None:
        turn_without_message_field: dict[str, Any] = {"id": "turn1"}
        result: str | None = extract_text_from_turn(turn_without_message_field)
        assert result is None

    def test_returns_none_when_message_field_lacks_content_or_parts(self) -> None:
        turn_with_empty_message: dict[str, Any] = {"message": {}}
        result: str | None = extract_text_from_turn(turn_with_empty_message)
        assert result is None

    def test_returns_none_when_parts_list_contains_no_strings(self) -> None:
        turn_with_non_string_parts: dict[str, Any] = {
            "message": {"content": {"parts": [{"content_type": "image", "asset_pointer": "pointer1"}]}}
        }
        result: str | None = extract_text_from_turn(turn_with_non_string_parts)
        assert result is None

    def test_joins_multiple_string_parts_using_delimiter(self) -> None:
        turn_with_multiple_string_parts: dict[str, Any] = {
            "message": {"content": {"parts": ["First part", "Second part"]}}
        }
        result: str | None = extract_text_from_turn(turn_with_multiple_string_parts)
        assert result == "First part | Second part"

    def test_trims_whitespace_and_returns_single_string_part(self) -> None:
        turn_with_single_string_part: dict[str, Any] = {
            "message": {"content": {"parts": ["   Single message with whitespace   "]}}
        }
        result: str | None = extract_text_from_turn(turn_with_single_string_part)
        assert result == "Single message with whitespace"
