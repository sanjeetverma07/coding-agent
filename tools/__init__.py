from .list_files import list_files
from .read_files import read_file
from .search_code import search_code
from .write_file import write_file
from .run_command import run_command
from .replace_in_file import replace_in_file

TOOLS = {
    "list_files": list_files,
    "read_file": read_file,
    "search_code": search_code,
    "run_command":run_command,
    "write_file":write_file,
    "replace_in_file": replace_in_file,
}


TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "list_files",
            "description": "List files inside the repository.",
            "parameters": {
                "type": "object",
                "properties": {
                    "directory": {
                        "type": "string",
                        "description": "Directory to list. Defaults to '.'"
                    }
                },
                "required": []
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read the contents of a repository file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string",
                        "description": "Path of the file to read."
                    }
                },
                "required": ["path"]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "search_code",
            "description": "Search for text or code inside the repository.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Text to search for."
                    }
                },
                "required": ["query"]
            }
        }
    },
     {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": (
                "Write complete contents to a repository file. "
                "Use only after the user has approved the modification."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "path": {
                        "type": "string"
                    },
                    "content": {
                        "type": "string"
                    }
                },
                "required": [
                    "path",
                    "content"
                ]
            }
        }
    },

    {
        "type": "function",
        "function": {
            "name": "run_command",
            "description": (
                "Run an allowed test command."
            ),
            "parameters": {
                "type": "object",
                "properties": {
                    "command": {
                        "type": "string"
                    }
                },
                "required": ["command"]
            }
        }
    },
    {
    "type": "function",
    "function": {
        "name": "replace_in_file",
        "description": (
            "Replace one exact piece of text in a repository file. "
            "Use this when modifying existing code. "
            "The old text must appear exactly once."
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "path": {
                    "type": "string",
                    "description": "File to modify."
                },
                "old": {
                    "type": "string",
                    "description": "Exact existing text."
                },
                "new": {
                    "type": "string",
                    "description": "Replacement text."
                }
            },
            "required": [
                "path",
                "old",
                "new"
            ]
        }
    }
}

]