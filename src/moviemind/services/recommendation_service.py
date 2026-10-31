import json

from src.moviemind.data.loader import (
    load_user_item_matrix,
    load_user_similarity,
    load_popularity_model,
    load_movies,
    load_mmr_artifacts,
)

from src.moviemind.recommenders.hybrid import recommend_hybrid
from src.moviemind.recommenders.mmr import recommend_mmr


class RecommendationService:

    def __init__(self):
        with open("config/model_config.json", encoding="utf-8") as file:
            self.config = json.load(file)

        self.user_item_matrix = load_user_item_matrix()
        self.user_similarity = load_user_similarity()
        self.popularity_model = load_popularity_model()
        self.movies = load_movies()

        mmr_artifacts = load_mmr_artifacts()
        self.movie_genres = mmr_artifacts["movie_genres"]
        self.genre_similarity = mmr_artifacts["genre_similarity"]

    def recommend(
        self,
        user_id: int,
        top_n: int = 10,
        diversity: bool = True,
        lambda_param: float = None,
    ):

        hybrid_config = self.config["temporal_hybrid"]
        mmr_config = self.config["mmr"]

        candidates = recommend_hybrid(
            user_id=user_id,
            user_item_matrix=self.user_item_matrix,
            user_similarity=self.user_similarity,
            popularity_model=self.popularity_model,
            top_n=200,
        )

        if diversity:
            if lambda_param is None:
                lambda_param = mmr_config["default_lambda"]

            recommendations = recommend_mmr(
                candidates=candidates,
                genre_similarity=self.genre_similarity,
                movie_genres=self.movie_genres,
                top_n=top_n,
                lambda_param=lambda_param,
            )
        else:
            recommendations = candidates.head(top_n).copy()

        recommendations = recommendations.merge(
            self.movies[["movie_id", "title"]],
            on="movie_id",
            how="left",
        )

        return recommendations.reset_index(drop=True)