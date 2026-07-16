# tools/search_tools/grep.py

from pathlib import Path

from tools.base_tool import BaseTool, is_ignored, require_directory


class GrepTool(BaseTool):
    """
    Search recursively for text inside files.
    """

    MAX_MATCHES = 200

    @property
    def name(self) -> str:
        return "grep"

    @property
    def description(self) -> str:
        return (
            "Search recursively for a literal string inside files and return "
            "matching lines with their line numbers."
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
                "pattern": {
                    "type": "string",
                    "description": "Literal text to search for.",
                },
                "file_pattern": {
                    "type": "string",
                    "description": "Glob limiting the files, e.g. '*.py'. Defaults to '*'.",
                },
            },
            "required": ["path", "pattern"],
        }

    def execute(
        self,
        path: str,
        pattern: str,
        file_pattern: str = "*",
    ) -> str:
        """
        Search every readable text file for the pattern.
        """

        root = require_directory(path)

        matches: list[str] = []

        for file in sorted(root.rglob(file_pattern)):

            if not file.is_file() or is_ignored(file, root):
                continue

            matches.extend(
                self._search_file(file, root, pattern)
            )

            if len(matches) >= self.MAX_MATCHES:
                matches = matches[: self.MAX_MATCHES]
                matches.append("[truncated: too many matches]")
                break

        if not matches:
            return f"No matches found for '{pattern}'."

        return "\n".join(matches)

    def _search_file(
        self,
        file: Path,
        root: Path,
        pattern: str,
    ) -> list[str]:
        """
        Return every matching line of a single file.
        """

        try:
            lines = file.read_text(encoding="utf-8").splitlines()

        except (OSError, UnicodeDecodeError):
            return []

        relative = file.relative_to(root)

        return [
            f"{relative}:{line_number}: {line.strip()}"
            for line_number, line in enumerate(lines, start=1)
            if pattern in line
        ]
