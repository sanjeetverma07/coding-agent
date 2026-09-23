from .config import ROOT
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(filename)s - %(levelname)s - %(message)s',
    handlers=[logging.StreamHandler(), logging.FileHandler('logs/agent.log')]
)

logger= logging.getLogger('agent_logger')