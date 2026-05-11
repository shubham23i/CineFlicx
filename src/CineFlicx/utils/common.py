import sys
import yaml
from src.CineFlicx.exception.exception_handler import CustomException
from src.CineFlicx.logger.log import logging

def read_yaml(file_path):
    try:
        with open(file_path,"r") as f:
            data=yaml.safe_load(f)
            return data
    except Exception as e:
        CustomException(e,sys)