import logging

logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(), logging.FileHandler('logs/codeagent.log')]
)
logging.getLogger("httpx").setLevel(logging.WARNING)
logging.getLogger("httpcore").setLevel(logging.WARNING)
logger= logging.getLogger('agent_logger')