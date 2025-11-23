import requests

NASA_API_KEY = "lsOOvgQsDAa6GCDmn52K7arK4IjzjccWz5GzhhSE"  # Replace with your actual key

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
            "url": data.get("url"),  # image url or video url
            "media_type": data.get("media_type"),  # 'image' or 'video'
        }
    except (requests.RequestException, ValueError) as e:
        print(f"Error fetching APOD: {e}")
        return None
