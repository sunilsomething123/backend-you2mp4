from flask import Flask, request, jsonify
from flask_cors import CORS
from utils import fetch_video_info, download_video

app = Flask(__name__)
CORS(app)  # This will enable CORS for all routes

@app.route('/api/download', methods=['POST'])
def download():
    data = request.get_json()
    url = data.get('url')

    if not url:
        return jsonify({'success': False, 'message': 'No URL provided'}), 400

    try:
        video_info = fetch_video_info(url)
        if not video_info:
            return jsonify({'success': False, 'message': 'Invalid video URL'}), 400

        preview_url = generate_preview_url(video_info)  # Generate URL for 30 seconds preview
        download_url = generate_download_url(video_info)  # Generate download URL

        return jsonify({'success': True, 'previewUrl': preview_url, 'downloadUrl': download_url})
    except Exception as e:
        return jsonify({'success': False, 'message': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
