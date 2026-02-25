import os
import re
import requests
import yt_dlp
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Pastikan API Key YouTube tersimpan di Environment Variables Vercel
YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY', '')

# --- METODE 1: Y2MATE (Manual Scraper - Tanpa Menulis ke File System) ---
def get_y2mate_data(video_id):
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
            'Referer': f'https://www.y2mate.com/youtube/{video_id}'
        }
        
        # Step 1: Analyze
        res_analyze = requests.post(
            "https://www.y2mate.com/mates/en/analyze/ajax",
            data={'url': f'https://www.youtube.com/watch?v={video_id}', 'q_auto': 0, 'ajax': 1},
            headers=headers, timeout=10
        ).json()
        
        if res_analyze.get('status') != 'success': return None
        
        # Cari token 'k' untuk MP3 via Regex
        html = res_analyze['result']
        k_search = re.findall(r'data-ftype="mp3".*?data-fquality="128".*?data-k="(.*?)"', html)
        if not k_search: k_search = re.findall(r'data-k="(.*?)"', html)
        
        if not k_search: return None
        
        # Step 2: Convert
        res_convert = requests.post(
            "https://www.y2mate.com/mates/en/convert/ajax",
            data={
                'type': 'youtube', '_id': res_analyze['id'], 'v_id': video_id,
                'ajax': '1', 'token': k_search[0], 'ftype': 'mp3', 'fquality': '128'
            },
            headers=headers, timeout=10
        ).json()
        
        if res_convert.get('status') == 'success':
            return {
                'title': res_analyze.get('title', 'YouTube Music'),
                'download_url': res_convert['result'],
                'format': 'mp3',
                'quality': '128',
                'method': 'Y2Mate (Metode 1)',
                'thumbnail': f"https://i.ytimg.com/vi/{video_id}/mqdefault.jpg",
                'artist': 'YouTube'
            }
    except Exception: pass
    return None

# --- METODE 2: YT-DLP ---
def get_yt_dlp_data(video_id):
    video_url = f'https://www.youtube.com/watch?v={video_id}'
    # Vercel hanya membolehkan menulis ke /tmp
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'cachedir': '/tmp/youtube-dl-cache',
        'extractor_args': {'youtube': {'player_client': ['android', 'web']}}
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(video_url, download=False)
            formats = [f for f in info.get('formats', []) if f.get('acodec') != 'none']
            if formats:
                best = formats[-1]
                return {
                    'title': info.get('title'),
                    'download_url': best.get('url'),
                    'format': best.get('ext'),
                    'quality': '128',
                    'method': 'yt-dlp (Metode 2)',
                    'thumbnail': info.get('thumbnail'),
                    'artist': info.get('uploader')
                }
    except Exception: pass
    return None

@app.route('/api/search', methods=['GET'])
def search():
    query = request.args.get('q', '')
    if not query: return jsonify({'error': 'Query required'}), 400
    
    # Gunakan Google API v3
    url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&type=video&maxResults=10&key={YOUTUBE_API_KEY}"
    try:
        res = requests.get(url).json()
        videos = []
        for item in res.get('items', []):
            videos.append({
                'id': item['id']['videoId'],
                'title': item['snippet']['title'],
                'thumbnail': item['snippet']['thumbnails']['medium']['url'],
                'channel': item['snippet']['channelTitle']
            })
        return jsonify({'videos': videos})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/download', methods=['GET'])
def download():
    video_id = request.args.get('id')
    if not video_id: return jsonify({'error': 'ID required'}), 400
    
    # Coba Y2Mate (Metode 1)
    res = get_y2mate_data(video_id)
    # Jika gagal, coba yt-dlp (Metode 2)
    if not res:
        res = get_yt_dlp_data(video_id)
        
    if res: return jsonify(res)
    return jsonify({'error': 'Gagal mengambil link download'}), 500

# Vercel butuh variable 'app'
handler = app
