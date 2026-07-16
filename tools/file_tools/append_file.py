# tools/file_tools/append_file.py

from tools.base_tool import BaseTool, require_file


class AppendFileTool(BaseTool):
    """
    Appends text to an existing file.
    """

    @property
    def name(self) -> str:
        return "append_file"

    @property
    def description(self) -> str:
        return "Append text to the end of an existing file."

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path of the file to append to.",
                },
                "content": {
                    "type": "string",
                    "description": "Text appended to the end of the file.",
                },
            },
            "required": ["path", "content"],
        }

    def execute(self, path: str, content: str) -> str:
        """
        Append content to a file.
        """

        file_path = require_file(path)

        with file_path.open("a", encoding="utf-8") as file:
            file.write(content)

        return f"Successfully appended to {path}"
