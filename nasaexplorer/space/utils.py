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


def search_nasa_images(query):
    """
    Search the NASA Image and Video Library API.
    Returns a list of image items with title, description, and thumbnail/full URLs.
    """
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


def get_epic_images():
    """
    Fetches EPIC (Earth Polychromatic Imaging Camera) natural color images.
    Returns a list of image dicts with URL and metadata.
    """
    url = f"https://api.nasa.gov/EPIC/api/natural/images?api_key={NASA_API_KEY}"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        images = []
        for item in data:
            date_str = item['date'].split()[0].replace('-', '/')
            image_name = item['image']
            image_url = f"https://epic.gsfc.nasa.gov/archive/natural/{date_str}/png/{image_name}.png"
            images.append({
                "identifier": item['identifier'],
                "caption": item.get('caption', ''),
                "date": item['date'],
                "image_url": image_url,
            })
        return images
    except (requests.RequestException, ValueError) as e:
        print(f"Error fetching EPIC images: {e}")
        return []
