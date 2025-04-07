import pytest
from typing import Any
from importer.graph import find_latest_conversation_turn

class TestFindLatestConversationTurn:
    def test_returns_only_leaf_when_single_node_exists(self) -> None:
        mapping: dict[str, Any] = {
            "node1": {"children": [], "parent": None, "message": {"create_time": 100}}
        }
        result: dict = find_latest_conversation_turn(mapping)
        assert result == mapping["node1"]

    def test_returns_only_leaf_when_only_one_leaf_present(self) -> None:
        mapping: dict[str, Any] = {
            "node1": {"children": ["node2"], "parent": None, "message": {"create_time": 100}},
            "node2": {"children": [], "parent": "node1", "message": {"create_time": 200}},
        }
        result: dict = find_latest_conversation_turn(mapping)
        assert result == mapping["node2"]

    def test_returns_latest_leaf_when_multiple_leaves_have_distinct_create_times(self) -> None:
        mapping: dict[str, Any] = {
            "node1": {"children": ["node2", "node3"], "parent": None, "message": {"create_time": 50}},
            "node2": {"children": [], "parent": "node1", "message": {"create_time": 300}},
            "node3": {"children": [], "parent": "node1", "message": {"create_time": 200}},
        }
        result: dict = find_latest_conversation_turn(mapping)
        assert result == mapping["node2"]

    def test_raises_value_error_when_multiple_leaves_share_highest_create_time(self) -> None:
        mapping: dict[str, Any] = {
            "node1": {"children": ["node2", "node3"], "parent": None, "message": {"create_time": 50}},
            "node2": {"children": [], "parent": "node1", "message": {"create_time": 300}},
            "node3": {"children": [], "parent": "node1", "message": {"create_time": 300}},
        }
        with pytest.raises(ValueError):
            find_latest_conversation_turn(mapping)

    def test_handles_none_create_time_by_treating_it_as_zero(self) -> None:
        mapping: dict[str, Any] = {
            "node1": {"children": ["node2"], "parent": None, "message": {"create_time": None}},
            "node2": {"children": [], "parent": "node1", "message": {"create_time": 50}},
        }
        result: dict = find_latest_conversation_turn(mapping)
        assert result == mapping["node2"]
