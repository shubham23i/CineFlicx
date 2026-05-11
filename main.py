from src.CineFlicx.exception.exception_handler import CustomException
import sys


if __name__ == "__main__":
    try:
        a=10/0
    except Exception as e:
        raise CustomException(e,sys)