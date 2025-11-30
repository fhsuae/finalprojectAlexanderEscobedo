import os
import requests
from datetime import datetime

NASA_API_KEY = os.getenv("NASA_API_KEY")

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


def get_donki_events():
    """
    Get recent solar flares from NASA DONKI Space Weather API.
    """
    url = f"https://api.nasa.gov/DONKI/FLR?api_key={NASA_API_KEY}"

    try:
        response = requests.get(url, timeout=8)
        response.raise_for_status()
        data = response.json()

        events = []
        for item in data[:30]:  # limit for UI sanity
            events.append({
                "id": item.get("flrID"),
                "class": item.get("classType"),
                "begin": item.get("beginTime"),
                "peak": item.get("peakTime"),
                "end": item.get("endTime"),
                "source": item.get("sourceLocation"),
                "active_region": item.get("activeRegionNum"),
            })

        return events

    except Exception as e:
        print(f"Error fetching DONKI data: {e}")
        return []


def get_asteroids():
    """
    Fetch a list of near-Earth asteroids approaching Earth today.
    """
    url = (
        f"https://api.nasa.gov/neo/rest/v1/feed/today?detailed=true&api_key={NASA_API_KEY}"
    )

    try:
        response = requests.get(url, timeout=8)
        response.raise_for_status()
        data = response.json()

        # NeoWs returns: near_earth_objects: { "YYYY-MM-DD": [asteroids...] }
        date_key = list(data["near_earth_objects"].keys())[0]
        raw_asteroids = data["near_earth_objects"][date_key]

        asteroids = []
        for obj in raw_asteroids[:40]:  # limit for readability
            approach = obj["close_approach_data"][0]

            asteroids.append({
                "name": obj.get("name"),
                "id": obj.get("id"),
                "hazardous": obj.get("is_potentially_hazardous_asteroid"),
                "magnitude": obj.get("absolute_magnitude_h"),
                "diameter_min": obj["estimated_diameter"]["meters"]["estimated_diameter_min"],
                "diameter_max": obj["estimated_diameter"]["meters"]["estimated_diameter_max"],
                "velocity": approach.get("relative_velocity", {}).get("kilometers_per_hour"),
                "miss_distance": approach.get("miss_distance", {}).get("kilometers"),
                "orbiting_body": approach.get("orbiting_body"),
            })

        return asteroids

    except Exception as e:
        print(f"Error fetching asteroid data: {e}")
        return []


def get_epic_images(date=None):
    """
    Fetch EPIC images. If a date is provided (YYYY-MM-DD), fetch images for that date.
    Otherwise fetch the most recent available EPIC images.
    """
    try:
        if date:
            url = f"https://epic.gsfc.nasa.gov/api/natural/date/{date}"
        else:
            url = "https://epic.gsfc.nasa.gov/api/natural"

        resp = requests.get(url, timeout=10)
        data = resp.json()

        if not data:
            return []

        images = []
        for item in data:
            image_name = item["image"]
            date_time = item["date"]

            year, month, day = date_time.split(" ")[0].split("-")
            img_url = f"https://epic.gsfc.nasa.gov/archive/natural/{year}/{month}/{day}/png/{image_name}.png"
            caption = item.get("caption", "")
            timestamp = date_time
            images.append({
                "date_time": timestamp,
                "caption": caption,
                "image": img_url,
            })
        return images
    except Exception:
        return []


def search_nasa_images(query):
    if not query:
        return []

    url = "https://images-api.nasa.gov/search"
    params = {"q": query, "media_type": "image"}

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()

        items = data.get("collection", {}).get("items", [])
        results = []

        for item in items:
            data_list = item.get("data", [])
            links_list = item.get("links", [])

            if not data_list or not links_list:
                continue

            info = data_list[0]
            link = links_list[0]

            results.append({
                "title": info.get("title"),
                "description": info.get("description"),
                "date_created": info.get("date_created"),
                "thumbnail": link.get("href"),
                "full_image": link.get("href"),
            })

        return results

    except Exception as e:
        print(f"Error searching NASA Image Library: {e}")
        return []

def get_exoplanets(limit=50):
    """
    Fetches basic exoplanet data from NASA’s Exoplanet Archive API.
    """
    url = (
        "https://exoplanetarchive.ipac.caltech.edu/TAP/sync?query="
        "select+pl_name,hostname,disc_year,pl_rade,pl_orbper,discoverymethod"
        "+from+ps&format=json"
    )

    try:
        response = requests.get(url, timeout=8)
        response.raise_for_status()
        data = response.json()

        planets = []
        for item in data[:limit]:  # limit results for performance
            planets.append({
                "name": item.get("pl_name"),
                "host": item.get("hostname"),
                "year": item.get("disc_year"),
                "radius": item.get("pl_rade"),
                "period": item.get("pl_orbper"),
                "method": item.get("discoverymethod"),
            })

        return planets

    except Exception as e:
        print(f"Error fetching Exoplanet data: {e}")
        return []
