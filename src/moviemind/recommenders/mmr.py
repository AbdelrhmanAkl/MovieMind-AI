import numpy as np
import pandas as pd


def recommend_mmr(
    candidates: pd.DataFrame,
    genre_similarity: np.ndarray,
    movie_genres: pd.DataFrame,
    top_n: int = 10,
    lambda_param: float = 0.7,
) -> pd.DataFrame:

    if candidates.empty:
        return candidates.copy()

    if not 0 <= lambda_param <= 1:
        raise ValueError("lambda_param must be between 0 and 1.")

    movie_ids = movie_genres["movie_id"].to_numpy()
    movie_to_index = {
        movie_id: index
        for index, movie_id in enumerate(movie_ids)
    }

    candidates = candidates[
        candidates["movie_id"].isin(movie_to_index)
    ].copy()

    if candidates.empty:
        return candidates

    candidate_ids = candidates["movie_id"].tolist()
    candidate_indices = [
        movie_to_index[movie_id]
        for movie_id in candidate_ids
    ]

    relevance = candidates["rrf_score"].to_numpy(dtype=float)

    if relevance.max() > relevance.min():
        relevance = (
            (relevance - relevance.min())
            / (relevance.max() - relevance.min())
        )
    else:
        relevance = np.ones(len(relevance))

    similarity = genre_similarity[
        np.ix_(candidate_indices, candidate_indices)
    ]

    selected = []
    remaining = list(range(len(candidate_ids)))

    while remaining and len(selected) < top_n:
        mmr_scores = []

        for idx in remaining:
            if not selected:
                diversity_penalty = 0
            else:
                diversity_penalty = max(
                    similarity[idx, selected]
                )

            score = (
                lambda_param * relevance[idx]
                - (1 - lambda_param) * diversity_penalty
            )

            mmr_scores.append((idx, score))

        best_idx, _ = max(mmr_scores, key=lambda item: item[1])

        selected.append(best_idx)
        remaining.remove(best_idx)

    result = candidates.iloc[selected].copy()
    result["mmr_rank"] = range(1, len(result) + 1)

    return result.reset_index(drop=True)