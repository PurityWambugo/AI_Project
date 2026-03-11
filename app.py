import streamlit as st
import pandas as pd
import pickle

st.set_page_config(
    page_title="CineMatch",
    page_icon="🎬",
    layout="centered",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700;900&family=DM+Sans:wght@300;400;500&display=swap');

:root {
    --cream: #F5F0E8;
    --charcoal: #1A1A1A;
    --gold: #C9A84C;
    --gold-light: #E8C97A;
    --rust: #B85C38;
    --warm-gray: #8A8078;
    --card-bg: #FFFFFF;
    --border: #E2D9CC;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--cream);
    color: var(--charcoal);
}

/* Hide Streamlit default elements */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 2rem 4rem; max-width: 720px; }

/* Hero Header */
.hero {
    text-align: center;
    padding: 3.5rem 0 2.5rem;
    border-bottom: 1px solid var(--border);
    margin-bottom: 2.5rem;
}

.hero-eyebrow {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 0.75rem;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 3.6rem;
    font-weight: 900;
    line-height: 1.05;
    color: var(--charcoal);
    margin: 0 0 1rem;
}

.hero-title span {
    color: var(--gold);
    font-style: italic;
}

.hero-subtitle {
    font-size: 1rem;
    font-weight: 300;
    color: var(--warm-gray);
    max-width: 380px;
    margin: 0 auto;
    line-height: 1.6;
}

/* Status badge */
.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    background: #F0FAF0;
    border: 1px solid #B8DFB8;
    color: #2D6A2D;
    padding: 6px 14px;
    border-radius: 100px;
    font-size: 0.78rem;
    font-weight: 500;
    margin-bottom: 2.5rem;
}

.status-dot {
    width: 7px;
    height: 7px;
    background: #4CAF50;
    border-radius: 50%;
    display: inline-block;
    animation: pulse 2s infinite;
}

@keyframes pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.4; }
}

/* Input card */
.input-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 2rem 2rem 1.5rem;
    margin-bottom: 1.5rem;
    box-shadow: 0 2px 16px rgba(0,0,0,0.05);
}

.input-label {
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--warm-gray);
    margin-bottom: 0.4rem;
}

/* Streamlit widget overrides */
div[data-testid="stNumberInput"] input,
div[data-testid="stTextInput"] input {
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1.05rem !important;
    padding: 0.65rem 1rem !important;
    background: var(--cream) !important;
    color: var(--charcoal) !important;
    transition: border-color 0.2s !important;
}

div[data-testid="stNumberInput"] input:focus,
div[data-testid="stTextInput"] input:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 3px rgba(201,168,76,0.15) !important;
}

/* Slider */
div[data-testid="stSlider"] div[data-baseweb="slider"] div[role="slider"] {
    background-color: var(--gold) !important;
}
div[data-testid="stSlider"] div[data-baseweb="slider"] div[data-testid="stSliderTrack"] div:first-child {
    background-color: var(--gold) !important;
}

/* Button */
div[data-testid="stButton"] > button {
    background: var(--charcoal) !important;
    color: var(--cream) !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.04em !important;
    padding: 0.75rem 2rem !important;
    width: 100% !important;
    cursor: pointer !important;
    transition: all 0.2s ease !important;
    margin-top: 0.5rem !important;
}

div[data-testid="stButton"] > button:hover {
    background: var(--gold) !important;
    color: var(--charcoal) !important;
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(201,168,76,0.35) !important;
}

/* Results section */
.results-header {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--charcoal);
    margin: 2rem 0 1rem;
}

.results-sub {
    font-size: 0.85rem;
    color: var(--warm-gray);
    margin-bottom: 1.25rem;
}

/* Movie cards */
.movie-card {
    background: var(--card-bg);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1rem 1.25rem;
    margin-bottom: 0.6rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    transition: box-shadow 0.2s, transform 0.2s;
}

.movie-card:hover {
    box-shadow: 0 4px 20px rgba(0,0,0,0.08);
    transform: translateY(-1px);
}

.movie-rank {
    font-family: 'Playfair Display', serif;
    font-size: 1.5rem;
    font-weight: 900;
    color: var(--border);
    min-width: 2.2rem;
    text-align: center;
    line-height: 1;
}

.movie-info { flex: 1; }

