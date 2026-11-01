import sys
from logger.custom_logger import CustomLogger

logger = CustomLogger().get_logger(__file__)

class DocumentPortalException(Exception):

    def __init__(self,error_message:str,error_details:sys):
        _,_, exc_tb = error_details.exc_info()
        self.file_name = exc_tb.tb_frame.f_code.co_filename
        self.line_number = exc_tb.tb_lineno
        self.error_message = str(error_message)

    def __str__(self):
        return f"error occured in script: [{self.file_name}] at line number: [{self.line_number}] error message: [{self.error_message}]"


if __name__ == "__main__":
    try:
        a = 1/0
        print(a)

    except Exception as e:
        logger.error(e)
        raise DocumentPortalException(e,sys)
