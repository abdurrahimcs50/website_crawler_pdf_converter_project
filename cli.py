import click
import asyncio
import unittest
from crawler.scheduler import start_scheduler, scheduled_crawl_sync
from crawler.web_crawler import WebCrawler
from crawler.report_generator import ReportGenerator
from utils import file_utils
from crawler.config import config
from utils.logging_utils import setup_logging
import logging

# Setup logger
logger = setup_logging(config.LOGS_DIR)

async def run_crawl():
    """Run the crawl process"""
    crawler = WebCrawler()
    stats = await crawler.run_crawl()
    stats_dict = stats.to_dict()  # Get the dictionary representation
    
    # Pass dictionary to report generators
    ReportGenerator.generate_html_report(stats_dict)
    ReportGenerator.generate_json_report(stats_dict)
@click.group()
def cli():
    """Website Crawler & PDF Converter CLI"""
    pass

@cli.command()
def crawl():
    """Run crawl once"""
    asyncio.run(run_crawl())

@cli.command()
@click.option('--hours', default=12, help='Schedule interval in hours')
def schedule(hours):
    """Start the scheduler"""
    start_scheduler(hours)

@cli.command()
def test():
    """Run tests"""
    # Simple test to verify basic functionality
    class TestCrawler(unittest.TestCase):
        def test_filename_generation(self):
            filename = file_utils.generate_filename("https://www.fdic.gov/risk-management-manual-examination-policies")
            self.assertTrue(filename.endswith('.pdf'))
            self.assertIn('example_com', filename)
        
        def test_checksum_calculation(self):
            checksum1 = file_utils.calculate_checksum(b"test content")
            checksum2 = file_utils.calculate_checksum(b"test content")
            self.assertEqual(checksum1, checksum2)
    
    unittest.main(argv=[''], exit=False)

if __name__ == "__main__":
    cli()