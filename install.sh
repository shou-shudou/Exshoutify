#!/bin/bash

echo "╔════════════════════════════════════════════════════════════════╗"
echo "║         Music Downloader untuk Termux - Installation           ║"
echo "╚════════════════════════════════════════════════════════════════╝"

# Update packages
echo "[*] Updating package manager..."
pkg update -y
pkg upgrade -y

# Install dependencies
echo "[*] Installing system dependencies..."
pkg install -y \
    python \
    pip \
    ffmpeg \
    git \
    curl

# Check Python version
python_version=$(python -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo "[✓] Python version: $python_version"

# Check FFmpeg
if command -v ffmpeg &> /dev/null; then
    ffmpeg_version=$(ffmpeg -version | head -1)
    echo "[✓] FFmpeg installed: $ffmpeg_version"
else
    echo "[✗] FFmpeg not found - installation may have failed"
    exit 1
fi

# Upgrade pip
echo "[*] Upgrading pip..."
pip install --upgrade pip

# Install Python dependencies
echo "[*] Installing Python packages..."
pip install -r requirements.txt

# Check spotdl
echo "[*] Checking spotdl..."
if python -c "import spotdl" 2>/dev/null; then
    echo "[✓] spotdl installed successfully"
else
    echo "[✗] spotdl installation failed"
fi

# Check yt-dlp
echo "[*] Checking yt-dlp..."
if python -c "import yt_dlp" 2>/dev/null; then
    echo "[✓] yt-dlp installed successfully"
else
    echo "[✗] yt-dlp installation failed"
fi

# Create necessary directories
echo "[*] Creating directories..."
mkdir -p ~/Music/Downloads
mkdir -p ~/Music/Organized
mkdir -p ~/.music_downloader/logs
mkdir -p ~/.music_downloader/temp

# Create symlink untuk easy access
echo "[*] Creating symlink..."
ln -sf $(pwd) ~/music-downloader

# Test installation
echo ""
echo "[*] Testing installation..."
python main.py --help > /dev/null 2>&1
if [ $? -eq 0 ]; then
    echo "[✓] Installation completed successfully!"
    echo ""
    echo "╔════════════════════════════════════════════════════════════════╗"
    echo "║                     INSTALLATION COMPLETE                      ║"
    echo "╚════════════════════════════════════════════════════════════════╝"
    echo ""
    echo "Usage examples:"
    echo "  python main.py 'https://open.spotify.com/track/...'"
    echo "  python main.py 'https://www.youtube.com/watch?v=...'"
    echo "  python main.py --batch urls.txt --parallel"
    echo "  python main.py 'url' --organize --format flac"
    echo ""
    echo "Download location: ~/Music/Downloads"
    echo "Organized downloads: ~/Music/Organized"
    echo "Logs: ~/.music_downloader/logs"
    echo ""
else
    echo "[✗] Installation test failed"
    exit 1
fi
