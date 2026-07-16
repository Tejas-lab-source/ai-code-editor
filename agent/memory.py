# agent/memory.py

import json
from pathlib import Path

from agent.exceptions import AgentMemoryError


class Memory:
    """
    Stores important long-term information for the AI Agent.

    When a storage path is given the memory is persisted as JSON, so it
    survives restarts. Without a path it stays purely in process.
    """

    def __init__(self, storage_path: Path | str | None = None):
        self._storage_path = Path(storage_path) if storage_path else None

        self._memory: dict[str, str] = {}

        self._load()

    def save(self, key: str, value: str) -> None:
        """
        Save a memory.
        """

        self._memory[key] = str(value)

        self._persist()

    def get(self, key: str) -> str | None:
        """
        Retrieve a memory by key.
        """

        return self._memory.get(key)

    def get_all(self) -> dict[str, str]:
        """
        Return all stored memories.
        """

        return dict(self._memory)

    def clear(self) -> None:
        """
        Remove every stored memory.
        """

        self._memory.clear()

        self._persist()

    def _load(self) -> None:
        """
        Read the memory file when one is configured.
        """

        if self._storage_path is None or not self._storage_path.is_file():
            return

        try:
            data = json.loads(
                self._storage_path.read_text(encoding="utf-8") or "{}"
            )

        except (OSError, json.JSONDecodeError) as error:
            raise AgentMemoryError(
                f"Could not read memory file {self._storage_path}: {error}"
            ) from error

        if not isinstance(data, dict):
            raise AgentMemoryError(
                f"Memory file {self._storage_path} must contain a JSON object."
            )

        self._memory = {
            str(key): str(value)
            for key, value in data.items()
        }

    def _persist(self) -> None:
        """
        Write the memory file when one is configured.
        """

        if self._storage_path is None:
            return

        try:
            self._storage_path.parent.mkdir(parents=True, exist_ok=True)

            self._storage_path.write_text(
                json.dumps(self._memory, indent=2),
                encoding="utf-8",
            )

        except OSError as error:
            raise AgentMemoryError(
                f"Could not write memory file {self._storage_path}: {error}"
            ) from error
