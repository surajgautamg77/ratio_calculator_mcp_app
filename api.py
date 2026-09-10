from contextlib import asynccontextmanager

from fastapi import FastAPI
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

MCP_SERVER_URL = "http://localhost:8000/mcp"


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with streamable_http_client(MCP_SERVER_URL) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            app.state.mcp_session = session
            yield


app = FastAPI(lifespan=lifespan)


@app.get("/add")
async def add(a: int, b: int):
    result = await app.state.mcp_session.call_tool("add", {"a": a, "b": b})
    return {"result": result.content[0].text}


@app.get("/multiply")
async def multiply(a: int, b: int):
    result = await app.state.mcp_session.call_tool("multiply", {"a": a, "b": b})
    return {"result": result.content[0].text}