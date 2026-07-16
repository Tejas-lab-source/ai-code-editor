# main.py

from pathlib import Path

from agent.brain import Brain
from agent.context import ContextBuilder
from agent.controller import AgentController
from agent.exceptions import AgentError
from agent.history import History
from agent.memory import Memory
from agent.state import StateManager
from agent.executor import Executor
from config import Config
from llm.client import LLMClient
from tools.directory_tools.find_file import FindFileTool
from tools.directory_tools.list_directory import ListDirectoryTool
from tools.directory_tools.tree import TreeTool
from tools.file_tools.append_file import AppendFileTool
from tools.file_tools.create_file import CreateFileTool
from tools.file_tools.delete_file import DeleteFileTool
from tools.file_tools.read_file import ReadFileTool
from tools.file_tools.write_file import WriteFileTool
from tools.project_tools.analyze_project import AnalyzeProjectTool
from tools.project_tools.statistics import StatisticsTool
from tools.project_tools.summarize import SummarizeTool
from tools.registry import ToolRegistry
from tools.search_tools.grep import GrepTool
from tools.search_tools.search_function import SearchFunctionTool
from tools.search_tools.search_text import SearchTextTool
from tools.terminal_tools.git import GitTool
from tools.terminal_tools.terminal import TerminalTool

MEMORY_FILE = Path(__file__).resolve().parent / "memory" / "cache.json"


def build_registry() -> ToolRegistry:
    """
    Create the registry and register every tool.
    """

    registry = ToolRegistry()

    registry.register_all(
        [
            ReadFileTool(),
            WriteFileTool(),
            CreateFileTool(),
            AppendFileTool(),
            DeleteFileTool(),
            ListDirectoryTool(),
            TreeTool(),
            FindFileTool(),
            GrepTool(),
            SearchTextTool(),
            SearchFunctionTool(),
            TerminalTool(),
            GitTool(),
            StatisticsTool(),
            SummarizeTool(),
        ]
    )

    # Composed tool: it needs the registry to reuse the tools above.
    registry.register(AnalyzeProjectTool(registry))

    return registry


def build_controller(config: Config) -> AgentController:
    """
    Wire every component together.

    This is the only place that knows how the pieces fit.
    """

    registry = build_registry()

    history = History()
    memory = Memory(storage_path=MEMORY_FILE)

    return AgentController(
        brain=Brain(LLMClient(config)),
        history=history,
        memory=memory,
        context_builder=ContextBuilder(
            history=history,
            memory=memory,
            workspace=config.workspace,
        ),
        state_manager=StateManager(),
        executor=Executor(registry),
        registry=registry,
        max_iterations=config.max_iterations,
    )


def main() -> None:
    """
    Application entry point.
    """

    config = Config.load()

    Path(config.workspace).mkdir(parents=True, exist_ok=True)

    controller = build_controller(config)

    print(f"AI Coding Agent ready. Model: {config.model}")
    print("Type 'exit' to quit.\n")

    while True:

        try:
            user_input = input("you> ").strip()

        except (EOFError, KeyboardInterrupt):
            print()
            break

        if not user_input:
            continue

        if user_input.lower() in {"exit", "quit"}:
            break

        try:
            answer = controller.run(user_input)

        except AgentError as error:
            print(f"\nagent error: {error}\n")
            continue

        print(f"\nagent> {answer}\n")


if __name__ == "__main__":
    main()
