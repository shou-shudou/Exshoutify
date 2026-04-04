"""
Cover art processor - download dan embed album cover
"""
import requests
from pathlib import Path
from PIL import Image
from io import BytesIO
from typing import Optional
from utils.logger import logger
from utils.config import TEMP_DIR


class CoverProcessor:
    """Handle album cover download dan embedding"""
    
    @staticmethod
    def download_cover(cover_url: str, output_path: Optional[Path] = None) -> Optional[Path]:
        """
        Download album cover dari URL
        
        Args:
            cover_url: URL ke cover image
            output_path: Path untuk save cover (optional)
        
        Returns:
            Path ke cover image jika sukses, None jika gagal
        """
        try:
            if not cover_url:
                logger.debug("No cover URL provided")
                return None
            
            logger.info(f"Downloading cover from: {cover_url}")
            
            response = requests.get(cover_url, timeout=10)
            response.raise_for_status()
            
            # Save cover image
            if output_path is None:
                output_path = TEMP_DIR / "cover_temp.jpg"
            
            output_path.parent.mkdir(parents=True, exist_ok=True)
            
            with open(output_path, 'wb') as f:
                f.write(response.content)
            
            logger.debug(f"Cover saved to: {output_path}")
            return output_path
        
        except requests.exceptions.RequestException as e:
            logger.warning(f"Failed to download cover: {e}")
            return None
        except Exception as e:
            logger.error(f"Error downloading cover: {e}")
            return None
    
    @staticmethod
    def optimize_cover(cover_path: Path, max_size: int = 500000) -> Path:
        """
        Optimize cover image (resize, compress)
        
        Args:
            cover_path: Path ke cover image
            max_size: Maksimal ukuran file dalam bytes
        
        Returns:
            Path ke cover yang sudah di-optimize
        """
        try:
            logger.debug(f"Optimizing cover: {cover_path.name}")
            
            img = Image.open(cover_path)
            
            # Resize jika terlalu besar (max 500x500)
            max_dimension = 500
            if img.width > max_dimension or img.height > max_dimension:
                img.thumbnail((max_dimension, max_dimension), Image.Resampling.LANCZOS)
            
            # Convert ke RGB jika RGBA
            if img.mode in ('RGBA', 'LA', 'P'):
                rgb_img = Image.new('RGB', img.size, (255, 255, 255))
                rgb_img.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
                img = rgb_img
            
            # Save dengan compression
            optimized_path = cover_path.parent / "cover_optimized.jpg"
            
            quality = 95
            while True:
                img.save(optimized_path, 'JPEG', quality=quality)
                
                if optimized_path.stat().st_size <= max_size or quality <= 50:
                    break
                
                quality -= 5
            
            logger.debug(f"Cover optimized: {optimized_path.stat().st_size / 1024:.1f} KB")
            
            return optimized_path
        
        except Exception as e:
            logger.error(f"Error optimizing cover: {e}")
            return cover_path
    
    @staticmethod
    def validate_cover(cover_path: Path) -> bool:
        """
        Validasi cover image
        
        Args:
            cover_path: Path ke cover image
        
        Returns:
            True jika valid, False jika tidak
        """
        try:
            if not cover_path.exists():
                return False
            
            img = Image.open(cover_path)
            # Validasi minimal resolution
            if img.width < 100 or img.height < 100:
                logger.warning(f"Cover too small: {img.width}x{img.height}")
                return False
            
            return True
        
        except Exception as e:
            logger.warning(f"Invalid cover image: {e}")
            return False

