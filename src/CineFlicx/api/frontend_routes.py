from fastapi import APIRouter
from fastapi import Request

from fastapi.templating import Jinja2Templates

from src.CineFlicx.pipelines.prediction_pipeline import (
    PredictionPipeline
)

from src.CineFlicx.components.tmdb_fetcher import (
    TMDBFetcher
)

import pandas as pd
from src.CineFlicx.recommender.semantic_search import ( SemanticSearch )
frontend_router = APIRouter()

templates = Jinja2Templates(
    directory="frontend/templates"
)

# =====================================================
# LOAD DATASET
# =====================================================

semantic_engine = SemanticSearch()




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

    # =====================================================
    # MOVIE DETAILS
    # =====================================================

    movie_details = (
        tmdb.get_movie_details(movieid)
        or {}
    )

    # =====================================================
    # VIDEOS
    # =====================================================

    videos = (
        tmdb.get_movie_videos(movieid)
        or []
    )

    # =====================================================
    # CAST
    # =====================================================

    cast = (
        tmdb.get_movie_cast(movieid)
        or []
    )

    # =====================================================
    # MORE LIKE THIS
    # =====================================================

    prediction_pipeline = PredictionPipeline()

    recommendations = (
        prediction_pipeline
        .collaborative_pipeline(
            movie_title=movie_details.get("title"),
            top_k=10
        )
    )

    enriched_recommendations = []

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

            enriched_recommendations.append({

                "tmdbid":
                tmdbid,

                "title":
                movie.get("title"),

                "genres":
                movie.get("genres", ""),

                "poster":
                details.get("poster"),

                "overview":
                details.get("overview"),

                "rating":
                details.get("rating", 0),

                "match":
                95 - len(enriched_recommendations) * 3
            })

        except Exception as e:

            print("RECOMMENDATION ERROR:", e)

            continue

    return templates.TemplateResponse(
        request=request,
        name="movie.html",
        context={

            "movie":
            movie_details,

            "videos":
            videos,

            "cast":
            cast,

            "recommendations":
            enriched_recommendations
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
# SEMANTIC SEARCH
# =====================================================

@frontend_router.get("/semantic/{query}")
def semantic_search(
    query: str,
    request: Request
):

    results = semantic_engine.search(
        query=query,
        top_k=10
    )

    tmdb = TMDBFetcher()

    enriched_movies = []

    for movie in results:

        try:

            # SEARCH TMDB USING TITLE
            tmdb_movie = tmdb.search_movie(
                movie["title"]
            )

            if not tmdb_movie:
                continue

            tmdbid = tmdb_movie["id"]

            details = tmdb.get_movie_details(
                tmdbid
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

            print(e)

            continue

    return templates.TemplateResponse(

        request=request,

        name="search.html",

        context={

            "movies":
            enriched_movies,

            "query":
            query
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