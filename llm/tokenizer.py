# llm/tokenizer.py

import tiktoken

from config import Config
from models.message import Message


class Tokenizer:
    """
    Handles token counting for LLM conversations.
    """

    FALLBACK_ENCODING = "o200k_base"

    def __init__(self, config: Config):
        """
        Initialize the tokenizer for the configured model.

        tiktoken does not recognise every model name, so unknown models fall
        back to the current default encoding instead of crashing.
        """

        try:
            self._encoding = tiktoken.encoding_for_model(config.model)

        except KeyError:
            self._encoding = tiktoken.get_encoding(self.FALLBACK_ENCODING)

    def count_text(self, text: str) -> int:
        """
        Return the number of tokens in a text string.
        """

        return len(self._encoding.encode(text))

    def count_messages(self, messages: list[Message]) -> int:
        """
        Return an approximate token count for a conversation.
        """

        return sum(
            self.count_text(message.content)
            for message in messages
        )
