from fastapi import APIRouter

from src.CineFlicx.pipelines.prediction_pipeline import (
    PredictionPipeline
)

recommendation_router = APIRouter(
    prefix="/recommendation",
    tags=["Recommendation"]
)

prediction_pipeline = PredictionPipeline()

# =====================================================
# COLLABORATIVE RECOMMENDATION
# =====================================================

@recommendation_router.get(
    "/recommend/{movie_name}"
)
def recommend_movies(
    movie_name: str,
    top_k: int = 10
):

    results = (
        prediction_pipeline
        .collaborative_pipeline(
            movie_title=movie_name,
            top_k=top_k
        )
    )

    return {
        "movie": movie_name,
        "recommendations": results
    }

# =====================================================
# SEMANTIC SEARCH
# =====================================================

@recommendation_router.get(
    "/semantic-search/{query}"
)
def semantic_search(
    query: str,
    top_k: int = 10
):

    results = (
        prediction_pipeline
        .semantic_pipeline(
            query=query,
            top_k=top_k
        )
    )

    return {
        "query": query,
        "results": results
    }

# =====================================================
# HYBRID RECOMMENDATION
# =====================================================

@recommendation_router.get(
    "/hybrid/{movie_name}"
)
def hybrid_recommendation(
    movie_name: str,
    query: str,
    top_k: int = 10
):

    results = (
        prediction_pipeline
        .hybrid_pipeline(
            movie_title=movie_name,
            query=query,
            top_k=top_k
        )
    )

    return {
        "movie": movie_name,
        "query": query,
        "recommendations": results
    }