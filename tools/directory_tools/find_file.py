# tools/directory_tools/find_file.py

from tools.base_tool import BaseTool, is_ignored, require_directory


class FindFileTool(BaseTool):
    """
    Searches recursively for files by name.
    """

    @property
    def name(self) -> str:
        return "find_file"

    @property
    def description(self) -> str:
        return (
            "Find files recursively by filename. "
            "The filename may contain glob wildcards such as '*.py'."
        )

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Directory to search in.",
                },
                "filename": {
                    "type": "string",
                    "description": "Filename or glob pattern, e.g. 'config.py'.",
                },
            },
            "required": ["path", "filename"],
        }

    def execute(self, path: str, filename: str) -> str:
        """
        Search for matching files.
        """

        root = require_directory(path)

        matches = sorted(
            str(match.relative_to(root))
            for match in root.rglob(filename)
            if match.is_file() and not is_ignored(match, root)
        )

        if not matches:
            return f"No file matching '{filename}' found."

        return "\n".join(matches)
