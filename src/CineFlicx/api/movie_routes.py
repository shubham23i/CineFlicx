from fastapi import APIRouter

from src.CineFlicx.pipelines.prediction_pipeline import (
    PredictionPipeline
)

from src.CineFlicx.components.tmdb_fetcher import (
    TMDBFetcher
)

movie_router = APIRouter(
    prefix="/movie",
    tags=["Movies"]
)

# =====================================================
# MOVIE DETAILS
# =====================================================

@movie_router.get("/{movieid}")
def get_movie(movieid: int):

    prediction_pipeline = PredictionPipeline()

    tmdb = TMDBFetcher()

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

    tmdbid = int(movie["tmdbid"])

    # -------------------------------------------------
    # TMDB DATA
    # -------------------------------------------------

    details = (
        tmdb.get_movie_details(tmdbid)
    )

    credits = (
        tmdb.get_movie_cast(tmdbid)
    )

    videos = (
        tmdb.get_movie_videos(tmdbid)
    )

    return {

        "movieid":
        movie["movieid"],

        "tmdbid":
        tmdbid,

        "imdbid":
        movie["imdbid"],

        "title":
        movie["title"],

        "genres":
        movie["genres"],

        # =============================================
        # TMDB DETAILS
        # =============================================

        "overview":
        details.get("overview"),

        "poster":
        details.get("poster"),

        "backdrop":
        details.get("backdrop"),

        "runtime":
        details.get("runtime"),

        "release_date":
        details.get("release_date"),

        "rating":
        details.get("rating"),

        "vote_count":
        details.get("vote_count"),

        "popularity":
        details.get("popularity"),

        # =============================================
        # CAST / DIRECTORS
        # =============================================

        "cast":
        credits.get("cast"),

        "directors":
        credits.get("directors"),

        # =============================================
        # VIDEOS / TRAILERS
        # =============================================

        "videos":
        videos
    }

# =====================================================
# GET ALL MOVIES
# =====================================================

@movie_router.get("/")
def get_all_movies():

    prediction_pipeline = PredictionPipeline()

    metadata = (
        prediction_pipeline
        .movie_recommender
        .metadata
    )

    movies = metadata[
        [
            "movieid",
            "title",
            "genres",
            "tmdbid"
        ]
    ].drop_duplicates()

    return movies.to_dict(
        orient="records"
    )