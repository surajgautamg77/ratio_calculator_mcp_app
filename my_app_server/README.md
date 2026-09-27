# Gemini Application Server

This folder contains the FastAPI endpoint, an interactive Gemini command-line client, and a direct MCP smoke-test client. These clients connect to the MCP math server in `mcp_server/`.

## Setup

From the repository root, install the shared dependencies:

```powershell
uv sync
```

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) first if needed. Python 3.13 or newer is required. Add `GEMINI_API_KEY=your-gemini-api-key` to a `.env` file in the repository root; the API and Gemini CLI load it automatically. Keep `.env` private; it is ignored by Git.

## Run the FastAPI app

Keep the MCP server running in a separate terminal:

```powershell
uv run python mcp_server/server.py
```

Then start this app from the repository root:

```powershell
uv run uvicorn my_app_server.api:app --reload --port 8080
```

Open `http://127.0.0.1:8080/docs` to try `POST /query`.

## Run the interactive client

With the MCP server running and `GEMINI_API_KEY` set:

```powershell
uv run python my_app_server/gemini_cli.py
```

## Test the MCP connection directly

With the MCP server running, this client lists and calls the math tools without using Gemini:

```powershell
uv run python my_app_server/mcp_client.py
```

The Gemini API key is read from the environment; do not commit it to source control. See the [project README](../README.md) for the full setup.
