<div align="center">

# 🎬 MovieMind AI

**A hybrid movie recommender with personalized ranking and diversity optimization**

[![Live Demo](https://img.shields.io/badge/Live_Demo-Streamlit-8B7CFF?style=for-the-badge&logo=streamlit&logoColor=white)](https://moviemind-ai-0.streamlit.app/)
[![Python](https://img.shields.io/badge/Python-3.13-42D6C5?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/Tests-7_passed-F2C879?style=for-the-badge&logo=pytest&logoColor=white)](#testing)

[**Live Demo**](https://moviemind-ai-0.streamlit.app/) · [**Architecture**](#architecture) · [**Evaluation**](#evaluation-results) · [**Run Locally**](#getting-started)

</div>

<p align="center">
  <img src="docs/screenshots/home.png" alt="MovieMind AI home page" width="900">
</p>

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Application Tour](#application-tour)
- [Architecture](#architecture)
- [Dataset](#dataset)
- [Evaluation Methodology](#evaluation-methodology)
- [Evaluation Results](#evaluation-results)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Movie Posters (TMDB)](#movie-posters-tmdb)
- [Testing](#testing)
- [Limitations and Roadmap](#limitations-and-roadmap)
- [Author](#author)

---

## Overview

MovieMind AI recommends movies by combining three signals: what similar users liked, what the whole community rates highly, and how varied the final list is.

It is built on **MovieLens 100K**. User-based collaborative filtering and popularity ranking are merged with **Reciprocal Rank Fusion (RRF)**, then optionally re-ranked with **Maximal Marginal Relevance (MMR)** to balance relevance against genre diversity.

The project also puts weight on honest evaluation: models are tested on a **chronological split**, so recommendations are never scored using future interactions.

## Key Features

| | Feature | Description |
|---|---|---|
| 🎯 | **Hybrid engine** | User-based collaborative filtering plus popularity ranking, merged with weighted RRF |
| 🌈 | **Diversity control** | MMR re-ranking with an adjustable relevance-versus-diversity slider |
| 🖼️ | **Poster-rich interface** | Real movie posters, hero collage, and detail view for every title |
| 🔎 | **Discovery** | Search by title, filter by genre and release year, browse by collection |
| 📊 | **Analytics** | Interactive Plotly charts for ratings, genres, and model evaluation |
| ✅ | **Rigorous evaluation** | Temporal validation, ranking metrics, and a diversity trade-off analysis |

## Application Tour

| Page | What it does |
|---|---|
| **Home** | Cinematic hero, dataset statistics, and Popular, Top Rated, and Hidden Gems collections |
| **Discover** | Search and filter the full catalog, with a detail panel per movie |
| **For You** | Pick a user profile, choose how many recommendations, toggle MMR, and generate ranked results |
| **Analytics** | Rating distribution, genre breakdown, and the temporal test metrics |
| **About** | Architecture overview, technology stack, and project links |

<p align="center">
  <img src="docs/screenshots/for-you.png" alt="Personalized recommendations" width="440">
  <img src="docs/screenshots/discover.png" alt="Movie discovery" width="440">
</p>

## Architecture

```text
                MovieLens 100K Dataset
                          |
                          v
                Data Preprocessing
                          |
                          v
                User-Item Interaction Matrix
                          |
             +------------+------------+
             |                         |
             v                         v
     User-Based CF              Popularity-Based
     Recommendations            Recommendations
             |                         |
             +------------+------------+
                          |
                          v
              Reciprocal Rank Fusion (RRF)
                          |
                          v
               Hybrid Candidate Ranking
                          |
                          v
               MMR Diversity Re-ranking
                          |
                          v
               Personalized Top-N Movies
```

### Components

**User-based collaborative filtering** finds users with similar rating patterns and uses their preferences to propose candidates.

**Popularity ranking** scores movies with a weighted popularity measure, which complements the personalized signal.

**Reciprocal Rank Fusion** merges both rankings. The temporal hybrid configuration uses:

| Parameter | Value |
|---|---:|
| User-based weight | 0.2 |
| Popularity weight | 0.8 |
| RRF constant | 60 |

**Maximal Marginal Relevance** re-ranks candidates using genre similarity. A higher lambda favors relevance, a lower lambda favors diversity. The default is set in `config/model_config.json`.

## Dataset

[MovieLens 100K](https://grouplens.org/datasets/movielens/100k/) from GroupLens.

| Property | Value |
|---|---:|
| Ratings | 100,000 |
| Users | 943 |
| Movies | 1,682 |
| Average rating | 3.53 |
| Rating scale | 1 to 5 |

MovieLens users are anonymous. The names shown in the interface are display aliases generated from the user ID, and each profile's taste label is computed from that user's real ratings of 4 stars and above.

## Evaluation Methodology

**Random per-user split.** An 80/20 split per user, used for baselines and initial analysis.

**Chronological temporal split.** All ratings are sorted by timestamp and divided into:

| Split | Interactions |
|---|---:|
| Training | 70,001 |
| Validation | 14,999 |
| Testing | 15,000 |

The final hybrid model is trained on training plus validation, then scored on the held-out test period. This limits leakage from future interactions. A movie counts as relevant when its rating is **4 or higher**.

## Evaluation Results

### Final temporal test performance

| Metric | @5 | @10 |
|---|---:|---:|
| Precision | 0.1415 | 0.1915 |
| Recall | 0.0222 | 0.0659 |
| MAP | 0.1029 | 0.1055 |
| NDCG | 0.1515 | 0.1889 |

### Relevance versus diversity (MMR lambda)

| Lambda | Precision@10 | NDCG@10 | Catalog coverage | Intra-list diversity |
|---:|---:|---:|---:|---:|
| 1.0 | 0.1915 | 0.1889 | 2.91% | 0.8259 |
| 0.7 | 0.1642 | 0.1658 | 4.10% | 0.9260 |
| 0.5 | 0.1486 | 0.1509 | 4.34% | 0.9389 |
| 0.3 | 0.1387 | 0.1429 | 5.17% | 0.9514 |

Lowering lambda raises coverage and intra-list diversity at the cost of ranking accuracy. MMR is a deliberate trade-off, not a free improvement.

### Model comparison

An SVD collaborative filtering model (Surprise) was also evaluated. The best grid-search configuration was 50 factors, 30 epochs, learning rate 0.005, and regularization 0.05, with a cross-validation RMSE of 0.9540.

## Tech Stack

| Category | Technologies |
|---|---|
| Language | Python |
| Data | Pandas, NumPy |
| Machine learning | Scikit-learn, Surprise (experiments) |
| Techniques | Collaborative filtering, RRF, MMR, SVD |
| Storage | Parquet, CSV, NumPy |
| Visualization | Plotly |
| Web app | Streamlit |
| Posters | TMDB API, Wikipedia (fallback) |
| Testing | Pytest |
| Tooling | Git, GitHub, Streamlit Community Cloud |

## Project Structure

```text
MovieMind-AI/
├── app.py                      # Streamlit application
├── requirements.txt
├── .streamlit/
│   ├── config.toml             # Theme
│   └── secrets.toml            # Local secrets (not committed)
├── artifacts/
│   ├── hybrid/                 # User-item matrix, similarity, popularity
│   └── mmr/                    # Genre similarity and MMR data
├── config/model_config.json
├── data/raw/                   # movies.csv, ratings.csv
├── docs/screenshots/           # README images
├── evaluation/                 # Metric CSVs for every experiment
├── notebooks/
├── src/moviemind/
│   ├── data/
│   ├── evaluation/
│   ├── recommenders/
│   ├── services/
│   └── utils/
└── tests/
```

## Getting Started

**Prerequisites:** Python 3.13 and Git.

```bash
git clone https://github.com/AbdelrhmanAkl/MovieMind-AI.git
cd MovieMind-AI

python -m venv .venv
.\.venv\Scripts\Activate.ps1          # Windows PowerShell
# source .venv/bin/activate           # Linux / macOS

pip install -r requirements.txt
streamlit run app.py
```

The app opens at `http://localhost:8501`.

## Movie Posters (TMDB)

Posters load from [TMDB](https://www.themoviedb.org/) when an API key is configured, and fall back to the film's Wikipedia image otherwise. A poster is shown only when the title and release year match. If none is found, a placeholder is displayed.

1. Create a free key at [themoviedb.org](https://www.themoviedb.org/settings/api).
2. Add it as a secret.

**Locally**, in `.streamlit/secrets.toml`:

```toml
TMDB_API_KEY = "your_api_key"
```

**On Streamlit Community Cloud**, open *Manage app → Settings → Secrets* and paste the same line.

Never commit `secrets.toml`. Make sure it is listed in `.gitignore`.

> This product uses the TMDB API but is not endorsed or certified by TMDB.

## Testing

```bash
python -m pytest -v
```

Current status: `7 passed`.

## Limitations and Roadmap

- Improve long-tail discovery and catalog coverage.
- Explore additional hybrid weighting strategies.
- Add cold-start handling for new users.
- Bring in richer movie metadata and content-based signals.
- Evaluate more ranking and diversity metrics.
- Collect user feedback for adaptive recommendations.

## Author

**Abdelrahman Akl**
AI Engineer · Machine Learning · Deep Learning · Agentic AI

[GitHub](https://github.com/AbdelrhmanAkl) · [LinkedIn](https://www.linkedin.com/in/abdelrahmanakl/)

---

<div align="center">

*MovieMind AI: smarter recommendations, better movie discovery.*

</div>
