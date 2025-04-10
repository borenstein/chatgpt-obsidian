import pytest
from typing import Any
from unittest.mock import patch
from importer.extract import extract_all_turns_as_markdown

class TestExtractAllTurnsAsMarkdown:
    @patch("importer.extract.extract_turn_as_markdown")
    def test_empty_message_chain_returns_empty_list(self, mock_extract_turn: Any) -> None:
        message_chain: list[dict[str, Any]] = []
        result: list[str] = extract_all_turns_as_markdown(message_chain)
        assert result == []

    @patch("importer.extract.extract_turn_as_markdown")
    def test_skips_none_results_from_delegate(self, mock_extract_turn: Any) -> None:
        message_chain: list[dict[str, Any]] = [
            {"id": "turn1"},
            {"id": "turn2"}
        ]
        mock_extract_turn.side_effect = [None, "Valid message"]
        result: list[str] = extract_all_turns_as_markdown(message_chain)
        assert result == ["Valid message"]

    @patch("importer.extract.extract_turn_as_markdown")
    def test_collects_valid_messages_in_order(self, mock_extract_turn: Any) -> None:
        message_chain: list[dict[str, Any]] = [
            {"id": "turn1"},
            {"id": "turn2"},
            {"id": "turn3"}
        ]
        mock_extract_turn.side_effect = ["First message", "Second message", "Third message"]
        result: list[str] = extract_all_turns_as_markdown(message_chain)
        assert result == ["First message", "Second message", "Third message"]
