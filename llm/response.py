# llm/response.py

import json

from llm.schemas import LLMResponse, TokenUsage
from models.tool_call import ToolCall


class ResponseParser:
    """
    Converts provider-specific responses into our internal LLMResponse.
    """

    @staticmethod
    def parse_openai(response) -> LLMResponse:
        """
        Parse an OpenAI ChatCompletion response.
        """

        choice = response.choices[0]
        message = choice.message

        return LLMResponse(
            content=message.content or "",
            model=response.model,
            finish_reason=choice.finish_reason or "",
            usage=ResponseParser._parse_usage(response),
            tool_calls=ResponseParser._parse_tool_calls(message),
            response_id=response.id,
        )

    @staticmethod
    def _parse_usage(response) -> TokenUsage:
        """
        Read token usage, which some providers omit.
        """

        usage = getattr(response, "usage", None)

        if usage is None:
            return TokenUsage()

        return TokenUsage(
            input_tokens=usage.prompt_tokens or 0,
            output_tokens=usage.completion_tokens or 0,
            total_tokens=usage.total_tokens or 0,
        )

    @staticmethod
    def _parse_tool_calls(message) -> list[ToolCall]:
        """
        Convert provider tool calls into ToolCall objects.
        """

        raw_tool_calls = getattr(message, "tool_calls", None) or []

        return [
            ToolCall(
                tool_name=raw.function.name,
                arguments=ResponseParser._parse_arguments(raw.function.arguments),
                tool_call_id=raw.id,
            )
            for raw in raw_tool_calls
        ]

    @staticmethod
    def _parse_arguments(raw_arguments: str | None) -> dict:
        """
        Decode the JSON argument string produced by the model.

        Malformed arguments become an empty dict. The tool then fails with a
        readable message the Brain can recover from.
        """

        if not raw_arguments:
            return {}

        try:
            arguments = json.loads(raw_arguments)

        except json.JSONDecodeError:
            return {}

        return arguments if isinstance(arguments, dict) else {}
