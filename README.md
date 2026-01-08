# My Art Helper

A Reflex web application that prompts for an art medium via dropdown and queries an LLM (via OpenRouter) for materials, practical tips, and upgrade suggestions.

## Setup

- Install dependencies with uv:

```bash
uv sync
```

- Set your OpenRouter API key in the environment (or copy `.env.example` to `.env` and populate):

```bash
export OPENAI_API_KEY="sk-..."
# optional
export OPENAI_API_BASE="https://openrouter.ai/api/v1"
export OPENAI_MODEL="mistralai/mistral-small-creative"
```

## Run

### Web App (broken)
```bash
uv run reflex run
```
The web app will be accessible at `http://localhost:3000`. Select a medium from the dropdown and click "Get Suggestions" to receive AI-powered material recommendations.

### Legacy CLI (recomended)
```bash
uv run main.py
```
Choose a medium and the app will print the LLM's response.

## Debugging & Network Issues

- Enable verbose debug output to see masked info and response status:

```bash
export DEBUG_OPENAI=true
uv run reflex run
```

- If you get a DNS or network error (failed to resolve `api.openrouter.ai`), possible fixes:
	- Ensure your machine has internet/DNS access.
	- Set `HTTP_PROXY`/`HTTPS_PROXY` if you are behind a proxy; `requests` respects these env vars.
	- Use a VPN or different network.
	- As a fallback, you can set `OPENAI_API_KEY` (an OpenAI key) and the app will attempt to use the OpenAI API instead.


Notes

- This project uses the OpenAI-compatible `openai` Python package pointed at the OpenRouter base URL. Ensure your key has access through OpenRouter.
- If you see an error about the API key, confirm `OPENROUTER_API_KEY` is set.
# my-art-helper