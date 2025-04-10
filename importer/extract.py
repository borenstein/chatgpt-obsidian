from datetime import datetime
from pathlib import Path

import pytz

from importer.dates import epoch_to_dt
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

def construct_header_for_turn(turn: dict[str, any]) -> str:
    message = turn.get("message", {})
    role = message.get("author", {}).get("role", "").lower()
    create_time = message.get("create_time")
    from importer.dates import epoch_to_human_timestamp
    date_str = epoch_to_human_timestamp(create_time) if create_time else "Unknown Time"
    if role == "user":
        label = "User"
    else:
        label = message.get("metadata", {}).get("model_slug", "System")
    return f"# {label} ({date_str})"

def extract_turn_as_markdown(turn: dict[str, any]) -> str | None:
    body: str = extract_text_from_turn(turn)
    if not body:
        return None

    header: str = construct_header_for_turn(turn)
    return f"{header}\n\n{body}"

def extract_all_turns_as_markdown(message_chain: list[dict[str, any]]) -> list[str]:
    messages: list[str] = []
    for turn in message_chain:
        message_text: str | None = extract_turn_as_markdown(turn)
        if message_text is not None:
            messages.append(message_text)
    return messages

def extract_filename_relative_path(conversation: dict[str, any]) -> Path:
    create_time: float = conversation["create_time"]
    title: str = conversation["title"]
    dt = epoch_to_dt(create_time)
    year: str = dt.strftime("%Y")
    month: str = dt.strftime("%m")
    day: str = dt.strftime("%d")
    date_str: str = dt.strftime("%Y-%m-%d")
    filename: str = f"{date_str} {title}.md"
    return Path(year) / month / day / filename


def extract_conversation_body(conversation: dict[str, any]) -> str:
    mapping: dict[str, dict] = conversation["mapping"]
    leaf_node: dict[str, any] = find_latest_conversation_turn(mapping)
    path_nodes: list[dict] = resolve_message_chain_from_latest(leaf_node, mapping)
    message_list: list[str] = extract_all_turns_as_markdown(path_nodes)
    return "\n\n".join(message_list)
