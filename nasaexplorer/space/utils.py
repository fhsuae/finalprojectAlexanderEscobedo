import requests
from datetime import datetime

NASA_API_KEY = "lsOOvgQsDAa6GCDmn52K7arK4IjzjccWz5GzhhSE"

ROVER_MISSION_DATES = {
    "curiosity": ("2012-08-06", "2025-12-31"),
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


def get_mars_rover_photos(rover='curiosity', earth_date=None, sol=None):
    if not earth_date and sol is None:
        print("No earth_date or sol provided")
        return []

    # Optional: validate earth_date within mission dates
    if earth_date:
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
    }
    if earth_date:
        params['earth_date'] = earth_date
    elif sol is not None:
        params['sol'] = sol

    try:
        response = requests.get(url, params=params, timeout=5)
        response.raise_for_status()
        data = response.json()
        print(f"Request URL: {response.url}")  # Debugging
        print(f"Photos found: {len(data.get('photos', []))}")
        return data.get('photos', [])
    except (requests.RequestException, ValueError) as e:
        print(f"Error fetching Mars Rover photos: {e}")
        print(f"URL was: {response.url if 'response' in locals() else url}")
        return []


def get_epic_images():
    """
    Fetches the latest EPIC natural color images from NASA API.
    Returns a list of images with URLs and metadata.
    """
    url = f"https://api.nasa.gov/EPIC/api/natural?api_key={NASA_API_KEY}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()

        # Build full image URLs from date and image name
        images = []
        for item in data:
            date_str = item['date'].split()[0]  # e.g. "2023-11-01"
            date_path = date_str.replace("-", "/")  # "2023/11/01"
            image_name = item['image']
            image_url = f"https://api.nasa.gov/EPIC/archive/natural/{date_path}/png/{image_name}.png?api_key={NASA_API_KEY}"
            images.append({
                "caption": item.get("caption"),
                "image_url": image_url,
                "date": item.get("date"),
                "identifier": item.get("identifier"),
            })
        return images

    except (requests.RequestException, ValueError) as e:
        print(f"Error fetching EPIC images: {e}")
        return []
