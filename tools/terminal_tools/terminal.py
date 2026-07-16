# tools/terminal_tools/terminal.py

import subprocess

from tools.base_tool import BaseTool


class TerminalTool(BaseTool):
    """
    Execute terminal commands.
    """

    DEFAULT_TIMEOUT = 120

    MAX_OUTPUT_CHARACTERS = 20_000

    @property
    def name(self) -> str:
        return "terminal"

    @property
    def description(self) -> str:
        return (
            "Run a shell command and return its exit code, stdout and stderr. "
            "A non-zero exit code is reported, not raised."
        )

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The shell command to run.",
                },
                "cwd": {
                    "type": "string",
                    "description": "Directory to run the command in.",
                },
                "timeout": {
                    "type": "integer",
                    "description": "Timeout in seconds. Defaults to 120.",
                },
            },
            "required": ["command"],
        }

    def execute(
        self,
        command: str,
        cwd: str | None = None,
        timeout: int = DEFAULT_TIMEOUT,
    ) -> str:
        """
        Execute a terminal command.

        A failing command is a normal observation for the agent, so the exit
        code is returned as text instead of raising. Only a timeout raises.
        """

        try:
            completed = subprocess.run(
                command,
                shell=True,
                cwd=cwd,
                capture_output=True,
                text=True,
                timeout=timeout,
            )

        except subprocess.TimeoutExpired as error:
            raise TimeoutError(
                f"Command timed out after {timeout} seconds: {command}"
            ) from error

        return self._format_result(
            exit_code=completed.returncode,
            stdout=completed.stdout,
            stderr=completed.stderr,
        )

    def _format_result(
        self,
        exit_code: int,
        stdout: str,
        stderr: str,
    ) -> str:
        """
        Build a readable report of a finished command.
        """

        sections = [f"exit_code: {exit_code}"]

        if stdout.strip():
            sections.append(f"stdout:\n{self._truncate(stdout.strip())}")

        if stderr.strip():
            sections.append(f"stderr:\n{self._truncate(stderr.strip())}")

        if len(sections) == 1:
            sections.append("(no output)")

        return "\n\n".join(sections)

    def _truncate(self, text: str) -> str:
        """
        Keep command output small enough for the context window.
        """

        if len(text) <= self.MAX_OUTPUT_CHARACTERS:
            return text

        return text[: self.MAX_OUTPUT_CHARACTERS] + "\n[truncated]"
