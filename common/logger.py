from loguru import logger 
from common.environment import current_environment_configuration
import sys

logger.remove()

if current_environment_configuration.can_log_data():
    # print("can lop data")
    logger.add(sys.stderr, level="INFO")


