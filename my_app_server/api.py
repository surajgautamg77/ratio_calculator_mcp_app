import json
import os
from contextlib import asynccontextmanager
from fastapi import FastAPI
from dotenv import load_dotenv
from pydantic import BaseModel
from google import genai
from google.genai import types
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

load_dotenv()

MCP_SERVER_URL = "http://localhost:8000/mcp"
gemini_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def mcp_tool_to_gemini_declaration(tool) -> types.FunctionDeclaration:
    return types.FunctionDeclaration(
        name=tool.name,
        description=tool.description or "",
        # `parameters` only accepts Gemini's own (flat) Schema type; MCP
        # tools with nested Pydantic models (e.g. calculate_all_ratios)
        # produce standard JSON Schema with $ref/$defs, which needs the
        # separate `parameters_json_schema` field instead.
        parameters_json_schema=tool.input_schema,
    )


async def call_mcp_tool(session: ClientSession, name: str, args: dict) -> str:
    try:
        result = await session.call_tool(name, args)
        return result.content[0].text
    except Exception as e:
        return f"Error: {e}"


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with streamable_http_client(MCP_SERVER_URL) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            mcp_tools = (await session.list_tools()).tools
            declarations = [mcp_tool_to_gemini_declaration(t) for t in mcp_tools]
            gemini_tool = types.Tool(function_declarations=declarations)

            app.state.mcp_session = session
            app.state.gemini_tool = gemini_tool
            print("Connected to MCP. Tools:", [t.name for t in mcp_tools])

            yield


app = FastAPI(lifespan=lifespan)


class QueryRequest(BaseModel):
    message: str


@app.post("/query")
async def query(req: QueryRequest):
    session: ClientSession = app.state.mcp_session
    gemini_tool = app.state.gemini_tool

    chat = gemini_client.chats.create(
        model="gemini-3.5-flash-lite",
        config=types.GenerateContentConfig(tools=[gemini_tool]),
    )

    response = chat.send_message(req.message)

    tool_calls_made = []
    ratios_report = None

    while response.function_calls:
        function_response_parts = []
        for fc in response.function_calls:
            args = dict(fc.args)
            result_text = await call_mcp_tool(session, fc.name, args)
            tool_calls_made.append({"tool": fc.name, "args": args, "result": result_text})
            if fc.name == "calculate_all_ratios":
                try:
                    ratios_report = json.loads(result_text)
                except json.JSONDecodeError:
                    ratios_report = result_text
            function_response_parts.append(
                types.Part.from_function_response(
                    name=fc.name,
                    response={"result": result_text},
                )
            )
        response = chat.send_message(function_response_parts)

    # calculate_all_ratios already returns a clean, structured report
    # (ratio name -> value, per period/domain, plus "unavailable"); skip
    # Gemini's prose summary and hand that report back directly.
    if ratios_report is not None:
        return {"ratios": ratios_report}

    return {
        "answer": response.text,
        "tool_calls": tool_calls_made,
    } 