.movie-title {
    font-size: 0.97rem;
    font-weight: 500;
    color: var(--charcoal);
    line-height: 1.3;
}

.movie-rating-wrap {
    display: flex;
    align-items: center;
    gap: 6px;
}

.rating-pill {
    background: var(--charcoal);
    color: var(--gold-light);
    font-family: 'Playfair Display', serif;
    font-size: 1.05rem;
    font-weight: 700;
    padding: 4px 12px;
    border-radius: 100px;
    white-space: nowrap;
}

.rating-bar-bg {
    height: 4px;
    background: var(--border);
    border-radius: 100px;
    width: 80px;
    overflow: hidden;
}

.rating-bar-fill {
    height: 4px;
    border-radius: 100px;
    background: linear-gradient(90deg, var(--gold), var(--gold-light));
}

/* Divider */
.section-divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 2rem 0;
}

/* Success / Error */
div[data-testid="stAlert"] {
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
}
</style>
""", unsafe_allow_html=True)


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">✦ Personalised Discovery</div>
    <h1 class="hero-title">Cine<span>Match</span></h1>
    <p class="hero-subtitle">Tell us who you are. We'll find what you'll love.</p>
</div>
""", unsafe_allow_html=True)


# ── Load model & data ─────────────────────────────────────────────────────────
@st.cache_resource(show_spinner=False)
def load_model():
    with open('model.pkl', 'rb') as f:
        return pickle.load(f)

@st.cache_data(show_spinner=False)
def load_data():
    ratings = pd.read_csv('ratings.csv')
    movies_clean = pd.read_csv('movies_clean.csv')
    return ratings, movies_clean

def get_recommendations(user_id, n, ratings, movies_clean, model):
    all_movie_ids = ratings['movie_id'].unique()
    watched = ratings[ratings['user_id'] == user_id]['movie_id'].unique()
    unwatched = [m for m in all_movie_ids if m not in watched]
    preds = [model.predict(user_id, mid) for mid in unwatched]
    preds.sort(key=lambda x: x.est, reverse=True)
    top_n = preds[:n]
    results = []
    for p in top_n:
        title = movies_clean[movies_clean['movie_id'] == p.iid]['title'].values[0]
        results.append({'title': title, 'rating': round(p.est, 2)})
    return results

model = load_model()
ratings, movies_clean = load_data()

st.markdown("""
<div style="text-align:center; margin-bottom: 2rem;">
    <span class="status-badge">
        <span class="status-dot"></span>
        Model ready · 943 users · 1,682 films
    </span>
</div>
""", unsafe_allow_html=True)


# ── Input card ────────────────────────────────────────────────────────────────
st.markdown('<div class="input-card">', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<div class="input-label">Your User ID</div>', unsafe_allow_html=True)
    user_id = st.number_input(
        label="user_id",
        min_value=1, max_value=943, value=1,
        label_visibility="collapsed"
    )

with col2:
    st.markdown('<div class="input-label">Recommendations</div>', unsafe_allow_html=True)
    n = st.slider(
        label="n_recs",
        min_value=5, max_value=20, value=10,
        label_visibility="collapsed"
    )

st.markdown('</div>', unsafe_allow_html=True)

run = st.button("✦ Discover My Films")


# ── Results ───────────────────────────────────────────────────────────────────
if run:
    with st.spinner("Curating your personal programme…"):
        try:
            results = get_recommendations(user_id, n, ratings, movies_clean, model)

            st.markdown(f"""
            <div class="results-header">Your Programme</div>
            <div class="results-sub">Top {n} picks for User #{user_id} — ranked by predicted enjoyment</div>
            """, unsafe_allow_html=True)

            for i, movie in enumerate(results, 1):
                rating = movie['rating']
                bar_pct = int((rating / 5) * 100)
                st.markdown(f"""
                <div class="movie-card">
                    <div class="movie-rank">{i:02d}</div>
                    <div class="movie-info">
                        <div class="movie-title">{movie['title']}</div>
                    </div>
                    <div class="movie-rating-wrap">
                        <div>
                            <div class="rating-bar-bg">
                                <div class="rating-bar-fill" style="width:{bar_pct}%"></div>
                            </div>
                        </div>
                        <div class="rating-pill">★ {rating}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

        except Exception as e:
            st.error(f"Something went wrong: {e}")
