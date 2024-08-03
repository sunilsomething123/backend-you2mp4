import requests
import os

API_KEY = os.getenv('AIzaSyBuLDbPhS5QddaZaETco_-MUtngmGSscH8')
YOUTUBE_API_URL = "https://www.googleapis.com/youtube/v3/videos"
YOUTUBE_DL_URL = "https://www.youtube.com/watch?v="

def fetch_video_info(video_url):
    video_id = video_url.split('v=')[-1]
    params = {
        'id': video_id,
        'key': API_KEY,
        'part': 'snippet,contentDetails'
    }
    response = requests.get(YOUTUBE_API_URL, params=params)
    if response.status_code != 200:
        raise Exception("Failed to fetch video info")

    data = response.json()
    if 'items' not in data or not data['items']:
        return None

    video_info = data['items'][0]
    return video_info

def generate_preview_url(video_info):
    video_id = video_info['id']
    return f"https://www.youtube.com/embed/{video_id}?start=0&end=30"

def generate_download_url(video_info):
    video_id = video_info['id']
    return f"{YOUTUBE_DL_URL}{video_id}"
