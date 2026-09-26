# from ..mcpServer.tools.list_files import list_files
# from ..mcpServer.tools.read_files import read_file
# from ..mcpServer.tools.search_code import search_code
# from ..mcpServer.tools.write_file import write_file
# from ..mcpServer.tools.run_command import run_command
# from ..mcpServer.tools.replace_in_file import replace_in_file
# from ..mcpServer.tools.search_repository import search_repository, search_repository_hybrid

# TOOLS = {
#     "list_files": list_files,
#     "read_file": read_file,
#     "search_code": search_code,
#     "run_command":run_command,
#     "write_file":write_file,
#     "replace_in_file": replace_in_file,
#     "search_repository":search_repository,
#     "search_repository_hybrid": search_repository_hybrid,
# }


# TOOL_DEFINITIONS = [
#     {
#         "type": "function",
#         "function": {
#             "name": "list_files",
#             "description": "List files inside the repository.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "directory": {
#                         "type": "string",
#                         "description": "Directory to list. Defaults to '.'"
#                     }
#                 },
#                 "required": []
#             }
#         }
#     },

#     {
#         "type": "function",
#         "function": {
#             "name": "read_file",
#             "description": "Read the contents of a repository file.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "path": {
#                         "type": "string",
#                         "description": "Path of the file to read."
#                     }
#                 },
#                 "required": ["path"]
#             }
#         }
#     },

#     {
#         "type": "function",
#         "function": {
#             "name": "search_code",
#             "description": "Search for text or code inside the repository.",
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "query": {
#                         "type": "string",
#                         "description": "Text to search for."
#                     }
#                 },
#                 "required": ["query"]
#             }
#         }
#     },
#      {
#         "type": "function",
#         "function": {
#             "name": "write_file",
#             "description": (
#                 "Write complete contents to a repository file. "
#                 "Use only after the user has approved the modification."
#             ),
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "path": {
#                         "type": "string"
#                     },
#                     "content": {
#                         "type": "string"
#                     }
#                 },
#                 "required": [
#                     "path",
#                     "content"
#                 ]
#             }
#         }
#     },

#     {
#         "type": "function",
#         "function": {
#             "name": "run_command",
#             "description": (
#                 "Run an allowed test command."
#             ),
#             "parameters": {
#                 "type": "object",
#                 "properties": {
#                     "command": {
#                         "type": "string"
#                     }
#                 },
#                 "required": ["command"]
#             }
#         }
#     },
#     {
#     "type": "function",
#     "function": {
#         "name": "replace_in_file",
#         "description": (
#             "Replace one exact piece of text in a repository file. "
#             "Use this when modifying existing code. "
#             "The old text must appear exactly once."
#         ),
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "path": {
#                     "type": "string",
#                     "description": "File to modify."
#                 },
#                 "old": {
#                     "type": "string",
#                     "description": "Exact existing text."
#                 },
#                 "new": {
#                     "type": "string",
#                     "description": "Replacement text."
#                 }
#             },
#             "required": [
#                 "path",
#                 "old",
#                 "new"
#             ]
#         }
#     }
# },
#     {
#     "type": "function",
#     "function": {
#         "name": "search_repository",
#         "description": (
#             "Perform semantic search over the repository "
#             "to find code relevant to a task. "
#             "Use this when you need to understand "
#             "which files or code sections are relevant."
#         ),
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "query": {
#                     "type": "string",
#                     "description": "Natural language description of the code you are looking for."
#                 },
#                 "top_k": {
#                     "type": "integer",
#                     "description": "Number of relevant code chunks to return.",
#                     "default": 5
#                 }
#             },
#             "required": ["query"]
#         }
#     }
# },
#     {
#     "type": "function",
#     "function": {
#         "name": "search_repository_hybrid",
#         "description": (
#             "Search the repository using both semantic search "
#             "and exact code/symbol matching. Use this when you "
#             "need to locate functionality, functions, classes, "
#             "symbols, or code related to a concept."
#         ),
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "query": {
#                     "type": "string",
#                     "description": (
#                         "Natural language description, "
#                         "function name, class name, variable name, "
#                         "or exact code text to search for."
#                     )
#                 },
#                 "top_k": {
#                     "type": "integer",
#                     "description": "Maximum number of results.",
#                     "default": 5
#                 }
#             },
#             "required": ["query"]
#         }
#     }
# },

# ]