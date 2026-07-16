# agent/exceptions.py

class AgentError(Exception):
    """
    Base exception for the AI Agent.
    """


class ToolNotFoundError(AgentError):
    """
    Raised when a requested tool does not exist.
    """


class ToolExecutionError(AgentError):
    """
    Raised when a tool fails during execution.
    """


class ParserError(AgentError):
    """
    Raised when LLM output cannot be parsed.
    """


class BrainError(AgentError):
    """
    Raised when the Brain fails to generate a response.
    """


class AgentMemoryError(AgentError):
    """
    Raised when a memory operation fails.

    Deliberately not called MemoryError: that name is a Python builtin and
    shadowing it hides real out-of-memory errors.
    """


class PlanningError(AgentError):
    """
    Raised when planning fails.
    """
