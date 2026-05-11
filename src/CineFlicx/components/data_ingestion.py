import os
import sys
import zipfile
from six.moves import urllib
from src.CineFlicx.exception.exception_handler import CustomException
from src.CineFlicx.logger.log import logging
from src.CineFlicx.configuration.configuration import Configuration

class DataIngestion:
    def __init__(self,app_config=Configuration()):
        try:
            logging.info(f"{'='*20} data ingestion log started {'='*20}")
            self.data_ingestion_config=app_config.get_data_ingestion_config()
        except Exception as e:
            raise CustomException(e,sys)
        
    def download_data(self):
        try:
            dataset_url=self.data_ingestion_config.dataset_download_url
            zip_download_dir=self.data_ingestion_config.raw_data_directory

            os.makedirs(zip_download_dir,exist_ok=True)

            data_file_name=os.path.basename(dataset_url)
            zip_file_path=os.path.join(zip_download_dir,data_file_name)

            logging.info(f"downloading data from {dataset_url} to {zip_file_path}")

            urllib.request.urlretrieve(dataset_url,zip_file_path)

            print("Saved file:", zip_file_path)
            print("File size:", os.path.getsize(zip_file_path))

            logging.info(f"download completed")

            return zip_file_path

        except Exception as e:
            raise CustomException(e,sys)
        

        
            
    def extract_zip_file(self,zip_file_path:str):
        print(zipfile.is_zipfile(zip_file_path))
        try:
            ingested_dir=self.data_ingestion_config.ingested_directory
            os.makedirs(ingested_dir,exist_ok=True)
            with zipfile.ZipFile(zip_file_path,'r') as zip_ref:
                zip_ref.extractall(ingested_dir)
            logging.info(f"extracted data from {zip_file_path} to {ingested_dir}")
        except Exception as e:
            raise CustomException(e,sys)
        
    def initiate_data_ingestion(self):
        try:
            zip_file_path=self.download_data()
            self.extract_zip_file(zip_file_path=zip_file_path)
            logging.info(f"{'='*20} data ingestion log completed {'='*20}")
        except Exception as e:
            raise CustomException(e,sys)
        
