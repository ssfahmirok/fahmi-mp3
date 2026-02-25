# 🎵 Fahmi Mp3

Aplikasi download lagu MP3 dari YouTube dengan UI Neon 3D yang powerful. Dibangun dengan Flask + yt-dlp + YouTube API v3.

![Fahmi Mp3](https://img.shields.io/badge/Fahmi-Mp3-ff00ff?style=for-the-badge)
![yt-dlp](https://img.shields.io/badge/powered%20by-yt--dlp-00ffff?style=for-the-badge)

## ✨ Fitur

- 🔍 **Search YouTube** - Cari lagu langsung dari YouTube API v3
- ⬇️ **Download MP3** - Download audio dengan yt-dlp (bypass bot detection)
- 🎨 **UI Neon 3D** - Tampilan modern dengan efek glow dan animasi
- 🎵 **Audio Player** - Preview sebelum download
- ⚡ **Cepat & Gratis** - Tanpa iklan, tanpa limit

## 🚀 Quick Deploy ke Vercel

### Langkah 1: Fork/Clone Repository

```bash
git clone https://github.com/username/fahmi-mp3.git
cd fahmi-mp3
```

### Langkah 2: Setup YouTube API Key

1. Buka [Google Cloud Console](https://console.cloud.google.com/)
2. Buat project baru
3. Enable **YouTube Data API v3**
4. Buat API Key di Credentials
5. Copy API Key

### Langkah 3: Deploy ke Vercel

[![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new)

Atau deploy via CLI:

```bash
npm i -g vercel
vercel --prod
```

### Langkah 4: Set Environment Variable

Di dashboard Vercel, tambahkan environment variable:
- **Name**: `YOUTUBE_API_KEY`
- **Value**: `your_api_key_here`

## 🛠️ Development (Local)

### Prerequisites
- Python 3.9+
- pip

### Setup & Run

```bash
# Install dependencies
pip install -r requirements.txt

# Set environment variable
export YOUTUBE_API_KEY=your_api_key_here

# Run Flask server
python api/index.py
```

Buka browser: `http://localhost:5000`

## 📁 Struktur Folder

```
fahmi-mp3/
├── api/
│   └── index.py          # Flask backend
├── static/
│   └── index.html        # Frontend UI
├── requirements.txt      # Python dependencies
├── vercel.json          # Vercel configuration
├── .env.example         # Environment template
└── README.md
```

## 🔌 API Endpoints

| Endpoint | Method | Parameters | Description |
|----------|--------|------------|-------------|
| `/api/search` | GET | `q` (string) | Cari video YouTube |
| `/api/download` | GET | `id` (video ID) | Get direct audio link |
| `/api/health` | GET | - | Health check |

### Contoh Response

**Search:**
```json
{
  "videos": [
    {
      "id": "dQw4w9WgXcQ",
      "title": "Rick Astley - Never Gonna Give You Up",
      "thumbnail": "https://i.ytimg.com/vi/...",
      "channel": "Rick Astley",
      "publishedAt": "2009-10-25T06:57:33Z"
    }
  ]
}
```

**Download:**
```json
{
  "title": "Never Gonna Give You Up",
  "artist": "Rick Astley",
  "duration": 213,
  "thumbnail": "https://i.ytimg.com/vi/...",
  "download_url": "https://...",
  "format": "m4a",
  "quality": "128"
}
```

## 🎨 Tech Stack

- **Backend**: Python, Flask, yt-dlp, YouTube API v3
- **Frontend**: HTML5, CSS3, Vanilla JavaScript
- **Deployment**: Vercel Serverless Functions

## ⚠️ Disclaimer

Aplikasi ini untuk edukasi. Pastikan kamu memiliki hak untuk mendownload konten. Kami tidak bertanggung jawab atas penyalahgunaan aplikasi ini.

## 📝 Catatan Penting

- yt-dlp digunakan untuk bypass bot detection YouTube
- Direct link audio kadang expired dalam beberapa menit
- Gunakan dengan bijak dan hormati copyright

## 🐛 Troubleshooting

### "YouTube API Key not configured"
Pastikan environment variable `YOUTUBE_API_KEY` sudah di-set di Vercel dashboard.

### "No audio format found"
Video mungkin memiliki restruksi atau tidak tersedia.

### Download link tidak bekerja
Direct link dari YouTube kadang expired cepat. Coba generate ulang.

## 📄 License

MIT License - feel free to use and modify!

---

Dibuat dengan ❤️ menggunakan yt-dlp & YouTube API
