import html
import re
from concurrent.futures import ThreadPoolExecutor

import pandas as pd
import plotly.express as px
import requests
import streamlit as st

from src.moviemind.data.loader import load_movies, load_ratings
from src.moviemind.services.recommendation_service import RecommendationService

st.set_page_config(page_title="MovieMind AI", page_icon="🎬", layout="wide",
                   initial_sidebar_state="collapsed")

PAGES = ["Home", "Discover", "For You", "Analytics", "About"]
GITHUB = "https://github.com/AbdelrhmanAkl/MovieMind-AI"
LIVE = "https://moviemind-ai-0.streamlit.app/"
LINKEDIN = "https://www.linkedin.com/in/abdelrahmanakl/"

# ---------------------------------------------------------------- styles
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600&family=Space+Grotesk:wght@500;600;700&display=swap');
:root{--bg:#080B12;--bg2:#101622;--card:#151D2B;--elev:#1B2637;--a:#8B7CFF;--b:#42D6C5;
--gold:#F2C879;--tx:#F5F7FC;--tx2:#9AA7BA;--mut:#657187;--bd:rgba(255,255,255,.08)}
html,body,[class*="css"]{font-family:'Inter',sans-serif}
.stApp{background:var(--bg);color:var(--tx)}
[data-testid="stHeader"],[data-testid="stSidebar"],[data-testid="collapsedControl"],footer{display:none!important}
.block-container{max-width:1240px;padding:1.2rem 1.5rem 3rem}
h1,h2,h3,.disp{font-family:'Space Grotesk',sans-serif;letter-spacing:-.02em;color:var(--tx)}
/* nav */
div[data-testid="stRadio"] > div[role="radiogroup"]{gap:6px;background:var(--bg2);border:1px solid var(--bd);
 padding:5px;border-radius:14px;width:fit-content;flex-wrap:wrap}
div[data-testid="stRadio"] label{padding:8px 18px;border-radius:10px;cursor:pointer;margin:0}
div[data-testid="stRadio"] label > div:first-child{display:none}
div[data-testid="stRadio"] label p{color:var(--tx2);font-weight:500;font-size:14px}
div[data-testid="stRadio"] label:has(input:checked){background:var(--elev)}
div[data-testid="stRadio"] label:has(input:checked) p{color:var(--tx)}
.brand{font-family:'Space Grotesk';font-weight:700;font-size:22px;color:var(--tx)}
.brand i{font-style:normal;color:var(--a)}
/* hero */
.hero{position:relative;border-radius:22px;overflow:hidden;min-height:430px;margin:14px 0 28px;
 border:1px solid var(--bd);background:linear-gradient(120deg,#1B1740,#0F2A33)}
.hero .wall{position:absolute;inset:-10px;display:grid;grid-template-columns:repeat(8,1fr);gap:8px;opacity:.55;transform:rotate(-4deg) scale(1.1)}
.hero .wall img{width:100%;aspect-ratio:2/3;object-fit:cover;border-radius:8px}
.hero .shade{position:absolute;inset:0;background:linear-gradient(90deg,rgba(8,11,18,.97) 0%,rgba(8,11,18,.82) 45%,rgba(8,11,18,.35) 100%)}
.hero .in{position:relative;padding:64px 52px;max-width:660px}
.hero h1{font-size:clamp(34px,5vw,58px);line-height:1.05;margin:0 0 16px;font-weight:700}
.hero p{color:var(--tx2);font-size:17px;line-height:1.7;margin:0}
h2.sec{font-size:26px;margin:34px 0 4px;font-weight:600}
.sub{color:var(--tx2);font-size:14px;margin-bottom:16px}
/* cards */
.poster{border-radius:14px;overflow:hidden;background:var(--card);border:1px solid var(--bd);transition:transform .2s,border-color .2s}
.poster:hover{transform:translateY(-4px);border-color:rgba(139,124,255,.6)}
.poster .img{aspect-ratio:2/3;width:100%;position:relative;background:linear-gradient(160deg,#241F4D,#12313A)}
.poster img{width:100%;height:100%;object-fit:cover;display:block}
.poster .ph{position:absolute;inset:0;display:flex;align-items:center;justify-content:center;
 font:700 54px 'Space Grotesk';color:rgba(255,255,255,.18)}
.poster .rk{position:absolute;top:10px;left:10px;background:var(--gold);color:#201500;font-weight:700;
 font-size:12px;padding:3px 9px;border-radius:20px;z-index:2}
.poster .bd{padding:12px 13px 14px}
.poster .t{font-weight:600;font-size:14px;line-height:1.35;min-height:38px;color:var(--tx);
 display:-webkit-box;-webkit-line-clamp:2;-webkit-box-orient:vertical;overflow:hidden}
.poster .m{color:var(--mut);font-size:12px;margin-top:4px}
.tag{display:inline-block;font-size:11px;color:var(--b);background:rgba(66,214,197,.09);
 border:1px solid rgba(66,214,197,.2);border-radius:20px;padding:2px 8px;margin:6px 4px 0 0}
.stat{background:var(--card);border:1px solid var(--bd);border-radius:16px;padding:20px 22px}
.stat b{font:700 32px 'Space Grotesk';display:block}.stat span{color:var(--tx2);font-size:13px}
.panel{background:var(--card);border:1px solid var(--bd);border-radius:18px;padding:24px}
.flow{display:flex;flex-wrap:wrap;gap:10px;align-items:center}
.flow div{background:var(--elev);border:1px solid var(--bd);border-radius:12px;padding:12px 16px;font-size:13px;font-weight:500}
.flow span{color:var(--a)}
.badge{display:inline-block;background:var(--elev);border:1px solid var(--bd);border-radius:10px;padding:8px 14px;margin:0 8px 8px 0;font-size:13px}
div.stButton>button{background:var(--a);color:#0B0820;border:0;border-radius:11px;font-weight:600;min-height:42px}
div.stButton>button:hover{background:#A094FF;color:#0B0820}
div.stButton>button[kind="secondary"]{background:var(--elev);color:var(--tx);border:1px solid var(--bd)}
div[data-baseweb="select"]>div,div[data-baseweb="input"]>div{background:var(--bg2)!important;border-color:var(--bd)!important;border-radius:11px}
a{color:var(--b)!important}
div[data-baseweb="popover"] ul,div[data-baseweb="menu"]{background:var(--elev)!important}
div[data-baseweb="popover"] li,div[data-baseweb="menu"] li{color:var(--tx)!important;background:transparent!important}
div[data-baseweb="popover"] li:hover,div[data-baseweb="popover"] li[aria-selected="true"]{background:rgba(139,124,255,.18)!important}
div[data-baseweb="slider"] div[role="slider"]{background:var(--a)!important;box-shadow:none!important}
div[data-testid="stSliderThumbValue"]{color:var(--a)!important}
@media(max-width:760px){.hero .in{padding:36px 22px}.hero .wall{grid-template-columns:repeat(4,1fr)}}
</style>
""", unsafe_allow_html=True)

# ---------------------------------------------------------------- data
@st.cache_data
def get_data():
    return load_movies(), load_ratings()

@st.cache_resource
def get_service():
    return RecommendationService()

try:
    movies, ratings = get_data()
except Exception as e:
    st.error(f"Unable to load project data: {e}")
    st.stop()

NON_GENRE = {"movie_id", "title", "release_date", "video_release_date", "IMDb URL"}
GENRES = [c for c in movies.columns if c not in NON_GENRE and pd.api.types.is_numeric_dtype(movies[c])]

def year_of(title):
    m = re.search(r"\((\d{4})\)\s*$", str(title))
    return int(m.group(1)) if m else None

def genres_of(row):
    return [g for g in GENRES if row.get(g, 0) == 1]

@st.cache_data
def movie_stats():
    g = ratings.groupby("movie_id")["rating"].agg(avg="mean", n="count").reset_index()
    return g

STATS = movie_stats().set_index("movie_id")

@st.cache_data
def profile_labels():
    """Taste label per user, computed from the real ratings (4 stars and above)."""
    gcols = [g for g in GENRES if g.lower() != "unknown"]
    liked = ratings[ratings["rating"] >= 4][["user_id", "movie_id"]]
    top = liked.merge(movies[["movie_id"] + gcols], on="movie_id").groupby("user_id")[gcols].sum()
    out = {}
    for u, row in top.iterrows():
        names = [g for g, v in row.sort_values(ascending=False).head(2).items() if v > 0]
        out[int(u)] = " & ".join(names)
    return out

PROFILES = profile_labels()

FIRST = ["Omar", "Sara", "Youssef", "Mona", "Karim", "Laila", "Hassan", "Nour", "Tarek", "Salma", "Adam", "Yasmin",
         "Ziad", "Dina", "Ali", "Hana", "Mostafa", "Farida", "Ibrahim", "Rana", "Khaled", "Mariam", "Amir", "Jana",
         "Sam", "Emma", "Liam", "Mia", "Noah", "Zoe", "Leo", "Ava", "Ethan", "Chloe", "Lucas", "Nina", "Ryan", "Lily",
         "Daniel", "Sofia", "Max", "Ella", "Jack", "Maya", "Ben", "Iris", "Theo", "Ruby", "Eli", "Nora", "Owen", "Alma"]

def display_name(u):
    """Stable display alias for an anonymous MovieLens user id (the dataset has no real names)."""
    u = int(u)
    return f"{FIRST[(u * 37) % len(FIRST)]} {chr(65 + (u * 11 + u // len(FIRST)) % 26)}."

def user_label(u):
    t = PROFILES.get(int(u))
    return f"{display_name(u)} (#{u})" + (f" · {t} fan" if t else "")

# ---------------------------------------------------------------- posters (TMDB, verified by title + year)
def _tmdb_key():
    try:
        return st.secrets.get("TMDB_API_KEY")
    except Exception:
        return None

def _clean(title):
    t = re.sub(r"\s*\(\d{4}\)\s*$", "", str(title))
    t = re.sub(r"\s*\([^)]*\)", "", t).strip()
    m = re.match(r"^(.*), (The|A|An|Les|La|Le|Il|Das|Der|Die)$", t)
    return f"{m.group(2)} {m.group(1)}" if m else t

def _norm(t):
    return re.sub(r"[^a-z0-9]", "", str(t).lower())

def _tmdb_poster(title, year):
    key = _tmdb_key()
    if not key:
        return None
    try:
        r = requests.get("https://api.themoviedb.org/3/search/movie", timeout=6,
                         params={"api_key": key, "query": _clean(title), "year": year})
        for item in r.json().get("results", []):
            rd = item.get("release_date", "")[:4]
            if item.get("poster_path") and rd.isdigit() and abs(int(rd) - year) <= 1:
                return f"https://image.tmdb.org/t/p/w342{item['poster_path']}"
    except Exception:
        pass
    return None

def _wiki_poster(title, year):
    """No-key fallback: the film's own Wikipedia page image, accepted only if title and year match."""
    clean = _clean(title)
    try:
        r = requests.get("https://en.wikipedia.org/w/api.php", timeout=6,
                         headers={"User-Agent": "MovieMindAI/1.0 (student project)"},
                         params={"action": "query", "format": "json", "generator": "search",
                                 "gsrsearch": f"{clean} {year} film", "gsrlimit": 4, "prop": "pageimages|extracts",
                                 "piprop": "thumbnail", "pithumbsize": 342, "exintro": 1, "explaintext": 1,
                                 "exsentences": 2, "exlimit": "max"})
        pages = sorted(r.json().get("query", {}).get("pages", {}).values(), key=lambda p: p.get("index", 99))
        for p in pages:
            ok_title = _norm(p.get("title", "")).startswith(_norm(clean))
            ok_year = str(year) in (p.get("title", "") + " " + p.get("extract", ""))
            if ok_title and ok_year and p.get("thumbnail"):
                return p["thumbnail"]["source"]
    except Exception:
        pass
    return None

@st.cache_data(show_spinner=False, ttl=60 * 60 * 24 * 7)
def poster_url(title):
    year = year_of(title)
    if not year:
        return None
    return _tmdb_poster(title, year) or _wiki_poster(title, year)

def posters_for(titles):
    titles = list(titles)
    with ThreadPoolExecutor(max_workers=8) as ex:
        return dict(zip(titles, ex.map(poster_url, titles)))

# ---------------------------------------------------------------- components
def render_movie_card(title, genres, url, rank=None, note=""):
    t = html.escape(str(title))
    img = (f'<img src="{url}" alt="{t}" loading="lazy">' if url
           else f'<div class="ph">{html.escape(_clean(title)[:1].upper())}</div>')
    badge = f'<div class="rk">#{rank}</div>' if rank else ""
    tags = "".join(f'<span class="tag">{html.escape(g)}</span>' for g in genres[:3])
    meta = " · ".join(x for x in [str(year_of(title) or ""), note] if x)
    st.markdown(f'<div class="poster"><div class="img">{badge}{img}</div><div class="bd">'
                f'<div class="t">{t}</div><div class="m">{html.escape(meta)}</div>{tags}</div></div>',
                unsafe_allow_html=True)

def rating_note(movie_id):
    if movie_id in STATS.index:
        r = STATS.loc[movie_id]
        return f"★ {r['avg']:.2f} ({int(r['n'])})"
    return ""

def render_movie_grid(df, cols=5, key="g"):
    df = df.reset_index(drop=True)
    urls = posters_for(df["title"])
    for i in range(0, len(df), cols):
        cs = st.columns(cols)
        for c, (_, m) in zip(cs, df.iloc[i:i + cols].iterrows()):
            with c:
                render_movie_card(m["title"], genres_of(m), urls[m["title"]], note=rating_note(m["movie_id"]))
                if st.button("Details", key=f"{key}_{m['movie_id']}", use_container_width=True, type="secondary"):
                    st.session_state["detail"] = int(m["movie_id"])
                    st.rerun()

def render_section_header(title, sub=""):
    st.markdown(f'<h2 class="sec">{title}</h2><div class="sub">{sub}</div>', unsafe_allow_html=True)

def render_empty_state(title, text):
    st.markdown(f'<div class="panel" style="text-align:center"><h3>{title}</h3>'
                f'<div class="sub" style="margin:0">{text}</div></div>', unsafe_allow_html=True)

def go(page):
    st.session_state["page"] = page

def render_hero():
    top = STATS.sort_values("n", ascending=False).head(16).index
    wall_titles = movies[movies["movie_id"].isin(top)]["title"].tolist()
    urls = [u for u in posters_for(wall_titles).values() if u]
    wall = ""
    if urls:
        urls = (urls * 3)[:16]
        wall = '<div class="wall">' + "".join(f'<img src="{u}" alt="">' for u in urls) + "</div>"
    st.markdown(f'''<div class="hero">{wall}<div class="shade"></div><div class="in">
        <div class="brand" style="margin-bottom:22px">Movie<i>Mind</i> AI</div>
        <h1>Discover your next favorite movie.</h1>
        <p>Explore a world of movies powered by intelligent recommendations tailored to your preferences.</p>
        </div></div>''', unsafe_allow_html=True)
    a, b, _ = st.columns([1, 1.5, 3])
    a.button("Explore Movies", on_click=go, args=("Discover",), use_container_width=True, key="h1")
    b.button("Get Personalized Recommendations", on_click=go, args=("For You",),
             use_container_width=True, type="secondary", key="h2")

def render_detail():
    mid = st.session_state.get("detail")
    if mid is None:
        return
    row = movies[movies["movie_id"] == mid]
    if row.empty:
        return
    m = row.iloc[0]
    url = poster_url(m["title"])
    st.markdown('<div class="panel">', unsafe_allow_html=True)
    c1, c2 = st.columns([1, 3])
    with c1:
        if url:
            st.image(url, use_container_width=True)
    with c2:
        st.markdown(f"### {m['title']}")
        st.markdown("".join(f'<span class="tag">{html.escape(g)}</span>' for g in genres_of(m)), unsafe_allow_html=True)
        if mid in STATS.index:
            s = STATS.loc[mid]
            st.markdown(f"**★ {s['avg']:.2f}** average from **{int(s['n']):,}** ratings")
        if m.get("release_date") and str(m["release_date"]) != "nan":
            st.caption(f"Release date: {m['release_date']}")
        if str(m.get("IMDb URL", "")) not in ("", "nan"):
            st.markdown(f"[View on IMDb]({m['IMDb URL']})")
        if st.button("Close", key="close_detail", type="secondary"):
            st.session_state["detail"] = None
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

def style_fig(fig, h=340):
    fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                      height=h, margin=dict(l=10, r=10, t=30, b=10), font=dict(family="Inter", color="#9AA7BA"),
                      xaxis=dict(gridcolor="rgba(255,255,255,.04)"), yaxis=dict(gridcolor="rgba(255,255,255,.06)"))
    return fig

# ---------------------------------------------------------------- navigation
st.session_state.setdefault("page", "Home")
st.session_state.setdefault("detail", None)
nav_l, nav_r = st.columns([1, 3])
nav_l.markdown('<div class="brand" style="padding-top:8px">Movie<i>Mind</i></div>', unsafe_allow_html=True)
with nav_r:
    page = st.radio("Navigation", PAGES, key="page", horizontal=True, label_visibility="collapsed")

# ---------------------------------------------------------------- HOME
if page == "Home":
    render_hero()
    stats = [(f"{movies['movie_id'].nunique():,}", "Movies"), (f"{ratings['user_id'].nunique():,}", "Users"),
             (f"{len(ratings):,}", "Ratings"), (f"{ratings['rating'].mean():.2f}", "Average rating")]
    for c, (v, l) in zip(st.columns(4), stats):
        c.markdown(f'<div class="stat"><b>{v}</b><span>{l}</span></div>', unsafe_allow_html=True)

    joined = movies.merge(STATS.reset_index(), on="movie_id")
    collections = [
        ("Popular movies", "Most rated by the community", joined.sort_values("n", ascending=False)),
        ("Top rated", "Highest average rating, minimum 100 ratings", joined[joined["n"] >= 100].sort_values("avg", ascending=False)),
        ("Hidden gems", "Rated 4.0 or higher with fewer than 60 ratings", joined[(joined["avg"] >= 4.0) & (joined["n"].between(10, 59))].sort_values("avg", ascending=False)),
    ]
    for title, sub, df in collections:
        render_section_header(title, sub)
        render_movie_grid(df.head(5), key=title)
    render_detail()

# ---------------------------------------------------------------- DISCOVER
elif page == "Discover":
    render_section_header("Discover movies", "Search the catalog and filter by genre or release year.")
    render_detail()
    c1, c2, c3 = st.columns([2, 1, 1])
    q = c1.text_input("Search by title", placeholder="Try “Star Wars” or “Casablanca”")
    g = c2.selectbox("Genre", ["All genres"] + sorted(GENRES))
    years = sorted({y for y in movies["title"].map(year_of) if y}, reverse=True)
    y = c3.selectbox("Release year", ["All years"] + years)
    f = movies
    if q:
        f = f[f["title"].str.contains(q, case=False, na=False, regex=False)]
    if g != "All genres":
        f = f[f[g] == 1]
    if y != "All years":
        f = f[f["title"].map(year_of) == y]
    if f.empty:
        render_empty_state("No movies found", "Try a different title, or clear a filter.")
    else:
        per = 15
        pages = (len(f) - 1) // per + 1
        st.markdown(f'<div class="sub">{len(f):,} movies</div>', unsafe_allow_html=True)
        n = st.number_input("Page", 1, pages, 1, key="disc_page", help=f"{pages} pages") if pages > 1 else 1
        render_movie_grid(f.iloc[(n - 1) * per:n * per], key="disc")

# ---------------------------------------------------------------- FOR YOU
elif page == "For You":
    render_section_header("For you", "Profile names are display aliases for anonymous MovieLens users. Your recommendations combine collaborative filtering with popularity-based "
                          "ranking to discover movies aligned with your viewing preferences.")
    try:
        service = get_service()
        users = sorted(service.user_item_matrix.index.astype(int).tolist())
    except Exception as e:
        st.error(f"Unable to initialize the recommendation engine: {e}")
        st.stop()

    with st.container(border=True):
        c1, c2 = st.columns(2)
        uid = c1.selectbox("User profile", users, format_func=user_label)
        top_n = c2.slider("Number of recommendations", 5, 20, 10)
        div = st.toggle("Diversity optimization (MMR)", value=False)
        lam = None
        if div:
            lam = st.slider("Relevance vs. diversity", 0.0, 1.0, 0.7, 0.1,
                            help="Higher favors relevance. Lower favors genre diversity.")
            st.caption("MMR helps balance relevance and genre diversity, introducing a broader selection of movies.")
        go_btn = st.button("Generate recommendations", use_container_width=True)

    if go_btn:
        try:
            with st.spinner("Analyzing preferences..."):
                rec = service.recommend(user_id=int(uid), top_n=top_n, diversity=div, lambda_param=lam)
            if rec.empty:
                st.warning("No recommendations are available for this profile.")
            else:
                st.session_state["rec"] = (rec, uid, div)
        except Exception as e:
            st.error(f"Recommendation generation failed: {e}")

    if "rec" in st.session_state:
        rec, ruid, rdiv = st.session_state["rec"]
        render_section_header(f"Picked for {display_name(ruid)}", "MMR diversity enabled." if rdiv else "Standard hybrid ranking.")
        rec = rec.merge(movies[["movie_id"] + GENRES], on="movie_id", how="left", suffixes=("", "_m"))
        urls = posters_for(rec["title"])
        score_col = next((c for c in ("score", "rrf_score", "hybrid_score", "final_score") if c in rec.columns), None)
        for i in range(0, len(rec), 5):
            for c, (j, r) in zip(st.columns(5), rec.iloc[i:i + 5].iterrows()):
                with c:
                    note = f"score {r[score_col]:.3f}" if score_col else ""
                    render_movie_card(r["title"], genres_of(r), urls[r["title"]], rank=int(j) + 1, note=note)
        st.caption("Recommendations come from the trained MovieLens model and are not guarantees of preference.")
    else:
        render_empty_state("No recommendations yet", "Pick a profile above and select Generate recommendations.")

# ---------------------------------------------------------------- ANALYTICS
elif page == "Analytics":
    render_section_header("Analytics", "Dataset insights and the temporal evaluation of the hybrid model.")
    a, b = st.columns(2)
    rd = ratings["rating"].value_counts().sort_index().reset_index()
    rd.columns = ["Rating", "Ratings"]
    a.plotly_chart(style_fig(px.bar(rd, x="Rating", y="Ratings", title="Rating distribution",
                                    color_discrete_sequence=["#8B7CFF"])), use_container_width=True)
    gd = pd.Series({g: int(movies[g].sum()) for g in GENRES}).sort_values().reset_index()
    gd.columns = ["Genre", "Movies"]
    b.plotly_chart(style_fig(px.bar(gd, x="Movies", y="Genre", orientation="h", title="Movies per genre",
                                    color_discrete_sequence=["#42D6C5"]), 420), use_container_width=True)
    render_section_header("Recommendation evaluation", "Temporal test results for the hybrid model "
                          "(user weight 0.2, popularity weight 0.8, RRF constant 60).")
    ev = pd.DataFrame({"Metric": ["Precision", "Recall", "MAP", "NDCG"],
                       "@5": [0.1415, 0.0222, 0.1029, 0.1515], "@10": [0.1915, 0.0659, 0.1055, 0.1889]})
    t, ch = st.columns([1, 2])
    t.dataframe(ev, hide_index=True, use_container_width=True)
    long = ev.melt("Metric", var_name="Cutoff", value_name="Score")
    ch.plotly_chart(style_fig(px.bar(long, x="Metric", y="Score", color="Cutoff", barmode="group",
                                     color_discrete_sequence=["#8B7CFF", "#F2C879"])), use_container_width=True)
    st.caption("Diversity optimization trades some relevance for genre variety. It does not improve every ranking metric.")

# ---------------------------------------------------------------- ABOUT
else:
    render_section_header("About MovieMind AI", "A hybrid movie recommendation system built on MovieLens 100K.")
    st.markdown('<div class="panel"><div class="flow"><div>MovieLens dataset</div><span>→</span>'
                '<div>Data processing</div><span>→</span><div>Collaborative filtering + popularity</div><span>→</span>'
                '<div>Reciprocal Rank Fusion</div><span>→</span><div>MMR re-ranking</div><span>→</span>'
                '<div>Personalized recommendations</div></div></div>', unsafe_allow_html=True)
    render_section_header("Technology")
    st.markdown("".join(f'<span class="badge">{x}</span>' for x in
                        ["Python", "Pandas", "NumPy", "Scikit-learn", "Streamlit", "Plotly", "Git", "GitHub"]),
                unsafe_allow_html=True)
    render_section_header("Project")
    st.markdown(f"**Author:** Abdelrahman Akl  \n[GitHub repository]({GITHUB}) · [Live demo]({LIVE}) · "
                f"[GitHub profile](https://github.com/AbdelrhmanAkl) · [LinkedIn]({LINKEDIN})")
    st.caption("Posters come from TMDB (when configured) or Wikipedia. This product uses the TMDB API but is not endorsed or certified by TMDB.")
