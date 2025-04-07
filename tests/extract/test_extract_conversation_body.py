from typing import Any
from importer.extract import extract_conversation_body


def test_extract_conversation_body_selects_latest_branch_and_assembles_message_chain() -> None:
    """
    Construct a conversation with branching:

    - "node1" is the root node with a simple message ("Root message").
    - Branch A: "node2" is a leaf node with a multi-part message (["First part", "Second part", image pointer])
      and a higher create_time (150).
    - Branch B: "node3" leads to "node4", where "node4" is a leaf node with a lower create_time (120).

    The function should:
      - Select the latest leaf from Branch A.
      - Resolve the message chain from the root ("node1") to the latest leaf ("node2").
      - Extract messages, joining multiple string parts with " | " and ignoring non-string parts.
      - Assemble the messages with "\n\n" as the delimiter.

    Expected result:
      "Root message\n\nFirst part | Second part"
    """
    conversation: dict[str, Any] = {
        "mapping": {
            "node1": {
                "children": ["node2", "node3"],
                "parent": None,
                "message": {
                    "content": {"parts": ["Root message"]},
                    "create_time": 50
                }
            },
            "node2": {
                "children": [],
                "parent": "node1",
                "message": {
                    "content": {
                        "parts": [
                            "First part",
                            "Second part",
                            {"content_type": "image", "asset_pointer": "dummy"}
                        ]
                    },
                    "create_time": 150
                }
            },
            "node3": {
                "children": ["node4"],
                "parent": "node1",
                "message": {
                    "content": {"parts": ["Branch B message"]},
                    "create_time": 100
                }
            },
            "node4": {
                "children": [],
                "parent": "node3",
                "message": {
                    "content": {"parts": ["Older message"]},
                    "create_time": 120
                }
            }
        }
    }
    expected: str = "Root message\n\nFirst part | Second part"
    result: str = extract_conversation_body(conversation)
    assert result == expected
