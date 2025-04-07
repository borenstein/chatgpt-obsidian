import pytest
from typing import Any
from unittest.mock import patch
from importer.extract import extract_messages

class TestExtractMessages:
    @patch("importer.extract.extract_text_from_turn")
    def test_empty_message_chain_returns_empty_list(self, mock_extract_text: Any) -> None:
        message_chain: list[dict[str, Any]] = []
        result: list[str] = extract_messages(message_chain)
        assert result == []

    @patch("importer.extract.extract_text_from_turn")
    def test_skips_none_results_from_delegate(self, mock_extract_text: Any) -> None:
        message_chain: list[dict[str, Any]] = [
            {"id": "turn1"},
            {"id": "turn2"}
        ]
        mock_extract_text.side_effect = [None, "Valid message"]
        result: list[str] = extract_messages(message_chain)
        assert result == ["Valid message"]

    @patch("importer.extract.extract_text_from_turn")
    def test_collects_valid_messages_in_order(self, mock_extract_text: Any) -> None:
        message_chain: list[dict[str, Any]] = [
            {"id": "turn1"},
            {"id": "turn2"},
            {"id": "turn3"}
        ]
        mock_extract_text.side_effect = ["First message", "Second message", "Third message"]
        result: list[str] = extract_messages(message_chain)
        assert result == ["First message", "Second message", "Third message"]
