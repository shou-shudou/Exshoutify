"""
Sanitizer untuk filename - menghapus karakter ilegal
"""
import re
from utils.config import ILLEGAL_CHARS


def sanitize_filename(filename: str, max_length: int = 200) -> str:
    """
    Sanitize filename dengan menghapus karakter ilegal
    
    Args:
        filename: Nama file yang akan di-sanitize
        max_length: Maksimal panjang filename
    
    Returns:
        Filename yang sudah di-sanitize
    """
    # Hapus karakter ilegal
    sanitized = re.sub(ILLEGAL_CHARS, "", filename)
    
    # Hapus leading/trailing spaces dan dots
    sanitized = sanitized.strip('. ')
    
    # Ganti multiple spaces dengan single space
    sanitized = re.sub(r'\s+', ' ', sanitized)
    
    # Truncate jika terlalu panjang (simpan extension)
    if len(sanitized) > max_length:
        name, ext = sanitized.rsplit('.', 1) if '.' in sanitized else (sanitized, '')
        name = name[:max_length - len(ext) - 1]
        sanitized = f"{name}.{ext}" if ext else name
    
    return sanitized


def sanitize_path_part(path_part: str) -> str:
    """
    Sanitize bagian dari path (artist, album, dll)
    
    Args:
        path_part: Bagian path yang akan di-sanitize
    
    Returns:
        Path part yang sudah di-sanitize
    """
    sanitized = re.sub(ILLEGAL_CHARS, "", path_part)
    sanitized = sanitized.strip('. ')
    sanitized = re.sub(r'\s+', ' ', sanitized)
    
    # Truncate untuk path part yang terlalu panjang
    if len(sanitized) > 100:
        sanitized = sanitized[:100]
    
    return sanitized
```
