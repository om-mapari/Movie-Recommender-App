import pickle
import pandas as pd
import streamlit as st
import requests


def fatch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=a0f9c9f8f7bc2d0af1b94eef3e178475&language=en-US'.format(movie_id))
    data = response.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)),reverse=True,key=lambda x:x[1])[1:6]
    recommend_movies = []
    recommend_movies_posters = []

    for i in movie_list:
        movi_id = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)
        recommend_movies_posters.append(fatch_poster(movi_id))
    return recommend_movies,recommend_movies_posters


movies_dict = pickle.load(open('model/movie_list.pkl','rb'))
similarity = pickle.load(open('model/similarity.pkl','rb'))

movies = pd.DataFrame(movies_dict)

st.title('Movie Recommender System')

selected_movie_name = st.selectbox(
     "Type or select a movie from the dropdown which you like",
     movies['title'].values
)

if st.button('Show Recommendation'):
    st.subheader('If you liked  "'+selected_movie_name+' Movie"  then You may also Like')
    names,posters = recommend(selected_movie_name)
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
    st.subheader('A Special Thank You For Using Our App')





