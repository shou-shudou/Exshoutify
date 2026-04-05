"""
Logger utility untuk aplikasi
"""
import logging
import sys
from pathlib import Path
from colorama import Fore, Style, init

# Initialize colorama
init(autoreset=True)

# Create logs directory
LOG_DIR = Path.home() / ".exshoutify" / "logs"
LOG_DIR.mkdir(parents=True, exist_ok=True)

# Configure logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# File handler
file_handler = logging.FileHandler(LOG_DIR / "exshoutify.log")
file_handler.setLevel(logging.DEBUG)

# Console handler dengan color
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)

# Formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
file_handler.setFormatter(formatter)

# Custom formatter untuk console dengan warna
class ColoredFormatter(logging.Formatter):
    COLORS = {
        'DEBUG': Fore.CYAN,
        'INFO': Fore.GREEN,
        'WARNING': Fore.YELLOW,
        'ERROR': Fore.RED,
        'CRITICAL': Fore.RED + Style.BRIGHT,
    }
    
    def format(self, record):
        log_color = self.COLORS.get(record.levelname, Fore.WHITE)
        record.levelname = f"{log_color}{record.levelname}{Style.RESET_ALL}"
        return super().format(record)

colored_formatter = ColoredFormatter(
    '[%(levelname)s] %(message)s'
)
console_handler.setFormatter(colored_formatter)

# Add handlers
logger.addHandler(file_handler)
logger.addHandler(console_handler)