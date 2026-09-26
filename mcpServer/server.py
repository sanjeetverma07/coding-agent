from .config import mcp
from .tools import (
    list_files as repo_list_files,
    read_file as repo_read_files,
    replace_in_file as repo_replace_in_file,
    run_command as repo_run_command,
    safe_path as repo_safe_path,
    search_code as repo_search_code,
    search_repository as repo_search_repository,
    write_file as repo_write_file
)

class TOOLS:

    @mcp.tool()
    def list_files(directory: str = ".") -> dict:
        return repo_list_files(directory)

    @mcp.tool()
    def read_file(path: str) -> dict:
        return repo_read_files(path)

    @mcp.tool()
    def replace_in_file(path: str, old: str, new: str) -> dict:
        return repo_replace_in_file(path, old, new)

    @mcp.tool()
    def run_command(command: str) -> dict:
        return repo_run_command(command)

    @mcp.tool()
    def safe_path(path: str) -> dict:
        return repo_safe_path(path)

    @mcp.tool()
    def search_code(query: str) -> dict:
        return repo_search_code(query)

    @mcp.tool()
    def search_repository(query: str, top_k: int = 5) -> dict:
        return repo_search_repository(query, top_k)

    @mcp.tool()
    def write_file(path: str, content: str) -> dict:
        return repo_write_file(path, content)