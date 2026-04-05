"""
Sanitizer utility untuk filename dan path
"""
import re
from pathlib import Path


def sanitize_filename(filename: str, max_length: int = 255) -> str:
    """
    Sanitize filename untuk semua OS
    
    Args:
        filename: Filename yang akan di-sanitize
        max_length: Maximum length untuk filename
    
    Returns:
        Sanitized filename
    """
    # Remove invalid characters
    invalid_chars = r'[<>:"/\\|?*\x00-\x1f]'
    filename = re.sub(invalid_chars, '', filename)
    
    # Replace multiple spaces dengan single space
    filename = re.sub(r'\s+', ' ', filename)
    
    # Remove leading/trailing spaces dan dots
    filename = filename.strip('. ')
    
    # Limit length
    if len(filename) > max_length:
        filename = filename[:max_length].rsplit(' ', 1)[0]
    
    # Ensure not empty
    if not filename:
        filename = 'untitled'
    
    return filename


def sanitize_path_part(path_part: str, max_length: int = 100) -> str:
    """
    Sanitize path part (folder name)
    
    Args:
        path_part: Path part yang akan di-sanitize
        max_length: Maximum length untuk folder name
    
    Returns:
        Sanitized path part
    """
    # Remove invalid characters
    invalid_chars = r'[<>:"/\\|?*\x00-\x1f]'
    path_part = re.sub(invalid_chars, '', path_part)
    
    # Replace multiple spaces
    path_part = re.sub(r'\s+', ' ', path_part)
    
    # Remove leading/trailing spaces dan dots
    path_part = path_part.strip('. ')
    
    # Limit length
    if len(path_part) > max_length:
        path_part = path_part[:max_length].rsplit(' ', 1)[0]
    
    # Ensure not empty
    if not path_part:
        path_part = 'unknown'
    
    return path_part


def sanitize_path(path_str: str) -> str:
    """
    Sanitize full path
    
    Args:
        path_str: Path yang akan di-sanitize
    
    Returns:
        Sanitized path
    """
    path = Path(path_str)
    parts = [sanitize_path_part(part) for part in path.parts]
    return str(Path(*parts))