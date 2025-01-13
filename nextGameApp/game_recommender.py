import pandas as pd
import requests
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Optional
import logging
import os
from datetime import datetime, timedelta

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SteamGameRecommender:
    def __init__(self, data_file='training_dataset/steam_games.csv', cache_duration_days=7):
        self.games = None
        self.similarity_matrix = None
        self.vectorizer = None
        self.data_file = data_file
        self.cache_duration_days = cache_duration_days
        
    def is_cache_valid(self) -> bool:
        """Check if cached data file exists and is recent enough."""
        if not os.path.exists(self.data_file):
            return False
            
        file_time = datetime.fromtimestamp(os.path.getmtime(self.data_file))
        cache_age = datetime.now() - file_time
        return cache_age.days < self.cache_duration_days
        
    def load_cached_data(self) -> Optional[pd.DataFrame]:
        """Load data from cache file if it exists and is valid."""
        try:
            if self.is_cache_valid():
                logger.info(f"Loading cached data from {self.data_file}")
                return pd.read_csv(self.data_file)
            return None
        except Exception as e:
            logger.error(f"Error loading cached data: {str(e)}")
            return None
            
    def save_to_cache(self, df: pd.DataFrame):
        """Save data to cache file."""
        try:
            logger.info(f"Saving data to cache file {self.data_file}")
            df.to_csv(self.data_file, index=False)
        except Exception as e:
            logger.error(f"Error saving data to cache: {str(e)}")

    def fetch_steamspy_data(self) -> Optional[pd.DataFrame]:
        """
        Fetch game data from cache or SteamSpy API with error handling.
        
        Returns:
            Optional[pd.DataFrame]: DataFrame containing game data or None if fetch fails
        """
        # Try loading from cache first
        cached_data = self.load_cached_data()
        if cached_data is not None:
            return cached_data
            
        # If no cache or cache is old, fetch from API
        try:
            logger.info("Fetching fresh data from SteamSpy API")
            url = "https://steamspy.com/api.php?request=all"
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            df = pd.DataFrame(data).T
            df.reset_index(drop=True, inplace=True)
            
            # Save to cache
            self.save_to_cache(df)
            
            return df
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch data from SteamSpy: {str(e)}")
            return None
        except ValueError as e:
            logger.error(f"Failed to parse JSON response: {str(e)}")
            return None

    def preprocess_data(self, games: pd.DataFrame) -> pd.DataFrame:
        """
        Clean and preprocess the games data.
        
        Args:
            games (pd.DataFrame): Raw games data
            
        Returns:
            pd.DataFrame: Preprocessed games data
        """
        columns_to_keep = [
            'appid', 'name', 'developer', 'publisher', 'score_rank',
            'positive', 'negative', 'userscore', 'owners', 'average_forever', 'price'
        ]
        
        missing_columns = [col for col in columns_to_keep if col not in games.columns]
        if missing_columns:
            logger.warning(f"Missing columns in data: {missing_columns}")
            columns_to_keep = [col for col in columns_to_keep if col not in missing_columns]
        
        games = games[columns_to_keep].copy()
        
        # Calculate user score as percentage of positive reviews
        games['positive'] = pd.to_numeric(games['positive'], errors='coerce')
        games['negative'] = pd.to_numeric(games['negative'], errors='coerce')
        total_reviews = games['positive'] + games['negative']
        games['user_score_percent'] = np.where(
            total_reviews > 0,
            (games['positive'] / total_reviews) * 100,
            0
        )
        
        # Clean other numeric columns
        games['score_rank'] = pd.to_numeric(games['score_rank'], errors='coerce')
        games['price'] = pd.to_numeric(games['price'], errors='coerce')
        
        # Fill missing values
        games['developer'] = games['developer'].fillna('Unknown Developer')
        games['publisher'] = games['publisher'].fillna('Unknown Publisher')
        games['score_rank'] = games['score_rank'].fillna(0)
        games['user_score_percent'] = games['user_score_percent'].fillna(0)
        
        games.reset_index(drop=True, inplace=True)
        return games

    def create_feature_matrix(self, games: pd.DataFrame):
        """
        Create TF-IDF feature matrix from game metadata.
        
        Args:
            games (pd.DataFrame): Preprocessed games data
        """
        games['combined_features'] = (
            games['developer'] + ' ' +
            games['publisher'] + ' ' +
            games['score_rank'].astype(str)
        )
        
        self.vectorizer = TfidfVectorizer(
            stop_words='english',
            max_features=1000,
            ngram_range=(1, 2)
        )
        
        features_matrix = self.vectorizer.fit_transform(games['combined_features'])
        self.similarity_matrix = cosine_similarity(features_matrix)

    def initialize(self):
        """Initialize the recommender system by fetching and processing data."""
        self.games = self.fetch_steamspy_data()
        if self.games is not None:
            self.games = self.preprocess_data(self.games)
            self.create_feature_matrix(self.games)
            logger.info("Recommender system initialized successfully")
            return True
        return False

    def recommend_games(
        self,
        played_games: List[str],
        top_n: int = 5,
        min_score: float = 0.0,
        min_reviews: int = 100
    ) -> pd.DataFrame:
        """
        Recommend games based on played games with additional filtering.
        
        Args:
            played_games (List[str]): List of game names played by the user
            top_n (int): Number of recommendations to return
            min_score (float): Minimum user score threshold (percentage of positive reviews)
            min_reviews (int): Minimum number of total reviews required
            
        Returns:
            pd.DataFrame: Recommended games with relevant details
        """
        if self.games is None or self.similarity_matrix is None:
            logger.error("Recommender system not initialized")
            return pd.DataFrame()
        
        try:
            # Find indices of played games (case-insensitive matching)
            played_games_lower = [game.lower() for game in played_games]
            matching_games = self.games[
                self.games['name'].str.lower().isin(played_games_lower)
            ]
            
            if matching_games.empty:
                logger.warning(f"No matches found for played games: {played_games}")
                return pd.DataFrame()
            
            played_indices = matching_games.index.values
            logger.info(f"Found matches at indices: {played_indices}")
            
            # Calculate similarity scores
            similarity_scores = self.similarity_matrix[played_indices]
            scores = np.mean(similarity_scores, axis=0) if len(played_indices) > 1 else similarity_scores.ravel()
            
            # Get sorted indices by similarity score
            candidate_indices = np.argsort(scores)[::-1]
            
            # Filter and rank games
            recommended_indices = []
            for idx in candidate_indices:
                game = self.games.iloc[idx]
                total_reviews = game['positive'] + game['negative']
                
                # Skip if it's a played game
                if idx in played_indices:
                    continue
                
                # Skip if not enough reviews
                if total_reviews < min_reviews:
                    continue
                
                # Skip if score is too low
                if game['user_score_percent'] < min_score:
                    continue
                
                recommended_indices.append(idx)
                if len(recommended_indices) >= top_n:
                    break
            
            if not recommended_indices:
                logger.warning("No recommendations found matching criteria")
                # Log some statistics about the filtering
                filtered_games = self.games.iloc[candidate_indices[:20]]  # Top 20 by similarity
                logger.info("Stats for top 20 similar games:")
                logger.info(f"User scores: {filtered_games['user_score_percent'].tolist()}")
                logger.info(f"Total reviews: {(filtered_games['positive'] + filtered_games['negative']).tolist()}")
                return pd.DataFrame()
            
            # Prepare recommendations
            recommendations = self.games.iloc[recommended_indices][
                ['name', 'developer', 'price', 'user_score_percent', 'positive', 'negative']
            ].copy()
            
            # Format output
            recommendations['price'] = recommendations['price'].apply(
                lambda x: f"${x:.2f}" if pd.notnull(x) and x > 0 else "Free"
            )
            recommendations['user_score_percent'] = recommendations['user_score_percent'].round(1)
            recommendations['total_reviews'] = recommendations['positive'] + recommendations['negative']
            
            # Reorder columns
            recommendations = recommendations[[
                'name', 'developer', 'price', 'user_score_percent', 'total_reviews'
            ]]
            
            return recommendations
            
        except Exception as e:
            logger.error(f"Error generating recommendations: {str(e)}")
            logger.error("Full error:", exc_info=True)
            return pd.DataFrame()

def recommend(played_games):
    # Initialize recommender with custom cache settings
    recommender = SteamGameRecommender(
        data_file='training_dataset/steam_games.csv',  # Cache file name
        cache_duration_days=7  # Update cache weekly
    )
    
    if not recommender.initialize():
        logger.error("Failed to initialize recommender system")
        return []
    
    # Get recommendations with more lenient criteria
    recommendations = recommender.recommend_games(
        played_games=played_games,
        top_n=20,
        min_score=50.0,  # More lenient score threshold
        min_reviews=50  # Minimum number of reviews
    )
    
    if not recommendations.empty:
        # Return the 'name' column as a list of strings
        return recommendations['name'].tolist()
    else:
        return []

