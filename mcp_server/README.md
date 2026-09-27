# MCP Math Server

This folder contains the MCP server exposing `add`, `subtract`, `multiply`, `divide`, and `power`.

## Setup

From the repository root, install the shared dependencies:

```powershell
uv sync
```

Install [uv](https://docs.astral.sh/uv/getting-started/installation/) first if needed. Python 3.13 or newer is required.

## Run

Start the server from the repository root and leave it running:

```powershell
uv run python mcp_server/server.py
```

It listens on `http://localhost:8000/mcp`.

To test its tools, use the [MCP smoke-test client](../my_app_server/mcp_client.py) in `my_app_server/`. See the [project README](../README.md) for the command and for running the Gemini/FastAPI application.
