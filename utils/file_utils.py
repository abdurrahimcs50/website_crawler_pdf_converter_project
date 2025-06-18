import hashlib
from pathlib import Path
from urllib.parse import urlparse
from datetime import datetime

def create_directories(directories: list):
    """Create necessary directories"""
    for directory in directories:
        directory.mkdir(parents=True, exist_ok=True)

def generate_filename(url: str, is_pdf: bool = False) -> str:
    """Generate a standardized filename for saved content"""
    parsed = urlparse(url)
    domain = parsed.netloc.replace('www.', '').replace('.', '_')
    
    # Create a clean path representation
    path = parsed.path.strip('/').replace('/', '_').replace('\\', '_')
    if parsed.query:
        # Include important query parameters
        query_hash = hashlib.md5(parsed.query.encode()).hexdigest()[:8]
        path += f"_q{query_hash}"
    
    # Limit filename length
    if len(path) > 100:
        path = path[:100] + hashlib.md5(path.encode()).hexdigest()[:8]
    
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    extension = '.pdf'
    
    return f"{domain}_{path}_{timestamp}{extension}"

def calculate_checksum(content: bytes) -> str:
    """Calculate MD5 checksum of content"""
    return hashlib.md5(content).hexdigest()