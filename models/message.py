# models/message.py

from dataclasses import dataclass, field
from enum import Enum

from models.tool_call import ToolCall


class Role(Enum):
    """
    Represents the role of a message.
    """

    SYSTEM = "system"
    USER = "user"
    ASSISTANT = "assistant"
    TOOL = "tool"


@dataclass
class Message:
    """
    Represents a single message in a conversation.

    An assistant message may carry tool_calls.
    A tool message must carry the tool_call_id it answers.
    """

    role: Role

    content: str = ""

    tool_calls: list[ToolCall] = field(default_factory=list)

    tool_call_id: str = ""
