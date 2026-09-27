import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

MCP_SERVER_URL = "http://localhost:8000/mcp"


async def main():
    async with streamable_http_client(MCP_SERVER_URL) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            tools = await session.list_tools()
            print("Available tools:", [t.name for t in tools.tools])

            for name, args in [
                ("add", {"a": 2, "b": 3}),
                ("subtract", {"a": 10, "b": 4}),
                ("multiply", {"a": 4, "b": 5}),
                ("divide", {"a": 20, "b": 4}),
                ("power", {"base": 2, "exponent": 8}),
            ]:
                result = await session.call_tool(name, args)
                print(f"{name}{args} = {result.content[0].text}")


if __name__ == "__main__":
    asyncio.run(main())