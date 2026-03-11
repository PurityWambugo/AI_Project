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
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=DM+Sans:wght@300;400;500;600&display=swap');

:root {
    --bg: #0D0D0F;
    --surface: #16161A;
    --surface2: #1E1E24;
    --border: #2A2A34;
    --gold: #C9A84C;
    --gold-light: #E8C97A;
    --gold-dim: rgba(201,168,76,0.15);
    --cream: #F0EAD6;
    --muted: #6B6878;
    --text: #EEEAE0;
}

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: var(--bg) !important;
    color: var(--text);
}

#MainMenu, footer, header { visibility: hidden; }
.block-container {
    padding: 0 1.5rem 4rem !important;
    max-width: 700px !important;
}

/* ── FILM STRIP TOP BORDER ── */
.filmstrip {
    width: 100%;
    height: 28px;
    background: var(--gold);
    display: flex;
    align-items: center;
    overflow: hidden;
    margin-bottom: 0;
}
.filmstrip-hole {
    width: 18px;
    height: 14px;
    background: var(--bg);
    border-radius: 3px;
    margin: 0 6px;
    flex-shrink: 0;
}

/* ── HERO ── */
.hero {
    text-align: center;
    padding: 3rem 1rem 2.5rem;
}

.hero-eyebrow {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.28em;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 1rem;
}

.hero-title {
    font-family: 'Playfair Display', serif;
    font-size: 4.2rem;
    font-weight: 900;
    line-height: 1;
    color: var(--cream);
    margin: 0 0 0.3rem;
}

.hero-title em {
    color: var(--gold);
    font-style: italic;
}

.hero-tagline {
    font-family: 'Playfair Display', serif;
    font-style: italic;
    font-size: 1rem;
    color: var(--muted);
    margin-bottom: 2rem;
}

/* ── STATS ROW ── */
.stats-row {
    display: flex;
    justify-content: center;
    border: 1px solid var(--border);
    border-radius: 14px;
    overflow: hidden;
    margin: 0 auto 2.5rem;
    max-width: 480px;
    background: var(--surface);
}

.stat-item {
    flex: 1;
    padding: 0.9rem 0.5rem;
    text-align: center;
    border-right: 1px solid var(--border);
}
.stat-item:last-child { border-right: none; }

.stat-number {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--gold);
    line-height: 1;
}

.stat-label {
    font-size: 0.65rem;
    font-weight: 500;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--muted);
    margin-top: 3px;
}

/* ── STATUS BADGE ── */
.status-wrap { text-align: center; margin-bottom: 2rem; }

.status-badge {
    display: inline-flex;
    align-items: center;
    gap: 7px;
    background: rgba(76,175,80,0.1);
    border: 1px solid rgba(76,175,80,0.3);
    color: #81C784;
    padding: 6px 16px;
    border-radius: 100px;
    font-size: 0.76rem;
    font-weight: 500;
}

.status-dot {
    width: 7px; height: 7px;
    background: #4CAF50;
    border-radius: 50%;
    display: inline-block;
    animation: blink 2s infinite;
}

@keyframes blink {
    0%,100% { opacity:1; }
    50% { opacity:0.3; }
}

/* ── HOW IT WORKS ── */
.how-section {
    display: flex;
    gap: 1rem;
    margin-bottom: 2.5rem;
}

.how-step {
    flex: 1;
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 1.1rem;
    text-align: center;
}

.how-icon { font-size: 1.5rem; margin-bottom: 0.4rem; }

.how-title {
    font-size: 0.78rem;
    font-weight: 600;
    color: var(--cream);
    margin-bottom: 0.25rem;
}

.how-desc {
    font-size: 0.72rem;
    color: var(--muted);
    line-height: 1.5;
}

/* ── SECTION LABEL ── */
.section-label {
    font-size: 0.68rem;
    font-weight: 600;
    letter-spacing: 0.22em;
    text-transform: uppercase;
    color: var(--gold);
    margin-bottom: 0.75rem;
    display: flex;
    align-items: center;
    gap: 8px;
}
.section-label::after {
    content: '';
    flex: 1;
    height: 1px;
    background: var(--border);
}

/* ── INPUT LABELS ── */
.field-label {
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.14em;
    text-transform: uppercase;
    color: var(--muted);
    margin-bottom: 5px;
}

.field-hint {
    font-size: 0.72rem;
    color: var(--muted);
    margin-top: 4px;
}

