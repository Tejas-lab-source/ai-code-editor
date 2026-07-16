# models/tool_call.py

from dataclasses import dataclass, field
from typing import Any
from uuid import uuid4


@dataclass
class ToolCall:
    """
    Represents a single request to execute a tool.

    The tool_call_id is generated locally when the agent creates the call
    itself, but it is overwritten with the provider id when the call comes
    back from the LLM. The provider id must be echoed back to the LLM.
    """

    tool_name: str = ""

    arguments: dict[str, Any] = field(default_factory=dict)

    tool_call_id: str = field(default_factory=lambda: str(uuid4()))
