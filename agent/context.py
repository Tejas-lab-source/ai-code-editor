# agent/context.py

from agent.history import History
from agent.memory import Memory
from agent.prompts import PromptManager
from models.message import Message, Role


class ContextBuilder:
    """
    Builds the context that will be sent to the Brain.
    """

    def __init__(
        self,
        history: History,
        memory: Memory,
        workspace: str = ".",
    ):
        self._history = history
        self._memory = memory
        self._workspace = workspace

    def build(self) -> list[Message]:
        """
        Combine system prompt, memory and history into one message list.
        """

        context: list[Message] = [
            Message(
                role=Role.SYSTEM,
                content=self._build_system_prompt(),
            )
        ]

        memory_message = self._build_memory_message()

        if memory_message is not None:
            context.append(memory_message)

        context.extend(self._history.get_messages())

        return context

    def _build_system_prompt(self) -> str:
        """
        Return the system prompt plus workspace information.
        """

        return (
            f"{PromptManager.get_system_prompt()}\n\n"
            f"The workspace directory is: {self._workspace}\n"
            "Use paths relative to that directory unless told otherwise."
        )

    def _build_memory_message(self) -> Message | None:
        """
        Render long-term memory as a system message, if there is any.
        """

        memories = self._memory.get_all()

        if not memories:
            return None

        memory_text = "\n".join(
            f"{key}: {value}"
            for key, value in memories.items()
        )

        return Message(
            role=Role.SYSTEM,
            content=f"Known information:\n{memory_text}",
        )
