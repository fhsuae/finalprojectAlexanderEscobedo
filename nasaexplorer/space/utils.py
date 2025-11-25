import requests
from datetime import datetime

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

def get_epic_images():
    url = f"https://epic.gsfc.nasa.gov/api/natural"
    try:
        response = requests.get(url, timeout=5)
        response.raise_for_status()
        data = response.json()
        images = []
        for item in data:
            date_str = item["date"].split()[0].replace("-", "/")
            image_url = (
                f"https://epic.gsfc.nasa.gov/archive/natural/"
                f"{date_str}/png/{item['image']}.png"
            )
            images.append({
                "caption": item["caption"],
                "date": item["date"],
                "image_url": image_url,
            })
        return images
    except (requests.RequestException, ValueError) as e:
        print(f"Error fetching EPIC images: {e}")
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

