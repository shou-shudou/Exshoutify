"""
Metadata processor - extract dan manage metadata dari audio file
"""
import json
from pathlib import Path
from typing import Dict, Optional
from mutagen.easyid3 import EasyID3
from mutagen.flac import FLAC
from utils.logger import logger


class MetadataProcessor:
    """Handle metadata extraction dan embedding"""
    
    @staticmethod
    def embed_metadata(
        audio_file: Path,
        metadata: Dict[str, str],
        cover_image: Optional[Path] = None
    ) -> bool:
        """
        Embed metadata ke dalam audio file
        
        Args:
            audio_file: Path ke audio file
            metadata: Dictionary berisi metadata (title, artist, album, year, etc)
            cover_image: Path ke cover image (opsional)
        
        Returns:
            True jika sukses, False jika gagal
        """
        try:
            file_ext = audio_file.suffix.lower()
            
            if file_ext == '.mp3':
                return MetadataProcessor._embed_mp3(audio_file, metadata, cover_image)
            elif file_ext == '.flac':
                return MetadataProcessor._embed_flac(audio_file, metadata, cover_image)
            else:
                logger.warning(f"Unsupported audio format: {file_ext}")
                return False
        
        except Exception as e:
            logger.error(f"Error embedding metadata: {e}")
            return False
    
    @staticmethod
    def _embed_mp3(
        audio_file: Path,
        metadata: Dict[str, str],
        cover_image: Optional[Path] = None
    ) -> bool:
        """Embed metadata ke MP3 file"""
        try:
            audio = EasyID3(str(audio_file))
            
            # Set metadata
            if 'title' in metadata:
                audio['title'] = metadata['title']
            if 'artist' in metadata:
                audio['artist'] = metadata['artist']
            if 'album' in metadata:
                audio['album'] = metadata['album']
            if 'date' in metadata:
                audio['date'] = str(metadata['date'])
            if 'genre' in metadata:
                audio['genre'] = metadata['genre']
            
            audio.save()
            logger.debug(f"MP3 metadata embedded: {audio_file.name}")
            
            return True
        
        except Exception as e:
            logger.error(f"Error embedding MP3 metadata: {e}")
            return False
    
    @staticmethod
    def _embed_flac(
        audio_file: Path,
        metadata: Dict[str, str],
        cover_image: Optional[Path] = None
    ) -> bool:
        """Embed metadata ke FLAC file"""
        try:
            audio = FLAC(str(audio_file))
            
            # Set metadata
            if 'title' in metadata:
                audio['title'] = metadata['title']
            if 'artist' in metadata:
                audio['artist'] = metadata['artist']
            if 'album' in metadata:
                audio['album'] = metadata['album']
            if 'date' in metadata:
                audio['date'] = str(metadata['date'])
            if 'genre' in metadata:
                audio['genre'] = metadata['genre']
            
            audio.save()
            logger.debug(f"FLAC metadata embedded: {audio_file.name}")
            
            return True
        
        except Exception as e:
            logger.error(f"Error embedding FLAC metadata: {e}")
            return False
    
    @staticmethod
    def extract_metadata(audio_file: Path) -> Dict[str, str]:
        """
        Extract metadata dari audio file
        
        Args:
            audio_file: Path ke audio file
        
        Returns:
            Dictionary berisi metadata
        """
        try:
            file_ext = audio_file.suffix.lower()
            metadata = {}
            
            if file_ext == '.mp3':
                audio = EasyID3(str(audio_file))
                metadata['title'] = audio.get('title', ['Unknown'])[0]
                metadata['artist'] = audio.get('artist', ['Unknown'])[0]
                metadata['album'] = audio.get('album', ['Unknown'])[0]
                metadata['date'] = audio.get('date', ['Unknown'])[0]
            
            elif file_ext == '.flac':
                audio = FLAC(str(audio_file))
                metadata['title'] = audio.get('title', ['Unknown'])[0]
                metadata['artist'] = audio.get('artist', ['Unknown'])[0]
                metadata['album'] = audio.get('album', ['Unknown'])[0]
                metadata['date'] = audio.get('date', ['Unknown'])[0]
            
            return metadata
        
        except Exception as e:
            logger.warning(f"Error extracting metadata: {e}")
            return {}
```
