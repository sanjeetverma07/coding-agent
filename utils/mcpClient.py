from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


class MCPClient:

    def __init__(self, url):
        self.url = url
        self.session = None
        self.http_context = None

    async def __aenter__(self):
        self.http_context = streamable_http_client(self.url)

        read_stream, write_stream = await self.http_context.__aenter__()

        self.session = ClientSession(
            read_stream,
            write_stream
        )

        await self.session.__aenter__()
        await self.session.initialize()

        return self

    async def __aexit__(self, exc_type, exc_value, traceback):
        if self.session:
            await self.session.__aexit__(
                exc_type,
                exc_value,
                traceback
            )

        if self.http_context:
            await self.http_context.__aexit__(
                exc_type,
                exc_value,
                traceback
            )

    async def list_tools(self):
        result = await self.session.list_tools()
        return result.tools

    async def call_tool(self, name, arguments):
        result = await self.session.call_tool(
            name,
            arguments=arguments
        )

        return result.model_dump()


'''
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
            
'''