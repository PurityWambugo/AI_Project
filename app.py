import streamlit as st
import pandas as pd
import pickle
from surprise import SVD, Dataset, Reader
from surprise.model_selection import train_test_split

# Loading data
ratings = pd.read_csv(r'C:\Users\Administrator\Downloads\ml-100k\u.data',
                      sep='\t',
                      names=['user_id', 'movie_id', 'rating', 'timestamp'])
ratings = ratings.drop(columns=['timestamp'])

movies_clean = pd.read_csv(r'C:\Users\Administrator\Downloads\ml-100k\u.item',
                           sep='|', encoding='latin-1',
                           names=['movie_id', 'title', 'release_date', 'video_release',
                                  'imdb_url'] + [f'genre_{i}' for i in range(19)])
movies_clean = movies_clean[['movie_id', 'title']]

# Training model
reader = Reader(rating_scale=(1, 5))
data = Dataset.load_from_df(ratings[['user_id', 'movie_id', 'rating']], reader)
trainset = data.build_full_trainset()
model = SVD(random_state=42)
model.fit(trainset)

# Recommendation function
def get_recommendations(user_id, n=10):
    all_movie_ids = ratings['movie_id'].unique()
    watched = ratings[ratings['user_id'] == user_id]['movie_id'].unique()
    unwatched = [m for m in all_movie_ids if m not in watched]
    predictions_list = [model.predict(user_id, movie_id) for movie_id in unwatched]
    predictions_list.sort(key=lambda x: x.est, reverse=True)
    top_n = predictions_list[:n]
    recommended = []
    for pred in top_n:
        title = movies_clean[movies_clean['movie_id'] == pred.iid]['title'].values[0]
        recommended.append({'Movie Title': title, 'Predicted Rating': round(pred.est, 2)})
    return pd.DataFrame(recommended)

# Streamlit UI
st.title(" Movie Recommendation System")
st.write("Enter a User ID to get personalised movie recommendations!")

user_id = st.number_input("Enter User ID (1-943):", min_value=1, max_value=943, value=1)
n = st.slider("Number of recommendations:", 5, 20, 10)

if st.button("Get Recommendations"):
    with st.spinner("Finding movies for you..."):
        results = get_recommendations(user_id, n)
    st.success(f"Top {n} recommendations for User {user_id}:")
    st.dataframe(results)