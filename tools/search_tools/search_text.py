# tools/search_tools/search_text.py

from tools.base_tool import BaseTool, is_ignored, require_directory


class SearchTextTool(BaseTool):
    """
    Search for text and return matching files with a preview line.
    """

    MAX_RESULTS = 50

    @property
    def name(self) -> str:
        return "search_text"

    @property
    def description(self) -> str:
        return (
            "Find which files contain a text query, case insensitive. "
            "Returns one preview line per file."
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
                "query": {
                    "type": "string",
                    "description": "Text to look for.",
                },
            },
            "required": ["path", "query"],
        }

    def execute(self, path: str, query: str) -> str:
        """
        Return the first matching line of every matching file.
        """

        root = require_directory(path)

        needle = query.lower()

        results: list[str] = []

        for file in sorted(root.rglob("*")):

            if not file.is_file() or is_ignored(file, root):
                continue

            try:
                lines = file.read_text(encoding="utf-8").splitlines()

            except (OSError, UnicodeDecodeError):
                continue

            for line in lines:

                if needle in line.lower():

                    relative = file.relative_to(root)

                    results.append(f"{relative}\n{line.strip()}")

                    break

            if len(results) >= self.MAX_RESULTS:
                results.append("[truncated: too many files matched]")
                break

        if not results:
            return f"No files contain '{query}'."

        return "\n-----------------\n".join(results)
