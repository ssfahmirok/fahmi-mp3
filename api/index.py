"""
Fahmi Mp3 - Backend API
Flask + YouTube API v3 + yt-dlp (Bypass Bot Detection)
"""
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
import requests
import yt_dlp
import random

app = Flask(__name__)
CORS(app)

# YouTube API Configuration
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY', '')
YOUTUBE_API_URL = 'https://www.googleapis.com/youtube/v3'

# User Agents yang realistis (rotasi)
USER_AGENTS = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0',
    'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2 Safari/605.1.15',
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 Edg/119.0.0.0',
]

def get_random_user_agent():
    return random.choice(USER_AGENTS)

def create_ydl_opts(method='web'):
    """Create yt-dlp options based on method"""
    user_agent = get_random_user_agent()
    
    base_opts = {
        'quiet': True,
        'no_warnings': True,
        'socket_timeout': 30,
        'retries': 3,
    }
    
    if method == 'web':
        base_opts.update({
            'format': 'bestaudio/best',
            'http_headers': {
                'User-Agent': user_agent,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
                'Accept-Encoding': 'gzip, deflate, br',
                'DNT': '1',
                'Connection': 'keep-alive',
                'Upgrade-Insecure-Requests': '1',
                'Sec-Fetch-Dest': 'document',
                'Sec-Fetch-Mode': 'navigate',
                'Sec-Fetch-Site': 'none',
                'Sec-Fetch-User': '?1',
                'Cache-Control': 'max-age=0',
            },
            'extractor_args': {
                'youtube': {
                    'player_client': ['web'],
                    'player_skip': ['webpage', 'configs', 'js'],
                }
            },
        })
    
    elif method == 'android':
        base_opts.update({
            'format': 'bestaudio[ext=m4a]/bestaudio/best',
            'http_headers': {
                'User-Agent': 'com.google.android.youtube/19.09.37 (Linux; U; Android 14) gzip',
                'Accept-Language': 'en-US',
            },
            'extractor_args': {
                'youtube': {
                    'player_client': ['android'],
                    'player_skip': ['webpage', 'configs'],
                }
            },
        })
    
    elif method == 'ios':
        base_opts.update({
            'format': 'bestaudio[ext=m4a]/bestaudio/best',
            'http_headers': {
                'User-Agent': 'com.google.ios.youtube/19.09.7 (iPhone; CPU iPhone OS 17_1_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1',
                'Accept-Language': 'en-US',
            },
            'extractor_args': {
                'youtube': {
                    'player_client': ['ios'],
                    'player_skip': ['webpage', 'configs'],
                }
            },
        })
    
    elif method == 'tv':
        base_opts.update({
            'format': 'bestaudio/best',
            'http_headers': {
                'User-Agent': 'Mozilla/5.0 (ChromiumStylePlatform) Cobalt/Version',
                'Accept-Language': 'en-US',
            },
            'extractor_args': {
                'youtube': {
                    'player_client': ['tv'],
                    'player_skip': ['webpage', 'configs'],
                }
            },
        })
    
    return base_opts

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
            'maxResults': 12,
            'key': YOUTUBE_API_KEY
        }
        
        response = requests.get(f'{YOUTUBE_API_URL}/search', params=params, timeout=10)
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
    """Get direct audio download link using yt-dlp (primary method)"""
    video_id = request.args.get('id', '')
    method = request.args.get('method', 'web')
    
    if not video_id:
        return jsonify({'error': 'Video ID parameter "id" is required'}), 400
    
    try:
        video_url = f'https://www.youtube.com/watch?v={video_id}'
        
        ydl_opts = create_ydl_opts(method)
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            
            # Get best audio format
            formats = info.get('formats', [])
            audio_formats = [f for f in formats if f.get('acodec') != 'none' and f.get('vcodec') == 'none']
            
            if audio_formats:
                audio_formats.sort(key=lambda x: x.get('abr', 0) or 0, reverse=True)
                best_audio = audio_formats[0]
            else:
                audio_formats = [f for f in formats if f.get('acodec') != 'none']
                if audio_formats:
                    audio_formats.sort(key=lambda x: x.get('abr', 0) or 0, reverse=True)
                    best_audio = audio_formats[0]
                else:
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
                'quality': best_audio.get('abr', 'Unknown'),
                'method': method
            })
    
    except Exception as e:
        error_msg = str(e)
        
        # Cek jika error karena bot detection
        if any(keyword in error_msg.lower() for keyword in ['sign in', 'bot', 'confirm']):
            return jsonify({
                'error': 'YouTube mendeteksi request sebagai bot.',
                'detail': error_msg,
                'solution': 'Coba gunakan method alternatif (android, ios, atau tv).',
                'need_fallback': True
            }), 403
        
        return jsonify({'error': error_msg}), 500

@app.route('/api/download-alt', methods=['GET'])
def get_download_link_alt():
    """Alternative download method - tries multiple clients"""
    video_id = request.args.get('id', '')
    
    if not video_id:
        return jsonify({'error': 'Video ID parameter "id" is required'}), 400
    
    methods = ['android', 'ios', 'tv', 'web']
    last_error = None
    
    for method in methods:
        try:
            video_url = f'https://www.youtube.com/watch?v={video_id}'
            ydl_opts = create_ydl_opts(method)
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(video_url, download=False)
                formats = info.get('formats', [])
                
                audio_formats = [f for f in formats if f.get('acodec') != 'none']
                if audio_formats:
                    audio_formats.sort(key=lambda x: x.get('abr', 0) or 0, reverse=True)
                    best_audio = audio_formats[0]
                else:
                    best_audio = formats[0] if formats else None
                
                if best_audio:
                    return jsonify({
                        'title': info.get('title', 'Unknown'),
                        'artist': info.get('uploader', 'Unknown'),
                        'duration': info.get('duration', 0),
                        'thumbnail': info.get('thumbnail', ''),
                        'download_url': best_audio.get('url', ''),
                        'format': best_audio.get('ext', 'mp3'),
                        'quality': best_audio.get('abr', 'Unknown'),
                        'method': method
                    })
        
        except Exception as e:
            last_error = str(e)
            continue  # Try next method
    
    # All methods failed
    return jsonify({
        'error': 'Semua metode gagal mengambil audio.',
        'detail': last_error,
        'solution': 'Video ini mungkin memiliki proteksi ketat atau memerlukan login. Coba video lain.'
    }), 403

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'ok', 
        'service': 'Fahmi Mp3 API',
        'yt_dlp_version': yt_dlp.version.__version__
    })

# Get static folder path
STATIC_DIR = os.path.join(os.path.dirname(__file__), '..', 'static')

# Serve static files
@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve(path):
    if path and os.path.exists(os.path.join(STATIC_DIR, path)):
        return send_from_directory(STATIC_DIR, path)
    return send_from_directory(STATIC_DIR, 'index.html')

# Vercel handler
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
