"""
Logging utility untuk tracking download progress dan errors
"""
import logging
import sys
from pathlib import Path
from datetime import datetime
from colorama import Fore, Style, init

init(autoreset=True)

class ColoredFormatter(logging.Formatter):
    """Custom formatter dengan warna untuk console output"""
    
    COLORS = {
        logging.DEBUG: Fore.CYAN,
        logging.INFO: Fore.GREEN,
        logging.WARNING: Fore.YELLOW,
        logging.ERROR: Fore.RED,
        logging.CRITICAL: Fore.RED + Style.BRIGHT
    }
    
    def format(self, record):
        log_color = self.COLORS.get(record.levelno, Fore.WHITE)
        record.msg = f"{log_color}{record.msg}{Style.RESET_ALL}"
        return super().format(record)


class Logger:
    """Logger utility untuk aplikasi Music Downloader"""
    
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Logger, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if hasattr(self, '_initialized'):
            return
        
        self._initialized = True
        self.logger = logging.getLogger("MusicDownloader")
        self.logger.setLevel(logging.DEBUG)
        
        # File handler
        log_file = Path.home() / ".music_downloader" / "logs" / f"download_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        log_file.parent.mkdir(parents=True, exist_ok=True)
        
        file_handler = logging.FileHandler(log_file)
        file_handler.setLevel(logging.DEBUG)
        file_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        file_handler.setFormatter(file_formatter)
        
        # Console handler dengan warna
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = ColoredFormatter(
            '[%(levelname)s] %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
    
    def info(self, message: str):
        """Log info level"""
        self.logger.info(message)
    
    def debug(self, message: str):
        """Log debug level"""
        self.logger.debug(message)
    
    def warning(self, message: str):
        """Log warning level"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """Log error level"""
        self.logger.error(message)
    
    def critical(self, message: str):
        """Log critical level"""
        self.logger.critical(message)


# Global logger instance
logger = Logger()
