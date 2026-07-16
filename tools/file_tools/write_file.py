# tools/file_tools/write_file.py

from pathlib import Path

from tools.base_tool import BaseTool


class WriteFileTool(BaseTool):
    """
    Writes text to a file, creating it when it does not exist.
    """

    @property
    def name(self) -> str:
        return "write_file"

    @property
    def description(self) -> str:
        return (
            "Write text to a file, replacing its contents. "
            "Creates the file and any missing parent folders."
        )

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path of the file to write.",
                },
                "content": {
                    "type": "string",
                    "description": "Full new content of the file.",
                },
            },
            "required": ["path", "content"],
        }

    def execute(self, path: str, content: str) -> str:
        """
        Write content to a file.
        """

        file_path = Path(path)

        if file_path.is_dir():
            raise IsADirectoryError(f"Not a file: {path}")

        file_path.parent.mkdir(parents=True, exist_ok=True)

        file_path.write_text(content, encoding="utf-8")

        return f"Successfully wrote {len(content)} characters to {path}"
