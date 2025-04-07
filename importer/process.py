import json
from pathlib import Path
from typing import Any
from tqdm import tqdm
from importer.extract import extract_conversation_body
from importer.extract import extract_filename_relative_path

def process_conversation(conversation: dict[str, Any], output_root: Path) -> None:
    relative_filepath: Path = extract_filename_relative_path(conversation)
    full_filepath: Path = output_root / relative_filepath
    full_filepath.parent.mkdir(parents=True, exist_ok=True)
    file_body: str = extract_conversation_body(conversation)
    full_filepath.write_text(file_body, encoding="utf-8")

def process_json_file(json_filepath: Path, output_root: Path) -> None:
    with json_filepath.open("r", encoding="utf-8") as json_file:
        conversations: list[dict[str, Any]] = json.load(json_file)
    for conversation in tqdm(conversations, desc="Processing conversations"):
        process_conversation(conversation, output_root)
