# tools/file_tools/read_file.py

from tools.base_tool import BaseTool, require_file


class ReadFileTool(BaseTool):
    """
    Reads the contents of a text file.
    """

    MAX_CHARACTERS = 40_000

    @property
    def name(self) -> str:
        return "read_file"

    @property
    def description(self) -> str:
        return "Read the contents of a text file."

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path of the file to read.",
                },
            },
            "required": ["path"],
        }

    def execute(self, path: str) -> str:
        """
        Read and return the file contents.
        """

        file_path = require_file(path)

        content = file_path.read_text(encoding="utf-8", errors="replace")

        if len(content) <= self.MAX_CHARACTERS:
            return content

        return (
            content[: self.MAX_CHARACTERS]
            + f"\n\n[truncated: file is {len(content)} characters]"
        )
