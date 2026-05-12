import os
import sys
import pickle
import numpy as np
import faiss

from sentence_transformers import SentenceTransformer

from src.CineFlicx.configuration.configuration import (
    Configuration
)

from src.CineFlicx.exception.exception_handler import (
    CustomException
)

from src.CineFlicx.logger.log import logging


class MovieRecommender:

    def __init__(self, app_config=Configuration()):

        try:

            self.config = (
                app_config.get_prediction_pipeline_config()
            )

            transformed_dir = (
                self.config.transformed_data_directory
            )

            # =================================================
            # LOAD METADATA
            # =================================================

            with open(
                os.path.join(
                    transformed_dir,
                    self.config.metadata_file
                ),
                "rb"
            ) as file_obj:

                self.metadata = pickle.load(file_obj)

            # =================================================
            # LOAD MOVIE PIVOT
            # =================================================

            with open(
                os.path.join(
                    transformed_dir,
                    self.config.movie_pivot_file
                ),
                "rb"
            ) as file_obj:

                self.movie_pivot = pickle.load(file_obj)

            # =================================================
            # LOAD SIMILARITY MATRIX
            # =================================================

            with open(
                os.path.join(
                    transformed_dir,
                    self.config.similarity_file
                ),
                "rb"
            ) as file_obj:

                self.similarity = pickle.load(file_obj)

            # =================================================
            # LOAD MAPPINGS
            # =================================================

            with open(
                os.path.join(
                    transformed_dir,
                    self.config.title_to_movieid_file
                ),
                "rb"
            ) as file_obj:

                self.title_to_movieid = pickle.load(file_obj)

            with open(
                os.path.join(
                    transformed_dir,
                    self.config.movieid_to_title_file
                ),
                "rb"
            ) as file_obj:

                self.movieid_to_title = pickle.load(file_obj)

            # =================================================
            # LOAD EMBEDDINGS
            # =================================================

            self.embeddings = np.load(
                os.path.join(
                    transformed_dir,
                    self.config.embeddings_file
                )
            )

            # =================================================
            # LOAD FAISS INDEX
            # =================================================

            self.faiss_index = faiss.read_index(
                os.path.join(
                    transformed_dir,
                    self.config.faiss_index_file
                )
            )

            # =================================================
            # LOAD SENTENCE TRANSFORMER
            # =================================================

            self.model = SentenceTransformer(
                self.config.model_name
            )

            logging.info(
                "Movie Recommender initialized"
            )

        except Exception as e:
            raise CustomException(e, sys)

    # =====================================================
    # FORMAT OUTPUT
    # =====================================================

    def format_output(self, df):

        try:

            results = []

            for _, row in df.iterrows():

                movie = {

                    "title": row.get("title"),

                    "genres": row.get("genres"),

                    "tmdbid": row.get("tmdbid"),

                    "imdbid": row.get("imdbid"),

                    "movieid": row.get("movieid")
                }

                results.append(movie)

            return results

        except Exception as e:
            raise CustomException(e, sys)

    # =====================================================
    # GET MOVIE METADATA
    # =====================================================

    def get_movie_metadata(
        self,
        movieids
    ):

        try:

            movie_df = (
                self.metadata[
                    self.metadata["movieid"]
                    .isin(movieids)
                ]
                .drop_duplicates("movieid")
            )

            return self.format_output(
                movie_df
            )

        except Exception as e:
            raise CustomException(e, sys)

    # =====================================================
    # COLLABORATIVE FILTERING
    # =====================================================

    def recommend_movies(
        self,
        movie_title,
        top_k=10
    ):

        try:

            if movie_title not in self.title_to_movieid:

                return {
                    "error": "Movie not found"
                }

            movieid = (
                self.title_to_movieid[movie_title]
            )

            if movieid not in self.movie_pivot.index:

                return {
                    "error": "Movie not present in pivot"
                }

            movie_index = (
                self.movie_pivot.index
                .get_loc(movieid)
            )

            similarity_scores = list(
                enumerate(
                    self.similarity[movie_index]
                )
            )

            similarity_scores = sorted(
                similarity_scores,
                key=lambda x: x[1],
                reverse=True
            )

            recommendations = (
                similarity_scores[1: top_k + 1]
            )

            recommended_movieids = []

            for movie in recommendations:

                recommended_movieids.append(
                    self.movie_pivot.index[
                        movie[0]
                    ]
                )

            return self.get_movie_metadata(
                recommended_movieids
            )

        except Exception as e:
            raise CustomException(e, sys)

    # =====================================================
    # SEMANTIC SEARCH
    # =====================================================

    def semantic_search(
        self,
        query,
        top_k=10
    ):

        try:

            query_embedding = self.model.encode(
                [query]
            )

            query_embedding = np.array(
                query_embedding,
                dtype="float32"
            )

            distances, indices = (
                self.faiss_index.search(
                    query_embedding,
                    top_k
                )
            )

            movie_df = (
                self.metadata.iloc[
                    indices[0]
                ]
                .drop_duplicates("movieid")
            )

            return self.format_output(
                movie_df
            )

        except Exception as e:
            raise CustomException(e, sys)

    # =====================================================
    # HYBRID RECOMMENDATION
    # =====================================================

    def hybrid_recommendation(
        self,
        movie_title,
        query,
        top_k=10
    ):

        try:

            collaborative_results = (
                self.recommend_movies(
                    movie_title=movie_title,
                    top_k=top_k
                )
            )

            semantic_results = (
                self.semantic_search(
                    query=query,
                    top_k=top_k
                )
            )

            combined_results = (
                collaborative_results
                + semantic_results
            )

            unique_movies = {}

            for movie in combined_results:

                unique_movies[
                    movie["movieid"]
                ] = movie

            final_results = list(
                unique_movies.values()
            )

            return final_results[:top_k]

        except Exception as e:
            raise CustomException(e, sys)