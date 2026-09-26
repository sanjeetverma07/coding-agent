from .config import mcp
from .tools import (
    list_files as repo_list_files,
    read_file as repo_read_files,
    replace_in_file as repo_replace_in_file,
    run_command as repo_run_command,
    safe_path as repo_safe_path,
    search_code as repo_search_code,
    search_repository as repo_search_repository,
    write_file as repo_write_file,
    git_status as repo_git_status,
    git_diff as repo_git_diff,
    git_log as repo_git_log,
    git_branch as repo_git_branch,
    git_create_branch as repo_git_create_branch,
    git_checkout as repo_git_checkout,
    git_add as repo_git_add,
    git_commit as repo_git_commit,
    git_stash_pop as repo_git_stash_pop,
    git_stash as repo_git_stash,
    run_git as repo_run_git
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
    
    @mcp.tool()
    def run_git(command:  list[str]) -> dict:
        return repo_run_git(command)
    
    # @mcp.tool()
    # def git_status() -> dict:
    #     return repo_git_status()


    # @mcp.tool()
    # def git_diff() -> dict:
    #     return repo_git_diff()


    # @mcp.tool()
    # def git_log(limit: int = 10) -> dict:
    #     return repo_git_log(limit)


    # @mcp.tool()
    # def git_branch() -> dict:
    #     return repo_git_branch()
    
    # @mcp.tool()
    # def git_create_branch(branch_name: str) -> dict:
    #     return repo_git_create_branch(branch_name)


    # @mcp.tool()
    # def git_checkout(branch_name: str) -> dict:
    #     return repo_git_checkout(branch_name)


    # @mcp.tool()
    # def git_add(paths: list[str]) -> dict:
    #     return repo_git_add(paths)


    # @mcp.tool()
    # def git_commit(message: str) -> dict:
    #     return repo_git_commit(message)
    
    # @mcp.tool()
    # def git_stash() -> dict:
    #     return repo_git_stash()


    # @mcp.tool()
    # def git_stash_pop() -> dict:
    #     return repo_git_stash_pop()