#!/usr/bin/env python3
"""
Website Crawler & PDF Converter
Main entry point for the application
"""

# from crawler.config import config
from crawler.config import config
from utils.logging_utils import setup_logging
import logging

# Setup logger
logger = setup_logging(config.LOGS_DIR)

if __name__ == "__main__":
    from cli import cli
    cli()