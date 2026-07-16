# tools/base_tool.py

from abc import ABC, abstractmethod
from pathlib import Path

# Directories that are never worth walking into. Shared by every tool that
# scans a project so the agent is not flooded with dependency and cache files.
IGNORED_DIRECTORIES = frozenset(
    {
        ".git",
        ".venv",
        "venv",
        "__pycache__",
        "node_modules",
        ".mypy_cache",
        ".pytest_cache",
        ".ruff_cache",
        "dist",
        "build",
        ".idea",
    }
)


def is_ignored(path: Path, root: Path) -> bool:
    """
    True when any part of the path below root is an ignored directory.
    """

    try:
        relative = path.relative_to(root)

    except ValueError:
        return False

    return any(
        part in IGNORED_DIRECTORIES
        for part in relative.parts
    )


def require_directory(path: str) -> Path:
    """
    Validate that a path points at an existing directory.
    """

    directory = Path(path)

    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {path}")

    if not directory.is_dir():
        raise NotADirectoryError(f"Not a directory: {path}")

    return directory


def require_file(path: str) -> Path:
    """
    Validate that a path points at an existing file.
    """

    file_path = Path(path)

    if not file_path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    if not file_path.is_file():
        raise IsADirectoryError(f"Not a file: {path}")

    return file_path


class BaseTool(ABC):
    """
    Base class for every tool.
    """

    @property
    @abstractmethod
    def name(self) -> str:
        """
        Unique name of the tool.
        """

    @property
    @abstractmethod
    def description(self) -> str:
        """
        Description shown to the LLM.
        """

    @property
    def parameters(self) -> dict:
        """
        JSON schema describing the arguments of execute().

        Tools without arguments can rely on this default.
        """

        return {
            "type": "object",
            "properties": {},
            "required": [],
        }

    @abstractmethod
    def execute(self, **kwargs) -> str:
        """
        Execute the tool and return its output as text.
        """

    def to_schema(self) -> dict:
        """
        Return the tool definition sent to the LLM.
        """

        return {
            "type": "function",
            "function": {
                "name": self.name,
                "description": self.description,
                "parameters": self.parameters,
            },
        }
