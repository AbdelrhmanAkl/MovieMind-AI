# MovieMind AI
### Hybrid Movie Recommendation System with Personalized Ranking & Diversity Optimization

<p align="center">
  <a href="https://moviemind-ai-0.streamlit.app/"><strong>Live Demo</strong></a>
  &nbsp; | &nbsp;
  <a href="https://github.com/AbdelrhmanAkl/MovieMind-AI"><strong>GitHub Repository</strong></a>
</p>

---

## Overview

**MovieMind AI** is an intelligent movie recommendation system designed to deliver personalized movie suggestions by combining collaborative filtering, popularity-based ranking, and diversity-aware recommendation techniques.

Built using the **MovieLens 100K dataset**, the system implements a hybrid recommendation pipeline that combines user preference signals with global movie popularity through **Reciprocal Rank Fusion (RRF)**. It also incorporates **Maximal Marginal Relevance (MMR)** to balance recommendation relevance with genre diversity.

The project focuses not only on generating recommendations, but also on evaluating them under a chronological data-splitting strategy to better simulate real-world recommendation scenarios.

## Live Application

Explore MovieMind AI:

**[Launch MovieMind AI](https://moviemind-ai-0.streamlit.app/)**

## Key Features

- **Hybrid Recommendation Engine:** Combines user-based collaborative filtering and popularity-based recommendations.
- **Reciprocal Rank Fusion:** Integrates multiple recommendation rankings using weighted reciprocal rank fusion.
- **Personalized Discovery:** Generates recommendations based on historical user interactions.
- **Diversity Optimization:** Applies MMR to reduce genre similarity among recommended movies.
- **Adjustable Diversity:** Allows experimentation with the relevance-diversity trade-off through the MMR lambda parameter.
- **Movie Exploration:** Browse and explore movies from the MovieLens catalog.
- **Interactive Dashboard:** Provides an accessible interface for exploring recommendation results and dataset insights.
- **Comprehensive Evaluation:** Includes ranking metrics, temporal validation, model comparisons, and recommendation quality analysis.

## Recommendation Architecture

MovieMind AI follows a hybrid recommendation pipeline:

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
              Reciprocal Rank Fusion
                    (RRF)
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

### Recommendation Components

**1. User-Based Collaborative Filtering**

Identifies users with similar rating patterns and uses their preferences to generate candidate movie recommendations.

**2. Popularity-Based Recommendation**

Ranks movies using a weighted popularity score, providing a complementary source of recommendations.

**3. Reciprocal Rank Fusion (RRF)**

Combines the collaborative filtering and popularity rankings using weighted reciprocal rank fusion.

The temporal hybrid configuration uses:

- User-based weight: `0.2`
- Popularity weight: `0.8`
- RRF constant: `60`

**4. Maximal Marginal Relevance (MMR)**

Re-ranks candidate movies by balancing recommendation relevance and genre diversity.

The lambda parameter controls the trade-off:

- Higher lambda: prioritizes recommendation relevance.
- Lower lambda: encourages greater diversity.

## Dataset

The project uses the **MovieLens 100K dataset**.

| Dataset Property | Value |
|---|---:|
| Total Ratings | 100,000 |
| Unique Users | 943 |
| Movies | 1,682 |
| Average Rating | 3.53 |
| Rating Scale | 1–5 |

### Data Preparation

- Loaded and inspected user ratings and movie metadata.
- Checked duplicate user-movie interactions.
- Analyzed rating distributions and interaction sparsity.
- Constructed user-item interaction matrices.
- Prepared movie genre representations for diversity calculations.
- Generated recommendation artifacts for application inference.

Dataset source: [MovieLens 100K – GroupLens](https://grouplens.org/datasets/movielens/100k/)

## Experimental Methodology

To evaluate the system under realistic conditions, the project uses two evaluation strategies.

### 1. Random Per-User Split

Ratings are split per user into training and testing sets using an 80/20 strategy.

This experiment is used for baseline comparisons and initial recommendation analysis.

### 2. Chronological Temporal Split

Ratings are globally sorted by timestamp and divided into:

| Split | Interactions |
|---|---:|
| Training | 70,001 |
| Validation | 14,999 |
| Testing | 15,000 |

The final hybrid model is trained using the training and validation interactions, then evaluated on the held-out temporal test set.

This approach helps reduce information leakage from future interactions into historical recommendations.

## Evaluation Results

### Final Temporal Test Performance

The following results were obtained from the final temporal test evaluation.

| Metric | @5 | @10 |
|---|---:|---:|
| Precision | 0.1415 | 0.1915 |
| Recall | 0.0222 | 0.0659 |
| MAP | 0.1029 | 0.1055 |
| NDCG | 0.1515 | 0.1889 |

The evaluation uses relevance defined as a rating of **4 or higher**.

### Recommendation Diversity Analysis

MMR provides an adjustable trade-off between ranking quality and recommendation diversity.

The following results compare different MMR lambda values on the temporal test evaluation:

| Lambda | Precision@10 | NDCG@10 | Catalog Coverage | Intra-list Diversity |
|---:|---:|---:|---:|---:|
| 1.0 | 0.1915 | 0.1889 | 2.91% | 0.8259 |
| 0.7 | 0.1642 | 0.1658 | 4.10% | 0.9260 |
| 0.5 | 0.1486 | 0.1509 | 4.34% | 0.9389 |
| 0.3 | 0.1387 | 0.1429 | 5.17% | 0.9514 |

**Key Observation**

Reducing lambda increases catalog coverage and intra-list diversity, while decreasing ranking performance.

This demonstrates the practical trade-off between recommending highly relevant movies and exposing users to a broader range of genres.

## Model Comparison

The project also evaluates a Singular Value Decomposition (SVD) collaborative filtering model using the Surprise library during experimentation.

The best grid-search configuration was:

| Parameter | Value |
|---|---:|
| Number of Factors | 50 |
| Epochs | 30 |
| Learning Rate | 0.005 |
| Regularization | 0.05 |
| Cross-validation RMSE | 0.9540 |

The experiments also compare SVD and hybrid recommendations under a realistic full-catalog evaluation setup.

## Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn |
| Recommendation Techniques | Collaborative Filtering, RRF, MMR, SVD |
| Data Storage | Parquet, CSV, NumPy |
| Visualization | Plotly |
| Web Application | Streamlit |
| Testing | Pytest |
| Version Control | Git, GitHub |
| Deployment | Streamlit Community Cloud |

## Project Structure

```text
MovieMind-AI/
│
├── app.py
├── requirements.txt
├── README.md
├── .gitignore
├── .env.example
├── project_audit.csv
│
├── artifacts/
│   ├── hybrid/
│   │   ├── id_mappings.json
│   │   ├── popularity_model.csv
│   │   ├── user_item_matrix.parquet
│   │   └── user_similarity.npy
│   │
│   └── mmr/
│       ├── genre_id_to_index.json
│       ├── genre_similarity.npy
│       ├── movie_genres.csv
│       └── mmr_rankings.json
│
├── config/
│   └── model_config.json
│
├── data/
│   └── raw/
│       ├── movies.csv
│       └── ratings.csv
│
├── evaluation/
│   ├── final_hybrid_test_metrics.csv
│   ├── hybrid_realistic_metrics.csv
│   ├── hybrid_weight_optimization.csv
│   ├── mmr_temporal_test_results.csv
│   ├── random_results.csv
│   ├── random_weight_optimization.csv
│   ├── svd_realistic_metrics.csv
│   ├── svd_tuning_results.csv
│   ├── svd_validation_metrics.csv
│   ├── temporal_final_metrics.csv
│   ├── temporal_final_test_metrics.csv
│   ├── temporal_quality_metrics.csv
│   └── temporal_weight_optimization.csv
│
├── notebooks/
│   └── MovieMind_AI_Recommendation_System.ipynb
│
├── outputs/
│
├── src/
│   └── moviemind/
│       ├── data/
│       ├── evaluation/
│       ├── recommenders/
│       ├── services/
│       └── utils/
│
└── tests/
    ├── test_data_loader.py
    └── test_recommenders.py
```

## Installation & Setup

### Prerequisites

- Python 3.13
- Git

### 1. Clone the Repository

```bash
git clone https://github.com/AbdelrhmanAkl/MovieMind-AI.git
cd MovieMind-AI
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
```

### 3. Activate the Environment

**Windows PowerShell:**

```powershell
.\.venv\Scripts\Activate.ps1
```

**Linux / macOS:**

```bash
source .venv/bin/activate
```

### 4. Install Dependencies

```bash
pip install -r requirements.txt
```

### 5. Run the Application

```bash
streamlit run app.py
```

The application will be available locally at:

```text
http://localhost:8501
```

## Testing

The project includes automated tests for the recommendation components and recommendation service.

Run the test suite:

```bash
python -m pytest -v
```

Current test status:

```text
7 passed
```

## Limitations & Future Improvements

Potential areas for further development include:

- Improving long-tail movie discovery and catalog coverage.
- Exploring additional hybrid weighting strategies.
- Enhancing cold-start recommendations for new users.
- Incorporating richer movie metadata and content-based signals.
- Evaluating additional ranking and diversity metrics.
- Adding user feedback to support more adaptive recommendations.

## Author

**Abdelrahman Akl**

AI Engineer | Machine Learning | Deep Learning | Agentic AI

- GitHub: [@AbdelrhmanAkl](https://github.com/AbdelrhmanAkl)
- LinkedIn: [linkedin.com/in/abdelrahmanakl](https://www.linkedin.com/in/abdelrahmanakl/)

---

*MovieMind AI — Smarter Recommendations. Better Movie Discovery.*