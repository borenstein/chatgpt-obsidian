from typing import Any

from importer.graph import resolve_message_chain_from_latest


class TestResolveMessageChainFromLatest:
    def test_returns_single_node_path_when_leaf_is_root(self) -> None:
        conversation_mapping: dict[str, Any] = {
            "node1": {"children": [], "parent": None, "message": {"create_time": 100}}
        }
        latest_turn: dict[str, Any] = conversation_mapping["node1"]
        result: list[dict[str, Any]] = resolve_message_chain_from_latest(latest_turn, conversation_mapping)
        assert result == [conversation_mapping["node1"]]

    def test_returns_linear_path_for_two_node_chain(self) -> None:
        conversation_mapping: dict[str, Any] = {
            "node1": {"children": ["node2"], "parent": None, "message": {"create_time": 50}},
            "node2": {"children": [], "parent": "node1", "message": {"create_time": 100}},
        }
        latest_turn: dict[str, Any] = conversation_mapping["node2"]
        result: list[dict[str, Any]] = resolve_message_chain_from_latest(latest_turn, conversation_mapping)
        assert result == [conversation_mapping["node1"], conversation_mapping["node2"]]

    def test_returns_full_path_for_multi_node_chain(self) -> None:
        conversation_mapping: dict[str, Any] = {
            "node1": {"children": ["node2"], "parent": None, "message": {"create_time": 10}},
            "node2": {"children": ["node3"], "parent": "node1", "message": {"create_time": 20}},
            "node3": {"children": ["node4"], "parent": "node2", "message": {"create_time": 30}},
            "node4": {"children": [], "parent": "node3", "message": {"create_time": 40}},
        }
        latest_turn: dict[str, Any] = conversation_mapping["node4"]
        result: list[dict[str, Any]] = resolve_message_chain_from_latest(latest_turn, conversation_mapping)
        assert result == [
            conversation_mapping["node1"],
            conversation_mapping["node2"],
            conversation_mapping["node3"],
            conversation_mapping["node4"],
        ]
