from typing import Any
from unittest.mock import patch
import pytest
from importer.extract import construct_header_for_turn

class TestConstructHeaderFromTurn:
    @patch("importer.dates.epoch_to_human_timestamp", return_value="Monday, December 7, 2001 14:32:27 UTC")
    def test_labels_as_user_when_user(self, mock_epoch: Any) -> None:
        turn = {
            "message": {
                "author": {
                    "role": "user"
                },
                "create_time": 1000000000.0
            }
        }
        header = construct_header_for_turn(turn)
        assert header == "# User (Monday, December 7, 2001 14:32:27 UTC)"

    @patch("importer.dates.epoch_to_human_timestamp", return_value="Monday, December 7, 2001 14:32:27 UTC")
    def test_labels_with_model_name_when_system(self, mock_epoch: Any) -> None:
        turn = {
            "message": {
                "author": {
                    "role": "assistant"
                },
                "create_time": 1000000000.0,
                "metadata": {
                    "model_slug": "GPT-4o"
                }
            }
        }
        header = construct_header_for_turn(turn)
        assert header == "# GPT-4o (Monday, December 7, 2001 14:32:27 UTC)"