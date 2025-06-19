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
        stats_dict = stats.to_dict()  # Convert to dictionary
        
        # Generate reports
        ReportGenerator.generate_html_report(stats_dict)
        ReportGenerator.generate_json_report(stats_dict)
        
        logger.info("Scheduled crawl completed successfully")
        return stats_dict
        
    except Exception as e:
        logger.exception(f"Scheduled crawl failed: {e}")
        raise

def scheduled_crawl_sync():
    """Synchronous wrapper for scheduled crawl"""
    # Create new event loop for each run
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(run_scheduled_crawl())
    finally:
        loop.close()

def setup_scheduler():
    """Setup job scheduler"""
    jobstores = {
        'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
    }
    executors = {
        'default': ThreadPoolExecutor(5)  # Reduced thread count
    }
    job_defaults = {
        'coalesce': True,  # Combine missed runs
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
    try:
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
        
        scheduler.start()
    except KeyboardInterrupt:
        logger.info("Scheduler stopped by user")
    except Exception as e:
        logger.exception(f"Failed to start scheduler: {e}")
        raise