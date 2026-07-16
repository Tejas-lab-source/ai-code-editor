# tools/directory_tools/tree.py

from pathlib import Path

from tools.base_tool import IGNORED_DIRECTORIES, BaseTool, require_directory


class TreeTool(BaseTool):
    """
    Generates a recursive directory tree.
    """

    DEFAULT_MAX_DEPTH = 3

    @property
    def name(self) -> str:
        return "tree"

    @property
    def description(self) -> str:
        return (
            "Show a directory tree. Dependency and cache folders are skipped."
        )

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Root directory of the tree.",
                },
                "max_depth": {
                    "type": "integer",
                    "description": "How many levels to descend. Defaults to 3.",
                },
            },
            "required": ["path"],
        }

    def execute(
        self,
        path: str = ".",
        max_depth: int = DEFAULT_MAX_DEPTH,
    ) -> str:
        """
        Build a directory tree.
        """

        root = require_directory(path)

        lines = [f"{root.name}/"]

        self._build_tree(
            directory=root,
            lines=lines,
            prefix="",
            depth=1,
            max_depth=max(1, int(max_depth)),
        )

        return "\n".join(lines)

    def _build_tree(
        self,
        directory: Path,
        lines: list[str],
        prefix: str,
        depth: int,
        max_depth: int,
    ) -> None:
        """
        Append one directory level to the tree.
        """

        if depth > max_depth:
            return

        items = [
            item
            for item in sorted(directory.iterdir())
            if item.name not in IGNORED_DIRECTORIES
        ]

        for index, item in enumerate(items):

            is_last = index == len(items) - 1

            connector = "└── " if is_last else "├── "
            suffix = "/" if item.is_dir() else ""

            lines.append(f"{prefix}{connector}{item.name}{suffix}")

            if item.is_dir():

                extension = "    " if is_last else "│   "

                self._build_tree(
                    directory=item,
                    lines=lines,
                    prefix=prefix + extension,
                    depth=depth + 1,
                    max_depth=max_depth,
                )
