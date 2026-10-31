
import re

import pandas as pd
import plotly.express as px
import streamlit as st

from src.moviemind.data.loader import load_movies, load_ratings
from src.moviemind.services.recommendation_service import RecommendationService


# =========================================================
# PAGE CONFIGURATION
# =========================================================

st.set_page_config(
    page_title="MovieMind AI",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)


# =========================================================
# DESIGN SYSTEM
# =========================================================

st.markdown(
    """
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    :root {
        --bg: #080D18;
        --surface: #101827;
        --surface-2: #151F31;
        --border: #243149;
        --text: #F1F5F9;
        --muted: #94A3B8;
        --accent: #38BDF8;
        --accent-2: #818CF8;
    }

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    .stApp {
        background:
            radial-gradient(ellipse at 15% 0%, rgba(56,189,248,.08), transparent 35%),
            radial-gradient(ellipse at 90% 10%, rgba(129,140,248,.07), transparent 30%),
            var(--bg);
        color: var(--text);
    }

    [data-testid="stHeader"] {
        background: transparent;
    }

    [data-testid="stSidebar"] {
        background: #0D1524;
        border-right: 1px solid var(--border);
    }

    [data-testid="stSidebar"] > div:first-child {
        padding-top: 2rem;
    }

    [data-testid="stSidebar"] * {
        color: var(--text);
    }

    .brand {
        font-size: 25px;
        font-weight: 800;
        letter-spacing: -1.2px;
        color: #F8FAFC;
    }

    .brand span {
        color: var(--accent);
    }

    .brand-caption {
        color: var(--muted);
        font-size: 11px;
        letter-spacing: 2px;
        margin-top: 5px;
    }

    .eyebrow {
        color: var(--accent);
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 2px;
        text-transform: uppercase;
        margin-bottom: 10px;
    }

    .hero-title {
        color: #F8FAFC;
        font-size: clamp(30px, 4vw, 48px);
        font-weight: 800;
        line-height: 1.15;
        letter-spacing: -2px;
        margin-bottom: 12px;
    }

    .hero-title span {
        color: var(--accent);
    }

    .hero-description {
        color: var(--muted);
        font-size: 14px;
        line-height: 1.8;
        max-width: 700px;
        margin-bottom: 28px;
    }

    .section-heading {
        color: var(--text);
        font-size: 22px;
        font-weight: 750;
        letter-spacing: -.6px;
        margin: 25px 0 5px 0;
    }

    .section-description {
        color: var(--muted);
        font-size: 13px;
        margin-bottom: 20px;
    }

    .metric-card {
        background: linear-gradient(145deg, #17243A, #101827);
        border: 1px solid var(--border);
        border-radius: 16px;
        padding: 21px;
        min-height: 125px;
        transition: .2s ease;
    }

    .metric-card:hover {
        border-color: #3B82F6;
        transform: translateY(-2px);
    }

    .metric-label {
        color: var(--muted);
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1px;
    }

    .metric-value {
        color: #F8FAFC;
        font-size: 29px;
        font-weight: 800;
        margin-top: 13px;
        letter-spacing: -1px;
    }

    .metric-note {
        color: #64748B;
        font-size: 11px;
        margin-top: 4px;
    }

    .movie-card {
        background: linear-gradient(155deg, #17243A, #101827);
        border: 1px solid var(--border);
        border-radius: 15px;
        padding: 17px;
        min-height: 190px;
        margin-bottom: 14px;
        transition: .2s ease;
    }

    .movie-card:hover {
        border-color: var(--accent);
        transform: translateY(-3px);
    }

    .movie-number {
        color: var(--accent);
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 1px;
        margin-bottom: 12px;
    }

    .movie-title {
        color: #F8FAFC;
        font-size: 16px;
        font-weight: 750;
        line-height: 1.5;
        margin-bottom: 12px;
    }

    .movie-meta {
        color: var(--muted);
        font-size: 12px;
        line-height: 1.8;
    }

    .movie-tag {
        display: inline-block;
        background: rgba(56,189,248,.10);
        color: #7DD3FC;
        border: 1px solid rgba(56,189,248,.20);
        border-radius: 20px;
        padding: 4px 9px;
        font-size: 10px;
        margin: 3px 3px 0 0;
    }

    .hero-panel {
        background: linear-gradient(115deg, #14243A, #171B35);
        border: 1px solid #2B3C58;
        border-radius: 20px;
        padding: 30px;
        margin: 15px 0 25px 0;
    }

    .hero-panel-title {
        font-size: 27px;
        font-weight: 800;
        color: #F8FAFC;
        margin-bottom: 9px;
    }

    .hero-panel-text {
        color: #A8B7CA;
        font-size: 13px;
        line-height: 1.8;
    }

    div.stButton > button {
        background: linear-gradient(100deg, #0284C7, #4F46E5);
        color: white;
        border: 0;
        border-radius: 10px;
        padding: 10px 18px;
        min-height: 43px;
        font-weight: 700;
        transition: .2s ease;
    }

    div.stButton > button:hover {
        border: 0;
        color: white;
        filter: brightness(1.15);
    }

    div[data-baseweb="select"] > div,
    div[data-baseweb="input"] > div {
        background: #111C2D;
        border-color: var(--border);
        border-radius: 10px;
    }

    .stTextInput label,
    .stSelectbox label,
    .stSlider label {
        color: #CBD5E1 !important;
        font-weight: 600;
    }

    [data-testid="stMetric"] {
        background: var(--surface);
        border: 1px solid var(--border);
        padding: 15px;
        border-radius: 12px;
    }

    [data-testid="stMetricLabel"] {
        color: var(--muted);
    }

    [data-testid="stMetricValue"] {
        color: var(--text);
    }

    hr {
        border-color: var(--border);
    }

    .footer {
        color: #64748B;
        font-size: 11px;
        text-align: center;
        padding: 25px 0 10px 0;
    }

    </style>
    """,
    unsafe_allow_html=True,
)


