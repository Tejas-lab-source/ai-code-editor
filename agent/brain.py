# agent/brain.py

from agent.exceptions import BrainError
from llm.client import LLMClient
from llm.schemas import LLMResponse
from models.message import Message


class Brain:
    """
    Responsible for reasoning.

    The Brain decides what should happen next. It never executes tools and it
    never touches the filesystem.
    """

    def __init__(self, llm_client: LLMClient):
        self._llm = llm_client

    def think(
        self,
        messages: list[Message],
        tools: list[dict] | None = None,
    ) -> LLMResponse:
        """
        Ask the LLM to reason about the current context.
        """

        try:
            return self._llm.generate(messages, tools=tools)

        except Exception as error:
            raise BrainError(
                f"The Brain failed to generate a response: {error}"
            ) from error
