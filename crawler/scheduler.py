from apscheduler.schedulers.blocking import BlockingScheduler
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore
from apscheduler.executors.pool import ThreadPoolExecutor
import asyncio
import logging
from crawler.web_crawler import WebCrawler
from crawler.report_generator import ReportGenerator
from crawler.config import config

logger = logging.getLogger(__name__)

async def run_scheduled_crawl():
    """Function to run scheduled crawling"""
    try:
        crawler = WebCrawler()
        stats = await crawler.run_crawl()
        
        # Generate reports
        ReportGenerator.generate_html_report(stats)
        ReportGenerator.generate_json_report(stats)
        
        logger.info("Scheduled crawl completed successfully")
        
    except Exception as e:
        logger.error(f"Scheduled crawl failed: {e}")

def scheduled_crawl_sync():
    """Synchronous wrapper for scheduled crawl"""
    asyncio.run(run_scheduled_crawl())

def setup_scheduler():
    """Setup job scheduler"""
    jobstores = {
        'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
    }
    executors = {
        'default': ThreadPoolExecutor(20)
    }
    job_defaults = {
        'coalesce': False,
        'max_instances': 1
    }
    
    scheduler = BlockingScheduler(
        jobstores=jobstores,
        executors=executors,
        job_defaults=job_defaults
    )
    
    return scheduler

def start_scheduler(hours: int):
    """Start the scheduler with the specified interval"""
    config.SCHEDULE_HOURS = hours
    scheduler = setup_scheduler()
    
    # Add the crawl job
    scheduler.add_job(
        func=scheduled_crawl_sync,
        trigger="interval",
        hours=hours,
        id='crawl_job',
        name='Website Crawl Job',
        replace_existing=True
    )
    
    logger.info(f"Scheduler started - will run every {hours} hours")
    logger.info("Press Ctrl+C to exit")
    
    try:
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("Scheduler stopped")