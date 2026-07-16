# llm/schemas.py

from dataclasses import dataclass, field

from models.tool_call import ToolCall


@dataclass
class TokenUsage:
    """
    Stores token usage information for an LLM response.
    """

    input_tokens: int = 0
    output_tokens: int = 0
    total_tokens: int = 0


@dataclass
class LLMResponse:
    """
    Standard response object returned by every LLM provider.
    """

    content: str = ""

    model: str = ""

    finish_reason: str = ""

    usage: TokenUsage = field(default_factory=TokenUsage)

    tool_calls: list[ToolCall] = field(default_factory=list)

    response_id: str = ""

    @property
    def has_tool_calls(self) -> bool:
        """
        True when the model asked for at least one tool.
        """

        return bool(self.tool_calls)
