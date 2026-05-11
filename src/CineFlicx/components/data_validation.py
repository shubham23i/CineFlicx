import os
import sys
import pandas as pd

from src.CineFlicx.logger.log import logging
from src.CineFlicx.exception.exception_handler import CustomException
from src.CineFlicx.configuration.configuration import Configuration


class DataValidation:

    def __init__(self, app_config=Configuration()):
        try:
            self.config = app_config.get_data_validation_config()
            self.transformation_config = app_config.get_data_transformation_config()

        except Exception as e:
            raise CustomException(e, sys)

    def initiate_data_validation(self):

        try:
            logging.info("Starting Data Validation Stage")

            # -----------------------------
            # Load CLEAN transformed data
            # -----------------------------
            ratings_path = os.path.join(
                self.transformation_config.transformed_data_directory,
                self.config.ratings_file_name
            )

            movies_path = os.path.join(
                self.transformation_config.transformed_data_directory,
                self.config.movies_file_name
            )

            links_path = os.path.join(
                self.transformation_config.transformed_data_directory,
                self.config.links_file_name
            )

            tags_path = os.path.join(
                self.transformation_config.transformed_data_directory,
                self.config.tags_file_name
            )

            ratings = pd.read_csv(ratings_path)
            movies = pd.read_csv(movies_path)
            links = pd.read_csv(links_path)
            tags = pd.read_csv(tags_path)

            logging.info("Clean files loaded successfully")

            # -----------------------------
            # FILTER: Active users
            # -----------------------------
            user_counts = ratings["userid"].value_counts()
            active_users = user_counts[
                user_counts > self.config.min_user_ratings_threshold
            ].index

            ratings = ratings[ratings["userid"].isin(active_users)]

            # -----------------------------
            # FILTER: Popular movies
            # -----------------------------
            movie_counts = ratings["movieid"].value_counts()
            popular_movies = movie_counts[
                movie_counts > self.config.min_movie_ratings_threshold
            ].index

            ratings = ratings[ratings["movieid"].isin(popular_movies)]

            logging.info("Filtering completed")

            # -----------------------------
            # CREATE MOVIE PIVOT (CORE STEP)
            # -----------------------------
            movie_pivot = ratings.pivot_table(
                index="movieid",
                columns="userid",
                values="rating"
            ).fillna(0)

            # -----------------------------
            # SAVE ARTIFACT
            # -----------------------------
            os.makedirs(self.config.validated_directory, exist_ok=True)

            pivot_path = os.path.join(
                self.config.validated_directory,
                "movie_pivot.csv"
            )

            movie_pivot.to_csv(pivot_path)

            logging.info(f"Movie pivot saved at {pivot_path}")

            return movie_pivot

        except Exception as e:
            raise CustomException(e, sys)