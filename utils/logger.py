from pathlib import Path
import logging

dir =Path('logs')
dir.mkdir(
    parents=True,
    exist_ok=True
)

logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(), logging.FileHandler(f'{dir}/codeagent.log')]
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logger= logging.getLogger('agent_logger')