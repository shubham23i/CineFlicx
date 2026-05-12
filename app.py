from fastapi import FastAPI
from src.CineFlicx.components.tmdb_fetcher import TMDBFetcher
from src.CineFlicx.api.recommendation_routes import (
    recommendation_router
)

from src.CineFlicx.api.movie_routes import (
    movie_router
)

from src.CineFlicx.api.actor_routes import (
    actor_router
)

from src.CineFlicx.api.director_routes import (
    director_router
)

app = FastAPI(
    title="CineFlicx API",
    version="1.0"
)

# =====================================================
# INCLUDE ROUTERS
# =====================================================

app.include_router(
    recommendation_router
)

app.include_router(
    movie_router
)

app.include_router(
    actor_router
)

app.include_router(
    director_router
)

# =====================================================
# HOME ROUTE
# =====================================================

@app.get("/")
def home():

    return {

        "message":
        "Welcome to CineFlicx API"
    }

