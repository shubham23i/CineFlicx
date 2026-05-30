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
            # LOAD VALIDATED FILES
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

            metadata_df["tag"] = (
                metadata_df["tag"].fillna("")
            )

            logging.info(
                "Metadata dataframe created"
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
            # KEEP ONLY POPULAR MOVIES
            # =====================================================

            metadata_df = metadata_df[
                metadata_df["movieid"]
                .isin(popular_movies)
            ]

            metadata_df = metadata_df.drop_duplicates(
                subset="movieid"
            )

            metadata_df = metadata_df.reset_index(
                drop=True
            )

            logging.info(
                f"Filtered metadata shape: {metadata_df.shape}"
            )
            # =====================================================
            # CREATE MAPPINGS
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
            # CREATE PIVOT TABLE
            # =====================================================

            movie_pivot = filtered_ratings.pivot_table(
                index="movieid",
                columns="userid",
                values="rating"
            )

            movie_pivot = movie_pivot.fillna(0)

            movie_pivot = movie_pivot.astype(
                "float32"
            )

            logging.info(
                f"Movie pivot shape: {movie_pivot.shape}"
            )

            # =====================================================
            # LIMIT MOVIES FOR MEMORY OPTIMIZATION
            # =====================================================

            MAX_MOVIES = 20000

            if len(movie_pivot) > MAX_MOVIES:

                movie_popularity = (
                    filtered_ratings["movieid"]
                    .value_counts()
                )

                top_movies = movie_popularity.head(
                    MAX_MOVIES
                ).index

                movie_pivot = movie_pivot.loc[
                    movie_pivot.index.isin(top_movies)
                ]

                logging.info(
                    f"Reduced movie pivot to top {MAX_MOVIES} movies"
                )

            # =====================================================
            # CREATE SIMILARITY MATRIX
            # =====================================================

            similarity = cosine_similarity(
                movie_pivot
            )

            similarity = similarity.astype(
                "float32"
            )

            logging.info(
                "Cosine similarity matrix created"
            )

            # =====================================================
            # CREATE LIGHTWEIGHT RECOMMENDATION DICTIONARY
            # =====================================================

            TOP_K = 20

            recommendation_dict = {}

            movie_ids = movie_pivot.index.tolist()

            for idx, movieid in enumerate(movie_ids):

                similarity_scores = list(
                    enumerate(similarity[idx])
                )

                similarity_scores = sorted(
                    similarity_scores,
                    key=lambda x: x[1],
                    reverse=True
                )[1: TOP_K + 1]

                recommendations = []

                for movie in similarity_scores:

                    recommended_movieid = (
                        movie_ids[movie[0]]
                    )

                    recommendations.append({
                        "movieid": int(recommended_movieid),
                        "score": float(movie[1])
                    })

                recommendation_dict[
                    int(movieid)
                ] = recommendations

            logging.info(
                "Recommendation dictionary created"
            )

            # =====================================================
            # FREE HEAVY MEMORY
            # =====================================================

            del similarity
            del movie_pivot

            logging.info(
                "Freed similarity matrix and pivot table memory"
            )

            # =====================================================
            # CREATE EMBEDDINGS
            # =====================================================

            model = SentenceTransformer(
                "all-MiniLM-L6-v2"
            )

            MAX_EMBEDDING_MOVIES = 5000

            metadata_df = metadata_df.iloc[
                :MAX_EMBEDDING_MOVIES
            ]

            embeddings = model.encode(
                metadata_df["combined_features"].tolist(),
                batch_size=32,
                show_progress_bar=True,
                convert_to_numpy=True
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

            faiss.normalize_L2(
                embeddings
            )

            faiss_index = faiss.IndexFlatIP(
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

            production_dir = os.path.join(
                self.transformation_config.transformed_data_directory,
                "production"
            )

            os.makedirs(
                production_dir,
                exist_ok=True
            )
            

            # =====================================================
            # SAVE PRODUCTION ARTIFACTS
            # =====================================================

            self.save_pickle_object(
                os.path.join(
                    production_dir,
                    "metadata.pkl"
                ),
                metadata_df
            )

            self.save_pickle_object(
                os.path.join(
                    production_dir,
                    "recommendation_dict.pkl"
                ),
                recommendation_dict
            )

            self.save_pickle_object(
                os.path.join(
                    production_dir,
                    "title_to_movieid.pkl"
                ),
                title_to_movieid
            )

            self.save_pickle_object(
                os.path.join(
                    production_dir,
                    "movieid_to_title.pkl"
                ),
                movieid_to_title
            )

            np.save(
                os.path.join(
                    production_dir,
                    "embeddings.npy"
                ),
                embeddings
            )

            faiss.write_index(
                faiss_index,
                os.path.join(
                    production_dir,
                    "faiss.index"
                )
            )

            logging.info(
                "Production artifacts saved successfully"
            )

            logging.info(
                f"{'='*20} Data Transformation Completed {'='*20}"
            )

            return (
                metadata_df,
                recommendation_dict,
                embeddings,
                faiss_index
            )

        except Exception as e:
            raise CustomException(e, sys)
        
