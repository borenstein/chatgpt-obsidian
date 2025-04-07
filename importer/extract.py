from datetime import datetime
from pathlib import Path
from typing import Any

import pytz

from importer.graph import find_latest_conversation_turn, resolve_message_chain_from_latest


def extract_text_from_turn(turn: dict[str, any]) -> str | None:
    message: any = turn.get("message")
    if not message:
        return None
    content: any = message.get("content")
    if not content:
        return None
    parts: any = content.get("parts")
    if not parts or not isinstance(parts, list):
        return None
    string_parts: list[str] = [part for part in parts if isinstance(part, str)]
    if not string_parts:
        return None
    if len(string_parts) == 1:
        return string_parts[0].strip()
    return " | ".join(part.strip() for part in string_parts)

def extract_messages(message_chain: list[dict[str, Any]]) -> list[str]:
    messages: list[str] = []
    for turn in message_chain:
        message_text: str | None = extract_text_from_turn(turn)
        if message_text is not None:
            messages.append(message_text)
    return messages

def extract_filename_relative_path(conversation: dict[str, Any]) -> Path:
    create_time: float = conversation["create_time"]
    title: str = conversation["title"]
    dt = datetime.fromtimestamp(create_time, tz=pytz.UTC)
    year: str = dt.strftime("%Y")
    month: str = dt.strftime("%m")
    day: str = dt.strftime("%d")
    date_str: str = dt.strftime("%Y-%m-%d")
    filename: str = f"{date_str} {title}.md"
    return Path(year) / month / day / filename


def extract_conversation_body(conversation: dict[str, Any]) -> str:
    mapping: dict[str, dict] = conversation["mapping"]
    leaf_node: dict[str, Any] = find_latest_conversation_turn(mapping)
    path_nodes: list[dict] = resolve_message_chain_from_latest(leaf_node, mapping)
    message_list: list[str] = extract_messages(path_nodes)
    return "\n\n".join(message_list)
