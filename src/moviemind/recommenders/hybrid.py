import pandas as pd

from src.moviemind.recommenders.user_based import recommend_user_based
from src.moviemind.recommenders.popularity import recommend_popular_movies


def reciprocal_rank_fusion(
    user_ranking,
    popularity_ranking,
    user_weight: float = 0.2,
    popularity_weight: float = 0.8,
    rrf_k: int = 60,
) -> pd.DataFrame:

    scores = {}

    for rank, movie_id in enumerate(user_ranking, start=1):
        scores[movie_id] = scores.get(movie_id, 0) + (
            user_weight / (rrf_k + rank)
        )

    for rank, movie_id in enumerate(popularity_ranking, start=1):
        scores[movie_id] = scores.get(movie_id, 0) + (
            popularity_weight / (rrf_k + rank)
        )

    result = pd.DataFrame(
        scores.items(),
        columns=["movie_id", "rrf_score"],
    )

    return result.sort_values(
        "rrf_score",
        ascending=False,
    ).reset_index(drop=True)


def recommend_hybrid(
    user_id: int,
    user_item_matrix: pd.DataFrame,
    user_similarity,
    popularity_model: pd.DataFrame,
    top_n: int = 10,
    candidate_size: int = 200,
) -> pd.DataFrame:

    if user_id not in user_item_matrix.index:
        return recommend_popular_movies(
            popularity_model,
            set(),
            top_n,
        )

    seen_movie_ids = set(
        user_item_matrix.columns[
            user_item_matrix.loc[user_id].fillna(0) > 0
        ]
    )

    user_results = recommend_user_based(
        user_id,
        user_item_matrix,
        user_similarity,
        candidate_size,
    )

    popularity_results = recommend_popular_movies(
        popularity_model,
        seen_movie_ids,
        candidate_size,
    )

    fused = reciprocal_rank_fusion(
        user_results["movie_id"].tolist(),
        popularity_results["movie_id"].tolist(),
    )

    fused = fused[~fused["movie_id"].isin(seen_movie_ids)]

    return fused.head(top_n).reset_index(drop=True)