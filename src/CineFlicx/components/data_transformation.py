import os
import sys
import pandas as pd

from src.CineFlicx.logger.log import logging
from src.CineFlicx.exception.exception_handler import CustomException
from src.CineFlicx.configuration.configuration import Configuration


class DataTransformation:

    def __init__(self, app_config=Configuration()):

        try:
            self.data_transformation_config = (
                app_config.get_data_transformation_config()
            )

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_transformation(self):

        try:

            logging.info("Starting data transformation")

            ratings_df = pd.read_csv(
                self.data_transformation_config.ratings_csv_file_path
            )

            movies_df = pd.read_csv(
                self.data_transformation_config.movies_csv_file_path
            )

            links_df = pd.read_csv(
                self.data_transformation_config.links_csv_file_path
            )

            tags_df = pd.read_csv(
                self.data_transformation_config.tags_csv_file_path
            )

            logging.info("Data loaded successfully")

            # -----------------------------
            # Rename columns to lowercase
            # -----------------------------

            ratings_df.rename(
                columns={
                    "userId": "userid",
                    "movieId": "movieid"
                },
                inplace=True
            )

            movies_df.rename(
                columns={
                    "movieId": "movieid"
                },
                inplace=True
            )

            links_df.rename(
                columns={
                    "movieId": "movieid",
                    "imdbId": "imdbid",
                    "tmdbId": "tmdbid"
                },
                inplace=True
            )

            tags_df.rename(
                columns={
                    "userId": "userid",
                    "movieId": "movieid"
                },
                inplace=True
            )

            logging.info("Column names converted")

            # -----------------------------
            # Remove null values
            # -----------------------------

            links_df.dropna(subset=["tmdbid"], inplace=True)

            # -----------------------------
            # Remove duplicates
            # -----------------------------

            ratings_df.drop_duplicates(inplace=True)
            movies_df.drop_duplicates(inplace=True)
            links_df.drop_duplicates(inplace=True)
            tags_df.drop_duplicates(inplace=True)

            logging.info("Nulls and duplicates handled")

            # -----------------------------
            # Create transformed directory
            # -----------------------------

            os.makedirs(
                self.data_transformation_config.transformed_data_directory,
                exist_ok=True
            )

            # -----------------------------
            # Save cleaned files
            # -----------------------------

            ratings_df.to_csv(
                os.path.join(
                    self.data_transformation_config.transformed_data_directory,
                    "clean_ratings.csv"
                ),
                index=False
            )

            movies_df.to_csv(
                os.path.join(
                    self.data_transformation_config.transformed_data_directory,
                    "clean_movies.csv"
                ),
                index=False
            )

            links_df.to_csv(
                os.path.join(
                    self.data_transformation_config.transformed_data_directory,
                    "clean_links.csv"
                ),
                index=False
            )

            tags_df.to_csv(
                os.path.join(
                    self.data_transformation_config.transformed_data_directory,
                    "clean_tags.csv"
                ),
                index=False
            )

            logging.info("Transformed files saved successfully")

        except Exception as e:
            raise CustomException(e, sys)