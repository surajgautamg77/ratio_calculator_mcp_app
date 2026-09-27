# MCP Math Assistant

```text
													 USER
														 |
														 v
							+-----------------------------+
							|           MCP HOST          |
							|                             |
							|  Python app (FastAPI)       |
							|  Domain router              |
							|  - identifies request area  |
							|  - selects that domain      |
							|                             |
							|  Gemini LLM                 |
							|  - receives selected tools  |
							|                             |
							|  MCP CLIENT                 |
							|  - discovers tools          |
							|  - invokes selected tool    |
							+-----------------------------+
														 |
														 | MCP protocol
														 | Streamable HTTP
														 | localhost:8000/mcp
														 v
							+-----------------------------+
							|       ONE MCP SERVER        |
							|                             |
							|  +-----------------------+  |
							|  | MATH (current)        |  |
							|  | add()                 |  |
							|  | subtract()            |  |
							|  | multiply()            |  |
							|  | divide()              |  |
							|  | power()               |  |
							|  +-----------------------+  |
							|                             |
							|  +-----------------------+  |
							|  | FILES (future domain) |  |
							|  | search() · read()     |  |
							|  | write()               |  |
							|  +-----------------------+  |
							|                             |
							|  +-----------------------+  |
							|  | DATABASE (future)     |  |
							|  | query() · get_record()|  |
							|  | update_record()       |  |
							|  +-----------------------+  |
							+-----------------------------+
														 |
														 | Tool result returns to MCP client,
														 | then Gemini creates the response
														 v
													 USER
```

The Math group is implemented in this project. Files and Database are examples of future groups, not existing tools or a configured database. MCP discovery returns a flat tool list; the host can organize that list by naming convention or metadata, route each request to a domain, and give Gemini only that domain's tool definitions. All selected tools are still invoked through the same MCP client and server.

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
