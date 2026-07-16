# tools/terminal_tools/git.py

import subprocess

from tools.base_tool import BaseTool


class GitTool(BaseTool):
    """
    Execute safe, read-only Git operations.
    """

    TIMEOUT = 30

    COMMANDS: dict[str, list[str]] = {
        "status": ["git", "status", "--short", "--branch"],
        "branch": ["git", "branch", "--all"],
        "log": ["git", "log", "--oneline", "-10"],
        "diff": ["git", "diff"],
        "diff_staged": ["git", "diff", "--staged"],
        "show": ["git", "show", "--stat", "HEAD"],
    }

    @property
    def name(self) -> str:
        return "git"

    @property
    def description(self) -> str:
        allowed = ", ".join(sorted(self.COMMANDS))

        return f"Run a read-only Git command. Allowed operations: {allowed}."

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "operation": {
                    "type": "string",
                    "enum": sorted(self.COMMANDS),
                    "description": "Which Git command to run.",
                },
                "cwd": {
                    "type": "string",
                    "description": "Repository directory.",
                },
            },
            "required": ["operation"],
        }

    def execute(
        self,
        operation: str,
        cwd: str | None = None,
    ) -> str:
        """
        Execute a Git operation.
        """

        if operation not in self.COMMANDS:
            raise ValueError(
                f"Unsupported Git operation: '{operation}'. "
                f"Allowed: {', '.join(sorted(self.COMMANDS))}"
            )

        completed = subprocess.run(
            self.COMMANDS[operation],
            cwd=cwd,
            capture_output=True,
            text=True,
            timeout=self.TIMEOUT,
        )

        if completed.returncode != 0:
            raise RuntimeError(
                completed.stderr.strip() or f"git {operation} failed"
            )

        return completed.stdout.strip() or "(no output)"
