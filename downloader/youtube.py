"""
YouTube downloader - menggunakan yt-dlp untuk download dari YouTube
"""
import subprocess
import json
from pathlib import Path
from typing import List, Dict, Optional
from utils.logger import logger
from utils.config import TEMP_DIR, YOUTUBE_CONFIG


class YouTubeDownloader:
    """Handle download dari YouTube menggunakan yt-dlp"""
    
    @staticmethod
    def check_ytdlp() -> bool:
        """
        Check apakah yt-dlp tersedia
        
        Returns:
            True jika yt-dlp tersedia, False jika tidak
        """
        try:
            result = subprocess.run(
                ['yt-dlp', '--version'],
                capture_output=True,
                text=True,
                timeout=10
            )
            if result.returncode == 0:
                logger.debug(f"yt-dlp is available: {result.stdout.strip()}")
                return True
            return False
        except (subprocess.TimeoutExpired, FileNotFoundError):
            logger.error("yt-dlp not found. Install with: pip install yt-dlp")
            return False
    
    @staticmethod
    def get_video_info(video_url: str) -> Optional[Dict]:
        """
        Get informasi video dari YouTube URL
        
        Args:
            video_url: URL ke YouTube video
        
        Returns:
            Dictionary berisi info video atau None jika gagal
        """
        try:
            logger.debug(f"Fetching YouTube video info: {video_url}")
            
            cmd = [
                'yt-dlp',
                '--dump-json',
                '--no-warnings',
                video_url
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=YOUTUBE_CONFIG['timeout']
            )
            
            if result.returncode == 0:
                info = json.loads(result.stdout)
                return {
                    'title': info.get('title', 'Unknown'),
                    'duration': info.get('duration', 0),
                    'channel': info.get('uploader', 'Unknown'),
                    'upload_date': info.get('upload_date', 'Unknown')
                }
            else:
                logger.warning(f"Failed to get video info: {result.stderr}")
                return None
        
        except json.JSONDecodeError:
            logger.warning("Failed to parse video info")
            return None
        except Exception as e:
            logger.warning(f"Error getting video info: {e}")
            return None
    
    @staticmethod
    def download_video(
        video_url: str,
        output_file: Path,
        audio_format: str = 'mp3',
        audio_quality: Optional[int] = None
    ) -> Optional[Path]:
        """
        Download audio dari YouTube video
        
        Args:
            video_url: URL ke YouTube video
            output_file: Path untuk menyimpan hasil download
            audio_format: Format audio (mp3/wav/m4a, default: mp3)
            audio_quality: Kualitas audio dalam kbps
        
        Returns:
            Path ke downloaded file jika sukses, None jika gagal
        """
        try:
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            logger.info(f"Downloading YouTube audio: {video_url}")
            
            # Build yt-dlp command untuk extract audio
            cmd = [
                'yt-dlp',
                '--extract-audio',
                '--audio-format', audio_format,
                '--audio-quality', str(audio_quality) if audio_quality else '192',
                '--output', str(output_file.parent / '%(title)s.%(ext)s'),
                '--no-warnings',
                video_url
            ]
            
            logger.debug(f"Running command: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=YOUTUBE_CONFIG['timeout']
            )
            
            if result.returncode == 0:
                # Find downloaded file
                downloaded_files = list(output_file.parent.glob(f'*.{audio_format}'))
                if downloaded_files:
                    downloaded_file = downloaded_files[-1]  # Get latest file
                    logger.info(f"Video downloaded successfully: {downloaded_file.name}")
                    return downloaded_file
            else:
                logger.error(f"YouTube download failed: {result.stderr}")
                return None
        
        except subprocess.TimeoutExpired:
            logger.error("YouTube download timeout")
            return None
        except Exception as e:
            logger.error(f"Error downloading YouTube video: {e}")
            return None
    
    @staticmethod
    def download_playlist(
        playlist_url: str,
        output_dir: Path,
        audio_format: str = 'mp3',
        audio_quality: Optional[int] = None,
        limit: Optional[int] = None
    ) -> List[Path]:
        """
        Download playlist dari YouTube
        
        Args:
            playlist_url: URL ke YouTube playlist
            output_dir: Directory untuk menyimpan hasil download
            audio_format: Format audio
            audio_quality: Kualitas audio dalam kbps
            limit: Maksimal jumlah video (None = all)
        
        Returns:
            List Path ke downloaded files
        """
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            
            logger.info(f"Downloading YouTube playlist: {playlist_url}")
            
            cmd = [
                'yt-dlp',
                '--extract-audio',
                '--audio-format', audio_format,
                '--audio-quality', str(audio_quality) if audio_quality else '192',
                '--output', str(output_dir / '%(playlist)s' / '%(title)s.%(ext)s'),
                '--no-warnings',
                playlist_url
            ]
            
            if limit:
                cmd.extend(['--playlist-items', f'1-{limit}'])
            
            logger.debug(f"Running command: {' '.join(cmd)}")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=1800  # 30 menit
            )
            
            if result.returncode == 0:
                downloaded_files = list(output_dir.rglob(f'*.{audio_format}'))
                logger.info(f"Playlist downloaded: {len(downloaded_files)} videos")
                return downloaded_files
            else:
                logger.error(f"Playlist download failed: {result.stderr}")
                return []
        
        except subprocess.TimeoutExpired:
            logger.error("Playlist download timeout")
            return []
        except Exception as e:
            logger.error(f"Error downloading playlist: {e}")
            return []
