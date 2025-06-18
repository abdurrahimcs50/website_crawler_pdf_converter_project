import logging
from datetime import datetime
from pathlib import Path

def setup_logging(logs_dir: Path) -> logging.Logger:
    """Setup logging configuration"""
    log_filename = logs_dir / f"crawler_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_filename),
            logging.StreamHandler()
        ]
    )
    
    return logging.getLogger(__name__)