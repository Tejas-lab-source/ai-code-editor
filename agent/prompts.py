# agent/prompts.py

from pathlib import Path


class PromptManager:
    """
    Loads the prompts used by the AI Agent.

    Prompts live in prompts/*.txt so they can change without touching code.
    A built-in default is used when a file is missing.
    """

    PROMPTS_DIRECTORY = Path(__file__).resolve().parent.parent / "prompts"

    DEFAULT_SYSTEM_PROMPT = (
        "You are an AI Coding Agent.\n"
        "Think carefully before answering.\n"
        "Use the available tools whenever you need real information.\n"
        "Never invent tool output or file contents.\n"
        "Work in small steps and check the result of each step.\n"
        "When the task is done, answer the user in plain text without tools."
    )

    DEFAULT_PLANNER_PROMPT = (
        "You are the planning component of an AI Coding Agent.\n"
        "Your job is not to solve the task.\n"
        "Produce a short numbered execution plan.\n"
        "Never execute tools."
    )

    @classmethod
    def load(cls, name: str, default: str = "") -> str:
        """
        Load a prompt file by name, without the .txt extension.
        """

        prompt_path = cls.PROMPTS_DIRECTORY / f"{name}.txt"

        if not prompt_path.is_file():
            return default

        content = prompt_path.read_text(encoding="utf-8").strip()

        return content or default

    @classmethod
    def get_system_prompt(cls) -> str:
        """
        Return the main system prompt.
        """

        return cls.load("system_prompt", cls.DEFAULT_SYSTEM_PROMPT)

    @classmethod
    def get_planner_prompt(cls) -> str:
        """
        Return the planner prompt.
        """

        return cls.load("planner_prompt", cls.DEFAULT_PLANNER_PROMPT)
