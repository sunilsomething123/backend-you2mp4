import os
from flask import Flask, request, jsonify, render_template
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from utils import fetch_video_info, download_video, RateLimiter, generate_joke

app = Flask(__name__)

# Load environment variables
API_KEY = os.getenv('YOUTUBE_API_KEY')
DOWNLOAD_HISTORY = []

rate_limiter = RateLimiter(max_requests=10000, period=3600)  # 10,000 requests per hour

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['POST'])
@rate_limiter.limit
def download():
    url = request.form['url']
    try:
        video_info = fetch_video_info(AIzaSyBuLDbPhS5QddaZaETco_-MUtngmGSscH8)
        video_id = video_info['id']
        resolutions = video_info['resolutions']
        chosen_resolution = request.form.get('resolution', '720p')  # Default to 720p if not specified
        video_file = download_video(video_id, chosen_resolution)
        
        DOWNLOAD_HISTORY.append({
            'url': url,
            'resolution': chosen_resolution,
            'file': video_file
        })
        
        return jsonify({
            'status': 'success',
            'file': video_file,
            'message': generate_joke(success=True)
        })
    except HttpError as e:
        return jsonify({
            'status': 'error',
            'message': generate_joke(success=False),
            'error': str(e)
        }), 500
    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': generate_joke(success=False),
            'error': str(e)
        }), 500

@app.route('/history', methods=['GET'])
def history():
    return jsonify(DOWNLOAD_HISTORY)

if __name__ == '__main__':
    app.run(debug=True)
