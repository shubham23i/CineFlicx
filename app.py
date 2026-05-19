from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.CineFlicx.api.movie_routes import (
    movie_router
)

from src.CineFlicx.api.recommendation_routes import (
    recommendation_router
)

from src.CineFlicx.api.actor_routes import (
    actor_router
)

from src.CineFlicx.api.frontend_routes import (
    frontend_router
)

app = FastAPI(
    title="CineFlicx"
)

# =====================================================
# STATIC FILES
# =====================================================

app.mount(
    "/static",
    StaticFiles(directory="frontend/static"),
    name="static"
)

# =====================================================
# FRONTEND ROUTES
# =====================================================

app.include_router(frontend_router)

# =====================================================
# API ROUTES
# =====================================================

app.include_router(movie_router)

app.include_router(recommendation_router)

app.include_router(actor_router)