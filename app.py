import streamlit as st
import pandas as pd
import pickle

st.title("Movie Recommendation System")
st.write("Enter a User ID to get personalised movie recommendations!")

@st.cache_resource(show_spinner=False)
def load_model():
    with open('model.pkl', 'rb') as f:
        model = pickle.load(f)
    return model

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
        title = movies_clean[
            movies_clean['movie_id'] == p.iid
        ]['title'].values[0]
        results.append({
            'Movie Title': title,
            'Predicted Rating': round(p.est, 2)
        })
    return pd.DataFrame(results)

model = load_model()
ratings, movies_clean = load_data()
st.success("Model ready!")

user_id = st.number_input(
    "Enter User ID (1-943):", min_value=1, max_value=943, value=1
)
n = st.slider("Number of recommendations:", 5, 20, 10)

if st.button("Get Recommendations"):
    with st.spinner("Finding movies for you..."):
        results = get_recommendations(
            user_id, n, ratings, movies_clean, model
        )
    st.success(f"Top {n} recommendations for User {user_id}:")
    st.dataframe(results)
