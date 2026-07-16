# models/tool_result.py

from dataclasses import dataclass


@dataclass
class ToolResult:
    """
    Represents the result returned by a tool.

    Every tool returns this shape, whether it succeeded or failed.
    """

    success: bool

    output: str = ""

    error: str = ""

    tool_call_id: str = ""

    @property
    def content(self) -> str:
        """
        Return the text that should be shown to the Brain.

        Failures are surfaced as readable text instead of exceptions so the
        Brain can reason about them and recover.
        """

        if self.success:
            return self.output

        return f"ERROR: {self.error}"
