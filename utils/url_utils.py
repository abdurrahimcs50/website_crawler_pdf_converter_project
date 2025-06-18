from urllib.parse import urlparse
from pathlib import Path

def is_valid_url(url: str, base_domain: str, excluded_keywords: list, allowed_extensions: set) -> bool:
    """Check if URL should be crawled"""
    try:
        parsed = urlparse(url)
        
        # Must be same domain
        if parsed.netloc != base_domain:
            return False
        
        # Check for excluded keywords
        url_lower = url.lower()
        for keyword in excluded_keywords:
            if keyword in url_lower:
                return False
        
        # Check file extension
        path = parsed.path.lower()
        if '.' in path:
            ext = Path(path).suffix
            if ext and ext not in allowed_extensions:
                return False
        
        return True
        
    except Exception:
        return False

def is_pdf_url(url: str) -> bool:
    """Check if URL points to a PDF file"""
    return url.lower().endswith('.pdf') or 'pdf' in url.lower()

def get_base_domain(url: str) -> str:
    """Extract base domain from URL"""
    return urlparse(url).netloc