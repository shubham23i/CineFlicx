import os
import sys
from src.CineFlicx.exception.exception_handler import CustomException
from src.CineFlicx.logger.log import logging
from src.CineFlicx.utils.common import read_yaml
from src.CineFlicx.entity.config_entity import DataIngestionConfig,DataTransformationConfig,DataValidationConfig
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
        
    def get_data_transformation_config(self):
        try:
            self.data_transformation_config = self.config_info['data_transformation_config']
            self.data_ingestion_config = self.config_info['data_ingestion_config']
            self.artifacts_config = self.config_info['artifacts_config']

            artifacts_directory = self.artifacts_config['artifacts_directory']

            ingested_directory = os.path.join(
                artifacts_directory,
                self.data_ingestion_config['ingested_directory']
            )

            transformed_data_directory = os.path.join(
                artifacts_directory,
                self.data_transformation_config['transformed_data_directory']
            )

            artifacts_directory = self.artifacts_config['artifacts_directory']

            ingested_base = os.path.join(
                artifacts_directory,
                self.data_ingestion_config['ingested_directory'],
                "ml-latest-small"
            )

            ratings_path = os.path.join(
                ingested_base,
                
                self.data_transformation_config['ratings_csv_file_name']
            )

            movies_path = os.path.join(
                ingested_base,
                
                self.data_transformation_config['movies_csv_file_name']
            )

            links_path = os.path.join(
                ingested_base,
                
                self.data_transformation_config['links_csv_file_name']
            )

            tags_path = os.path.join(
                ingested_base,
                
                self.data_transformation_config['tags_csv_file_name']
            )
            response = DataTransformationConfig(
                transformed_data_directory=transformed_data_directory,
                ratings_csv_file_path=ratings_path,
                movies_csv_file_path=movies_path,
                links_csv_file_path=links_path,
                tags_csv_file_path=tags_path
            )

            return response

        except Exception as e:
            raise CustomException(e, sys)     
        

    def get_data_validation_config(self):
        try:
            artifacts = self.config_info["artifacts_config"]
            validation = self.config_info["data_validation_config"]
            files = self.config_info["file_names"]

            artifacts_dir = artifacts["artifacts_directory"]

            validated_dir = os.path.join(
                artifacts_dir,
                validation["validated_directory"]
            )

            response = DataValidationConfig(
                validated_directory=validated_dir,
                min_user_ratings_threshold=validation["min_user_ratings_threshold"],
                min_movie_ratings_threshold=validation["min_movie_ratings_threshold"],
                ratings_file_name=files["ratings_file"],
                movies_file_name=files["movies_file"],
                links_file_name=files["links_file"],
                tags_file_name=files["tags_file"]
            )

            return response

        except Exception as e:
            raise CustomException(e, sys)

                    