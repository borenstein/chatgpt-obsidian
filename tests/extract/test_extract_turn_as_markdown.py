from typing import Any
from unittest.mock import patch
from importer.extract import extract_turn_as_markdown

class TestExtractTurnFromMarkdown:
    @patch("importer.extract.extract_text_from_turn")
    @patch("importer.extract.construct_header_for_turn")
    def test_returns_header_and_body_when_delegates_return_values(self, mock_construct_header: Any, mock_extract_text: Any) -> None:
        mock_construct_header.return_value = "# User (Wed, 2025-04-09 14:37:52) ^turn-1"
        mock_extract_text.return_value = "Turn message"
        turn = {"dummy": "data"}
        result = extract_turn_as_markdown(turn)
        assert result == "# User (Wed, 2025-04-09 14:37:52) ^turn-1\n\nTurn message"

    @patch("importer.extract.extract_text_from_turn")
    @patch("importer.extract.construct_header_for_turn")
    def test_returns_none_when_body_is_missing(self, mock_construct_header: Any, mock_extract_text: Any) -> None:
        mock_construct_header.return_value = "# User (Wed, 2025-04-09 14:37:52) ^turn-1"
        mock_extract_text.return_value = None
        turn = {"dummy": "data"}
        result = extract_turn_as_markdown(turn)
        assert result is None
