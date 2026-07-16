# tools/directory_tools/list_directory.py

from tools.base_tool import BaseTool, require_directory


class ListDirectoryTool(BaseTool):
    """
    Lists the immediate contents of a directory.
    """

    @property
    def name(self) -> str:
        return "list_directory"

    @property
    def description(self) -> str:
        return "List the files and folders directly inside a directory."

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path of the directory to list.",
                },
            },
            "required": ["path"],
        }

    def execute(self, path: str) -> str:
        """
        Return the contents of a directory.
        """

        directory = require_directory(path)

        items = sorted(directory.iterdir())

        if not items:
            return "(empty directory)"

        return "\n".join(
            f"{item.name}/" if item.is_dir() else item.name
            for item in items
        )
