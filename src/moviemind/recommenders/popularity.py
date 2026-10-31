import pandas as pd


def recommend_popular_movies(
    popularity_model: pd.DataFrame,
    seen_movie_ids: set,
    top_n: int = 10,
) -> pd.DataFrame:
    recommendations = popularity_model[
        ~popularity_model["movie_id"].isin(seen_movie_ids)
    ].copy()

    recommendations = recommendations.sort_values(
        "weighted_rating",
        ascending=False,
    )

    return recommendations.head(top_n).reset_index(drop=True)