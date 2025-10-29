# backend/app/ml.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pandas as pd
import numpy as np

def get_recommendations(pois_df, user_interests_str, top_n=10):
    """Recommends POIs based on content similarity."""
    pois_df['tags'] = pois_df['tags'].fillna('')

    # Create TF-IDF matrix from POI tags
    tfidf = TfidfVectorizer()
    poi_matrix = tfidf.fit_transform(pois_df['tags'])

    # Transform user interests
    user_vector = tfidf.transform([user_interests_str])

    # Calculate cosine similarity
    cosine_sim = cosine_similarity(user_vector, poi_matrix).flatten()

    # Get top N recommendations
    top_indices = cosine_sim.argsort()[-top_n:][::-1]

    recommendations = pois_df.iloc[top_indices]
    recommendations['score'] = cosine_sim[top_indices]

    return recommendations

def get_next_poi(last_poi, candidate_pois):
    """
    Simplified sequencer.
    Instead of an LSTM, this finds the geographically closest POI from the candidates.
    """
    if candidate_pois.empty:
        return None

    last_loc = np.array([[last_poi['lat'], last_poi['lon']]])
    candidate_locs = candidate_pois[['lat', 'lon']].to_numpy()

    # Calculate Euclidean distance (a simple proxy for travel distance)
    distances = np.linalg.norm(candidate_locs - last_loc, axis=1)

    # Find the index of the closest POI
    closest_index = distances.argmin()

    return candidate_pois.iloc[closest_index]