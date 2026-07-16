# tools/registry.py

from agent.exceptions import ToolNotFoundError
from tools.base_tool import BaseTool


class ToolRegistry:
    """
    Stores and retrieves all available tools.
    """

    def __init__(self):
        self._tools: dict[str, BaseTool] = {}

    def register(self, tool: BaseTool) -> None:
        """
        Register a new tool.
        """

        self._tools[tool.name] = tool

    def register_all(self, tools: list[BaseTool]) -> None:
        """
        Register several tools at once.
        """

        for tool in tools:
            self.register(tool)

    def get_tool(self, name: str) -> BaseTool:
        """
        Return a tool by name.
        """

        if name not in self._tools:
            raise ToolNotFoundError(
                f"Unknown tool: '{name}'. "
                f"Available tools: {', '.join(sorted(self._tools))}"
            )

        return self._tools[name]

    def list_tools(self) -> list[BaseTool]:
        """
        Return every registered tool.
        """

        return list(self._tools.values())

    def get_schemas(self) -> list[dict]:
        """
        Return the tool definitions sent to the LLM.
        """

        return [
            tool.to_schema()
            for tool in self._tools.values()
        ]
