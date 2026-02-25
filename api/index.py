"""
Fahmi Mp3 - Backend API
Flask + YouTube API v3 + yt-dlp
"""
from flask import Flask, request, jsonify
from flask_cors import CORS
import os
import requests
import yt_dlp

app = Flask(__name__)
CORS(app)

# YouTube API Configuration
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY', '')
YOUTUBE_API_URL = 'https://www.googleapis.com/youtube/v3'

@app.route('/api/search', methods=['GET'])
def search_videos():
    """Search YouTube videos using YouTube API v3"""
    query = request.args.get('q', '')
    
    if not query:
        return jsonify({'error': 'Query parameter "q" is required'}), 400
    
    if not YOUTUBE_API_KEY:
        return jsonify({'error': 'YouTube API Key not configured'}), 500
    
    try:
        params = {
            'part': 'snippet',
            'q': query,
            'type': 'video',
            'maxResults': 10,
            'key': YOUTUBE_API_KEY
        }
        
        response = requests.get(f'{YOUTUBE_API_URL}/search', params=params)
        data = response.json()
        
        if 'error' in data:
            return jsonify({'error': data['error']['message']}), 400
        
        videos = []
        for item in data.get('items', []):
            video = {
                'id': item['id']['videoId'],
                'title': item['snippet']['title'],
                'thumbnail': item['snippet']['thumbnails']['high']['url'] if 'high' in item['snippet']['thumbnails'] else item['snippet']['thumbnails']['default']['url'],
                'channel': item['snippet']['channelTitle'],
                'publishedAt': item['snippet']['publishedAt']
            }
            videos.append(video)
        
        return jsonify({'videos': videos})
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download', methods=['GET'])
def get_download_link():
    """Get direct audio download link using yt-dlp"""
    video_id = request.args.get('id', '')
    
    if not video_id:
        return jsonify({'error': 'Video ID parameter "id" is required'}), 400
    
    try:
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        
        ydl_opts = {
            'format': 'bestaudio/best',
            'quiet': True,
            'no_warnings': True,
            'extract_flat': False,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            
            # Get best audio format
            formats = info.get('formats', [])
            audio_formats = [f for f in formats if f.get('acodec') != 'none' and f.get('vcodec') == 'none']
            
            if audio_formats:
                # Sort by quality (abr - audio bitrate)
                audio_formats.sort(key=lambda x: x.get('abr', 0) or 0, reverse=True)
                best_audio = audio_formats[0]
            else:
                # Fallback to any format with audio
                best_audio = formats[0] if formats else None
            
            if not best_audio:
                return jsonify({'error': 'No audio format found'}), 404
            
            return jsonify({
                'title': info.get('title', 'Unknown'),
                'artist': info.get('uploader', 'Unknown'),
                'duration': info.get('duration', 0),
                'thumbnail': info.get('thumbnail', ''),
                'download_url': best_audio.get('url', ''),
                'format': best_audio.get('ext', 'mp3'),
                'quality': best_audio.get('abr', 'Unknown')
            })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'service': 'Fahmi Mp3 API'})

# Vercel handler
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
