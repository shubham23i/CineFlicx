from fastapi import APIRouter

from src.CineFlicx.pipelines.prediction_pipeline import (
    PredictionPipeline
)

from src.CineFlicx.components.tmdb_fetcher import (
    TMDBFetcher
)

recommendation_router = APIRouter(
    prefix="/recommendation",
    tags=["Recommendation"]
)

# =====================================================
# ENRICH MOVIE DATA
# =====================================================

def enrich_movies(movie_list):

    tmdb = TMDBFetcher()

    enriched = []

    for movie in movie_list:

        try:

            tmdbid = int(movie["tmdbid"])

            details = (
                tmdb.get_movie_details(tmdbid)
            )

            enriched.append({

                "movieid":
                movie["movieid"],

                "title":
                movie["title"],

                "genres":
                movie["genres"],

                "tmdbid":
                tmdbid,

                "imdbid":
                movie["imdbid"],

                "overview":
                details.get("overview"),

                "poster":
                details.get("poster"),

                "backdrop":
                details.get("backdrop"),

                "rating":
                details.get("rating"),

                "release_date":
                details.get("release_date")
            })

        except:

            enriched.append(movie)

    return enriched

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

    prediction_pipeline = PredictionPipeline()

    results = (
        prediction_pipeline
        .collaborative_pipeline(
            movie_title=movie_name,
            top_k=top_k
        )
    )

    enriched_results = (
        enrich_movies(results)
    )

    return {

        "movie":
        movie_name,

        "recommendations":
        enriched_results
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

    prediction_pipeline = PredictionPipeline()

    results = (
        prediction_pipeline
        .semantic_pipeline(
            query=query,
            top_k=top_k
        )
    )

    enriched_results = (
        enrich_movies(results)
    )

    return {

        "query":
        query,

        "results":
        enriched_results
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

    prediction_pipeline = PredictionPipeline()

    results = (
        prediction_pipeline
        .hybrid_pipeline(
            movie_title=movie_name,
            query=query,
            top_k=top_k
        )
    )

    enriched_results = (
        enrich_movies(results)
    )

    return {

        "movie":
        movie_name,

        "query":
        query,

        "recommendations":
        enriched_results
    }