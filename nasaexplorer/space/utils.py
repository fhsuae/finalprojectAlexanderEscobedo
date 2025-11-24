import requests

NASA_API_KEY = "lsOOvgQsDAa6GCDmn52K7arK4IjzjccWz5GzhhSE"

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
    url = f"https://api.nasa.gov/mars-photos/api/v1/rovers/{rover}/photos"
    params = {
        'api_key': NASA_API_KEY,
    }
    if earth_date:
        params['earth_date'] = earth_date

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        return data.get('photos', [])
    except (requests.RequestException, ValueError) as e:
        print(f"Error fetching Mars Rover photos: {e}")
        return []
