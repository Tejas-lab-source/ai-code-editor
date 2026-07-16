# llm/messages.py

import json

from models.message import Message, Role
from models.tool_call import ToolCall


class MessageFormatter:
    """
    Converts internal Message objects into provider-specific dictionaries.

    All OpenAI-shaped formatting lives here so the rest of the project only
    ever speaks in Message objects.
    """

    @staticmethod
    def format_tool_call(tool_call: ToolCall) -> dict:
        """
        Convert a ToolCall into the OpenAI tool_call payload.
        """

        return {
            "id": tool_call.tool_call_id,
            "type": "function",
            "function": {
                "name": tool_call.tool_name,
                "arguments": json.dumps(tool_call.arguments),
            },
        }

    @classmethod
    def format_message(cls, message: Message) -> dict:
        """
        Convert a single Message object.
        """

        if message.role is Role.TOOL:
            return {
                "role": Role.TOOL.value,
                "tool_call_id": message.tool_call_id,
                "content": message.content,
            }

        payload: dict = {
            "role": message.role.value,
            "content": message.content,
        }

        if message.role is Role.ASSISTANT and message.tool_calls:
            # OpenAI expects null content when the turn is only tool calls.
            payload["content"] = message.content or None

            payload["tool_calls"] = [
                cls.format_tool_call(tool_call)
                for tool_call in message.tool_calls
            ]

        return payload

    @classmethod
    def format_messages(cls, messages: list[Message]) -> list[dict]:
        """
        Convert a list of Message objects.
        """

        return [
            cls.format_message(message)
            for message in messages
        ]
