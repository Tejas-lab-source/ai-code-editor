# tools/file_tools/create_file.py

from pathlib import Path

from tools.base_tool import BaseTool


class CreateFileTool(BaseTool):
    """
    Creates a new empty file.
    """

    @property
    def name(self) -> str:
        return "create_file"

    @property
    def description(self) -> str:
        return "Create a new empty file. Fails if the file already exists."

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path of the file to create.",
                },
            },
            "required": ["path"],
        }

    def execute(self, path: str) -> str:
        """
        Create a new file.
        """

        file_path = Path(path)

        if file_path.exists():
            raise FileExistsError(f"File already exists: {path}")

        file_path.parent.mkdir(parents=True, exist_ok=True)

        file_path.touch()

        return f"Successfully created {path}"
