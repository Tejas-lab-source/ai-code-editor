# tools/executor.py

from models.tool_result import ToolResult
from tools.base_tool import BaseTool


class ToolExecutor:
    """
    Executes a concrete tool and normalises the outcome.

    This is the only place where a tool exception becomes a ToolResult.
    """

    def execute(
        self,
        tool: BaseTool,
        arguments: dict | None = None,
    ) -> ToolResult:
        """
        Execute the given tool with the given arguments.
        """

        arguments = arguments or {}

        try:
            output = tool.execute(**arguments)

        except TypeError as error:
            return ToolResult(
                success=False,
                error=f"Invalid arguments for '{tool.name}': {error}",
            )

        except Exception as error:
            return ToolResult(
                success=False,
                error=f"{type(error).__name__}: {error}",
            )

        return ToolResult(
            success=True,
            output="" if output is None else str(output),
        )
