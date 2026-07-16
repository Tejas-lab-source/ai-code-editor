# llm/client.py

from openai import OpenAI

from config import Config
from llm.messages import MessageFormatter
from llm.response import ResponseParser
from llm.schemas import LLMResponse
from models.message import Message


class LLMClient:
    """
    Handles communication with the LLM provider.

    Groq is OpenAI-compatible, so the official openai SDK talks to it with
    nothing but a base_url swap. Nothing outside this package knows or cares
    which provider is behind it.
    """

    # OpenAI reasoning models reject any temperature other than the default.
    MODELS_WITHOUT_TEMPERATURE = ("gpt-5", "o1", "o3", "o4")

    # Groq's non-GPT-OSS reasoning models default to reasoning_format="raw",
    # which is rejected with a 400 when tools are supplied. GPT-OSS models do
    # not accept reasoning_format at all, so they must not be listed here.
    MODELS_NEEDING_REASONING_FORMAT = ("qwen/",)

    def __init__(self, config: Config):
        """
        Initialize the LLM client.
        """

        self._client = OpenAI(
            api_key=config.api_key,
            base_url=config.base_url or None,
        )

        self._model = config.model
        self._temperature = config.temperature

    def generate(
        self,
        messages: list[Message],
        tools: list[dict] | None = None,
    ) -> LLMResponse:
        """
        Send messages to the LLM and return a parsed response.
        """

        request: dict = {
            "model": self._model,
            "messages": MessageFormatter.format_messages(messages),
        }

        if self._supports_temperature():
            request["temperature"] = self._temperature

        if tools:
            request["tools"] = tools
            request["tool_choice"] = "auto"

            if self._needs_reasoning_format():
                # reasoning_format is a Groq extension, so it has to travel in
                # extra_body: the openai SDK rejects unknown keyword arguments.
                request["extra_body"] = {"reasoning_format": "hidden"}

        response = self._client.chat.completions.create(**request)

        return ResponseParser.parse_openai(response)

    def _supports_temperature(self) -> bool:
        """
        True when the configured model accepts a custom temperature.
        """

        return not self._model.startswith(self.MODELS_WITHOUT_TEMPERATURE)

    def _needs_reasoning_format(self) -> bool:
        """
        True when the model needs reasoning_format pinned for tool calls.
        """

        return self._model.startswith(self.MODELS_NEEDING_REASONING_FORMAT)
