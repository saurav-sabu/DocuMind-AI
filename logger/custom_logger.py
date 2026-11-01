import logging
import os
import structlog
from datetime import datetime

class CustomLogger:

    def __init__(self):
        
        self.logs_dir = os.path.join(os.getcwd(),"LOGS")
        os.makedirs(self.logs_dir,exist_ok=True)
        
        LOG_FILE = f"{datetime.now().strftime("%m_%d_%Y_%H_%M")}.log"
        self.log_file_path = os.path.join(self.logs_dir,LOG_FILE)


    def get_logger(self,name=__file__):

        logger_name = os.path.basename(name)

        file_handler = logging.FileHandler(self.log_file_path)
        file_handler.setLevel(logging.INFO)
        file_handler.setFormatter(logging.Formatter("%(message)s"))

        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        console_handler.setFormatter(logging.Formatter("%(message)s"))

        logging.basicConfig(
            handlers=[console_handler,file_handler],
            format="%(message)s",
            level=logging.INFO
        )

        structlog.configure(
                processors=[
                    structlog.processors.TimeStamper(fmt="iso",utc=True,key="timestamp"),
                    structlog.processors.add_log_level,
                    structlog.processors.EventRenamer(to="event"),
                    structlog.processors.JSONRenderer()
                ],
                logger_factory=structlog.stdlib.LoggerFactory(),
                cache_logger_on_first_use=True
            )

        return structlog.getLogger(logger_name)


if __name__ == "__main__":
    logger = CustomLogger()
    logger = logger.get_logger(os.path.basename(__file__))
    logger.info("Custom logger has been initialized using structlog")