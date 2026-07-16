# agent/state.py

from models.agent_state import AgentState, AgentStatus


class StateManager:
    """
    Manages the current state of the AI Agent.
    """

    def __init__(self):
        self._state = AgentState()

    def get_state(self) -> AgentState:
        """
        Return the current state.
        """

        return self._state

    def set_status(self, status: AgentStatus) -> None:
        """
        Update the agent's status.
        """

        self._state.status = status

    def set_task(self, task: str) -> None:
        """
        Update the current task.
        """

        self._state.current_task = task

    def increment_iteration(self) -> None:
        """
        Increase the iteration count.
        """

        self._state.iteration += 1

    def reset(self) -> None:
        """
        Reset the agent state.
        """

        self._state = AgentState()
