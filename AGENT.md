# AGENT.md - Guidelines for AI Coding Agents

This document provides architecture context, conventions, and operational instructions for AI coding agents working on this codebase.

---

## 1. Project Overview

`three-one-agent` is a terminal-based conversational agent built in Python 3.13+ using the official `google-genai` SDK. It integrates tool calling (Function Calling) for persistent user memory and real-time web search.

---

## 2. Architecture & Key Patterns

### 2.1 Google GenAI Client (`src/client/index.py`)

- **API**: Uses the new stateful **Interactions API** (`self.client.interactions.create`).
- **Tool Loop (`ask`)**:
  - The model runs in a `while True` loop until no more `function_call` steps remain in `interaction.steps`.
  - **State continuation**: Subsequent turns in the tool loop MUST pass `previous_interaction_id=interaction.id`. Do NOT re-send the initial user prompt or full conversation arrays as user input.
  - **Tool result format**: When tools are executed, each tool return must be passed as an input step with the following structure:
    ```python
    {
        "type": "function_result",
        "name": fn.name,       # REQUIRED: Name must match the called function
        "call_id": fn.id,      # REQUIRED: ID matching the function call step
        "result": result,      # String, dictionary, or content list
    }
    ```
  - When no `function_call` steps are present, return `interaction.output_text`.

### 2.2 Tools Subsystem (`src/tools/`)

- **Declarations (`src/tools/functions_list.py`)**:
  - `TOOLS` list exporting tool schemas accepted by Google Gemini.
  - Strict JSON schema format with `"strict": True`, `"additionalProperties": False`.
- **Implementations (`src/tools/functions_def.py`)**:
  - `remember(user_id, key, value)`: Stores a key-value pair under the user's namespace in the JSON memory file.
  - `recall(user_id, key)`: Retrieves a key-value pair for the specified user.
  - `web_search(query, max_results)`: Searches the web via `tavily-python`.
  - `run_tool(name, arguments, user_id)`: Central dispatcher matching tool names to implementations.

### 2.3 Configuration (`src/config/env.py`)

- Uses `pydantic-settings` with `.env` file support via `BaseSettings`.
- Centralized singleton `env_variables` exposing:
  - `google_api_key: str`
  - `tavily_api_key: str`
  - `memory_path: str`

### 2.4 CLI Entry Point (`main.py`)

- Runs a multi-turn REPL loop prompting for `user_id` (defaults to `"guest"`).
- Forwards user queries to `client.ask(message, user_id)`.

---

## 3. How to Add a New Tool

When extending the agent with a new capability:

1. **Declare the schema** in `src/tools/functions_list.py`:
   - Add a tool definition dictionary into the `TOOLS` list with name, description, parameters, and required fields.
2. **Implement the function** in `src/tools/functions_def.py`:
   - Write typed function with full docstring (`Args`, `Returns`).
3. **Register in dispatcher**:
   - Add a `case "<tool_name>":` branch inside `run_tool()`.
4. **Update system prompt** (if necessary):
   - Update `INSTRUCTIONS` in `src/client/index.py` so the model knows when to use the tool.

---

## 4. Coding Standards

- **Python Version**: `>= 3.13`. Use modern typing (`int | str`, `list[dict]`, `Final`, etc.).
- **Docstrings**: Google/standard docstrings for public functions and classes with parameter and return descriptions.
- **Error Handling**: Graceful fallbacks for missing environment variables, file I/O errors, or external API failures.
- **Formatting & Linting**:
  - Ruff is configured in `pyproject.toml` (double quotes, space indent, docstring code formatting enabled).
  - Check: `uv run ruff check .`
  - Format: `uv run ruff format .`

---

## 5. Git Commit Conventions

Commits must follow the conventional commit specification with project scopes:

### Commit Format

```text
type(scope): Subject in imperative mood
```

### Valid Scopes

- `agent`: Root files (`pyproject.toml`, `uv.lock`, `main.py`, `.gitignore`)
- `client`: Client logic (`src/client/`)
- `config`: Configuration files (`src/config/`, `.env.sample`)
- `tools`: Tool definitions and schemas (`src/tools/`)
- `memory`: Memory storage handling (`src/memory/`)

### Rules

- Max 50 characters for the subject line.
- Capitalize the first letter of the subject.
- Imperative mood (e.g. `Add`, `Fix`, `Update`, `Refactor`).
- Create atomic commits per logical change.
