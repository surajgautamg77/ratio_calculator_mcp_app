import asyncio
import os

from google import genai
from google.genai import types
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

MCP_SERVER_URL = "http://localhost:8000/mcp"

gemini_client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])


def mcp_tool_to_gemini_declaration(tool) -> types.FunctionDeclaration:
    return types.FunctionDeclaration(
        name=tool.name,
        description=tool.description or "",
        parameters=tool.inputSchema,
    )


async def call_mcp_tool(session: ClientSession, name: str, args: dict) -> str:
    try:
        result = await session.call_tool(name, args)
        return result.content[0].text
    except Exception as e:
        return f"Error: {e}"


async def main():
    async with streamable_http_client(MCP_SERVER_URL) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            mcp_tools = (await session.list_tools()).tools
            declarations = [mcp_tool_to_gemini_declaration(t) for t in mcp_tools]
            gemini_tool = types.Tool(function_declarations=declarations)

            print("Connected. Available tools:", [t.name for t in mcp_tools])

            chat = gemini_client.chats.create(
                model="gemini-3.5-flash",
                config=types.GenerateContentConfig(tools=[gemini_tool]),
            )

            print("Type a math question (or 'exit' to quit).")

            while True:
                user_input = input("\nYou: ").strip()
                if user_input.lower() in ("exit", "quit"):
                    break

                response = chat.send_message(user_input)

                # Keep resolving tool calls until Gemini gives a final text answer
                while response.function_calls:
                    function_response_parts = []
                    for fc in response.function_calls:
                        print(f"  [calling tool: {fc.name}({dict(fc.args)})]")
                        result_text = await call_mcp_tool(session, fc.name, dict(fc.args))
                        function_response_parts.append(
                            types.Part.from_function_response(
                                name=fc.name,
                                response={"result": result_text},
                            )
                        )
                    response = chat.send_message(function_response_parts)

                print(f"Gemini: {response.text}")


if __name__ == "__main__":
    asyncio.run(main())