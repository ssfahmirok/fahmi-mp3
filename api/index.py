import os
from flask import Flask, request, jsonify
from flask_cors import CORS
import yt_dlp
from y2mate_api import Handler # Menggunakan library sesuai dokumentasi

app = Flask(__name__)
CORS(app)

# --- METODE 1: Y2MATE (Menggunakan Library y2mate-api) ---
def get_y2mate_data(video_id):
    try:
        # Dokumentasi: Handler menerima query (id/url/title)
        api = Handler(video_id)
        
        # Dokumentasi: api.run(format="mp3") mengembalikan generator metadata
        # Kita ambil hasil pertama saja
        for audio_metadata in api.run(format="mp3"):
            if audio_metadata.get('status') == 'ok':
                return {
                    'title': audio_metadata.get('title'),
                    'download_url': audio_metadata.get('dlink'), # Link ada di 'dlink'
                    'format': 'mp3',
                    'quality': audio_metadata.get('q'),
                    'method': 'Y2Mate (Metode 1)'
                }
        return None
    except Exception as e:
        print(f"Y2Mate Library Error: {e}")
        return None

# --- METODE 2: YT-DLP ---
def get_yt_dlp_data(video_id):
    video_url = f'https://www.youtube.com/watch?v={video_id}'
    ydl_opts = {
        'format': 'bestaudio/best',
        'quiet': True,
        'no_warnings': True,
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
                    'quality': f"{int(best.get('abr', 0))}kbps",
                    'method': 'yt-dlp (Metode 2)'
                }
        return None
    except Exception as e:
        print(f"yt-dlp Error: {e}")
        return None

# --- ENDPOINT ---
@app.route('/api/download', methods=['GET'])
def download():
    video_id = request.args.get('id')
    if not video_id:
        return jsonify({'error': 'ID video wajib diisi'}), 400

    # Jalankan Metode 1
    print("Mencoba Y2Mate...")
    res = get_y2mate_data(video_id)
    
    # Jika Metode 1 Gagal, jalankan Metode 2
    if not res:
        print("Y2Mate Gagal, beralih ke yt-dlp...")
        res = get_yt_dlp_data(video_id)
        
    if res:
        return jsonify(res)
    
    return jsonify({'error': 'Gagal mengambil data dari semua metode'}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5000)
