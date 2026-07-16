# What was broken and why

Every item below stopped the project from running, or would have stopped the
agent from ever using a tool.

## Fatal — the project could not even import

| # | File | Bug | Fix |
|---|------|-----|-----|
| 1 | `models/message.py` | The file began with a stray `config.model` before the comment. Python evaluates it at import time → `NameError`. This is the red `1` VS Code shows on `message.py`. | Removed. |
| 2 | `main.py` | `from agent.controller import Controller` — the class is called `AgentController`. → `ImportError`. | Import `AgentController`. |
| 3 | `main.py` | `Brain(config)` — `Brain.__init__` takes an `LLMClient`, not a `Config`. | `Brain(LLMClient(config))`. |
| 4 | `main.py` | `Controller(brain, memory, config)` — the real signature needs `history`, `context_builder`, `state_manager`. | Full wiring in `build_controller()`. |
| 5 | `main.py` | `controller.run()` called with no arguments; `run()` requires `user_input`. | REPL loop passes the user's input. |
| 6 | `llm/client.py` | `MessageFormatter.format(messages)` — that method does not exist; it is `format_messages`. → `AttributeError` on the first LLM call. | Calls `format_messages`. |

## Fatal — no agent loop existed

| # | Bug | Fix |
|---|-----|-----|
| 7 | `AgentController.run()` called the Brain **once** and returned. The Parser, Executor, Registry and all 16 tools were unreachable dead code. This is why the agent "does nothing". | `run()` is now a real think → act → observe loop bounded by `max_iterations`. |
| 8 | Tools were never sent to the model. Without a `tools=[...]` parameter, OpenAI cannot request a tool, so `tool_calls` was always empty. | `BaseTool.to_schema()` + `ToolRegistry.get_schemas()`; the client sends them. |
| 9 | `Message` had no `tool_calls` / `tool_call_id` fields, so a tool result could never be sent back. | Added both fields; `MessageFormatter` emits assistant `tool_calls` and `role: "tool"` messages. |
| 10 | `ResponseParser` passed raw OpenAI tool-call objects straight through, leaking the SDK into every layer. | Converted into our own `ToolCall` objects, keeping the provider's `id` — the id **must** be echoed back or the next request is rejected. |

## Configuration / runtime

| # | Bug | Fix |
|---|-----|-----|
| 11 | `.env` set `MODEL=gpt-5` **and** `TEMPERATURE=0.7`. gpt-5 and the o-series reject any non-default temperature → 400 error on every call. | Client omits `temperature` for those models; `.env.example` defaults to `gpt-4o-mini`. |
| 12 | `tiktoken.encoding_for_model("gpt-5")` raises `KeyError` for unknown model names. | Falls back to `o200k_base`. |
| 13 | `requirements.txt` listed `pydantic` and `typing-extensions`, which nothing imports. | Removed. |

## Design bugs that would bite later

| # | Bug | Fix |
|---|-----|-----|
| 14 | `agent/exceptions.py` defined `MemoryError`, shadowing the Python builtin. | Renamed `AgentMemoryError`. |
| 15 | `ToolRegistry.get_tool` raised `ValueError`, not the `ToolNotFoundError` that was defined for exactly that purpose. | Raises `ToolNotFoundError`. |
| 16 | `agent/executor.py` and `tools/executor.py` were two unrelated executors with different return types. | `ToolExecutor` (tools) runs a tool and normalises errors into `ToolResult`. `Executor` (agent) resolves `ToolCall → tool` and delegates. One job each. |
| 17 | `AnalyzeProjectTool` called `self.executor.execute(tool, path=path)` and treated the result as a string — the new signature returns a `ToolResult`. Its `statistics` lookup also crashed if the tool wasn't registered. | Uses `ToolResult.content`. |
| 18 | `TerminalTool` **raised** on any non-zero exit code. `pytest` finding a failing test would look like a crash instead of an observation. | Returns exit code + stdout + stderr as text. Added a timeout and output truncation. |
| 19 | `TreeTool` / `GrepTool` / `StatisticsTool` walked `.venv`, `.git`, `node_modules`, `__pycache__` — thousands of files straight into the context window. | Shared `IGNORED_DIRECTORIES` + `max_depth` on `tree`, result caps on `grep` / `search_text`, truncation on `read_file`. |
| 20 | `WriteFileTool` refused to write unless the file already existed, forcing `create_file` before every write. | Creates the file and any missing parents. |
| 21 | `agent/context.py` hard-coded its system prompt while `PromptManager` and `prompts/*.txt` sat unused. | `PromptManager` loads `prompts/*.txt` with a built-in fallback. |
| 22 | `Memory` was in-process only; `memory/cache.json` was never touched. | Optional JSON persistence via `Memory(storage_path=...)`. |
| 23 | `Parser` crashed on fenced ```json blocks and raised bare `JSONDecodeError`. | Handles fences, raises `ParserError`. |
| 24 | `tools/*/` subpackages had no `__init__.py`. | Added. |
| 25 | Tests called tools with the old signatures and never covered the loop. | Rewritten: 34 tests, all passing. |

## Deliberate design notes

- **`ToolResult.content`** renders failures as `ERROR: ...` text. Tool failures are
  observations the Brain should reason about, not exceptions that kill the run.
- **`Planner` is optional.** Pass `planner=Planner(brain)` to `AgentController` to
  get a plan injected before the loop. It costs one extra LLM call, so it is off
  by default.
- **Not fixed on purpose:** tools accept any absolute path — nothing confines them
  to `workspace/`. `TerminalTool` runs arbitrary shell commands. That is fine for a
  learning project on your own machine; sandbox it before pointing this at anything
  you care about.
