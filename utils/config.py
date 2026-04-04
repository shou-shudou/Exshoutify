"""
Configuration dan konstanta aplikasi Music Downloader
"""
import os
from pathlib import Path

# User home directory
HOME_DIR = Path.home()

# Download directory
DOWNLOAD_DIR = HOME_DIR / "Music" / "Downloads"
DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Folder structure untuk organized downloads
ORGANIZED_DOWNLOAD_DIR = HOME_DIR / "Music" / "Organized"
ORGANIZED_DOWNLOAD_DIR.mkdir(parents=True, exist_ok=True)

# Temporary directory untuk processing
TEMP_DIR = HOME_DIR / ".music_downloader" / "temp"
TEMP_DIR.mkdir(parents=True, exist_ok=True)

# Audio quality settings
AUDIO_QUALITY = {
    "mp3": {
        "default": 320,
        "options": [128, 192, 256, 320]
    },
    "flac": {
        "default": "best",
        "lossless": True
    }
}

# Spotify API settings (menggunakan spotdl yang sudah integrated)
SPOTIFY_CONFIG = {
    "use_cache": True,
    "max_retries": 3,
    "timeout": 30
}

# YouTube settings
YOUTUBE_CONFIG = {
    "max_retries": 3,
    "timeout": 30,
    "extract_audio": True
}

# FFmpeg settings
FFMPEG_CONFIG = {
    "preset": "fast",  # fast, medium, slow
    "loglevel": "error"
}

# Logging
LOG_DIR = HOME_DIR / ".music_downloader" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Batch processing
BATCH_CONFIG = {
    "max_workers": 3,  # untuk multi-threading
    "queue_mode": True,
    "timeout_per_track": 300  # 5 menit per track
}

# Character yang dilarang di filename
ILLEGAL_CHARS = r'[<>:"/\\|?*\x00-\x1f]'

# Audio codec
AUDIO_CODEC = {
    "mp3": "libmp3lame",
    "flac": "flac"
}
