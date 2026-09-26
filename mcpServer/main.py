from .config import mcp
from .server import TOOLS
tools = TOOLS()

if __name__=='__main__':
    mcp.run(
        transport="streamable-http",
        host="127.0.0.1",
        port=8000,
        streamable_http_path="/mcp"
    )
    
# from mcp.server.mcpserver import MCPServer
# from .tools.list_files import list_files as repo_list_files

# mcp = MCPServer('coding-assistant')

# @mcp.tool()
# def list_files(directory: str = ".") -> dict:
#     return repo_list_files(directory)
