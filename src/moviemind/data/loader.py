from pathlib import Path
import json

import numpy as np
import pandas as pd


ROOT_DIR = Path(__file__).resolve().parents[3]

DATA_DIR = ROOT_DIR / "data" / "raw"
HYBRID_DIR = ROOT_DIR / "artifacts" / "hybrid"
MMR_DIR = ROOT_DIR / "artifacts" / "mmr"


def load_movies():
    return pd.read_csv(DATA_DIR / "movies.csv")


def load_ratings():
    return pd.read_csv(DATA_DIR / "ratings.csv")


def load_user_item_matrix():
    return pd.read_parquet(HYBRID_DIR / "user_item_matrix.parquet")


def load_user_similarity():
    return np.load(HYBRID_DIR / "user_similarity.npy")


def load_popularity_model():
    return pd.read_csv(HYBRID_DIR / "popularity_model.csv")


def load_id_mappings():
    with open(HYBRID_DIR / "id_mappings.json", encoding="utf-8") as file:
        return json.load(file)


def load_mmr_artifacts():
    return {
        "movie_genres": pd.read_csv(MMR_DIR / "movie_genres.csv"),
        "genre_similarity": np.load(MMR_DIR / "genre_similarity.npy"),
    }