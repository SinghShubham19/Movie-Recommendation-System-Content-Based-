import streamlit as st
import pickle
import pandas as pd
import requests
import bz2
import random
import os

page_bg_img = """
<style>
[data-testid = "stAppViewContainer"]{
background-image: url('https://pixabay.com/get/gf7395ecc9439c17520f12d07f9c7f072889b1b9f0f37c0ce274bd96fb77fd10597b06a3dfdbc47c1678c8dba2905663c.jpg');
background-size: cover;
}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)


def fetch_poster(movie_id):
    response = requests.get(
        'https://api.themoviedb.org/3/movie/{}?api_key=3eeac16efb69a49bb47cfdb636e9c303'.format(movie_id))
    data = response.json()
    return 'http://image.tmdb.org/t/p/w500/' + data['poster_path']


def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    recommended_movies_poster = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        # fetch psoter from API

        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_poster.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_poster


st.title('Movie Recommendation System')

movie_dict = pickle.load(open('movie_dict.pkl', 'rb'))
movies = pd.DataFrame(movie_dict)
ifile = bz2.BZ2File("BinaryData",'rb')
similarity = pickle.load(ifile)
ifile.close()
# similarity = pickle.load(open('similarity.pkl', 'rb'))


selected_movie_name = st.selectbox(
    'Select Your Movie',
    movies['title'].values)

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
