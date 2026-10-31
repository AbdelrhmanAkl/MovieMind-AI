import pandas as pd


def recommend_user_based(
    user_id: int,
    user_item_matrix: pd.DataFrame,
    user_similarity,
    top_n: int = 200,
) -> pd.DataFrame:

    if user_id not in user_item_matrix.index:
        return pd.DataFrame(
            columns=["movie_id", "user_score", "support"]
        )

    matrix = user_item_matrix.fillna(0)

    user_index = matrix.index.get_loc(user_id)
    similarities = user_similarity[user_index]

    weighted_scores = matrix.T.dot(similarities)

    rated_mask = matrix.loc[user_id] > 0
    weighted_scores = weighted_scores[~rated_mask]

    recommendations = weighted_scores.sort_values(
        ascending=False
    ).head(top_n)

    return pd.DataFrame({
        "movie_id": recommendations.index,
        "user_score": recommendations.values,
        "support": 0,
    }).reset_index(drop=True)