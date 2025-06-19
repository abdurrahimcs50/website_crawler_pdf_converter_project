import asyncio
import aiohttp
import ssl
import certifi
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import Set, List
import logging

from crawler.config import config
from crawler.crawl_stats import CrawlStats
from crawler.pdf_converter import PDFConverter
from utils.url_utils import is_valid_url, is_pdf_url, get_base_domain

logger = logging.getLogger(__name__)

class WebCrawler:
    """Main web crawler class with MAX_PAGES limit"""

    def __init__(self):
        self.pdf_converter = PDFConverter()

    async def get_page_links(self, url: str, session: aiohttp.ClientSession) -> List[str]:
        """Extract all links from a page"""
        try:
            async with session.get(url, ssl=ssl.create_default_context(cafile=certifi.where())) as response:
                if response.status != 200:
                    return []

                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')

                links = []
                for link in soup.find_all('a', href=True):
                    absolute_url = urljoin(url, link['href'])
                    links.append(absolute_url)
                    
                logger.info(f"Extracted {len(links)} links from {url}")
                return links

        except Exception as e:
            logger.error(f"Failed to extract links from {url}: {e}")
            return []

    async def crawl_url(self, url: str, base_domain: str, visited: Set[str], depth: int, session: aiohttp.ClientSession, stats: CrawlStats):
        """Crawl a single URL with MAX_PAGES limit"""
        # Termination checks
        if (depth > config.MAX_DEPTH or 
            url in visited or 
            await stats.has_reached_limit()):
            return
        
        visited.add(url)
        logger.info(f"Crawling (depth {depth}): {url}")

        try:
            # Check again before processing (might have changed in parallel)
            if await stats.has_reached_limit():
                logger.info("Page limit reached, skipping URL")
                return

            # Process URL
            if is_pdf_url(url):
                await self.pdf_converter.download_pdf(url, session, stats)
            else:
                await self.pdf_converter.convert_html_to_pdf(url, stats)

            # Check again after processing
            if await stats.has_reached_limit():
                logger.info("Page limit reached after processing URL")
                return

            # Only process links if we haven't reached limits
            if depth < config.MAX_DEPTH:
                links = await self.get_page_links(url, session)
                logger.info(f"Found {len(links)} links on {url}")
                
                for link in links:
                    # Exit immediately if limit reached
                    if await stats.has_reached_limit():
                        logger.info("MAX_PAGES limit reached, stopping link processing")
                        break
                    
                    if (link not in visited and 
                        is_valid_url(
                            link, 
                            base_domain, 
                            config.EXCLUDED_KEYWORDS, 
                            config.ALLOWED_EXTENSIONS
                        )):
                        await asyncio.sleep(config.DELAY_BETWEEN_REQUESTS)
                        await self.crawl_url(link, base_domain, visited, depth + 1, session, stats)

        except Exception as e:
            error_msg = f"Error crawling URL: {str(e)}"
            logger.error(f"{error_msg} - URL: {url}")
            await stats.add_error(url, error_msg)

    async def crawl_website(self, base_url: str, stats: CrawlStats):
        """Crawl an entire website"""
        base_domain = get_base_domain(base_url)
        visited = set()

        # Create SSL context with certifi certificates
        ssl_context = ssl.create_default_context(cafile=certifi.where())
        connector = aiohttp.TCPConnector(
            limit=config.MAX_CONCURRENT,
            ssl=ssl_context
        )
        timeout = aiohttp.ClientTimeout(total=config.TIMEOUT)

        async with aiohttp.ClientSession(connector=connector, timeout=timeout) as session:
            await self.crawl_url(base_url, base_domain, visited, 0, session, stats)

    async def run_crawl(self) -> CrawlStats:
        """Run the complete crawling process"""
        stats = CrawlStats(config.MAX_PAGES)
        logger.info("Starting crawl process...")

        try:
            # Process each base URL
            for base_url in config.BASE_URLS:
                if await stats.has_reached_limit():
                    logger.info("Page limit reached before processing base URL")
                    break
                    
                logger.info(f"Processing base URL: {base_url}")
                await self.crawl_website(base_url, stats)

        except Exception as e:
            logger.error(f"Critical error during crawl: {e}")
            await stats.add_error("SYSTEM", str(e))

        finally:
            self.pdf_converter.cleanup()

        logger.info("Crawl process completed")
        return stats