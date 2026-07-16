# tests/test_tools.py

from pathlib import Path

from tools.directory_tools.find_file import FindFileTool
from tools.directory_tools.list_directory import ListDirectoryTool
from tools.directory_tools.tree import TreeTool
from tools.file_tools.append_file import AppendFileTool
from tools.file_tools.create_file import CreateFileTool
from tools.file_tools.delete_file import DeleteFileTool
from tools.file_tools.read_file import ReadFileTool
from tools.file_tools.write_file import WriteFileTool
from tools.project_tools.statistics import StatisticsTool
from tools.project_tools.summarize import SummarizeTool
from tools.search_tools.grep import GrepTool
from tools.search_tools.search_function import SearchFunctionTool
from tools.search_tools.search_text import SearchTextTool
from tools.terminal_tools.terminal import TerminalTool


def test_create_file(tmp_path):
    path = tmp_path / "test.txt"

    CreateFileTool().execute(str(path))

    assert path.exists()


def test_write_and_read(tmp_path):
    path = tmp_path / "hello.txt"

    WriteFileTool().execute(path=str(path), content="Hello World")

    assert ReadFileTool().execute(path=str(path)) == "Hello World"


def test_write_creates_missing_parents(tmp_path):
    path = tmp_path / "src" / "deep" / "hello.txt"

    WriteFileTool().execute(path=str(path), content="Hi")

    assert path.read_text(encoding="utf-8") == "Hi"


def test_append(tmp_path):
    path = tmp_path / "notes.txt"

    WriteFileTool().execute(path=str(path), content="Hello")
    AppendFileTool().execute(path=str(path), content="\nWorld")

    assert "World" in ReadFileTool().execute(path=str(path))


def test_delete(tmp_path):
    path = tmp_path / "temp.txt"

    CreateFileTool().execute(str(path))
    DeleteFileTool().execute(str(path))

    assert not path.exists()


def test_list_directory(tmp_path):
    (tmp_path / "a.py").touch()
    (tmp_path / "b.py").touch()

    output = ListDirectoryTool().execute(str(tmp_path))

    assert "a.py" in output
    assert "b.py" in output


def test_tree(tmp_path):
    source = tmp_path / "src"
    source.mkdir()
    (source / "main.py").touch()

    output = TreeTool().execute(str(tmp_path))

    assert "main.py" in output


def test_tree_skips_ignored_directories(tmp_path):
    cache = tmp_path / "__pycache__"
    cache.mkdir()
    (cache / "junk.pyc").touch()

    output = TreeTool().execute(str(tmp_path))

    assert "junk.pyc" not in output


def test_find_file(tmp_path):
    backend = tmp_path / "backend"
    backend.mkdir()
    (backend / "config.py").touch()

    output = FindFileTool().execute(path=str(tmp_path), filename="config.py")

    assert "config.py" in output


def test_grep(tmp_path):
    (tmp_path / "app.py").write_text("# TODO: fix login\n", encoding="utf-8")

    output = GrepTool().execute(path=str(tmp_path), pattern="TODO")

    assert "app.py:1" in output


def test_search_text(tmp_path):
    (tmp_path / "notes.md").write_text("Hello Agent\n", encoding="utf-8")

    output = SearchTextTool().execute(path=str(tmp_path), query="agent")

    assert "notes.md" in output


def test_search_function(tmp_path):
    (tmp_path / "service.py").write_text(
        "def login(user):\n    return user\n",
        encoding="utf-8",
    )

    output = SearchFunctionTool().execute(path=str(tmp_path), symbol="login")

    assert "service.py:1" in output


def test_statistics(tmp_path):
    (tmp_path / "a.py").write_text("x = 1\n", encoding="utf-8")

    output = StatisticsTool().execute(str(tmp_path))

    assert "Total Files: 1" in output
    assert ".py: 1" in output


def test_summarize_detects_python(tmp_path):
    (tmp_path / "requirements.txt").touch()

    output = SummarizeTool().execute(str(tmp_path))

    assert "Python" in output


def test_terminal_reports_exit_code_instead_of_raising():
    output = TerminalTool().execute(command="exit 3")

    assert "exit_code: 3" in output


def test_terminal_captures_stdout():
    output = TerminalTool().execute(command="echo hello")

    assert "hello" in output


def test_tool_schema_shape():
    schema = ReadFileTool().to_schema()

    assert schema["type"] == "function"
    assert schema["function"]["name"] == "read_file"
    assert "path" in schema["function"]["parameters"]["properties"]
