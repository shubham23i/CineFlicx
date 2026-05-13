from fastapi import APIRouter

from src.CineFlicx.components.tmdb_fetcher import (
    TMDBFetcher
)

actor_router = APIRouter(
    prefix="/actor",
    tags=["Actors"]
)

# =====================================================
# SEARCH ACTOR
# =====================================================

@actor_router.get("/{actor_name}")
def get_actor(actor_name: str):

    tmdb = TMDBFetcher()

    actor = tmdb.search_actor(actor_name)

    if not actor:

        return {
            "error": "Actor not found"
        }

    movies = (
        tmdb.get_actor_movies(
            actor["id"]
        )
    )

    return {

        "actor":
        actor,

        "movies":
        movies
    }