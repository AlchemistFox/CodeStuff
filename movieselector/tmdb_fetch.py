# tmdb_fetch.py

import requests

API_KEY = '0d9a9a2de301dd853240df42caa2d5ba'  # Replace with your real API key
BASE_URL = 'https://api.themoviedb.org/3'

def get_popular_movies():
    url = f'{BASE_URL}/movie/popular'
    params = {'api_key': API_KEY, 'language': 'en-US', 'page': 1}
    response = requests.get(url, params=params)
    data = response.json()
    return data['results']

if __name__ == '__main__':
    movies = get_popular_movies()
    for movie in movies[:5]:
        print(f"{movie['title']} ({movie['release_date']})")
