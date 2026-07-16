# models/agent_state.py

from dataclasses import dataclass
from enum import Enum


class AgentStatus(Enum):
    """
    Represents the current status of the AI Agent.
    """

    IDLE = "idle"

    PLANNING = "planning"

    THINKING = "thinking"

    EXECUTING = "executing"

    OBSERVING = "observing"

    FINISHED = "finished"

    ERROR = "error"


@dataclass
class AgentState:
    """
    Stores the current state of the AI Agent.
    """

    status: AgentStatus = AgentStatus.IDLE

    current_task: str = ""

    iteration: int = 0
