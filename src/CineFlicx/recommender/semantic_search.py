import pandas as pd

from sklearn.feature_extraction.text import (
    TfidfVectorizer
)

from sklearn.metrics.pairwise import (
    cosine_similarity
)


class SemanticSearch:

    def __init__(self):

        self.movies = pd.read_csv(
            "artifacts/validated_data/clean_movies.csv"
        )

        # =========================================
        # CREATE TEXT FEATURES
        # =========================================

        self.movies["combined_text"] = (

            self.movies["title"]
            .fillna("")

            + " " +

            self.movies["genres"]
            .fillna("")
        )

        # =========================================
        # TF-IDF
        # =========================================

        self.vectorizer = TfidfVectorizer(
            stop_words="english"
        )

        self.vectors = self.vectorizer.fit_transform(
            self.movies["combined_text"]
        )

    # =============================================
    # SEARCH
    # =============================================

    def search(
        self,
        query,
        top_k=10
    ):

        query_vector = self.vectorizer.transform(
            [query]
        )

        similarity = cosine_similarity(
            query_vector,
            self.vectors
        ).flatten()

        top_indices = similarity.argsort()[-top_k:][::-1]

        results = []

        for idx in top_indices:

            movie = self.movies.iloc[idx]

            results.append({

                "movieid":
                movie["movieId"],

                "title":
                movie["title"],

                "genres":
                movie["genres"],

                "score":
                float(similarity[idx])
            })

        return results