# tmdb_fetch.py

import requests
import os
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

TMDB_API_KEY = os.getenv("TMDB_API_KEY")
BASE_URL = 'https://api.themoviedb.org/3'

def get_popular_movies():
    url = f'{BASE_URL}/movie/popular'
    params = {'api_key': TMDB_API_KEY, 'language': 'en-US', 'page': 1}
    response = requests.get(url, params=params)
    data = response.json()
    return data['results']

if __name__ == '__main__':
    movies = get_popular_movies()
    for movie in movies[:5]:
        print(f"{movie['title']} ({movie['release_date']})")