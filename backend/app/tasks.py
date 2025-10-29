# backend/app/tasks.py
from . import celery, db
from .ml import get_recommendations, get_next_poi
import pandas as pd
from bson import ObjectId

@celery.task(bind=True)
def generate_itinerary_task(self, user_interests, duration_days):
    """The main Celery task for generating an itinerary."""
    try:
        # 1. Fetch all POIs from MongoDB
        pois_cursor = db.pois.find()
        pois_list = list(pois_cursor)
        if not pois_list:
            raise ValueError("No POIs found in the database.")

        pois_df = pd.DataFrame(pois_list)

        # 2. Get a candidate pool of relevant POIs
        interests_str = " ".join(user_interests)
        candidate_pool = get_recommendations(pois_df, interests_str, top_n=20)

        if candidate_pool.empty:
            raise ValueError("No recommendations could be generated for the given interests.")

        # 3. Build the itinerary day by day
        itinerary = []
        visited_poi_ids = set()

        # Sort candidates by recommendation score initially
        candidate_pool = candidate_pool.sort_values(by='score', ascending=False)

        for day_num in range(1, duration_days + 1):
            daily_schedule = []
            # Assume a day runs from 9 AM to 7 PM (10 hours)
            time_left_today = 10.0 
            last_poi = None

            # Start the day with the best available recommendation
            if not candidate_pool.empty:
                # Select the best POI not yet visited
                start_poi_df = candidate_pool[~candidate_pool['_id'].isin(visited_poi_ids)]
                if not start_poi_df.empty:
                    start_poi = start_poi_df.iloc[0].to_dict()

                    if start_poi['duration'] <= time_left_today:
                        daily_schedule.append(start_poi)
                        visited_poi_ids.add(start_poi['_id'])
                        time_left_today -= start_poi['duration']
                        last_poi = start_poi

            # Iteratively add more POIs for the day
            while time_left_today > 1.0 and last_poi:
                # Filter candidates to those not yet visited
                remaining_candidates = candidate_pool[~candidate_pool['_id'].isin(visited_poi_ids)]

                if remaining_candidates.empty:
                    break

                next_poi_series = get_next_poi(last_poi, remaining_candidates)
                if next_poi_series is None:
                    break

                next_poi = next_poi_series.to_dict()

                # Simple check for time
                if next_poi['duration'] <= time_left_today:
                    daily_schedule.append(next_poi)
                    visited_poi_ids.add(next_poi['_id'])
                    time_left_today -= next_poi['duration']
                    last_poi = next_poi
                else:
                    # If this POI doesn't fit, remove it from consideration for this day and try another
                    candidate_pool = candidate_pool[candidate_pool['_id'] != next_poi['_id']]

            itinerary.append({"day": day_num, "schedule": daily_schedule})

        # Convert ObjectId to string for JSON serialization
        for day in itinerary:
            for item in day['schedule']:
                item['_id'] = str(item['_id'])

        return {'status': 'SUCCESS', 'itinerary': itinerary}

    except Exception as e:
        # Handle errors
        return {'status': 'FAILURE', 'message': str(e)}