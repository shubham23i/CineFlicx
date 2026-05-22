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

    tmdb = TMDBFetcher()

    # =========================================
    # FETCH MOVIE DETAILS
    # =========================================

    movie_details = (
        tmdb.get_movie_details(movieid)
        or {}
    )

    # =========================================
    # FETCH VIDEOS
    # =========================================

    videos = (
        tmdb.get_movie_videos(movieid)
        or []
    )

    # =========================================
    # FETCH CAST
    # =========================================

    cast = (
        tmdb.get_movie_cast(movieid)
        or []
    )

    # =========================================
    # RENDER TEMPLATE
    # =========================================

    return templates.TemplateResponse(
        request=request,
        name="movie.html",
        context={
            "movie": movie_details,
            "videos": videos,
            "cast": cast
        }
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
                or {}
            )

            enriched_movies.append({

                "movieid":
                movie["movieid"],

                "tmdbid":
                tmdbid,

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

            print("SEARCH ERROR:", e)

            continue

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