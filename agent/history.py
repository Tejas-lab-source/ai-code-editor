# agent/history.py

from models.conversation import Conversation
from models.message import Message


class History:
    """
    Stores the complete conversation history in chronological order.
    """

    def __init__(self):
        self._conversation = Conversation()

    def add(self, message: Message) -> None:
        """
        Add a message to the conversation history.
        """

        self._conversation.add_message(message)

    def get_messages(self) -> list[Message]:
        """
        Return every message in chronological order.
        """

        return list(self._conversation.messages)

    def clear(self) -> None:
        """
        Remove the entire conversation history.
        """

        self._conversation.clear()
