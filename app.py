import streamlit as st
import pickle
import requests
import base64
from load_css import local_css

local_css("./static/style.css")

#load_pickle
movies = pickle.load(open('./model/movie.pkl','rb'))
similarity = pickle.load(open('./model/similarity.pkl','rb'))
print("Model Loaded")

def get_base64(bin_file):
    with open(bin_file, 'rb') as f1:
        data = f1.read()
    return base64.b64encode(data).decode()

#background-img
def set_background(png_file):
    bin_str = get_base64(png_file)
    page_bg_img = '''
    <style>
    .stApp {
    background-image: url("data:image/png;base64,%s");
    background-size: cover;
    }
    </style>
    ''' % bin_str
    st.markdown(page_bg_img, unsafe_allow_html=True)

set_background('./static/movie.jpg')

#ttile
t = "<div><h1 class='h1'>Movie Recommender System</h1></div>"
st.markdown(t, unsafe_allow_html=True)

#break
br = "<div><br></div>"
st.markdown(br, unsafe_allow_html=True)

#movie-selector
movie_list = movies['title'].values
t2 = "<div><h2 class='h2'>Type or select a movie from the dropdown ᐁ</h2></div>"
st.markdown(t2, unsafe_allow_html=True)
selected_movie = st.selectbox("",movie_list)

#poster
def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

#recommender
def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names,recommended_movie_posters

#button
if st.button('Show Recommendation'):
    st.markdown(br, unsafe_allow_html=True)
    t3 = "<div><label class='label'>Recommended movies for you ⮯</label></div>"
    st.markdown(t3, unsafe_allow_html=True)
    st.markdown(br, unsafe_allow_html=True)
    recommended_movie_names,recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])