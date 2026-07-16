# tools/search_tools/search_function.py

import re

from tools.base_tool import BaseTool, is_ignored, require_directory


class SearchFunctionTool(BaseTool):
    """
    Search for Python function or class definitions.
    """

    @property
    def name(self) -> str:
        return "search_function"

    @property
    def description(self) -> str:
        return "Find where a Python function or class is defined."

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Directory to search in.",
                },
                "symbol": {
                    "type": "string",
                    "description": "Exact function or class name.",
                },
            },
            "required": ["path", "symbol"],
        }

    def execute(self, path: str, symbol: str) -> str:
        """
        Return every definition site of the symbol.
        """

        root = require_directory(path)

        pattern = re.compile(
            rf"^\s*(?:async\s+def|def|class)\s+{re.escape(symbol)}\b"
        )

        matches: list[str] = []

        for file in sorted(root.rglob("*.py")):

            if is_ignored(file, root):
                continue

            try:
                lines = file.read_text(encoding="utf-8").splitlines()

            except (OSError, UnicodeDecodeError):
                continue

            relative = file.relative_to(root)

            matches.extend(
                f"{relative}:{line_number}: {line.strip()}"
                for line_number, line in enumerate(lines, start=1)
                if pattern.search(line)
            )

        if not matches:
            return f"No definition found for '{symbol}'."

        return "\n".join(matches)
