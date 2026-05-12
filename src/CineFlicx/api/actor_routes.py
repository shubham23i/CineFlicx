from fastapi import APIRouter

actor_router = APIRouter(
    prefix="/actor",
    tags=["Actors"]
)

# =====================================================
# PLACEHOLDER ROUTES
# =====================================================

@actor_router.get("/{actor_name}")
def get_actor(actor_name: str):

    return {

        "actor": actor_name,

        "message":
        "Actor APIs will be implemented later"
    }

@actor_router.get("/movies/{actor_name}")
def get_actor_movies(actor_name: str):

    return {

        "actor": actor_name,

        "movies": []
    }