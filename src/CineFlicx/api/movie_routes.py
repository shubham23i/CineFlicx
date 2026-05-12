from fastapi import APIRouter

from src.CineFlicx.pipelines.prediction_pipeline import (
    PredictionPipeline
)

movie_router = APIRouter(
    prefix="/movie",
    tags=["Movies"]
)

prediction_pipeline = PredictionPipeline()

# =====================================================
# MOVIE DETAILS
# =====================================================

@movie_router.get("/{movieid}")
def get_movie(movieid: int):

    metadata = (
        prediction_pipeline
        .movie_recommender
        .metadata
    )

    movie = metadata[
        metadata["movieid"] == movieid
    ]

    if movie.empty:

        return {
            "error": "Movie not found"
        }

    movie = movie.iloc[0]

    return {

        "movieid": movie["movieid"],

        "title": movie["title"],

        "genres": movie["genres"],

        "tmdbid": movie["tmdbid"],

        "imdbid": movie["imdbid"]
    }

# =====================================================
# GET ALL MOVIES
# =====================================================

@movie_router.get("/")
def get_all_movies():

    metadata = (
        prediction_pipeline
        .movie_recommender
        .metadata
    )

    movies = metadata[
        [
            "movieid",
            "title",
            "genres"
        ]
    ].drop_duplicates()

    return movies.to_dict(
        orient="records"
    )