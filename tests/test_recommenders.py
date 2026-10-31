import pandas as pd

from src.moviemind.recommenders.popularity import recommend_popular_movies


def test_popularity_recommendations():
    popularity_model = pd.DataFrame({
        "movie_id": [1, 2, 3, 4],
        "weighted_rating": [4.5, 4.2, 4.8, 4.0],
        "title": ["Movie A", "Movie B", "Movie C", "Movie D"],
    })

    original_model = popularity_model.copy()

    recommendations = recommend_popular_movies(
        popularity_model=popularity_model,
        seen_movie_ids={3},
        top_n=2,
    )

    assert len(recommendations) == 2
    assert 3 not in recommendations["movie_id"].values
    assert recommendations["weighted_rating"].is_monotonic_decreasing
    pd.testing.assert_frame_equal(popularity_model, original_model)

import numpy as np

from src.moviemind.recommenders.user_based import recommend_user_based
from src.moviemind.recommenders.hybrid import reciprocal_rank_fusion
from src.moviemind.recommenders.mmr import recommend_mmr


def test_user_based_recommendations():
    matrix = pd.DataFrame(
        [[5.0, 4.0, float("nan")],
         [4.0, float("nan"), 5.0]],
        index=[1, 2],
        columns=[10, 20, 30],
    )

    similarity = np.array([
        [1.0, 0.5],
        [0.5, 1.0],
    ])

    result = recommend_user_based(1, matrix, similarity, top_n=2)

    assert len(result) == 1
    assert result.iloc[0]["movie_id"] == 30
    assert result["user_score"].notna().all()


def test_reciprocal_rank_fusion():
    result = reciprocal_rank_fusion(
        user_ranking=[1, 2, 3],
        popularity_ranking=[2, 3, 4],
        user_weight=0.2,
        popularity_weight=0.8,
        rrf_k=60,
    )

    assert set(result["movie_id"]) == {1, 2, 3, 4}
    assert result["rrf_score"].notna().all()
    assert result["rrf_score"].is_monotonic_decreasing
    assert result.iloc[0]["movie_id"] == 2

def test_mmr_recommendations():
    candidates = pd.DataFrame({
        "movie_id": [1, 2, 3],
        "rrf_score": [0.9, 0.8, 0.7],
    })

    movie_genres = pd.DataFrame({
        "movie_id": [1, 2, 3],
    })

    genre_similarity = np.array([
        [1.0, 0.95, 0.10],
        [0.95, 1.0, 0.15],
        [0.10, 0.15, 1.0],
    ])

    result = recommend_mmr(
        candidates=candidates,
        genre_similarity=genre_similarity,
        movie_genres=movie_genres,
        top_n=2,
        lambda_param=0.5,
    )

    assert len(result) == 2
    assert result["movie_id"].nunique() == 2
    assert result["mmr_rank"].tolist() == [1, 2]
    assert result["rrf_score"].notna().all()


def test_mmr_rejects_invalid_lambda():
    candidates = pd.DataFrame({
        "movie_id": [1],
        "rrf_score": [0.9],
    })

    movie_genres = pd.DataFrame({"movie_id": [1]})
    similarity = np.array([[1.0]])

    import pytest

    with pytest.raises(ValueError):
        recommend_mmr(
            candidates,
            similarity,
            movie_genres,
            lambda_param=1.5,
        )

from src.moviemind.services.recommendation_service import RecommendationService


def test_recommendation_service():
    service = RecommendationService()

    result = service.recommend(
        user_id=1,
        top_n=10,
    )

    assert len(result) == 10
    assert result["movie_id"].is_unique
    assert result["title"].notna().all()
    assert result["mmr_rank"].tolist() == list(range(1, 11))
    assert result["rrf_score"].notna().all()


def test_recommendation_service_without_diversity():
    service = RecommendationService()

    result = service.recommend(
        user_id=1,
        top_n=5,
        diversity=False,
    )

    assert len(result) == 5
    assert result["movie_id"].is_unique
    assert result["title"].notna().all()
    assert "mmr_rank" not in result.columns