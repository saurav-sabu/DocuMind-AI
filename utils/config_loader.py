import yaml
from logger.custom_logger import CustomLogger

logger = CustomLogger().get_logger(__name__)

def load_config(file_path: str = r"configs\config.yaml"):
    with open(file_path,"r") as file:
        config = yaml.safe_load(file)
    logger.info(config)
    return config

load_config()