/* ── Streamlit widgets ── */
div[data-testid="stNumberInput"] input {
    background: var(--surface2) !important;
    border: 1.5px solid var(--border) !important;
    border-radius: 10px !important;
    color: var(--cream) !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1.1rem !important;
}
div[data-testid="stNumberInput"] input:focus {
    border-color: var(--gold) !important;
    box-shadow: 0 0 0 3px var(--gold-dim) !important;
}
div[data-testid="stNumberInput"] button {
    background: var(--surface2) !important;
    border-color: var(--border) !important;
    color: var(--gold) !important;
}

div[data-testid="stButton"] > button {
    background: var(--gold) !important;
    color: #0D0D0F !important;
    border: none !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
    padding: 0.8rem 2rem !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
    margin-top: 0.25rem !important;
}
div[data-testid="stButton"] > button:hover {
    background: var(--gold-light) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 28px rgba(201,168,76,0.4) !important;
}

/* Download button — outlined gold style */
div[data-testid="stDownloadButton"] > button {
    background: transparent !important;
    color: var(--gold) !important;
    border: 1.5px solid var(--gold) !important;
    border-radius: 10px !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.9rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.04em !important;
    padding: 0.65rem 2rem !important;
    width: 100% !important;
    transition: all 0.2s ease !important;
}
div[data-testid="stDownloadButton"] > button:hover {
    background: var(--gold-dim) !important;
    color: var(--gold-light) !important;
    border-color: var(--gold-light) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(201,168,76,0.25) !important;
}

/* ── RESULTS ── */
.results-heading {
    font-family: 'Playfair Display', serif;
    font-size: 1.6rem;
    font-weight: 700;
    color: var(--cream);
    margin: 2.5rem 0 0.25rem;
}
.results-sub {
    font-size: 0.82rem;
    color: var(--muted);
    margin-bottom: 1.25rem;
}

.movie-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.55rem;
    display: flex;
    align-items: center;
    gap: 1rem;
    transition: border-color 0.2s, transform 0.15s;
}
.movie-card:hover {
    border-color: var(--gold);
    transform: translateX(3px);
}

.movie-rank {
    font-family: 'Playfair Display', serif;
    font-size: 1.4rem;
    font-weight: 900;
    color: var(--border);
    min-width: 2rem;
    text-align: center;
}

.movie-title {
    flex: 1;
    font-size: 0.95rem;
    font-weight: 500;
    color: var(--cream);
    line-height: 1.35;
}

.rating-pill {
    background: var(--gold-dim);
    border: 1px solid var(--gold);
    color: var(--gold-light);
    font-family: 'Playfair Display', serif;
    font-size: 0.95rem;
    font-weight: 700;
    padding: 4px 11px;
    border-radius: 100px;
    white-space: nowrap;
}

.bar-wrap {
    width: 60px; height: 3px;
    background: var(--border);
    border-radius: 100px;
    overflow: hidden;
    margin: 4px 0 0 auto;
}
.bar-fill {
    height: 3px;
    border-radius: 100px;
    background: linear-gradient(90deg, var(--gold), var(--gold-light));
}

.gold-divider {
    border: none;
    border-top: 1px solid var(--border);
    margin: 2rem 0;
}
</style>
""", unsafe_allow_html=True)


# ── Film strip decoration ──────────────────────────────────────────────────────
holes = "".join(['<div class="filmstrip-hole"></div>'] * 35)
st.markdown(f'<div class="filmstrip">{holes}</div>', unsafe_allow_html=True)


# ── Hero ──────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="hero">
    <div class="hero-eyebrow">✦ AI-Powered &nbsp;·&nbsp; Collaborative Filtering</div>
    <div class="hero-title">Cine<em>Match</em></div>
    <div class="hero-tagline">"The right film, for the right person, at the right moment."</div>
</div>
""", unsafe_allow_html=True)


# ── Stats row ─────────────────────────────────────────────────────────────────
st.markdown("""
<div class="stats-row">
    <div class="stat-item">
        <div class="stat-number">943</div>
        <div class="stat-label">Users</div>
    </div>
    <div class="stat-item">
        <div class="stat-number">1,682</div>
        <div class="stat-label">Films</div>
    </div>
    <div class="stat-item">
        <div class="stat-number">100K+</div>
        <div class="stat-label">Ratings</div>
    </div>
    <div class="stat-item">
        <div class="stat-number">SVD</div>
        <div class="stat-label">Algorithm</div>
    </div>
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

# ── Status badge ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="status-wrap">
    <span class="status-badge">
        <span class="status-dot"></span>
        Model loaded &amp; ready
    </span>
</div>
""", unsafe_allow_html=True)


