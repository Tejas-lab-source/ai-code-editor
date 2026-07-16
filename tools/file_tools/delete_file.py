# tools/file_tools/delete_file.py

from tools.base_tool import BaseTool, require_file


class DeleteFileTool(BaseTool):
    """
    Deletes an existing file.
    """

    @property
    def name(self) -> str:
        return "delete_file"

    @property
    def description(self) -> str:
        return "Delete an existing file."

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Path of the file to delete.",
                },
            },
            "required": ["path"],
        }

    def execute(self, path: str) -> str:
        """
        Delete a file.
        """

        file_path = require_file(path)

        file_path.unlink()

        return f"Successfully deleted {path}"
