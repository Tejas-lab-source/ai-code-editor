# tools/project_tools/summarize.py

from pathlib import Path

from tools.base_tool import IGNORED_DIRECTORIES, BaseTool, require_directory


class SummarizeTool(BaseTool):
    """
    Generate a structured project report.
    """

    TECHNOLOGY_MARKERS: dict[str, str] = {
        "requirements.txt": "Python",
        "pyproject.toml": "Python",
        "package.json": "Node.js",
        "Dockerfile": "Docker",
        "docker-compose.yml": "Docker Compose",
        "go.mod": "Go",
        "Cargo.toml": "Rust",
        "pom.xml": "Java / Maven",
    }

    @property
    def name(self) -> str:
        return "summarize"

    @property
    def description(self) -> str:
        return "Summarise the top level layout and detected technologies."

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
        Describe the top level of a project.
        """

        root = require_directory(path)

        folders: list[str] = []
        files: list[str] = []

        for item in sorted(root.iterdir()):

            if item.name in IGNORED_DIRECTORIES:
                continue

            if item.is_dir():
                folders.append(item.name)

            elif item.is_file():
                files.append(item.name)

        report = [f"Project: {root.name}", ""]

        report.extend(
            self._section("Top-Level Directories", folders)
        )

        report.extend(
            self._section("Top-Level Files", files)
        )

        report.extend(
            self._section(
                "Detected Technologies",
                self._detect_technologies(root),
            )
        )

        return "\n".join(report).strip()

    def _detect_technologies(self, root: Path) -> list[str]:
        """
        Look for well known marker files.
        """

        return [
            technology
            for marker, technology in self.TECHNOLOGY_MARKERS.items()
            if (root / marker).exists()
        ]

    def _section(self, title: str, items: list[str]) -> list[str]:
        """
        Render one titled bullet list.
        """

        lines = [f"{title}:"]

        lines.extend(
            f"- {item}"
            for item in items
        )

        if not items:
            lines.append("- (none)")

        lines.append("")

        return lines
