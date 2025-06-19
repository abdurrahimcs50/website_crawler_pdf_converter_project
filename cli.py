import click
import asyncio
from crawler.scheduler import start_scheduler
from crawler.web_crawler import WebCrawler
from crawler.report_generator import ReportGenerator
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
    return stats_dict

@click.group()
def cli():
    """Website Crawler & PDF Converter CLI"""
    pass

@cli.command()
def crawl():
    """Run crawl once"""
    asyncio.run(run_crawl())

@cli.command()
@click.option('--hours', default=12, type=int, help='Schedule interval in hours')
def schedule(hours):
    """Start the scheduler"""
    start_scheduler(hours)

if __name__ == "__main__":
    cli()