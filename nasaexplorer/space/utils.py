import requests
from datetime import datetime

NASA_API_KEY = "lsOOvgQsDAa6GCDmn52K7arK4IjzjccWz5GzhhSE"

ROVER_MISSION_DATES = {
    "curiosity": ("2012-08-06", "2025-12-31"),  # ongoing; arbitrary future end date
    "opportunity": ("2004-01-25", "2018-06-10"),
    "spirit": ("2004-01-04", "2010-03-22"),
}

def get_apod():
    url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        return {
            "title": data.get("title"),
            "date": data.get("date"),
            "explanation": data.get("explanation"),
            "url": data.get("url"),
            "media_type": data.get("media_type"),
        }
    except (requests.RequestException, ValueError) as e:
        print(f"Error fetching APOD: {e}")
        return None

def get_mars_rover_photos(rover='curiosity', earth_date=None):
    if not earth_date:
        print("No earth_date provided")
        return []

    mission_start, mission_end = ROVER_MISSION_DATES.get(rover, (None, None))
    if mission_start is None or mission_end is None:
        print(f"Unknown rover: {rover}")
        return []

    try:
        date_obj = datetime.strptime(earth_date, "%Y-%m-%d")
        start_obj = datetime.strptime(mission_start, "%Y-%m-%d")
        end_obj = datetime.strptime(mission_end, "%Y-%m-%d")
    except ValueError:
        print(f"Invalid date format: {earth_date}")
        return []

    if not (start_obj <= date_obj <= end_obj):
        print(f"Date {earth_date} out of mission range for rover {rover}")
        return []

    url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/photos"
    params = {
        'api_key': NASA_API_KEY,
        'earth_date': earth_date,
    }

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get('photos', [])
    except (requests.RequestException, ValueError) as e:
        print(f"Error fetching Mars Rover photos: {e}")
        print(f"URL was: {response.url if 'response' in locals() else url}")
        return []
