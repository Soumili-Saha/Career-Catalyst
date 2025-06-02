import requests


API_KEY = your_api_key
SEARCH_QUERY = "pokemon ash vs leon"

youtube_url = "https://www.googleapis.com/youtube/v3/search"

params = {
    "part": "snippet",
    "q": SEARCH_QUERY,
    "type": "video",
    "maxResults": 10,
    "key": API_KEY
}

response = requests.get(youtube_url, params=params)

if response.status_code == 200:
    results = response.json()
    for item in results.get("items", []):
        title = item["snippet"]["title"]
        vdo_id = item["id"]["videoId"]
        print(f"Title: {title}")
        print(f"URL: https://www.youtube.com/watch?v={vdo_id}\n")
else:
    print("Error:", response.json())
