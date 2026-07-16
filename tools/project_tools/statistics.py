# tools/project_tools/statistics.py

from collections import Counter

from tools.base_tool import BaseTool, is_ignored, require_directory


class StatisticsTool(BaseTool):
    """
    Collect statistics about a project.
    """

    @property
    def name(self) -> str:
        return "statistics"

    @property
    def description(self) -> str:
        return "Collect file, directory, size and extension statistics."

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "Root directory of the project.",
                },
            },
            "required": ["path"],
        }

    def execute(self, path: str) -> str:
        """
        Walk the project and summarise what is inside it.
        """

        root = require_directory(path)

        total_files = 0
        total_directories = 0
        total_size = 0

        extensions: Counter[str] = Counter()

        for item in root.rglob("*"):

            if is_ignored(item, root):
                continue

            if item.is_dir():
                total_directories += 1
                continue

            if not item.is_file():
                continue

            total_files += 1

            try:
                total_size += item.stat().st_size

            except OSError:
                pass

            if item.suffix:
                extensions[item.suffix] += 1

        report = [
            f"Total Files: {total_files}",
            f"Total Directories: {total_directories}",
            f"Total Size: {total_size} bytes",
            "",
            "File Extensions:",
        ]

        report.extend(
            f"{extension}: {count}"
            for extension, count in extensions.most_common()
        )

        if not extensions:
            report.append("(none)")

        return "\n".join(report)
