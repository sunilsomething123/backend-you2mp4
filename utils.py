import os
import re
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
import random

def fetch_video_info(AIzaSyBuLDbPhS5QddaZaETco_-MUtngmGSscH8):
    youtube = build('youtube', 'v3', developerKey=api_key)
    video_id = extract_video_id(url)
    response = youtube.videos().list(part='snippet,contentDetails', id=video_id).execute()
    
    if not response['items']:
        raise ValueError('Invalid video URL')
    
    video_info = response['items'][0]
    resolutions = get_available_resolutions(video_info)
    
    return {
        'id': video_id,
        'title': video_info['snippet']['title'],
        'resolutions': resolutions
    }

def extract_video_id(url):
    regex = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
    match = re.match(regex, url)
    if not match:
        raise ValueError('Invalid YouTube URL')
    return match.group(1)

def get_available_resolutions(video_info):
    # Implement logic to fetch available resolutions
    return ['144p', '240p', '360p', '480p', '720p', '1080p']

def download_video(video_id, resolution):
    # Implement logic to download video
    return f"{video_id}_{resolution}.mp4"

class RateLimiter:
    def __init__(self, max_requests, period):
        self.max_requests = max_requests
        self.period = period
        self.requests = {}

    def limit(self, func):
        def wrapper(*args, **kwargs):
            user_ip = request.remote_addr
            if user_ip not in self.requests:
                self.requests[user_ip] = []
            
            self.requests[user_ip] = [timestamp for timestamp in self.requests[user_ip] if timestamp > time.time() - self.period]
            
            if len(self.requests[user_ip]) >= self.max_requests:
                return jsonify({'error': 'Rate limit exceeded'}), 429
            
            self.requests[user_ip].append(time.time())
            return func(*args, **kwargs)
        
        return wrapper

def generate_joke(success):
    jokes = {
        True: [
            "Success! Here's your video, freshly baked!",
            "Your video is ready! No need to thank us, just enjoy!"
        ],
        False: [
            "Oops! Something went wrong. Did you try turning it off and on again?",
            "Error! Maybe the internet gods are angry. Try again later."
        ]
    }
    return random.choice(jokes[success])
