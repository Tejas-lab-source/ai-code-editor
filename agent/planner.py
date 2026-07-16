# agent/planner.py

from agent.brain import Brain
from agent.exceptions import BrainError, PlanningError
from agent.prompts import PromptManager
from models.message import Message, Role


class Planner:
    """
    Turns a high level task into a step-by-step plan.

    The Planner produces text only. It never executes anything.
    """

    def __init__(self, brain: Brain):
        self._brain = brain

    def create_plan(self, task: str) -> str:
        """
        Ask the Brain to generate a plan for the task.
        """

        messages = [
            Message(
                role=Role.SYSTEM,
                content=PromptManager.get_planner_prompt(),
            ),
            Message(
                role=Role.USER,
                content=task,
            ),
        ]

        try:
            response = self._brain.think(messages)

        except BrainError as error:
            raise PlanningError(
                f"Could not create a plan: {error}"
            ) from error

        return response.content
