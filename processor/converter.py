"""
Audio converter - convert ke MP3 320kbps atau FLAC dengan ffmpeg
"""
import subprocess
from pathlib import Path
from typing import Optional, Literal
from utils.logger import logger
from utils.config import FFMPEG_CONFIG, AUDIO_CODEC


class AudioConverter:
    """Handle audio conversion dengan ffmpeg"""
    
    @staticmethod
    def check_ffmpeg() -> bool:
        """
        Check apakah ffmpeg tersedia di system
        
        Returns:
            True jika ffmpeg tersedia, False jika tidak
        """
        try:
            subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
            logger.debug("FFmpeg is available")
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            logger.error("FFmpeg not found. Please install ffmpeg first.")
            return False
    
    @staticmethod
    def convert_to_mp3(
        input_file: Path,
        output_file: Path,
        bitrate: int = 320
    ) -> bool:
        """
        Convert audio ke MP3 dengan bitrate tertentu
        
        Args:
            input_file: Path ke input audio file
            output_file: Path ke output MP3 file
            bitrate: Bitrate dalam kbps (default: 320)
        
        Returns:
            True jika sukses, False jika gagal
        """
        try:
            if not input_file.exists():
                logger.error(f"Input file not found: {input_file}")
                return False
            
            logger.info(f"Converting to MP3 {bitrate}kbps: {input_file.name}")
            
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            cmd = [
                'ffmpeg',
                '-i', str(input_file),
                '-codec:a', AUDIO_CODEC['mp3'],
                '-b:a', f'{bitrate}k',
                '-q:a', '0',  # Variable bitrate
                '-f', 'mp3',
                '-y',  # Overwrite output file
                str(output_file)
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                logger.debug(f"MP3 conversion successful: {output_file.name}")
                return True
            else:
                logger.error(f"MP3 conversion failed: {result.stderr}")
                return False
        
        except subprocess.TimeoutExpired:
            logger.error("MP3 conversion timeout")
            return False
        except Exception as e:
            logger.error(f"Error converting to MP3: {e}")
            return False
    
    @staticmethod
    def convert_to_flac(
        input_file: Path,
        output_file: Path
    ) -> bool:
        """
        Convert audio ke FLAC (lossless)
        
        Args:
            input_file: Path ke input audio file
            output_file: Path ke output FLAC file
        
        Returns:
            True jika sukses, False jika gagal
        """
        try:
            if not input_file.exists():
                logger.error(f"Input file not found: {input_file}")
                return False
            
            logger.info(f"Converting to FLAC: {input_file.name}")
            
            output_file.parent.mkdir(parents=True, exist_ok=True)
            
            cmd = [
                'ffmpeg',
                '-i', str(input_file),
                '-codec:a', AUDIO_CODEC['flac'],
                '-compression_level', '8',  # Maximum compression
                '-f', 'flac',
                '-y',
                str(output_file)
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300
            )
            
            if result.returncode == 0:
                logger.debug(f"FLAC conversion successful: {output_file.name}")
                return True
            else:
                logger.error(f"FLAC conversion failed: {result.stderr}")
                return False
        
        except subprocess.TimeoutExpired:
            logger.error("FLAC conversion timeout")
            return False
        except Exception as e:
            logger.error(f"Error converting to FLAC: {e}")
            return False
    
    @staticmethod
    def get_audio_info(audio_file: Path) -> dict:
        """
        Get informasi tentang audio file menggunakan ffprobe
        
        Args:
            audio_file: Path ke audio file
        
        Returns:
            Dictionary berisi informasi audio (duration, bitrate, codec, dll)
        """
        try:
            cmd = [
                'ffprobe',
                '-v', 'error',
                '-show_entries', 'format=duration,bit_rate:stream=codec_name,bit_rate',
                '-of', 'default=noprint_wrappers=1:nokey=1:noinval=1',
                str(audio_file)
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                output = result.stdout.strip().split('\n')
                return {
                    'available': True,
                    'info': output
                }
            else:
                return {'available': False}
        
        except Exception as e:
            logger.warning(f"Could not get audio info: {e}")
            return {'available': False}
