# tests/test_agent.py

import pytest

from agent.exceptions import ParserError
from agent.executor import Executor
from agent.history import History
from agent.memory import Memory
from agent.parser import Parser
from agent.state import StateManager
from models.agent_state import AgentStatus
from models.message import Message, Role
from models.tool_call import ToolCall
from tools.base_tool import BaseTool
from tools.registry import ToolRegistry


class EchoTool(BaseTool):
    """
    Minimal tool used to test the execution path.
    """

    @property
    def name(self) -> str:
        return "echo"

    @property
    def description(self) -> str:
        return "Echo the given text."

    def execute(self, text: str) -> str:
        return text


class ExplodingTool(BaseTool):
    """
    Tool that always fails.
    """

    @property
    def name(self) -> str:
        return "explode"

    @property
    def description(self) -> str:
        return "Always raises."

    def execute(self) -> str:
        raise RuntimeError("boom")


def build_executor() -> Executor:
    registry = ToolRegistry()
    registry.register_all([EchoTool(), ExplodingTool()])
    return Executor(registry)


def test_memory():
    memory = Memory()
    memory.save("language", "python")

    assert memory.get("language") == "python"


def test_memory_clear():
    memory = Memory()
    memory.save("a", "b")
    memory.clear()

    assert memory.get("a") is None


def test_memory_persists_to_disk(tmp_path):
    storage = tmp_path / "cache.json"

    Memory(storage_path=storage).save("project", "py-agent")

    assert Memory(storage_path=storage).get("project") == "py-agent"


def test_history():
    history = History()
    history.add(Message(role=Role.USER, content="Hello"))

    assert len(history.get_messages()) == 1


def test_history_clear():
    history = History()
    history.add(Message(role=Role.USER, content="Hello"))
    history.clear()

    assert history.get_messages() == []


def test_state_manager():
    manager = StateManager()

    manager.set_task("Build AI Agent")
    manager.set_status(AgentStatus.THINKING)
    manager.increment_iteration()

    state = manager.get_state()

    assert state.current_task == "Build AI Agent"
    assert state.status is AgentStatus.THINKING
    assert state.iteration == 1


def test_parser_reads_json_tool_call():
    tool_call = Parser().parse_tool_call(
        '{"tool": "read_file", "arguments": {"path": "README.md"}}'
    )

    assert tool_call.tool_name == "read_file"
    assert tool_call.arguments == {"path": "README.md"}


def test_parser_reads_fenced_json():
    tool_call = Parser().parse_tool_call(
        'Sure!\n```json\n{"tool": "tree", "arguments": {"path": "."}}\n```'
    )

    assert tool_call.tool_name == "tree"


def test_parser_rejects_garbage():
    with pytest.raises(ParserError):
        Parser().parse_tool_call("not json at all")


def test_executor_runs_tool():
    result = build_executor().execute(
        ToolCall(tool_name="echo", arguments={"text": "hi"})
    )

    assert result.success is True
    assert result.output == "hi"


def test_executor_reports_unknown_tool():
    result = build_executor().execute(ToolCall(tool_name="nope"))

    assert result.success is False
    assert "Unknown tool" in result.error


def test_executor_reports_tool_failure():
    result = build_executor().execute(ToolCall(tool_name="explode"))

    assert result.success is False
    assert result.content.startswith("ERROR:")


def test_executor_keeps_tool_call_id():
    tool_call = ToolCall(
        tool_name="echo",
        arguments={"text": "hi"},
        tool_call_id="call_123",
    )

    assert build_executor().execute(tool_call).tool_call_id == "call_123"
