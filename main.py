from src.CineFlicx.exception.exception_handler import CustomException
from src.CineFlicx.logger.log import logging
import sys


if __name__ == "__main__":
    try:
        logging.info(f"logger is working fine")
        a=10/0
     

    except Exception as e:
        raise CustomException(e,sys)
    