# =========================================================
# DATA AND MODEL LOADING
# =========================================================

@st.cache_data
def get_data():
    movies = load_movies()
    ratings = load_ratings()
    return movies, ratings


@st.cache_resource
def get_recommendation_service():
    return RecommendationService()


try:
    movies, ratings = get_data()
except Exception as error:
    st.error(f"Unable to load project data: {error}")
    st.stop()


# =========================================================
# SHARED HELPERS
# =========================================================

GENRE_COLUMNS = [
    column
    for column in movies.columns
    if column not in {
        "movie_id",
        "title",
        "release_date",
        "video_release_date",
        "IMDb URL",
    }
    and pd.api.types.is_numeric_dtype(movies[column])
]

def extract_year(title):
    match = re.search(r"\((\d{4})\)\s*$", str(title))
    return int(match.group(1)) if match else None


def get_movie_genres(row):
    return [
        genre
        for genre in GENRE_COLUMNS
        if row.get(genre, 0) == 1
    ]


def render_movie_card(title, genres, rank=None, year=None):
    number = f"RECOMMENDATION #{rank}" if rank else "MOVIE"
    genre_html = "".join(
        f'<span class="movie-tag">{genre}</span>'
        for genre in genres[:4]
    )

    year_text = str(year) if year else "Year unavailable"

    st.markdown(
        f"""
        <div class="movie-card">
            <div class="movie-number">{number}</div>
            <div class="movie-title">{title}</div>
            <div class="movie-meta">{year_text}</div>
            <div style="margin-top:10px">{genre_html}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric(label, value, note=""):
    st.markdown(
        f"""
        <div class="metric-card">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_page_header(eyebrow, title, description):
    st.markdown(
        f"""
        <div class="eyebrow">{eyebrow}</div>
        <div class="hero-title">{title}</div>
        <div class="hero-description">{description}</div>
        """,
        unsafe_allow_html=True,
    )


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:
    st.markdown(
        '<div class="brand">MOVIE<span>MIND</span></div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="brand-caption">INTELLIGENT MOVIE DISCOVERY</div>',
        unsafe_allow_html=True,
    )

    st.divider()

    page = st.radio(
        "EXPLORE",
        [
            "Dashboard",
            "Movie Discovery",
            "Recommendations",
            "About",
        ],
        label_visibility="visible",
    )

    st.divider()

    st.markdown("**PROJECT INFORMATION**")
    st.caption("Dataset: MovieLens 100K")
    st.caption("Movies: 1,682")
    st.caption("Recommendation: Hybrid + MMR")

    st.divider()

    st.caption("MOVIEMIND AI")
    st.caption("Machine Learning Recommendation Platform")


# =========================================================
# DASHBOARD
# =========================================================

if page == "Dashboard":

    render_page_header(
        "YOUR PERSONAL MOVIE INTELLIGENCE",
        'Discover Movies <span>Smarter.</span>',
        "Explore a movie universe powered by collaborative filtering, "
        "hybrid recommendation algorithms, and intelligent ranking.",
    )

    total_movies = movies["movie_id"].nunique()
    total_users = ratings["user_id"].nunique()
    total_ratings = len(ratings)
    average_rating = ratings["rating"].mean()

    columns = st.columns(4)

    metrics = [
        ("MOVIES", f"{total_movies:,}", "Available in the catalog"),
        ("USERS", f"{total_users:,}", "Dataset user profiles"),
        ("RATINGS", f"{total_ratings:,}", "Recorded user ratings"),
        ("AVG. RATING", f"{average_rating:.2f}/5", "Overall dataset average"),
    ]

    for column, (label, value, note) in zip(columns, metrics):
        with column:
            render_metric(label, value, note)

    st.markdown(
        '<div class="section-heading">Explore MovieMind</div>',
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div class="section-description">'
        'Everything you need to discover your next favorite movie.'
        '</div>',
        unsafe_allow_html=True,
    )

    left, right = st.columns(2)

    with left:
        st.markdown(
            """
            <div class="hero-panel">
                <div class="eyebrow">MOVIE EXPLORATION</div>
                <div class="hero-panel-title">Find your next favorite.</div>
                <div class="hero-panel-text">
                    Search the movie catalog and explore titles
                    across different genres and release years.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Explore Movies", key="dashboard_discovery"):
            st.session_state["navigation"] = "Movie Discovery"
            st.rerun()

    with right:
        st.markdown(
            """
            <div class="hero-panel">
                <div class="eyebrow">PERSONALIZED DISCOVERY</div>
                <div class="hero-panel-title">Made around your taste.</div>
                <div class="hero-panel-text">
                    Select a user profile and discover recommendations
                    generated by our hybrid recommendation engine.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        if st.button("Get Recommendations", key="dashboard_recommendations"):
            st.session_state["navigation"] = "Recommendations"
            st.rerun()

    st.markdown(
        '<div class="section-heading">Rating Distribution</div>',
        unsafe_allow_html=True,
    )

    rating_distribution = (
        ratings["rating"]
        .value_counts()
        .sort_index()
        .rename_axis("Rating")
        .reset_index(name="Number of Ratings")
    )

    fig = px.bar(
        rating_distribution,
        x="Rating",
        y="Number of Ratings",
        text="Number of Ratings",
        template="plotly_dark",
    )

    fig.update_traces(
        marker_color="#38BDF8",
        textposition="outside",
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, t=20, b=10),
        height=330,
        xaxis=dict(dtick=1),
    )

    st.plotly_chart(fig, use_container_width=True)


# =========================================================
# MOVIE DISCOVERY
# =========================================================

elif page == "Movie Discovery":

    render_page_header(
        "EXPLORE THE CATALOG",
        "Movie Discovery",
        "Search, filter, and explore movies from the MovieLens collection.",
    )

    search_col, genre_col, year_col = st.columns([2, 1, 1])

    with search_col:
        search = st.text_input(
            "Search by title",
            placeholder="Search for a movie...",
        )

    with genre_col:
        available_genres = sorted(GENRE_COLUMNS)
        selected_genre = st.selectbox(
            "Genre",
            ["All Genres"] + available_genres,
        )

    movie_years = sorted(
        {
            year
            for year in movies["title"].apply(extract_year)
            if year is not None
        },
        reverse=True,
    )

    with year_col:
        selected_year = st.selectbox(
            "Release year",
            ["All Years"] + movie_years,
        )

    filtered = movies.copy()

    if search:
        filtered = filtered[
            filtered["title"].str.contains(
                search,
                case=False,
                na=False,
                regex=False,
            )
        ]

    if selected_genre != "All Genres":
        filtered = filtered[
            filtered[selected_genre] == 1
        ]

    if selected_year != "All Years":
        filtered = filtered[
            filtered["title"].apply(extract_year) == selected_year
        ]

    st.markdown(
        f'<div class="section-description">{len(filtered):,} movies found</div>',
        unsafe_allow_html=True,
    )

    if filtered.empty:
        st.info("No movies match your search. Try different filters.")
    else:
        page_size = 12
        total_pages = (len(filtered) - 1) // page_size + 1

        selected_page = st.selectbox(
            "Page",
            range(1, total_pages + 1),
            format_func=lambda value: f"Page {value} of {total_pages}",
        )

        start = (selected_page - 1) * page_size
        page_movies = filtered.iloc[start:start + page_size]

        for start_index in range(0, len(page_movies), 3):
            row = page_movies.iloc[start_index:start_index + 3]
            columns = st.columns(3)

            for column, (_, movie) in zip(columns, row.iterrows()):
                with column:
                    render_movie_card(
                        title=movie["title"],
                        genres=get_movie_genres(movie),
                        year=extract_year(movie["title"]),
                    )


# =========================================================
# RECOMMENDATIONS
# =========================================================

elif page == "Recommendations":

    render_page_header(
        "PERSONALIZED FOR YOU",
        "Your Next Favorite Movie.",
        "Choose a user profile and let MovieMind AI discover movies "
        "based on collaborative preferences and intelligent ranking.",
    )

    st.markdown(
        """
        <div class="hero-panel">
            <div class="eyebrow">HYBRID RECOMMENDATION ENGINE</div>
            <div class="hero-panel-title">Discover beyond your watchlist.</div>
            <div class="hero-panel-text">
                Our system combines user-based collaborative filtering
                with popularity ranking using Reciprocal Rank Fusion.
                Optional MMR ranking can increase recommendation diversity.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    try:
        service = get_recommendation_service()
        available_users = sorted(
            service.user_item_matrix.index.astype(int).tolist()
        )
    except Exception as error:
        st.error(f"Unable to initialize recommendation engine: {error}")
        st.stop()

    with st.container(border=True):
        st.markdown("### Select your profile")
        st.caption(
            "Choose one of the user profiles available in the trained model."
        )

        selected_user = st.selectbox(
            "User profile",
            options=available_users,
            format_func=lambda user_id: f"User #{user_id}",
        )

        diversity_enabled = st.toggle(
            "Enable recommendation diversity (MMR)",
            value=False,
        )

        lambda_param = 1.0

        if diversity_enabled:
            lambda_param = st.slider(
                "Relevance vs. Diversity",
                min_value=0.0,
                max_value=1.0,
                value=0.7,
                step=0.1,
                help=(
                    "Higher values prioritize relevance. "
                    "Lower values prioritize genre diversity."
                ),
            )

        generate = st.button(
            "Generate My Recommendations",
            type="primary",
            use_container_width=True,
        )

    if generate:
        try:
            with st.spinner("Analyzing preferences and generating recommendations..."):
                recommendations = service.recommend(
                    user_id=int(selected_user),
                    top_n=10,
                    diversity=diversity_enabled,
                    lambda_param=lambda_param if diversity_enabled else None,
                )

            if recommendations.empty:
                st.warning("No recommendations are available for this profile.")
            else:
                st.session_state["recommendation_results"] = recommendations
                st.session_state["recommendation_user"] = selected_user
                st.session_state["recommendation_diversity"] = diversity_enabled

        except Exception as error:
            st.error(f"Recommendation generation failed: {error}")

    if "recommendation_results" in st.session_state:
        results = st.session_state["recommendation_results"]
        result_user = st.session_state["recommendation_user"]
        result_diversity = st.session_state["recommendation_diversity"]

        st.divider()

        st.markdown(
            '<div class="section-heading">Your Recommended Movies</div>',
            unsafe_allow_html=True,
        )

        st.markdown(
            f'<div class="section-description">'
            f'Recommendations generated for User #{result_user}. '
            f'{"MMR diversity enabled." if result_diversity else "Standard hybrid ranking."}'
            f'</div>',
            unsafe_allow_html=True,
        )

        extra_columns = [
            column
            for column in GENRE_COLUMNS
            if column in movies.columns
        ]

        results = results.merge(
            movies[["movie_id"] + extra_columns],
            on="movie_id",
            how="left",
        )

        for start_index in range(0, len(results), 2):
            row = results.iloc[start_index:start_index + 2]
            columns = st.columns(2)

            for column, (_, recommendation) in zip(columns, row.iterrows()):
                with column:
                    genres = get_movie_genres(recommendation)
                    render_movie_card(
                        title=recommendation["title"],
                        genres=genres,
                        rank=int(recommendation.get("mmr_rank", start_index + 1)),
                        year=extract_year(recommendation["title"]),
                    )

        st.caption(
            "Recommendations are generated from the trained MovieLens model. "
            "They are not guarantees of personal preference."
        )


# =========================================================
# ABOUT
# =========================================================

elif page == "About":

    render_page_header(
        "THE TECHNOLOGY BEHIND THE EXPERIENCE",
        "About MovieMind AI",
        "A machine learning recommendation platform built to make "
        "movie discovery more intelligent and personalized.",
    )

    st.markdown(
        """
        <div class="hero-panel">
            <div class="eyebrow">PROJECT OVERVIEW</div>
            <div class="hero-panel-title">Intelligent Movie Discovery</div>
            <div class="hero-panel-text">
                MovieMind AI uses the MovieLens 100K dataset to explore
                personalized recommendation strategies. The platform
                combines collaborative filtering, popularity-based ranking,
                and recommendation diversity techniques.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Recommendation Architecture")
        st.markdown(
            """
            - User-Based Collaborative Filtering
            - Popularity-Based Recommendation
            - Reciprocal Rank Fusion (RRF)
            - Maximum Marginal Relevance (MMR)
            """
        )

    with col2:
        st.markdown("### Technology Stack")
        st.markdown(
            """
            - Python
            - Pandas and NumPy
            - Scikit-learn
            - Streamlit
            - Plotly
            """
        )

    st.markdown("### Dataset")
    st.write(
        "MovieLens 100K — 100,000 ratings from 943 users "
        "across 1,682 movies."
    )


# =========================================================
# FOOTER
# =========================================================

st.markdown(
    """
    <div class="footer">
        MOVIEMIND AI &nbsp; | &nbsp; INTELLIGENT MOVIE DISCOVERY
    </div>
    """,
    unsafe_allow_html=True,
)
