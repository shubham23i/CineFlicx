import os
import sys
import pickle
import numpy as np
import pandas as pd
import faiss

from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

from src.CineFlicx.logger.log import logging
from src.CineFlicx.exception.exception_handler import CustomException
from src.CineFlicx.configuration.configuration import Configuration


class DataTransformation:

    def __init__(self, app_config=Configuration()):

        try:

            self.validation_config = (
                app_config.get_data_validation_config()
            )

            self.transformation_config = (
                app_config.get_data_transformation_config()
            )

        except Exception as e:
            raise CustomException(e, sys)

    # =========================================================
    # SAVE PICKLE OBJECT
    # =========================================================

    def save_pickle_object(self, file_path, obj):

        try:

            with open(file_path, "wb") as file_obj:
                pickle.dump(obj, file_obj)

        except Exception as e:
            raise CustomException(e, sys)

    # =========================================================
    # DATA TRANSFORMATION PIPELINE
    # =========================================================

    def initiate_data_transformation(self):

        try:

            logging.info(
                f"{'='*20} Data Transformation Started {'='*20}"
            )

            # =====================================================
            # LOAD VALIDATED CLEAN FILES
            # =====================================================

            validated_dir = (
                self.validation_config.validated_directory
            )

            ratings_df = pd.read_csv(
                os.path.join(
                    validated_dir,
                    self.validation_config.ratings_file_name
                )
            )

            movies_df = pd.read_csv(
                os.path.join(
                    validated_dir,
                    self.validation_config.movies_file_name
                )
            )

            links_df = pd.read_csv(
                os.path.join(
                    validated_dir,
                    self.validation_config.links_file_name
                )
            )

            tags_df = pd.read_csv(
                os.path.join(
                    validated_dir,
                    self.validation_config.tags_file_name
                )
            )

            logging.info(
                "Validated files loaded successfully"
            )

            # =====================================================
            # RENAME COLUMNS
            # =====================================================

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

            logging.info(
                "Columns renamed successfully"
            )

            # =====================================================
            # MERGE DATASETS
            # =====================================================

            metadata_df = pd.merge(
                movies_df,
                links_df,
                on="movieid",
                how="inner"
            )

            metadata_df = pd.merge(
                metadata_df,
                tags_df,
                on="movieid",
                how="left"
            )

            logging.info(
                "Metadata dataframe created"
            )

            # =====================================================
            # HANDLE NULL TAGS
            # =====================================================

            metadata_df["tag"] = (
                metadata_df["tag"].fillna("")
            )

            # =====================================================
            # TITLE ↔ MOVIEID MAPPINGS
            # =====================================================

            title_to_movieid = dict(
                zip(
                    metadata_df["title"],
                    metadata_df["movieid"]
                )
            )

            movieid_to_title = dict(
                zip(
                    metadata_df["movieid"],
                    metadata_df["title"]
                )
            )

            logging.info(
                "Movie mappings created"
            )

            # =====================================================
            # CREATE COMBINED FEATURES
            # =====================================================

            metadata_df["combined_features"] = (
                metadata_df["title"].fillna('') + " " +
                metadata_df["genres"].fillna('') + " " +
                metadata_df["tag"].fillna('')
            )

            logging.info(
                "Combined features created"
            )

            # =====================================================
            # FILTER ACTIVE USERS
            # =====================================================

            user_counts = (
                ratings_df["userid"].value_counts()
            )

            active_users = user_counts[
                user_counts >
                self.transformation_config
                .min_user_ratings_threshold
            ].index

            filtered_ratings = ratings_df[
                ratings_df["userid"].isin(active_users)
            ]

            logging.info(
                "Active users filtered"
            )

            # =====================================================
            # FILTER POPULAR MOVIES
            # =====================================================

            movie_counts = (
                filtered_ratings["movieid"]
                .value_counts()
            )

            popular_movies = movie_counts[
                movie_counts >
                self.transformation_config
                .min_movie_ratings_threshold
            ].index

            filtered_ratings = filtered_ratings[
                filtered_ratings["movieid"]
                .isin(popular_movies)
            ]

            logging.info(
                "Popular movies filtered"
            )

            # =====================================================
            # CREATE MOVIE PIVOT
            # =====================================================

            movie_pivot = filtered_ratings.pivot_table(
                index="movieid",
                columns="userid",
                values="rating"
            ).fillna(0)

            logging.info(
                "Movie pivot created"
            )

            # =====================================================
            # COSINE SIMILARITY
            # =====================================================

            similarity = cosine_similarity(
                movie_pivot
            )

            logging.info(
                "Cosine similarity matrix created"
            )

            # =====================================================
            # SENTENCE TRANSFORMER EMBEDDINGS
            # =====================================================

            model = SentenceTransformer(
                "all-MiniLM-L6-v2"
            )

            embeddings = model.encode(
                metadata_df["combined_features"].tolist(),
                show_progress_bar=True
            )

            embeddings = np.array(
                embeddings,
                dtype="float32"
            )

            logging.info(
                "Sentence embeddings created"
            )

            # =====================================================
            # CREATE FAISS INDEX
            # =====================================================

            dimension = embeddings.shape[1]

            faiss_index = faiss.IndexFlatL2(
                dimension
            )

            faiss_index.add(
                embeddings
            )

            logging.info(
                "FAISS index created"
            )

            # =====================================================
            # CREATE OUTPUT DIRECTORY
            # =====================================================

            transformed_dir = (
                self.transformation_config
                .transformed_data_directory
            )

            os.makedirs(
                transformed_dir,
                exist_ok=True
            )

            # =====================================================
            # SAVE ARTIFACTS
            # =====================================================

            # metadata.pkl
            self.save_pickle_object(
                os.path.join(
                    transformed_dir,
                    "metadata.pkl"
                ),
                metadata_df
            )

            # movie_pivot.pkl
            self.save_pickle_object(
                os.path.join(
                    transformed_dir,
                    "movie_pivot.pkl"
                ),
                movie_pivot
            )

            # similarity.pkl
            self.save_pickle_object(
                os.path.join(
                    transformed_dir,
                    "similarity.pkl"
                ),
                similarity
            )

            # title_to_movieid.pkl
            self.save_pickle_object(
                os.path.join(
                    transformed_dir,
                    "title_to_movieid.pkl"
                ),
                title_to_movieid
            )

            # movieid_to_title.pkl
            self.save_pickle_object(
                os.path.join(
                    transformed_dir,
                    "movieid_to_title.pkl"
                ),
                movieid_to_title
            )

            # embeddings.npy
            np.save(
                os.path.join(
                    transformed_dir,
                    "embeddings.npy"
                ),
                embeddings
            )

            # faiss.index
            faiss.write_index(
                faiss_index,
                os.path.join(
                    transformed_dir,
                    "faiss.index"
                )
            )

            logging.info(
                "All transformation artifacts saved successfully"
            )

            logging.info(
                f"{'='*20} Data Transformation Completed {'='*20}"
            )

            return (
                metadata_df,
                movie_pivot,
                similarity,
                embeddings,
                faiss_index
            )

        except Exception as e:
            raise CustomException(e, sys)