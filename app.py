import base64
import streamlit as st
import pickle
import pandas as pd
import requests
from zipfile import ZipFile

# Setting page config
st.set_page_config(page_title="Movie Recommender System", page_icon="🎬")

# Loading the temp.zip and creating a zip object
with ZipFile("similarity.zip", 'r') as zObject:
    # Extracting specific file in the zip into a specific location.
    zObject.extract("similarity.pkl", path=(""))
zObject.close()

# Function to set background image
def get_base64(bin_file):
    with open(bin_file, 'rb') as f:
        data = f.read()
    return base64.b64encode(data).decode()

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

set_background('image.jpg')


# Load movie data
movies_dict = pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)

# Function to fetch movie details from TMDB API
def fetch_movie_details(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=70ac935a984880f2fd11a4196f60e328&language=en-US')
    return response.json()

# Function to fetch movie poster from TMDB API
def fetch_poster(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=70ac935a984880f2fd11a4196f60e328&language=en-US'.format(movie_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500/" +data['poster_path']

# Function to recommend similar movies
def recommend(movie, num_recommendations=5):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:num_recommendations+1]
    recommended_movies = []

    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]])
    
    return recommended_movies

# Function to fetch movie trailer from TMDB API
def fetch_trailer(movie_id):
    response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key=70ac935a984880f2fd11a4196f60e328&language=en-US')
    trailer_data = response.json()
    for video in trailer_data['results']:
        if video['type'] == 'Trailer':
            return f"https://www.youtube.com/watch?v={video['key']}"
    return None

# Set page title and favicon


# Title and subtitle
st.title('Movie Recommender System')

# Sidebar for user interaction
st.sidebar.title('Movie Recommender System')
st.sidebar.markdown('Select a movie from the dropdown menu and choose to get recommendations or view movie details.')


# Dropdown menu to select a movie
selected_movie = st.sidebar.selectbox('Select a movie', movies['title'].values)

# Dropdown menu for selecting action (recommendations or details)
action = st.sidebar.selectbox('Select Action', ['Get Recommendations', 'View Movie Details'])


# Button to initiate the action
if st.sidebar.button('Go'):
    if action == 'Get Recommendations':
        similarity = pickle.load(open('similarity.pkl','rb'))
        recommended_movies = recommend(selected_movie, num_recommendations=5)
        st.subheader('Recommended Movies:')
        for movie in recommended_movies:
            st.image(fetch_poster(movie['movie_id']), width=150)
            movie_details = fetch_movie_details(movie['movie_id'])
            st.write('**Title:**', movie_details['title'])
            st.write('**Release Date:**', movie_details.get('release_date', 'Not available'))
            st.write('**Average Vote:**', movie_details.get('vote_average', 'Not available'))
            st.write('**Overview:**', movie_details.get('overview', 'Not available'))
            # Fetch and display movie trailer
            st.markdown(f'For more details, check out the movie on [TMDB](https://www.themoviedb.org/movie/{movie["movie_id"]}).')
        # ...
            trailer_url = fetch_trailer(movie['movie_id'])
            if trailer_url:
                st.subheader('Trailer:')
                st.markdown(f'<a href="{trailer_url}" target="_blank" style="display: inline-block; background-color: #FF0000; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Watch Trailer</a>', unsafe_allow_html=True)
            else:
                st.write('Trailer not available.')
    elif action == 'View Movie Details':
        movie = movies[movies['title'] == selected_movie].iloc[0]
        movie_details = fetch_movie_details(movie['movie_id'])
        st.subheader('Movie Details:')
        col1, col2 = st.columns([2, 3])
        with col1:
            st.image(f"https://image.tmdb.org/t/p/w500/{movie_details['poster_path']}", width=200)
        with col2:
            st.markdown(f"**Title:** {movie_details['title']}")
            st.markdown(f"**Release Date:** {movie_details.get('release_date', 'Not available')}")
            st.markdown(f"**Average Vote:** {movie_details.get('vote_average', 'Not available')}")
            st.markdown(f"**Overview:** {movie_details.get('overview', 'Not available')}")
            st.markdown(f'For more details, check out the movie on [TMDB](https://www.themoviedb.org/movie/{movie["movie_id"]}).')
        # Fetch and display movie trailer
        trailer_url = fetch_trailer(movie['movie_id'])
        if trailer_url:
            st.subheader('Trailer:')
            st.markdown(f'<a href="{trailer_url}" target="_blank" style="display: inline-block; background-color: #FF0000; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px;">Watch Trailer</a>', unsafe_allow_html=True)
        else:
            st.write('Trailer not available.')
