<<<<<<< HEAD
import streamlit as st
import pickle
import requests

# Load the pre-saved movie list and similarity matrix
lom = pickle.load(open("movie_list.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))

st.set_page_config(layout="wide")
# Title of the Streamlit app
st.title("Movie Recommendation System")

# Contact option (this seems unrelated to the main functionality, but I'll leave it here)
option1 = st.selectbox('How would you like to be contacted?', ("E-mail", "Whatsapp", "Mobile Phone"))

# Select box to choose a movie
mov_select = st.selectbox('Select the movie', lom["title"])

st.markdown(
    """
    <style>
    
    /* Add styles for movie boxes */
    .movie-box {
        padding: 10px;
        margin: 10px;
        
        text-align: center;
    }
    .movie-box img {
        max-width: 100%;
        height: auto;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Function to fetch the movie poster and IMDb ID from The Movie Database API
def fetch_movie_details(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    data = requests.get(url).json()
    poster_path = data['poster_path']
    imdb_id = data['imdb_id']
    full_poster_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    imdb_url = f"https://www.imdb.com/title/{imdb_id}/"
    return full_poster_path, imdb_url

# Function to recommend movies based on the selected movie
def recommend(movie):
    index = lom[lom['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_details = []
    for i in distances[1:7]:
        movie_id = lom.iloc[i[0]].movie_id
        poster, imdb_url = fetch_movie_details(movie_id)
        title = lom.iloc[i[0]].title
        recommended_movie_details.append((title, poster, imdb_url))
    return recommended_movie_details

# Button to trigger the recommendation
if st.button("Recommend"):
    recommendations = recommend(mov_select)
    st.write("The suggestions by our system are as follows:")

    # Display recommendations in columns
    cols1 = st.columns(3)
    for i in range(3):
        with cols1[i]:
            title, poster, imdb_url = recommendations[i]
            st.markdown(f'''
                <div class="movie-box">
                    <a href="{imdb_url}" target="_blank">
                        <img src="{poster}" alt="{title}">
                    </a>
                    <p>{title}</p>
                </div>
            ''', unsafe_allow_html=True)

    cols2 = st.columns(3)
    for i in range(3, 6):
        with cols2[i-3]:  # Adjust the index for the second row
            title, poster, imdb_url = recommendations[i]
            st.markdown(f'''
                <div class="movie-box">
                    <a href="{imdb_url}" target="_blank">
                        <img src="{poster}" alt="{title}">
                    </a>
                    <p>{title}</p>
                </div>
            ''', unsafe_allow_html=True)
=======
version https://git-lfs.github.com/spec/v1
oid sha256:5c072f9893631516bec6c312a3a237a55508192e70d33bccb9fe61f3d815a2ff
size 3080
>>>>>>> 049707b7b5afadf9c48a3c5aefdb96f95cae6b96
