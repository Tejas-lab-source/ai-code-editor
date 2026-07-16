# models/conversation.py

from dataclasses import dataclass, field
from uuid import uuid4

from models.message import Message


@dataclass
class Conversation:
    """
    Represents a conversation between the user and the AI.
    """

    conversation_id: str = field(default_factory=lambda: str(uuid4()))

    messages: list[Message] = field(default_factory=list)

    def add_message(self, message: Message) -> None:
        """
        Add a message to the conversation.
        """

        self.messages.append(message)

    def clear(self) -> None:
        """
        Remove every message.
        """

        self.messages.clear()
