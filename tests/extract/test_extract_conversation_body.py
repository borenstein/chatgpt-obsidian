from importer.extract import extract_conversation_body

def test_extract_conversation_body_selects_latest_branch_and_assembles_message_chain() -> None:
    conversation: dict[str, any] = {
        "mapping": {
            "node1": {
                "id": "node1",
                "children": ["node2", "node3"],
                "parent": None,
                "message": {
                    "author": {"role": "user"},
                    "content": {"parts": ["Root message"]},
                    "create_time": 50
                }
            },
            "node2": {
                "id": "node2",
                "children": [],
                "parent": "node1",
                "message": {
                    "author": {"role": "assistant"},
                    "content": {
                        "parts": [
                            "First part",
                            "Second part",
                            {"content_type": "image", "asset_pointer": "dummy"}
                        ]
                    },
                    "create_time": 150,
                    "metadata": {"model_slug": "GPT-4o"}
                }
            },
            "node3": {
                "id": "node3",
                "children": ["node4"],
                "parent": "node1",
                "message": {
                    "author": {"role": "assistant"},
                    "content": {"parts": ["Branch B message"]},
                    "create_time": 100
                }
            },
            "node4": {
                "id": "node4",
                "children": [],
                "parent": "node3",
                "message": {
                    "author": {"role": "assistant"},
                    "content": {"parts": ["Older message"]},
                    "create_time": 120
                }
            }
        }
    }
    expected: str = (
        "# User (Thursday, January 1, 1970 00:00:50 UTC) ^node1\n\n"
        "Root message\n\n"
        "# GPT-4o (Thursday, January 1, 1970 00:02:30 UTC) ^node2\n\n"
        "First part | Second part"
    )
    result: str = extract_conversation_body(conversation)
    assert result == expected
