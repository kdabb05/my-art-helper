# Copilot Instructions for my-art-helper

## Project Overview
A Reflex web application that allows users to select an art medium via dropdown, then queries an LLM (via OpenRouter API) for materials, practical tips, and budget/upgrade suggestions. The app uses OpenAI-compatible client libraries pointed at external API endpoints, with a modern React-based UI built on Reflex.

## Architecture & Key Files

### Core Components
- **[art_helper/state.py](../art_helper/state.py)** — Reflex State class managing:
  - `mediums` — Static list of supported art mediums
  - `ArtHelperState` — Manages UI state: selected medium, LLM response, loading status, error messages
  - `build_prompt()` — Crafts structured prompt with four required heading sections
  - `fetch_materials()` — Async method that calls OpenRouter API and updates state
  - `set_selected_medium()` — Event handler for dropdown selection

- **[art_helper/pages/index.py](../art_helper/pages/index.py)** — Main UI page containing:
  - `rx.select()` dropdown bound to `ArtHelperState.selected_medium`
  - "Get Suggestions" button triggering `fetch_materials()`
  - Loading indicator via `is_loading` state
  - Error alert display when API fails
  - Results container with `white_space="pre-wrap"` to preserve LLM formatting

- **[rxconfig.py](../rxconfig.py)** — Reflex configuration with app name and database settings
- **[art_helper/__init__.py](../art_helper/__init__.py)** — App entry point; creates Reflex app and registers index page
- **[main.py](../main.py)** — Legacy CLI version (archived; can be removed)

## Critical Workflows

### Run the Web App
```bash
# Install dependencies (includes reflex)
pip install -r requirements.txt

# Start development server (auto-reloads on code changes)
reflex run

# App will be accessible at http://localhost:3000
```

### Environment Setup
The app reads three categories of env variables (same as CLI version):
1. **API Credentials** (required): `OPENAI_API_KEY` — OpenRouter API key
2. **API Configuration** (optional): `OPENAI_API_BASE` (default: `https://openrouter.ai/api/v1`), `OPENAI_MODEL` (default: `mistralai/mistral-small-creative`)
3. **Debugging**: `DEBUG_OPENAI` — Set to `"true"` to log API details

Load `.env` file automatically via `load_dotenv()` from python-dotenv package.

### Testing
```bash
# Run existing CLI tests (legacy)
pytest tests/test_main.py -v

# TODO: Add Reflex component tests (e.g., state mutation, async fetch mocking)
```

## Project-Specific Conventions

### Reflex State Management
- State class inherits from `rx.State` and is located in [art_helper/state.py](../art_helper/state.py)
- State properties automatically become reactive and trigger re-renders
- Async methods (e.g., `fetch_materials()`) handle long-running operations without blocking UI
- Event handlers are methods that accept arguments from UI components (e.g., `set_selected_medium(medium: str)`)

### API Client Pattern (Unchanged from CLI)
- Uses `openai` Python package (OpenAI-compatible) with custom `base_url` parameter for OpenRouter
- **No hardcoded API keys** — All credentials via environment variables with fallback to OpenAI API
- **Error handling**: Try-catch with state-based error messages; no retry logic

### Prompt Engineering
- `build_prompt()` in State returns structured instruction to LLM with explicit heading format requirements
- Output must contain exactly: `'Essential Materials:'`, `'Practical Tips:'`, `'Budget Upgrades:'`, `'Nice-to-Have Upgrades:'` (plain text, specific casing)
- Max tokens set to 600; temperature 0.7 for balanced creativity

### UI Patterns (Reflex-specific)
- **Dropdown**: `rx.select()` with `value` bound to state, `on_change` event triggers handler
- **Loading state**: `rx.button()` has `is_loading` parameter that shows spinner and disables button during async operations
- **Error display**: `rx.alert()` conditionally rendered based on `error_message` state
- **Result display**: `rx.box()` with `white_space="pre-wrap"` preserves LLM response formatting

## Integration Points & Dependencies

### External APIs
- **OpenRouter API** (primary) — OpenAI-compatible endpoint at `https://openrouter.ai/api/v1`
- **OpenAI API** (fallback) — Triggered if `OPENAI_API_KEY` set but `OPENROUTER_API_BASE` not accessible
- Uses `requests` (implicit dependency via `openai` package) which respects `HTTP_PROXY` and `HTTPS_PROXY` env vars

### Dependencies
- `openai>=0.27.0` — LLM client library
- `python-dotenv>=0.21.0` — Load `.env` files
- `requests>=2.28.0` — HTTP transport (used by openai package)
- `pytest>=7.0.0` — Test framework
- `reflex>=0.5.0` — Web framework for reactive UIs

### Known Issues & Workarounds
- DNS/network failures: Check internet connectivity, set proxy env vars if behind firewall, or fallback to OpenAI API
- Hardcoded `MEDIUMS` list — extend via adding items to list in [art_helper/state.py](../art_helper/state.py#L17), no external config

## Code Style & Patterns
- Reflex app split into state management and UI components for clarity
- Input validation in State class methods
- Type hints used in function signatures (e.g., `def set_selected_medium(self, medium: str)`)
- Async operations in State methods prevent UI blocking during API calls
