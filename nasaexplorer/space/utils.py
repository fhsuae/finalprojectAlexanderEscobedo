import requests
from django.core.cache import cache
from django.conf import settings

NASA_API_KEY = "lsOOvgQsDAa6GCDmn52K7arK4IjzjccWz5GzhhSE"  # Replace with your key

def get_apod():
    cache_key = "nasa_apod"
    cached_data = cache.get(cache_key)
    if cached_data:
        return cached_data

    url = f"https://api.nasa.gov/planetary/apod?api_key={NASA_API_KEY}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        apod_data = {
            "title": data.get("title"),
            "date": data.get("date"),
            "explanation": data.get("explanation"),
            "url": data.get("url"),
            "media_type": data.get("media_type"),
        }
        cache.set(cache_key, apod_data, timeout=getattr(settings, "APOD_CACHE_TIMEOUT", 21600))
        return apod_data
    except (requests.RequestException, ValueError) as e:
        print(f"Error fetching APOD: {e}")
        return None
