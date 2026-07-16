# agent/controller.py

from agent.brain import Brain
from agent.context import ContextBuilder
from agent.executor import Executor
from agent.history import History
from agent.memory import Memory
from agent.planner import Planner
from agent.state import StateManager
from models.agent_state import AgentStatus
from models.message import Message, Role
from models.tool_call import ToolCall
from tools.registry import ToolRegistry


class AgentController:
    """
    Coordinates the complete AI Agent workflow.

    This is the reasoning loop: think, act, observe, repeat, until the Brain
    answers without asking for a tool or the iteration budget runs out.

    The Controller coordinates. It never reasons.
    """

    def __init__(
        self,
        brain: Brain,
        history: History,
        memory: Memory,
        context_builder: ContextBuilder,
        state_manager: StateManager,
        executor: Executor,
        registry: ToolRegistry,
        max_iterations: int = 10,
        planner: Planner | None = None,
    ):
        self._brain = brain
        self._history = history
        self._memory = memory
        self._context = context_builder
        self._state = state_manager
        self._executor = executor
        self._registry = registry
        self._max_iterations = max_iterations
        self._planner = planner

    def run(self, user_input: str) -> str:
        """
        Process one user request and return the final answer.
        """

        self._start_task(user_input)

        tool_schemas = self._registry.get_schemas()

        for _ in range(self._max_iterations):

            self._state.increment_iteration()
            self._state.set_status(AgentStatus.THINKING)

            response = self._brain.think(
                self._context.build(),
                tools=tool_schemas,
            )

            self._history.add(
                Message(
                    role=Role.ASSISTANT,
                    content=response.content,
                    tool_calls=response.tool_calls,
                )
            )

            if not response.has_tool_calls:
                self._state.set_status(AgentStatus.FINISHED)
                return response.content

            self._state.set_status(AgentStatus.EXECUTING)
            self._execute_tool_calls(response.tool_calls)
            self._state.set_status(AgentStatus.OBSERVING)

        self._state.set_status(AgentStatus.ERROR)

        return (
            f"Stopped after {self._max_iterations} iterations without "
            "reaching a final answer. Try a smaller task or raise "
            "MAX_ITERATIONS."
        )

    def _start_task(self, user_input: str) -> None:
        """
        Reset the per-task state and record the request.
        """

        self._state.reset()
        self._state.set_task(user_input)

        self._history.add(
            Message(
                role=Role.USER,
                content=user_input,
            )
        )

        if self._planner is None:
            return

        self._state.set_status(AgentStatus.PLANNING)

        plan = self._planner.create_plan(user_input)

        self._history.add(
            Message(
                role=Role.SYSTEM,
                content=f"Execution plan for the current task:\n{plan}",
            )
        )

    def _execute_tool_calls(self, tool_calls: list[ToolCall]) -> None:
        """
        Run every requested tool and feed the results back to the Brain.

        Every tool call must be answered by a tool message carrying the same
        id, otherwise the next request to the provider is rejected.
        """

        for tool_call in tool_calls:

            result = self._executor.execute(tool_call)

            self._history.add(
                Message(
                    role=Role.TOOL,
                    content=result.content,
                    tool_call_id=result.tool_call_id,
                )
            )
