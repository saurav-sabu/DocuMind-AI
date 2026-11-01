import logging
import os
from datetime import datetime

class CustomLogger:

    def __init__(self):
        
        self.logs_dir = os.path.join(os.getcwd(),"LOGS")
        os.makedirs(self.logs_dir,exist_ok=True)
        
        LOG_FILE = f"{datetime.now().strftime("%m_%d_%Y_%H_%M")}.log"
        LOG_FILE_PATH = os.path.join(self.logs_dir,LOG_FILE)
        
        logging.basicConfig(
            filename=LOG_FILE_PATH,
            format="%(asctime)s-%(name)s-%(levelname)s - %(message)s",
            level=logging.INFO
        )

    def get_logger(self,name=__file__):
        return logging.getLogger(name)


if __name__ == "__main__":
    logger = CustomLogger()
    logger = logger.get_logger(os.path.basename(__file__))
    logger.info("Custom logger has been initialized")