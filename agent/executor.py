# agent/executor.py

from agent.exceptions import ToolNotFoundError
from models.tool_call import ToolCall
from models.tool_result import ToolResult
from tools.executor import ToolExecutor
from tools.registry import ToolRegistry


class Executor:
    """
    Turns a ToolCall into a ToolResult.

    Resolving the tool is this class's job. Running it safely is delegated to
    the ToolExecutor in the tools layer.
    """

    def __init__(
        self,
        registry: ToolRegistry,
        tool_executor: ToolExecutor | None = None,
    ):
        self._registry = registry
        self._tool_executor = tool_executor or ToolExecutor()

    def execute(self, tool_call: ToolCall) -> ToolResult:
        """
        Execute a tool call.
        """

        try:
            tool = self._registry.get_tool(tool_call.tool_name)

        except ToolNotFoundError as error:
            return ToolResult(
                success=False,
                error=str(error),
                tool_call_id=tool_call.tool_call_id,
            )

        result = self._tool_executor.execute(tool, tool_call.arguments)

        result.tool_call_id = tool_call.tool_call_id

        return result
