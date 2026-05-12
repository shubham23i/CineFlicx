from src.CineFlicx.components.Prediction import (
    MovieRecommender
)


class PredictionPipeline:

    def __init__(self):

        self.movie_recommender = (
            MovieRecommender()
        )

    # =====================================================
    # COLLABORATIVE PIPELINE
    # =====================================================

    def collaborative_pipeline(
        self,
        movie_title,
        top_k=10
    ):

        results = (
            self.movie_recommender
            .recommend_movies(
                movie_title=movie_title,
                top_k=top_k
            )
        )

        return results

    # =====================================================
    # SEMANTIC PIPELINE
    # =====================================================

    def semantic_pipeline(
        self,
        query,
        top_k=10
    ):

        results = (
            self.movie_recommender
            .semantic_search(
                query=query,
                top_k=top_k
            )
        )

        return results

    # =====================================================
    # HYBRID PIPELINE
    # =====================================================

    def hybrid_pipeline(
        self,
        movie_title,
        query,
        top_k=10
    ):

        results = (
            self.movie_recommender
            .hybrid_recommendation(
                movie_title=movie_title,
                query=query,
                top_k=top_k
            )
        )

        return results