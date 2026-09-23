# import sys
from pathlib import Path
from dotenv import load_dotenv
import os

load_dotenv()

# sys.path.append(str(Path(__file__).resolve().parent.parent))

REPO_ROOT = Path("./test_repo").resolve()
ROOT = Path("./").resolve()
ALLOWED_COMMANDS = {
    "pytest",
    "python -m pytest",
}

def read_env(variable:str):
    return os.getenv(variable)

class LLM_SETTING:
    MODEL_NAME ="openai/gpt-oss-120b"
    MODEL_API_KEY=read_env("API_KEY")
    TEMPERATURE=1
    MAX_TOKENS=2048
    STREAM=False
    REASONING_EFFORT="medium"
    TOP_P=1
    STOP=None
    
LLM_SETTINGS= LLM_SETTING()