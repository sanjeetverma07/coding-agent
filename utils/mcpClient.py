import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


class MCPClient:

    def __init__(self, url):
        self.url = url
        self.session = None
        self.read_stream = None
        self.write_stream = None
        self.http_context = None

    async def connect(self):
        self.http_context = streamable_http_client(self.url)
        self.read_stream, self.write_stream = (
            await self.http_context.__aenter__()
        )
        self.session = ClientSession(
            self.read_stream,
            self.write_stream
        )
        await self.session.__aenter__()
        await self.session.initialize()
    async def list_tools(self):
        result = await self.session.list_tools()
        return result.tools
    
    async def call_tool(self, name, arguments):

        result = await self.session.call_tool(
            name,
            arguments=arguments
        )

        return result.model_dump()
    async def close(self):
        if self.session:
            await self.session.__aexit__(None, None, None)
        if self.http_context:
            await self.http_context.__aexit__(None, None, None)
            

mcp_client = MCPClient("http://127.0.0.1:8000/mcp")

async def client():
    await mcp_client.connect()
    tools = await mcp_client.list_tools()