from fastapi import APIRouter

director_router = APIRouter(
    prefix="/director",
    tags=["Directors"]
)

# =====================================================
# PLACEHOLDER ROUTES
# =====================================================

@director_router.get("/{director_name}")
def get_director(director_name: str):

    return {

        "director": director_name,

        "message":
        "Director APIs will be implemented later"
    }

@director_router.get("/movies/{director_name}")
def get_director_movies(director_name: str):

    return {

        "director": director_name,

        "movies": []
    }