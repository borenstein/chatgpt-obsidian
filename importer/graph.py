from typing import Any


def find_latest_conversation_turn(mapping: dict[str, dict]) -> dict:
    leaf_turns: list[dict] = [node for node in mapping.values() if not node["children"]]
    latest_timestamp: float = max(
        (node["message"]["create_time"] if node["message"]["create_time"] is not None else 0)
        for node in leaf_turns
    )
    candidates: list[dict] = [
        node
        for node in leaf_turns
        if (node["message"]["create_time"] if node["message"]["create_time"] is not None else 0)
        == latest_timestamp
    ]
    if len(candidates) != 1 and latest_timestamp != 0:
        raise ValueError("Multiple leaves share the highest create_time")
    return candidates[0]

def resolve_message_chain_from_latest(
        latest_turn: dict[str, Any], conversation_mapping: dict[str, Any]
) -> list[dict[str, Any]]:
    message_chain: list[dict[str, Any]] = []
    current_turn: dict[str, Any] | None = latest_turn
    while current_turn is not None:
        message_chain.append(current_turn)
        previous_turn_id: str | None = current_turn.get("parent")
        if not previous_turn_id:
            break
        current_turn = conversation_mapping.get(previous_turn_id)
    return message_chain[::-1]