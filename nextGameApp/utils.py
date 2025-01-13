import requests,os
from nextGameApp.models import Game
from django.utils.dateparse import parse_datetime, parse_date
import pandas as pd
import requests
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Optional
import logging
import os
from datetime import datetime, timedelta

def get_api_key_from_file(file_path='secrets.txt'):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The secrets (RAWG API Key) file '{file_path}' does not exist.")
    
    with open(file_path, 'r') as file:
        for line in file:
            if line.startswith("RAWG_API_KEY="):
                return line.split("=", 1)[1].strip()
    
    raise ValueError("API key not found in the secrets file.")

def save_games_to_db(popular_games):
    """
    Takes a list of games (from RAWG API) and saves them to the database.

    Args:
        popular_games (list): List of game dictionaries fetched from the RAWG API.
    """
    for game_data in popular_games:
        try:
            game, created = Game.objects.update_or_create(
                id=game_data['id'],  # Use 'id' as the unique identifier
                defaults={
                    'slug': game_data.get('slug', ''),
                    'name': game_data.get('name', ''),
                    'description': game_data.get('description', ''),
                    'metacritic': game_data.get('metacritic'),
                    'released': parse_date(game_data.get('released')) if game_data.get('released') else None,
                    'tba': game_data.get('tba', False),
                    'updated': parse_datetime(game_data.get('updated')) if game_data.get('updated') else None,
                    'background_image': game_data.get('background_image'),
                    'background_image_additional': game_data.get('background_image_additional'),
                    'website': game_data.get('website'),
                    'rating': game_data.get('rating', 0.0),
                    'rating_top': game_data.get('rating_top', 0),
                    'ratings': game_data.get('ratings', {}),
                    'reactions': game_data.get('reactions', {}),
                    'added': game_data.get('added', 0),
                    'added_by_status': game_data.get('added_by_status', {}),
                    'playtime': game_data.get('playtime', 0),
                    'screenshots_count': game_data.get('screenshots_count', 0),
                    'movies_count': game_data.get('movies_count', 0),
                    'creators_count': game_data.get('creators_count', 0),
                    'achievements_count': game_data.get('achievements_count', 0),
                    'parent_achievements_count': game_data.get('parent_achievements_count', 0),
                    'reddit_url': game_data.get('reddit_url'),
                    'reddit_name': game_data.get('reddit_name'),
                    'reddit_description': game_data.get('reddit_description'),
                    'reddit_logo': game_data.get('reddit_logo'),
                    'reviews_text_count': game_data.get('reviews_text_count'),
                    'ratings_count': game_data.get('ratings_count', 0),
                    'suggestions_count': game_data.get('suggestions_count', 0),
                    'alternative_names': game_data.get('alternative_names', []),
                    'metacritic_url': game_data.get('metacritic_url'),
                    'parents_count': game_data.get('parents_count', 0),
                    'additions_count': game_data.get('additions_count', 0),
                    'game_series_count': game_data.get('game_series_count', 0),
                    'reviews_count': game_data.get('reviews_count', 0),
                    'stores': game_data.get('stores', []),
                    'developers': game_data.get('developers', []),
                    'genres': game_data.get('genres', []),
                    'tags': game_data.get('tags', []),
                    'description_raw': game_data.get('description_raw', ''),
                }
            )
            if created:
                print(f"Created new game: {game.name}")
            else:
                print(f"Updated game: {game.name}")

        except Exception as e:
            print(f"Error saving game {game_data.get('name', 'unknown')}: {str(e)}")

def import_games():
    API_KEY = get_api_key_from_file()
    BASE_URL = 'https://api.rawg.io/api/games'
    PAGE_SIZE = 40  
    TOTAL_GAMES = 10000  

    def fetch_popular_games(api_key, total_games, page_size):
        games = []
        pages = total_games // page_size
        
        for page in range(1, pages + 1):
            response = requests.get(
                BASE_URL,
                params={
                    'key': api_key,
                    'page_size': page_size,
                    'page': page,
                    'ordering': '-rating',  # Order by descending rating
                },
            )
            
            if response.status_code == 200:
                data = response.json()
                games.extend(data['results'])
            else:
                print(f"Error: {response.status_code}")
                break

        return games

    # Fetch the games
    popular_games = fetch_popular_games(API_KEY, TOTAL_GAMES, PAGE_SIZE)
    save_games_to_db(popular_games)

