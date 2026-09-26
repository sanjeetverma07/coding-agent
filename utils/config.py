import os
# import sys
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

# sys.path.append(str(Path(__file__).resolve().parent.parent))

REPO_ROOT = Path("./test_repo").resolve()
ROOT = Path("./").resolve()
ALLOWED_COMMANDS = {
    "pytest",
    "python -m pytest",
}

IGNORE_DIRS = {
    ".git",
    "__pycache__",
    ".venv",
    "venv",
    "node_modules",
    ".virtualenv",
    "virtualenv"
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

def read_env(variable:str):
    return os.getenv(variable)

class LlmSetting:
    MODEL_NAME ="openai/gpt-oss-120b"
    MODEL_API_KEY=read_env("API_KEY")
    TEMPERATURE=0
    MAX_TOKENS=2048
    STREAM=False
    REASONING_EFFORT="medium"
    TOP_P=1
    STOP=None
    
LLM_SETTINGS= LlmSetting()