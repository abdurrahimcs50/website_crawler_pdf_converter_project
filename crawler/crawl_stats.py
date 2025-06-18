# from datetime import datetime
# from typing import Dict, Set

# class CrawlStats:
#     """Statistics tracking for crawl operations"""
    
#     def __init__(self):
#         self.start_time = datetime.now()
#         self.pages_crawled = 0
#         self.pdfs_found = 0
#         self.pdfs_downloaded = 0
#         self.errors = []
#         self.duplicates_skipped = 0
#         self.visited_urls: Set[str] = set()
#         self.pdf_checksums: Set[str] = set()
    
#     def add_error(self, url: str, error: str):
#         """Add an error to the statistics"""
#         self.errors.append({
#             'url': url,
#             'error': error,
#             'timestamp': datetime.now().isoformat()
#         })
    
#     def to_dict(self) -> Dict:
#         """Convert stats to dictionary for reporting"""
#         return {
#             'start_time': self.start_time.isoformat(),
#             'end_time': datetime.now().isoformat(),
#             'duration_minutes': (datetime.now() - self.start_time).total_seconds() / 60,
#             'pages_crawled': self.pages_crawled,
#             'pdfs_found': self.pdfs_found,
#             'pdfs_downloaded': self.pdfs_downloaded,
#             'duplicates_skipped': self.duplicates_skipped,
#             'errors_count': len(self.errors),
#             'errors': self.errors
#         }

import asyncio
from datetime import datetime
from typing import Dict, Set, List

class CrawlStats:
    """Statistics tracking for crawl operations with MAX_PAGES limit"""
    
    def __init__(self, max_pages: int):
        self.start_time = datetime.now()
        self.max_pages = max_pages
        self.pages_crawled = 0
        self.pdfs_found = 0
        self.pdfs_downloaded = 0
        self.errors: List[dict] = []
        self.duplicates_skipped = 0
        self.visited_urls: Set[str] = set()
        self.pdf_checksums: Set[str] = set()
        self.lock = asyncio.Lock()
    
    async def record_html_page(self):
        """Record a successfully converted HTML page"""
        async with self.lock:
            self.pages_crawled += 1
    
    async def record_pdf_download(self):
        """Record a successfully downloaded PDF"""
        async with self.lock:
            self.pdfs_downloaded += 1
    
    async def record_pdf_found(self):
        """Record a PDF found (will be downloaded)"""
        async with self.lock:
            self.pdfs_found += 1
    
    async def record_duplicate(self):
        """Record a duplicate PDF skipped"""
        async with self.lock:
            self.duplicates_skipped += 1
    
    async def total_processed(self) -> int:
        """Get total processed pages (HTML conversions + PDF downloads)"""
        async with self.lock:
            return self.pages_crawled + self.pdfs_downloaded
    
    async def has_reached_limit(self) -> bool:
        """Check if MAX_PAGES limit has been reached"""
        async with self.lock:
            return (self.pages_crawled + self.pdfs_downloaded) >= self.max_pages
    
    async def add_error(self, url: str, error: str):
        """Add an error to the statistics"""
        async with self.lock:
            self.errors.append({
                'url': url,
                'error': error,
                'timestamp': datetime.now().isoformat()
            })
    
    def to_dict(self) -> Dict:
        """Convert stats to dictionary for reporting"""
        return {
            'start_time': self.start_time.isoformat(),
            'end_time': datetime.now().isoformat(),
            'duration_minutes': (datetime.now() - self.start_time).total_seconds() / 60,
            'pages_crawled': self.pages_crawled,
            'pdfs_found': self.pdfs_found,
            'pdfs_downloaded': self.pdfs_downloaded,
            'duplicates_skipped': self.duplicates_skipped,
            'errors_count': len(self.errors),
            'errors': self.errors
        }