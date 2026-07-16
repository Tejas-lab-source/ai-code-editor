# agent/parser.py

import json
import re

from agent.exceptions import ParserError
from models.tool_call import ToolCall


class Parser:
    """
    Converts raw LLM text into structured objects.

    The primary path uses native provider tool calls, which arrive already
    structured. This parser is the fallback for models that describe a tool
    call as JSON inside their text answer.
    """

    JSON_BLOCK = re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.DOTALL)

    def parse_tool_call(self, response_text: str) -> ToolCall:
        """
        Parse a JSON tool call returned by the LLM.
        """

        data = self._extract_json(response_text)

        tool_name = data.get("tool") or data.get("tool_name")

        if not tool_name:
            raise ParserError(
                "Tool call JSON is missing the 'tool' field."
            )

        arguments = data.get("arguments", {})

        if not isinstance(arguments, dict):
            raise ParserError(
                "Tool call 'arguments' must be a JSON object."
            )

        return ToolCall(
            tool_name=str(tool_name),
            arguments=arguments,
        )

    def _extract_json(self, response_text: str) -> dict:
        """
        Pull a JSON object out of the response text.
        """

        candidate = (response_text or "").strip()

        match = self.JSON_BLOCK.search(candidate)

        if match:
            candidate = match.group(1)

        try:
            data = json.loads(candidate)

        except json.JSONDecodeError as error:
            raise ParserError(
                f"LLM output is not valid JSON: {error}"
            ) from error

        if not isinstance(data, dict):
            raise ParserError(
                "LLM output must be a JSON object."
            )

        return data
