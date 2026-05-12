import os
import sys

from src.CineFlicx.exception.exception_handler import CustomException
from src.CineFlicx.utils.common import read_yaml

from src.CineFlicx.entity.config_entity import (
    DataIngestionConfig,
    DataValidationConfig,
    DataTransformationConfig,
    PredictionPipelineConfig
)

from src.CineFlicx.constants import CONFIG_FILE_PATH


class Configuration:

    def __init__(self,
                 config_file_path: str = CONFIG_FILE_PATH):

        try:
            self.config_info = read_yaml(
                file_path=config_file_path
            )

        except Exception as e:
            raise CustomException(e, sys)

    # =========================================================
    # DATA INGESTION CONFIG
    # =========================================================

    def get_data_ingestion_config(self):

        try:

            ingestion_config = (
                self.config_info["data_ingestion_config"]
            )

            artifacts_config = (
                self.config_info["artifacts_config"]
            )

            artifacts_directory = (
                artifacts_config["artifacts_directory"]
            )

            dataset_download_url = (
                ingestion_config["dataset_download_url"]
            )

            raw_data_directory = os.path.join(
                artifacts_directory,
                ingestion_config["raw_data_directory"]
            )

            ingested_directory = os.path.join(
                artifacts_directory,
                ingestion_config["ingested_directory"]
            )

            response = DataIngestionConfig(
                dataset_download_url=dataset_download_url,
                ingested_directory=ingested_directory,
                raw_data_directory=raw_data_directory
            )

            return response

        except Exception as e:
            raise CustomException(e, sys)

    # =========================================================
    # DATA VALIDATION CONFIG
    # =========================================================

    def get_data_validation_config(self):

        try:

            validation_config = (
                self.config_info["data_validation_config"]
            )

            artifacts_config = (
                self.config_info["artifacts_config"]
            )

            file_config = (
                self.config_info["file_names"]
            )

            artifacts_directory = (
                artifacts_config["artifacts_directory"]
            )

            validated_directory = os.path.join(
                artifacts_directory,
                validation_config["validated_directory"]
            )

            response = DataValidationConfig(
                validated_directory=validated_directory,
                ratings_file_name=file_config["ratings_file"],
                movies_file_name=file_config["movies_file"],
                links_file_name=file_config["links_file"],
                tags_file_name=file_config["tags_file"]
            )

            return response

        except Exception as e:
            raise CustomException(e, sys)

    # =========================================================
    # DATA TRANSFORMATION CONFIG
    # =========================================================

    def get_data_transformation_config(self):

        try:

            transformation_config = (
                self.config_info["data_transformation_config"]
            )

            artifacts_config = (
                self.config_info["artifacts_config"]
            )

            artifacts_directory = (
                artifacts_config["artifacts_directory"]
            )

            transformed_data_directory = os.path.join(
                artifacts_directory,
                transformation_config[
                    "transformed_data_directory"
                ]
            )

            response = DataTransformationConfig(
                transformed_data_directory=(
                    transformed_data_directory
                ),

                min_user_ratings_threshold=(
                    transformation_config[
                        "min_user_ratings_threshold"
                    ]
                ),

                min_movie_ratings_threshold=(
                    transformation_config[
                        "min_movie_ratings_threshold"
                    ]
                )
            )

            return response

        except Exception as e:
            raise CustomException(e, sys)
        
    # =====================================================
    # PREDICTION PIPELINE CONFIG
    # =====================================================

    def get_prediction_pipeline_config(self):

        try:

            prediction_config = (
                self.config_info[
                    "prediction_pipeline_config"
                ]
            )

            artifact_files = (
                self.config_info[
                    "artifact_files"
                ]
            )

            artifacts_directory = (
                self.config_info[
                    "artifacts_config"
                ]["artifacts_directory"]
            )

            transformed_directory = os.path.join(
                artifacts_directory,
                self.config_info[
                    "data_transformation_config"
                ]["transformed_data_directory"]
            )

            response = PredictionPipelineConfig(

                transformed_data_directory=(
                    transformed_directory
                ),

                model_name=(
                    prediction_config["model_name"]
                ),

                metadata_file=(
                    artifact_files["metadata_file"]
                ),

                movie_pivot_file=(
                    artifact_files[
                        "movie_pivot_file"
                    ]
                ),

                similarity_file=(
                    artifact_files[
                        "similarity_file"
                    ]
                ),

                title_to_movieid_file=(
                    artifact_files[
                        "title_to_movieid_file"
                    ]
                ),

                movieid_to_title_file=(
                    artifact_files[
                        "movieid_to_title_file"
                    ]
                ),

                embeddings_file=(
                    artifact_files[
                        "embeddings_file"
                    ]
                ),

                faiss_index_file=(
                    artifact_files[
                        "faiss_index_file"
                    ]
                )
            )

            return response

        except Exception as e:
            raise CustomException(e, sys)