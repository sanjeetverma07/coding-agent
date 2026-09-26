import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client

async def main():

    url = "http://127.0.0.1:8000/mcp"

    async with streamable_http_client(url) as (
        read_stream,
        write_stream,
    ):
        async with ClientSession(
            read_stream,
            write_stream
        ) as session:
            # Initialize MCP connection
            await session.initialize()
            # Ask server for its tools
            tools = await session.list_tools()

            print("\nAvailable MCP tools:")
            for tool in tools.tools:
                print(
                    f"- {tool.name}: "
                    f"{tool.description}"
                )
            # result = await session.call_tool(
            #     "list_files",
            #     arguments={
            #         "directory": "."
            #     }
            # )

            # print("\nTool result:")
            # print(result)


if __name__ == "__main__":
    asyncio.run(main())