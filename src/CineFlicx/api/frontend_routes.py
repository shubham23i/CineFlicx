from fastapi import APIRouter
from fastapi import Request

from fastapi.templating import Jinja2Templates

from src.CineFlicx.pipelines.prediction_pipeline import (
    PredictionPipeline
)

from src.CineFlicx.components.tmdb_fetcher import (
    TMDBFetcher
)

frontend_router = APIRouter()

templates = Jinja2Templates(
    directory="frontend/templates"
)

# =====================================================
# HOME PAGE
# =====================================================

@frontend_router.get("/")
def home(request: Request):

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={}
    )

# =====================================================
# MOVIE DETAILS PAGE
# =====================================================

@frontend_router.get("/movie/{movieid}")
def movie_page(
    movieid: int,
    request: Request
):

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

        return templates.TemplateResponse(

            "search.html",

            {
                "request": request,
                "error": "Movie not found"
            }
        )

    movie = movie.iloc[0]

    tmdbid = int(movie["tmdbid"])

    # =================================================
    # TMDB DETAILS
    # =================================================

    details = (
        tmdb.get_movie_details(tmdbid)
    )

    credits = (
        tmdb.get_movie_cast(tmdbid)
    )

    videos = (
        tmdb.get_movie_videos(tmdbid)
    )

    movie_data = {

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

        "runtime":
        details.get("runtime"),

        "rating":
        details.get("rating"),

        "release_date":
        details.get("release_date"),

        "cast":
        credits.get("cast"),

        "directors":
        credits.get("directors"),

        "videos":
        videos
    }

    return templates.TemplateResponse(
    request=request,
    name="index.html",
    context={}
)

# =====================================================
# SEARCH PAGE
# =====================================================

@frontend_router.get("/search/{movie_name}")
def search_movie(
    movie_name: str,
    request: Request
):

    prediction_pipeline = PredictionPipeline()

    recommendations = (
        prediction_pipeline
        .collaborative_pipeline(
            movie_title=movie_name,
            top_k=10
        )
    )

    tmdb = TMDBFetcher()

    enriched_movies = []

    for movie in recommendations:

        try:

            tmdbid = movie.get("tmdbid")

            if not tmdbid:
                continue

            tmdbid = int(float(tmdbid))

            details = (
                tmdb.get_movie_details(tmdbid)
            )

            enriched_movies.append({

                "movieid":
                movie["movieid"],

                "title":
                movie["title"],

                "genres":
                movie["genres"],

                "poster":
                details.get("poster"),

                "rating":
                details.get("rating"),

                "overview":
                details.get("overview")
            })

        except Exception as e:

            print(e)

            continue

    print(enriched_movies)

    return templates.TemplateResponse(
        request=request,
        name="search.html",
        context={
            "movies": enriched_movies,
            "query": movie_name
        }
    )

# =====================================================
# ACTOR PAGE
# =====================================================

@frontend_router.get("/actor/{actor_name}")
def actor_page(
    actor_name: str,
    request: Request
):

    tmdb = TMDBFetcher()

    actor = tmdb.search_actor(actor_name)

    if not actor:

        return templates.TemplateResponse(

            "actor.html",

            {
                "request": request,
                "error": "Actor not found"
            }
        )

    movies = (
        tmdb.get_actor_movies(
            actor["id"]
        )
    )

    return templates.TemplateResponse(
    request=request,
    name="index.html",
    context={}
)