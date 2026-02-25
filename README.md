# 🎵 Fahmi Mp3

Aplikasi download lagu MP3 dari YouTube dengan UI Neon 3D yang powerful. Dibangun dengan Flask + React + yt-dlp.

## ✨ Fitur

- 🔍 **Search YouTube** - Cari lagu langsung dari YouTube API v3
- ⬇️ **Download MP3** - Download audio dengan yt-dlp (bypass bot detection)
- 🎨 **UI Neon 3D** - Tampilan modern dengan efek glow dan animasi
- 🎵 **Audio Player** - Preview sebelum download
- ⚡ **Cepat & Gratis** - Tanpa iklan, tanpa limit

## 🚀 Deploy ke Vercel

### 1. Clone Repository

```bash
git clone https://github.com/username/fahmi-mp3.git
cd fahmi-mp3
```

### 2. Setup Environment Variables

```bash
cp .env.example .env
```

Edit file `.env` dan tambahkan YouTube API Key:
```
YOUTUBE_API_KEY=your_api_key_here
```

### 3. Deploy

```bash
npm install
npm run build
vercel --prod
```

Atau connect repository ke Vercel Dashboard dan set environment variable `YOUTUBE_API_KEY`.

## 🛠️ Development (Local)

### Prerequisites
- Python 3.9+
- Node.js 18+

### Setup Backend

```bash
# Install Python dependencies
pip install -r requirements.txt

# Run Flask server
python api/index.py
```

Backend akan berjalan di `http://localhost:5000`

### Setup Frontend

```bash
# Install Node dependencies
npm install

# Run dev server
npm run dev
```

Frontend akan berjalan di `http://localhost:5173`

## 📁 Struktur Folder

```
fahmi-mp3/
├── api/
│   └── index.py          # Flask backend
├── src/
│   ├── components/       # React components
│   ├── hooks/           # Custom hooks
│   ├── types/           # TypeScript types
│   ├── lib/             # Utilities
│   ├── App.tsx          # Main app
│   └── main.tsx         # Entry point
├── dist/                # Build output
├── vercel.json          # Vercel config
├── requirements.txt     # Python deps
├── package.json         # Node deps
└── README.md
```

## 🔑 Mendapatkan YouTube API Key

1. Buka [Google Cloud Console](https://console.cloud.google.com/)
2. Buat project baru
3. Enable **YouTube Data API v3**
4. Buat API Key di Credentials
5. Copy API Key ke environment variable

## 📝 API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/search?q={query}` | GET | Cari video YouTube |
| `/api/download?id={videoId}` | GET | Get direct audio link |
| `/api/health` | GET | Health check |

## 🎨 Tech Stack

- **Backend**: Flask, yt-dlp, YouTube API v3
- **Frontend**: React, TypeScript, Vite, Tailwind CSS
- **Animation**: Framer Motion
- **Icons**: Lucide React
- **Deployment**: Vercel

## ⚠️ Disclaimer

Aplikasi ini untuk edukasi. Pastikan kamu memiliki hak untuk mendownload konten. Kami tidak bertanggung jawab atas penyalahgunaan aplikasi ini.

## 📄 License

MIT License - feel free to use and modify!

---

Dibuat dengan ❤️ oleh Fahmi
