import os
from pathlib import Path
from utils.file_utils import create_directories
from decouple import config, Csv
import logging

logger = logging.getLogger(__name__)

class Config:
    """Configuration class for the crawler"""
    
    def __init__(self):
        # Load and validate BASE_URLS
        base_urls = config('BASE_URLS', default='', cast=Csv())
        if not base_urls:
            logger.error("No BASE_URLS provided in the environment variables.")
            raise ValueError("BASE_URLS must be set in the environment variables.")
        
        self.BASE_URLS = [url.strip() for url in base_urls]
        logger.info(f"Loaded BASE_URLS: {self.BASE_URLS}")
        
        # Crawler settings
        self.MAX_DEPTH = config('MAX_DEPTH', default=3, cast=int)
        self.MAX_PAGES = config('MAX_PAGES', default=100, cast=int)
        self.DELAY_BETWEEN_REQUESTS = config('DELAY_BETWEEN_REQUESTS', default=1.0, cast=float)
        self.TIMEOUT = config('TIMEOUT', default=30, cast=int)
        self.MAX_CONCURRENT = config('MAX_CONCURRENT', default=5, cast=int)
        
        # Output settings
        self.OUTPUT_DIR = Path(config('OUTPUT_DIR', default='crawler_output')).resolve()
        self.LOGS_DIR = self.OUTPUT_DIR / 'logs'
        self.PDFS_DIR = self.OUTPUT_DIR / 'pdfs'
        self.REPORTS_DIR = self.OUTPUT_DIR / 'reports'
        
        # Schedule settings
        self.SCHEDULE_HOURS = config('SCHEDULE_HOURS', default=12, cast=int)
        
        # Filtering settings
        self.EXCLUDED_KEYWORDS = [
            'logout', 'admin', 'login', 'signin', 'signout',
            'password', 'register', 'signup', 'auth'
        ]
        
        self.ALLOWED_EXTENSIONS = {'.pdf', '.html', '.htm', '.aspx', '.php'}
        
        # Create directories
        directories = [self.OUTPUT_DIR, self.LOGS_DIR, self.PDFS_DIR, self.REPORTS_DIR]
        create_directories(directories)
        
        # Log configuration
        logger.info(f"Configuration loaded: "
                   f"MAX_DEPTH={self.MAX_DEPTH}, "
                   f"MAX_PAGES={self.MAX_PAGES}, "
                   f"DELAY={self.DELAY_BETWEEN_REQUESTS}s, "
                   f"TIMEOUT={self.TIMEOUT}s, "
                   f"CONCURRENT={self.MAX_CONCURRENT}, "
                   f"OUTPUT_DIR={self.OUTPUT_DIR}")

# Create config instance
config = Config()