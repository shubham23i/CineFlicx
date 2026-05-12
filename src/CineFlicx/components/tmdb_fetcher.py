import os
import requests

from dotenv import load_dotenv


load_dotenv()


class TMDBFetcher:

    def __init__(self):

        self.api_key = os.getenv(
            "TMDB_API_KEY"
        )

        self.base_url = (
            "https://api.themoviedb.org/3"
        )

        self.image_base_url = (
            "https://image.tmdb.org/t/p/w500"
        )

    # =====================================================
    # GET MOVIE DETAILS
    # =====================================================

    def get_movie_details(self, tmdbid):

        try:

            url = (
                f"{self.base_url}/movie/{tmdbid}"
            )

            params = {
                "api_key": self.api_key
            }

            response = requests.get(
                url,
                params=params
            )

            data = response.json()

            return {

                "title":
                data.get("title"),

                "overview":
                data.get("overview"),

                "poster":
                self.image_base_url +
                data.get("poster_path", ""),

                "backdrop":
                self.image_base_url +
                data.get("backdrop_path", ""),

                "release_date":
                data.get("release_date"),

                "rating":
                data.get("vote_average"),

                "runtime":
                data.get("runtime"),

                "genres":
                data.get("genres")
            }

        except Exception as e:

            return {
                "error": str(e)
            }

    # =====================================================
    # GET MOVIE CAST
    # =====================================================

    def get_movie_cast(self, tmdbid):

        try:

            url = (
                f"{self.base_url}/movie/{tmdbid}/credits"
            )

            params = {
                "api_key": self.api_key
            }

            response = requests.get(
                url,
                params=params
            )

            data = response.json()

            cast_data = []

            for actor in data.get("cast", [])[:10]:

                cast_data.append({

                    "name":
                    actor.get("name"),

                    "character":
                    actor.get("character"),

                    "profile":
                    self.image_base_url +
                    str(actor.get("profile_path"))
                })

            return cast_data

        except Exception as e:

            return {
                "error": str(e)
            }

    # =====================================================
    # SEARCH ACTOR
    # =====================================================

    def search_actor(self, name):

        try:

            url = (
                f"{self.base_url}/search/person"
            )

            params = {

                "api_key": self.api_key,

                "query": name
            }

            response = requests.get(
                url,
                params=params
            )

            data = response.json()

            if len(data["results"]) == 0:

                return {}

            actor = data["results"][0]

            return {

                "id":
                actor.get("id"),

                "name":
                actor.get("name"),

                "profile":
                self.image_base_url +
                str(actor.get("profile_path")),

                "known_for":
                actor.get("known_for_department")
            }

        except Exception as e:

            return {
                "error": str(e)
            }

    # =====================================================
    # GET ACTOR MOVIES
    # =====================================================

    def get_actor_movies(self, person_id):

        try:

            url = (
                f"{self.base_url}/person/{person_id}/movie_credits"
            )

            params = {
                "api_key": self.api_key
            }

            response = requests.get(
                url,
                params=params
            )

            data = response.json()

            movies = []

            for movie in data.get("cast", [])[:20]:

                movies.append({

                    "title":
                    movie.get("title"),

                    "poster":
                    self.image_base_url +
                    str(movie.get("poster_path")),

                    "rating":
                    movie.get("vote_average"),

                    "release_date":
                    movie.get("release_date")
                })

            return movies

        except Exception as e:

            return {
                "error": str(e)
            }