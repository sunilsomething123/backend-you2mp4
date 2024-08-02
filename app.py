from flask import Flask, request, jsonify, render_template
from utils import fetch_video_info, download_video, RateLimiter, generate_joke

app = Flask(__name__)

# Set API Key directly
API_KEY = 'AIzaSyBuLDbPhS5QddaZaETco_-MUtngmGSscH8'
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
        video_info = fetch_video_info(url, API_KEY)
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
