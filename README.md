# Python AI Agent (From Scratch)

An autonomous AI Coding Agent in pure Python. No LangChain, no LangGraph, no CrewAI.

## Run

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env             # then put your real OPENAI_API_KEY in it
python main.py
```

```
you> what files are in the workspace?
you> read workspace/README.md and summarise it
you> exit
```

## Tests

```bash
pytest -q
```

## The loop

`AgentController.run()` is the whole agent:

```
user input
    ↓
ContextBuilder  →  system prompt + memory + history
    ↓
Brain.think(messages, tools)      ← LLM decides
    ↓
tool_calls?  ── no ──▶  final answer
    │ yes
    ▼
Executor → Registry → Tool → ToolResult
    ↓
history (role="tool")
    ↓
back to Brain          (repeat, up to MAX_ITERATIONS)
```

The Brain only reasons. Tools only act. The Controller only coordinates.

## Layout

| Folder | Responsibility |
|--------|----------------|
| `models/` | Shared data structures: `Message`, `Conversation`, `ToolCall`, `ToolResult`, `AgentState` |
| `llm/` | The only place that knows OpenAI exists |
| `agent/` | Brain, Controller, Planner, Parser, Executor, Memory, History, Context, State |
| `tools/` | Every executable capability, behind `BaseTool` |
| `prompts/` | Prompt templates as `.txt`, editable without touching code |
| `workspace/` | The project the agent operates on |

## Adding a tool

```python
# tools/file_tools/my_tool.py
from tools.base_tool import BaseTool

class MyTool(BaseTool):
    @property
    def name(self) -> str:
        return "my_tool"

    @property
    def description(self) -> str:
        return "What this does — the LLM reads this to decide when to call it."

    @property
    def parameters(self) -> dict:
        return {
            "type": "object",
            "properties": {"path": {"type": "string", "description": "..."}},
            "required": ["path"],
        }

    def execute(self, path: str) -> str:
        return "..."
```

Then add `MyTool()` to `build_registry()` in `main.py`. Nothing else changes —
that is the Open/Closed Principle doing its job.

## Optional planner

```python
from agent.planner import Planner

AgentController(..., planner=Planner(brain))
```

Costs one extra LLM call per task, so it is off by default.

## Config

Runs on **Groq** by default (OpenAI-compatible endpoint).

| Variable | Default | Notes |
|----------|---------|-------|
| `GROQ_API_KEY` | — | required — https://console.groq.com/keys |
| `BASE_URL` | `https://api.groq.com/openai/v1` | the `/v1` is required |
| `MODEL` | `openai/gpt-oss-120b` | see table below |
| `TEMPERATURE` | `0.2` | low is better for tool use |
| `WORKSPACE` | `./workspace` | |
| `MAX_ITERATIONS` | `10` | tool-loop budget per task |

### Groq models with tool calling

| Model ID | Speed | $ / 1M in-out | Notes |
|----------|-------|---------------|-------|
| `openai/gpt-oss-120b` | ~500 t/s | 0.15 / 0.60 | best tool use — **default** |
| `openai/gpt-oss-20b` | ~1000 t/s | 0.075 / 0.30 | fastest |
| `llama-3.3-70b-versatile` | ~280 t/s | 0.59 / 0.79 | solid, no reasoning field |
| `llama-3.1-8b-instant` | ~560 t/s | 0.05 / 0.08 | cheapest, unreliable at tools |

All are 131k context. Groq rotates its lineup often — `console.groq.com/docs/models`
is the source of truth, and `curl https://api.groq.com/openai/v1/models` lists
what your key can actually reach.

### Switching back to OpenAI

Only the `.env` changes, because the provider is confined to `llm/`:

```env
OPENAI_API_KEY=sk-...
BASE_URL=https://api.openai.com/v1
MODEL=gpt-4o-mini
```

## Warning

Tools accept any path and `terminal` runs arbitrary shell commands. Nothing
confines the agent to `workspace/`. Fine for learning on your own machine —
sandbox it before pointing it at anything you care about.

See `FIXES.md` for what was wrong with the previous version.
