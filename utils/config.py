import os
# import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()
def read_env(variable:str):
    return os.getenv(variable)


# sys.path.append(str(Path(__file__).resolve().parent.parent))

REPO_ROOT = Path(read_env("REPO_ROOT")).resolve()
ROOT = Path("./").resolve()
MCP_CLIENT_URI="http://127.0.0.1:8000/mcp"


ALLOWED_COMMANDS = {
    "pytest",
    "python -m pytest",
    "python",
    "pylint"
}

IGNORE_DIRS = {
    ".git",
    "node_modules",
    "__pycache__",
    ".venv",
    "venv",
    "dist",
    "build",
    ".next",
    ".idea",
    ".virtualenv",
    "virtualenv",
    "transformer_model"
}

ACCEPTED_FILE_SUFFIX = {".py",
                ".js",
                ".ts",
                ".tsx",
                ".java",
                ".go",
                ".jsx"}

APPROVAL_REQUIRED=[
    "write_file",
    "replace_in_file",
    "run_command",
    "run_git"
]


class LlmSetting:
    MODEL_NAME =read_env("MODEL_NAME")
    MODEL_API_KEY=read_env("API_KEY")
    TEMPERATURE=0
    MAX_TOKENS=2048
    STREAM=False
    REASONING_EFFORT="medium"
    TOP_P=1
    STOP=None
    
LLM_SETTINGS= LlmSetting()