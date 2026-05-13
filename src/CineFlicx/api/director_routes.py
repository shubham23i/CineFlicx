from fastapi import APIRouter

director_router = APIRouter(
    prefix="/director",
    tags=["Directors"]
)

@director_router.get("/{director_name}")
def get_director(director_name: str):

    return {

        "director":
        director_name,

        "message":
        "Director APIs coming soon"
    }