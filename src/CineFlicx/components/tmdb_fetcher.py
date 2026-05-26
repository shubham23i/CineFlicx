import os
import requests

from dotenv import load_dotenv

from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry


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

        self.session = requests.Session()



        retries = Retry(
            total=5,
            backoff_factor=1,
            status_forcelist=[429, 500, 502, 503, 504]
        )

        adapter = HTTPAdapter(max_retries=retries)

        self.session.mount("https://", adapter)

    # =====================================================
    # GET MOVIE DETAILS
    # =====================================================

    def get_movie_details(self, tmdbid):

        try:

            url = f"{self.base_url}/movie/{tmdbid}"

            response = self.session.get(
                url,
                params={
                    "api_key": self.api_key
                },
                timeout=15
            )

            response.raise_for_status()

            data = response.json()

            poster = None
            backdrop = None

            if data.get("poster_path"):

                poster = (
                    self.image_base_url +
                    data["poster_path"]
                )

            if data.get("backdrop_path"):

                backdrop = (
                    self.image_base_url +
                    data["backdrop_path"]
                )

            
            return {

                "title":
                data.get("title"),

                "genres":
                "|".join(
                    [
                        genre.get("name")
                        for genre in data.get("genres", [])
                    ]
                ),

                "overview":
                data.get("overview"),

                "poster":
                poster,

                "backdrop":
                backdrop,

                "runtime":
                data.get("runtime"),

                "rating":
                round(
                    data.get("vote_average", 0),
                    1
                ),

                "release_date":
                data.get("release_date")
            }



        except Exception as e:

            print("DETAILS ERROR:", e)

            return {}
        

    # =====================================================
    # SEARCH MOVIE
    # =====================================================

    def search_movie(self, title):

        try:

            url = (
                f"{self.base_url}/search/movie"
            )

            response = self.session.get(

                url,

                params={
                    "api_key": self.api_key,
                    "query": title
                },

                timeout=15
            )

            response.raise_for_status()

            data = response.json()

            results = data.get("results", [])

            if len(results) == 0:

                return {}

            movie = results[0]

            return {

                "id":
                movie.get("id"),

                "title":
                movie.get("title")
            }

        except Exception as e:

            print("SEARCH MOVIE ERROR:", e)

            return {}

    # =====================================================
    # GET MOVIE CAST
    # =====================================================

    def get_movie_cast(self, tmdbid):

        try:

            url = f"{self.base_url}/movie/{tmdbid}/credits"

            response = self.session.get(
                url,
                params={
                    "api_key": self.api_key
                },
                timeout=15
            )

            response.raise_for_status()

            data = response.json()

            cast_data = []

            for actor in data.get("cast", [])[:10]:

                profile_path = actor.get("profile_path")

                cast_data.append({

                    "name":
                    actor.get("name"),

                    "character":
                    actor.get("character"),

                    "profile":
                    self.image_base_url + profile_path
                    if profile_path else None
                })

            return cast_data

        except Exception as e:

            print("CAST ERROR:", e)

            return []

    # =====================================================
    # GET MOVIE VIDEOS
    # =====================================================

    def get_movie_videos(self, tmdbid):

        try:

            url = f"{self.base_url}/movie/{tmdbid}/videos"

            response = self.session.get(
                url,
                params={
                    "api_key": self.api_key
                },
                timeout=15
            )

            response.raise_for_status()

            data = response.json()

            videos = []

            for video in data.get("results", []):

                if video.get("site") == "YouTube":

                    videos.append({

                        "name":
                        video.get("name"),

                        "key":
                        video.get("key")
                    })

            return videos

        except Exception as e:

            print("VIDEO ERROR:", e)

            return []