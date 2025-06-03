import streamlit as st
import pandas as pd
import requests
import pickle
from dotenv import load_dotenv
import os
load_dotenv()



def fetch_poster(id):
    
    api_key = os.getenv("tmdb_api_key")
    url = f"https://api.themoviedb.org/3/movie/{id}?api_key={api_key}&language=en-US"
    response = requests.get(url)
    data = response.json()
    print(data)
    poster_path = data['poster_path']
    full_image_url = f"https://image.tmdb.org/t/p/w500{poster_path}"
    return 'https://image.tmdb.org/t/p/w500'+ data['poster_path']


movies_list = pd.read_pickle('movies.pkl')
movies = movies_list['title'].values
## with open('similarity.pkl', 'rb') as f:
    ##similarity = pickle.load(f)
with open('similarity_matrix.pkl', 'rb') as f:
    similarity_matrix = pickle.load(f)


def recommend(movie):
    movie_index = movies_list[movies_list['title'] ==movie].index[0]
    distances = similarity_matrix[movie_index]
    movies_recommended_list = sorted(list(enumerate(distances)), reverse=True, key = lambda x:x[1])[1:6]
    recommended_movies = []
    recommended_movies_posters = []
    for i in movies_recommended_list:
        movie_id = movies_list.iloc[i[0]].id
        recommended_movies.append(movies_list.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_movies_posters


st.title('Movie Recommender System')




selected_movie_name = st.selectbox(
    'Select the movie that you like',
     movies)

if st.button('Recommend'):
    names, posters = recommend(selected_movie_name)
    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])

    