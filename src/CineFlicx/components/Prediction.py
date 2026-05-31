from difflib import get_close_matches
import os
import sys
import pickle
import numpy as np
import faiss
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

            # =================================================
            # PRODUCTION ARTIFACT DIRECTORY
            # =================================================

            transformed_dir = os.path.join(
                self.config.transformed_data_directory,
                "production"
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

                self.metadata = pickle.load(
                    file_obj
                )

            # =================================================
            # LOAD PRECOMPUTED RECOMMENDATIONS
            # =================================================

            with open(
                os.path.join(
                    transformed_dir,
                    "recommendation_dict.pkl"
                ),
                "rb"
            ) as file_obj:

                self.recommendation_dict = (
                    pickle.load(file_obj)
                )

            # =================================================
            # LOAD TITLE TO MOVIEID
            # =================================================

            with open(
                os.path.join(
                    transformed_dir,
                    self.config.title_to_movieid_file
                ),
                "rb"
            ) as file_obj:

                self.title_to_movieid = (
                    pickle.load(file_obj)
                )

            # =================================================
            # LOAD MOVIEID TO TITLE
            # =================================================

            with open(
                os.path.join(
                    transformed_dir,
                    self.config.movieid_to_title_file
                ),
                "rb"
            ) as file_obj:

                self.movieid_to_title = (
                    pickle.load(file_obj)
                )

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
            # LOAD SENTENCE TRANSFORMER MODEL
            # =================================================

            self.model = None

            logging.info(
                "Movie Recommender initialized successfully"
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

    def get_movie_metadata(self, movieids):

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

            movie_title = movie_title.strip().lower()

            matched_title = None

            # ============================================
            # EXACT MATCH (IGNORE YEAR)
            # ============================================

            for title in self.title_to_movieid.keys():

                clean_title = (
                    title.rsplit("(", 1)[0]
                    .strip()
                    .lower()
                )

                if clean_title == movie_title:

                    matched_title = title
                    break

            # ============================================
            # FUZZY MATCH
            # ============================================

            if matched_title is None:

                cleaned_titles = {}

                for title in self.title_to_movieid.keys():

                    clean_title = (
                        title.rsplit("(", 1)[0]
                        .strip()
                    )

                    cleaned_titles[clean_title] = title

                matches = get_close_matches(
                    movie_title,
                    [x.lower() for x in cleaned_titles.keys()],
                    n=1,
                    cutoff=0.7
                )

                if matches:

                    matched_clean = matches[0]

                    for clean_title, original_title in cleaned_titles.items():

                        if clean_title.lower() == matched_clean:

                            matched_title = original_title
                            break

            if matched_title is None:
                return []

            movieid = self.title_to_movieid[matched_title]

            recommendations = self.recommendation_dict.get(
                movieid,
                []
            )

            if len(recommendations) == 0:
                return []

            recommended_movieids = [

                rec["movieid"]

                for rec in recommendations[:top_k]
            ]

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
                [query],
                convert_to_numpy=True
            )

            query_embedding = np.array(
                query_embedding,
                dtype="float32"
            )

            # =================================================
            # NORMALIZE FOR COSINE SIMILARITY
            # =================================================

            faiss.normalize_L2(
                query_embedding
            )

            # =================================================
            # SEARCH FAISS
            # =================================================

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

            # =================================================
            # REMOVE DUPLICATES
            # =================================================

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
        