# ── How it works ──────────────────────────────────────────────────────────────
st.markdown("""
<div class="how-section">
    <div class="how-step">
        <div class="how-icon">🎭</div>
        <div class="how-title">Your Taste Profile</div>
        <div class="how-desc">Your past ratings reveal hidden preferences across genres and eras.</div>
    </div>
    <div class="how-step">
        <div class="how-icon">🧠</div>
        <div class="how-title">SVD Matching</div>
        <div class="how-desc">Matrix factorisation finds users like you and surfaces what they loved.</div>
    </div>
    <div class="how-step">
        <div class="how-icon">🎬</div>
        <div class="how-title">Your Programme</div>
        <div class="how-desc">A ranked shortlist of unseen films, scored by predicted enjoyment.</div>
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)


# ── Inputs ────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">Your preferences</div>', unsafe_allow_html=True)

col1, col2 = st.columns([1, 1], gap="large")

with col1:
    st.markdown('<div class="field-label">User ID</div>', unsafe_allow_html=True)
    user_id = st.number_input(
        label="uid", min_value=1, max_value=943, value=1,
        label_visibility="collapsed"
    )
    st.markdown('<div class="field-hint">Any ID from 1 – 943</div>', unsafe_allow_html=True)

with col2:
    st.markdown('<div class="field-label">Number of Recommendations</div>', unsafe_allow_html=True)
    n = st.slider(
        label="n", min_value=5, max_value=20, value=10,
        label_visibility="collapsed"
    )
    st.markdown(f'<div class="field-hint">Top <strong style="color:var(--gold-light)">{n}</strong> unseen films</div>', unsafe_allow_html=True)

st.markdown("")
run = st.button("🎬  Generate My Recommendations")


# ── Results ───────────────────────────────────────────────────────────────────
if run:
    with st.spinner("Scanning 1,682 films…"):
        try:
            results = get_recommendations(user_id, n, ratings, movies_clean, model)

            st.markdown(f"""
            <div class="results-heading">Your Programme</div>
            <div class="results-sub">
                {n} personalised picks for User #{user_id} &nbsp;·&nbsp; ranked by predicted rating
            </div>
            """, unsafe_allow_html=True)

            for i, movie in enumerate(results, 1):
                rating = movie['rating']
                bar_pct = int((rating / 5) * 100)
                st.markdown(f"""
                <div class="movie-card">
                    <div class="movie-rank">{i:02d}</div>
                    <div class="movie-title">{movie['title']}</div>
                    <div style="text-align:right">
                        <div class="rating-pill">★ {rating}</div>
                        <div class="bar-wrap">
                            <div class="bar-fill" style="width:{bar_pct}%"></div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

            # ── Download ──────────────────────────────────────────────────────
            st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)

            df_download = pd.DataFrame([
                {"Rank": i, "Movie Title": m['title'], "Predicted Rating": m['rating']}
                for i, m in enumerate(results, 1)
            ])
            csv = df_download.to_csv(index=False).encode('utf-8')

            st.markdown("""
            <div style="text-align:center; margin-bottom: 0.6rem;">
                <div style="font-size:0.68rem; font-weight:600; letter-spacing:0.18em;
                            text-transform:uppercase; color:var(--muted); margin-bottom:0.5rem;">
                    Save your list
                </div>
            </div>
            """, unsafe_allow_html=True)

            st.download_button(
                label="⬇  Download Recommendations (.csv)",
                data=csv,
                file_name=f"cinematch_user{user_id}_top{n}.csv",
                mime="text/csv",
            )

        except Exception as e:
            st.error(f"Something went wrong: {e}")


# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown('<hr class="gold-divider">', unsafe_allow_html=True)
st.markdown("""
<div style="text-align:center; color:#3A3A48; font-size:0.72rem; padding-bottom:1rem;">
    Powered by Surprise &nbsp;·&nbsp; SVD Collaborative Filtering &nbsp;·&nbsp; MovieLens 100K Dataset
</div>
""", unsafe_allow_html=True)
