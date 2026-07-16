# tests/test_llm.py

import json

from llm.messages import MessageFormatter
from models.message import Message, Role
from models.tool_call import ToolCall


def test_single_message():
    result = MessageFormatter.format_message(
        Message(role=Role.USER, content="Hello")
    )

    assert result == {"role": "user", "content": "Hello"}


def test_multiple_messages():
    formatted = MessageFormatter.format_messages(
        [
            Message(role=Role.SYSTEM, content="System"),
            Message(role=Role.USER, content="Hello"),
        ]
    )

    assert len(formatted) == 2
    assert formatted[0]["role"] == "system"
    assert formatted[1]["role"] == "user"


def test_assistant_message_with_tool_calls():
    message = Message(
        role=Role.ASSISTANT,
        content="",
        tool_calls=[
            ToolCall(
                tool_name="read_file",
                arguments={"path": "README.md"},
                tool_call_id="call_1",
            )
        ],
    )

    result = MessageFormatter.format_message(message)

    assert result["content"] is None
    assert result["tool_calls"][0]["id"] == "call_1"
    assert result["tool_calls"][0]["function"]["name"] == "read_file"

    arguments = json.loads(result["tool_calls"][0]["function"]["arguments"])

    assert arguments == {"path": "README.md"}


def test_tool_message():
    result = MessageFormatter.format_message(
        Message(
            role=Role.TOOL,
            content="file contents",
            tool_call_id="call_1",
        )
    )

    assert result == {
        "role": "tool",
        "tool_call_id": "call_1",
        "content": "file contents",
    }
