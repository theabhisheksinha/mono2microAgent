# Mono2Microagent Crew (Archaion)

Mono2Microagent is a CrewAI “crew” project that generates a modernization blueprint for transforming a monolith into microservices. It can optionally connect to a CAST MCP server (Model Context Protocol over HTTP) to ground the blueprint in deterministic discovery results (DB tables, transaction graphs, ISO 5055 findings).

## Project Layout

```
mono2microagent/
├─ pyproject.toml
├─ uv.lock
└─ src/
   └─ mono2microagent/
      ├─ main.py
      ├─ crew.py
      └─ config/
         ├─ agents.yaml
         └─ tasks.yaml
```

## What Each File Does

### `src/mono2microagent/main.py`

Purpose: entry point used by `crewai run`.

Key responsibilities:
- Defines the input variables (`selected_app`, `tech_stack`, `loc`, `is_mainframe`, `target_cloud`) that are interpolated into your YAML prompts.
- Builds a per-run output file path under `tests/`.
- Exports that output path through `ARCHAION_OUTPUT_FILE` so the task can write the blueprint to a dynamic location.
- Starts the crew by calling `ArchaionCrew().crew().kickoff(inputs=inputs)`.

### `src/mono2microagent/crew.py`

Purpose: CrewAI orchestration (agents + tasks + run configuration).

#### `ArchaionCrew.__init__()`
- Reads model/provider settings from environment variables:
  - `MODEL` (example: `openai/gpt-4o-mini`)
  - `OPENAI_API_KEY` or `OPENROUTER_API_KEY` (OpenRouter keys typically start with `sk-or-`)
  - `OPENAI_BASE_URL` (set to `https://openrouter.ai/api/v1` when using OpenRouter)
- Builds a `crewai.LLM` instance used by the agent.
- Optionally wires a CAST MCP server if both are present:
  - `CAST_ENDPOINT` (MCP HTTP endpoint)
  - `CAST_X_API_KEY` (API key sent as `x-api-key`)
- Applies an MCP tool allowlist (so the agent only “sees” the tools it needs), reducing prompt size:
  - `application_database_explorer`
  - `transaction_graph` / `transaction_graphs`
  - `application_iso_5055_explorer`

#### `ArchaionCrew.mono2microAgent()`
- Creates the single agent from `config/agents.yaml` (`mono2microAgent` key).
- Injects:
  - `llm` (the model configured in `__init__`)
  - `mcps` (CAST MCP server config if present; otherwise none)
  - `verbose=True` (shows run output)
  - `memory=False` (disabled to avoid local storage issues in restricted environments)

#### `ArchaionCrew.refactoring_blueprint_task()`
- Creates the task from `config/tasks.yaml` (`refactoring_blueprint_task` key).
- Writes the output to:
  - `ARCHAION_OUTPUT_FILE` (set by `main.py`), otherwise `refactoring_blueprint.md`

#### `ArchaionCrew.crew()`
- Creates the `Crew` object with:
  - sequential execution
  - verbose output
- Forces CrewAI runtime storage to a local folder (`./.crewai`) in restricted environments so the CLI doesn’t try to write to `~/.config/crewai` or OS AppData locations.

### `src/mono2microagent/config/agents.yaml`

Defines the agent prompt/persona under the key `mono2microAgent`.

Inputs used via interpolation:
- `{selected_app}`, `{tech_stack}`, `{loc}`, `{is_mainframe}`, `{target_cloud}`

### `src/mono2microagent/config/tasks.yaml`

Defines the task prompt under the key `refactoring_blueprint_task`.

The task expects the agent to:
- call CAST MCP tools (if configured) to ground results
- produce a Markdown blueprint, including a cloud provider mapping section

## Environment Variables (`.env`)

CrewAI loads `.env` automatically at runtime.

### Using OpenRouter (recommended)

Create `mono2microagent/.env`:

```env
MODEL=openai/gpt-4o-mini
OPENAI_API_KEY=sk-or-...
OPENAI_BASE_URL=https://openrouter.ai/api/v1
```

### Using OpenAI directly

```env
MODEL=openai/gpt-4o-mini
OPENAI_API_KEY=sk-...
```

### Optional: Enable CAST MCP Tooling

```env
CAST_ENDPOINT=https://your-cast-mcp-server.example.com/mcp
CAST_X_API_KEY=your_cast_key
```

## Install & Run (Windows)

From PowerShell:

```powershell
cd C:\Personal-docs\crewai\mono2microagent

pip install uv

crewai install
crewai run
```

Output:
- A Markdown blueprint is saved under `mono2microagent/tests/` with a filename based on the selected application.

## Install & Run (macOS)

From Terminal:

```bash
cd ~/crewai/mono2microagent

python3 -m pip install uv

crewai install
crewai run
```

## Troubleshooting

### `lancedb` install fails on Windows

Symptom:
- `lancedb==0.30.1 ... doesn't have a source distribution or wheel for the current platform`

Fix:
- This project sets uv’s platform markers in `pyproject.toml` so `uv` resolves a Windows-compatible lancedb build. If you still see the error:
  - run `uv lock` then `crewai install` again
  - confirm you’re running from the `mono2microagent` folder (not another crew folder)

### `ModuleNotFoundError: No module named 'my_project'`

Cause:
- `main.py` imports a package that doesn’t exist in this repo.

Fix:
- Ensure `main.py` imports `mono2microagent.crew`.

### “LLM context length exceeded”

Cause:
- Too many MCP tools (or very large tool schemas) being injected into the prompt.

Fix:
- Keep the MCP tool allowlist in `crew.py` so only the required tools are exposed.

### “Database initialization error: unable to open database file” / `~/.config/crewai` write errors

Cause:
- Some environments disallow writing to user profile paths.

Fix:
- This project redirects CrewAI storage to a local `./.crewai` folder when running the crew, and the agent memory is disabled.
