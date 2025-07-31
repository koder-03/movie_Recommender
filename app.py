import streamlit as st
import pandas as pd
import requests
import os
# import os
import subprocess

# Ensure tmdbv3api is installed in case Streamlit fails
try:
    from tmdbv3api import TMDb, Movie
except ModuleNotFoundError:
    subprocess.check_call(["pip", "install", "tmdbv3api"])
    from tmdbv3api import TMDb, Movie


# from IPython.display import Image, display
from tmdbv3api import TMDb, Movie

tmdb = TMDb()
tmdb.api_key = 'b4889c220bb2a9153b9cbef13509f81e' 


def download_file(url, filename):
    if not os.path.exists(filename):
        with open(filename, 'wb') as f:
            response = requests.get(url)
            f.write(response.content)

download_file('https://drive.google.com/uc?id=1hT8IgPCK3jDJJM-LIhTbPNvDJZ-FArt0', 'similarity.pkl')

st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title( "🎬Movie Recommender System")


import pickle 

with open('new_df.pkl', 'rb') as file:
    new_df = pickle.load(file)


with open('similarity.pkl', 'rb') as file:
    similarity = pickle.load(file)


def poster(movie_name):
    movie = Movie()
    try:
        results = movie.search(movie_name)
        movie_id = results[0].id
        details = movie.details(movie_id)
        poster_path = details.poster_path
        poster_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
        return poster_url
    except:
        return "https://via.placeholder.com/300x450.png?text=No+Image"




def recommend(movie):
    movies_name = []
    movies_poster = []
    movie_index = new_df[new_df.title == movie].index[0]
    values = sorted(enumerate(similarity[movie_index]), key=lambda x: x[1], reverse=True)[1:6]
    for i in values:
        movies_name.append(new_df.iloc[i[0]].title)
        movies_poster.append(poster(new_df.iloc[i[0]].title))

    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.image(movies_poster[idx])
            st.caption(movies_name[idx])


option = st.selectbox(
    "what is your current favourite movie",
    (new_df['title']),
)

st.write("You selected:", option)

if st.button("Recommend"):
    recommend(option)



