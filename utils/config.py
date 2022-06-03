import logging.config
import yaml
import os

INITIAL_CONFIG_PATH = 'configs/'
LOGGING_CONFIG_PATH = 'configs/logging_config.yaml'

with open(LOGGING_CONFIG_PATH, 'r') as f:
    config = yaml.safe_load(f.read())
    logging.config.dictConfig(config)
    logging.captureWarnings(True)

def get_logger(name: str):
    """
    Logs a message
    Args:name(str): name of logger
    """
    logger = logging.getLogger(name)
    return logger


def load_config(config_name: str):
    """
    Load yaml configuration file
    Args:config_name(str): name of initial config
    """
    with open(os.path.join(INITIAL_CONFIG_PATH, config_name)) as file:
        config = yaml.safe_load(file)

    return config
