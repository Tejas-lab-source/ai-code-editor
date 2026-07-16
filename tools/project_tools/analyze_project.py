# tools/project_tools/analyze_project.py

from pathlib import Path

from tools.base_tool import BaseTool
from tools.executor import ToolExecutor
from tools.registry import ToolRegistry


class AnalyzeProjectTool(BaseTool):
    """
    Analyze an entire project by composing existing tools.
    """

    def __init__(
        self,
        registry: ToolRegistry,
        executor: ToolExecutor | None = None,
    ):
        self._registry = registry
        self._executor = executor or ToolExecutor()

    @property
    def name(self) -> str:
        return "analyze_project"

    @property
    def description(self) -> str:
        return (
            "Analyze a software project: directory tree, statistics and README."
        )

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Root directory of the project.",
                },
            },
            "required": ["path"],
        }

    def execute(self, path: str) -> str:
        """
        Produce a combined report about the project.
        """

        tree = self._run("tree", {"path": path})
        statistics = self._run("statistics", {"path": path})
        readme = self._run(
            "read_file",
            {"path": str(Path(path) / "README.md")},
        )

        return (
            "=== PROJECT TREE ===\n"
            f"{tree}\n\n"
            "=== STATISTICS ===\n"
            f"{statistics}\n\n"
            "=== README ===\n"
            f"{readme}"
        )

    def _run(self, tool_name: str, arguments: dict) -> str:
        """
        Run another registered tool and return its text output.
        """

        tool = self._registry.get_tool(tool_name)

        result = self._executor.execute(tool, arguments)

        return result.content
