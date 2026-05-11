import os
import sys
from src.CineFlicx.exception.exception_handler import CustomException
from src.CineFlicx.logger.log import logging
from src.CineFlicx.utils.common import read_yaml
from src.CineFlicx.entity.config_entity import DataIngestionConfig
from src.CineFlicx.constants import CONFIG_FILE_PATH

class Configuration:
    def __init__(self,config_file_path:str=CONFIG_FILE_PATH):
        try:        
            self.config_info=read_yaml(file_path=config_file_path)
        except Exception as e:
            raise CustomException(e,sys)

    def get_data_ingestion_config(self):
        try:
            self.data_ingestion_config=self.config_info['data_ingestion_config']
            self.artifacts_config=self.config_info['artifacts_config']
            artifacts_directory=self.artifacts_config['artifacts_directory']
            dataset_download_url = self.data_ingestion_config['dataset_download_url']
            raw_data_directory = os.path.join(
                artifacts_directory,
                self.config_info["data_ingestion_config"]["raw_data_directory"]
            )

            ingested_directory = os.path.join(
                artifacts_directory,
                self.config_info["data_ingestion_config"]["ingested_directory"]
            )

            response = DataIngestionConfig(
            dataset_download_url=dataset_download_url,
            ingested_directory=ingested_directory,
            raw_data_directory=raw_data_directory
            )
            return response
        except Exception as e:
            raise CustomException(e,sys)
            