import os
import sys
import pandas as pd

from src.CineFlicx.logger.log import logging
from src.CineFlicx.exception.exception_handler import CustomException
from src.CineFlicx.configuration.configuration import Configuration


class DataValidation:

    def __init__(self, app_config=Configuration()):

        try:
            self.validation_config = (
                app_config.get_data_validation_config()
            )

            self.ingestion_config = (
                app_config.get_data_ingestion_config()
            )

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_validation(self):

        try:

            logging.info("Starting Data Validation")

            # ---------------------------------------------------
            # INGESTED DATA DIRECTORY
            # ---------------------------------------------------

            ingested_dir = os.path.join(
                self.ingestion_config.ingested_directory,
                "ml-latest-small"
            )

            # ---------------------------------------------------
            # LOAD RAW FILES
            # ---------------------------------------------------

            ratings_df = pd.read_csv(
                os.path.join(ingested_dir, "ratings.csv")
            )

            movies_df = pd.read_csv(
                os.path.join(ingested_dir, "movies.csv")
            )

            links_df = pd.read_csv(
                os.path.join(ingested_dir, "links.csv")
            )

            tags_df = pd.read_csv(
                os.path.join(ingested_dir, "tags.csv")
            )

            logging.info("Files loaded successfully")

            # ---------------------------------------------------
            # CHECK NULL VALUES
            # ---------------------------------------------------

            logging.info(
                f"Ratings null values:\n{ratings_df.isnull().sum()}"
            )

            logging.info(
                f"Movies null values:\n{movies_df.isnull().sum()}"
            )

            logging.info(
                f"Links null values:\n{links_df.isnull().sum()}"
            )

            logging.info(
                f"Tags null values:\n{tags_df.isnull().sum()}"
            )

            # ---------------------------------------------------
            # REMOVE NULL VALUES
            # ---------------------------------------------------

            ratings_df.dropna(inplace=True)
            movies_df.dropna(inplace=True)
            links_df.dropna(inplace=True)
            tags_df.dropna(inplace=True)

            logging.info("Null values removed")

            # ---------------------------------------------------
            # CHECK DUPLICATES
            # ---------------------------------------------------

            logging.info(
                f"Ratings duplicates: {ratings_df.duplicated().sum()}"
            )

            logging.info(
                f"Movies duplicates: {movies_df.duplicated().sum()}"
            )

            logging.info(
                f"Links duplicates: {links_df.duplicated().sum()}"
            )

            logging.info(
                f"Tags duplicates: {tags_df.duplicated().sum()}"
            )

            # ---------------------------------------------------
            # REMOVE DUPLICATES
            # ---------------------------------------------------

            ratings_df.drop_duplicates(inplace=True)
            movies_df.drop_duplicates(inplace=True)
            links_df.drop_duplicates(inplace=True)
            tags_df.drop_duplicates(inplace=True)

            logging.info("Duplicates removed")

            # ---------------------------------------------------
            # CREATE VALIDATED DIRECTORY
            # ---------------------------------------------------

            os.makedirs(
                self.validation_config.validated_directory,
                exist_ok=True
            )

            # ---------------------------------------------------
            # SAVE CLEAN FILES
            # ---------------------------------------------------

            ratings_df.to_csv(
                os.path.join(
                    self.validation_config.validated_directory,
                    "clean_ratings.csv"
                ),
                index=False
            )

            movies_df.to_csv(
                os.path.join(
                    self.validation_config.validated_directory,
                    "clean_movies.csv"
                ),
                index=False
            )

            links_df.to_csv(
                os.path.join(
                    self.validation_config.validated_directory,
                    "clean_links.csv"
                ),
                index=False
            )

            tags_df.to_csv(
                os.path.join(
                    self.validation_config.validated_directory,
                    "clean_tags.csv"
                ),
                index=False
            )

            logging.info("Clean validated files saved successfully")

        except Exception as e:
            raise CustomException(e, sys)