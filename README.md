# MCP Math Assistant

A small math MCP server with a FastAPI/Gemini app, an interactive Gemini command-line client, and a direct MCP smoke-test client.

## Requirements

- Python 3.13 or newer
- [uv](https://docs.astral.sh/uv/getting-started/installation/)
- A Gemini API key to use either Gemini client

## Setup

Run these commands from the repository root:

```powershell
uv sync
```

Create a `.env` file in the repository root and add your Gemini API key:

```dotenv
GEMINI_API_KEY=your-gemini-api-key
```

Replace the placeholder with your key. The API and Gemini CLI load this file automatically; `.env` is excluded from Git. A `.env.example` template is included for reference.

## Run the API

Open two terminals in the repository root. Start the MCP server in the first and keep it running:

```powershell
uv run python mcp_server/server.py
```

Start the FastAPI app in the second:

```powershell
uv run uvicorn my_app_server.api:app --reload --port 8080
```

The API is available at `http://127.0.0.1:8080`; interactive API docs are at `http://127.0.0.1:8080/docs`. Send a query to `POST /query` with JSON such as `{"message":"What is 12 times 8?"}`.

## Other Commands

- Test the MCP tools directly: `uv run python my_app_server/mcp_client.py` (requires the MCP server to be running; no Gemini API key needed).
- Run the interactive Gemini client: `uv run python my_app_server/gemini_cli.py` (requires the MCP server and `GEMINI_API_KEY`).

## Folders

- `mcp_server/` contains the math tools exposed by the MCP server. See [its README](mcp_server/README.md).
- `my_app_server/` contains the FastAPI app and clients that consume the MCP server. See [its README](my_app_server/README.md).
