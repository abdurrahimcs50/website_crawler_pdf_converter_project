# import ssl
# import certifi

# import asyncio
# import aiohttp
# import base64
# import logging
# from typing import Optional
# from selenium import webdriver
# from selenium.webdriver.chrome.options import Options
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.ui import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# import aiofiles
# from utils.file_utils import calculate_checksum, generate_filename
# from crawler.config import config

# logger = logging.getLogger(__name__)

# class PDFConverter:
#     """Handle PDF conversion and management"""
    
#     def __init__(self):
#         self.driver_options = self._setup_chrome_options()
#         self.driver = None
    
#     def _setup_chrome_options(self) -> Options:
#         """Setup Chrome options for headless browsing"""
#         options = Options()
#         options.add_argument('--headless')
#         options.add_argument('--no-sandbox')
#         options.add_argument('--disable-dev-shm-usage')
#         options.add_argument('--disable-gpu')
#         options.add_argument('--window-size=1920,1080')
#         options.add_argument('--disable-extensions')
#         options.add_argument('--disable-logging')
#         options.add_argument('--disable-web-security')
#         options.add_argument('--allow-running-insecure-content')
        
#         # PDF settings
#         options.add_experimental_option('useAutomationExtension', False)
#         options.add_experimental_option("excludeSwitches", ["enable-automation"])
        
#         return options
    
#     def _get_driver(self):
#         """Get or create a WebDriver instance"""
#         if self.driver is None:
#             try:
#                 self.driver = webdriver.Chrome(options=self.driver_options)
#                 logger.info("Chrome WebDriver initialized successfully")
#             except Exception as e:
#                 logger.error(f"Failed to initialize Chrome WebDriver: {e}")
#                 raise
#         return self.driver
    
#     async def convert_html_to_pdf(self, url: str, stats) -> Optional[str]:
#         """Convert HTML page to PDF"""
#         try:
#             driver = self._get_driver()
#             logger.info(f"Converting HTML to PDF: {url}")
            
#             driver.get(url)
            
#             # Wait for page to load
#             WebDriverWait(driver, config.TIMEOUT).until(
#                 EC.presence_of_element_located((By.TAG_NAME, "body"))
#             )
            
#             # Additional wait for dynamic content
#             await asyncio.sleep(3)
            
#             # Execute JavaScript to get PDF
#             pdf_data = driver.execute_cdp_cmd('Page.printToPDF', {
#                 'format': 'A4',
#                 'printBackground': True,
#                 'marginTop': 0.4,
#                 'marginBottom': 0.4,
#                 'marginLeft': 0.4,
#                 'marginRight': 0.4
#             })
            
#             # Decode base64 PDF data
#             pdf_bytes = base64.b64decode(pdf_data['data'])
            
#             # Check for duplicates
#             checksum = calculate_checksum(pdf_bytes)
#             if checksum in stats.pdf_checksums:
#                 logger.info(f"Duplicate PDF skipped: {url}")
#                 stats.duplicates_skipped += 1
#                 return None
            
#             stats.pdf_checksums.add(checksum)
            
#             # Save PDF
#             filename = generate_filename(url)
#             filepath = config.PDFS_DIR / filename
            
#             async with aiofiles.open(filepath, 'wb') as f:
#                 await f.write(pdf_bytes)
            
#             logger.info(f"PDF saved: {filepath}")
#             stats.pdfs_downloaded += 1
#             return str(filepath)
            
#         except Exception as e:
#             error_msg = f"Failed to convert HTML to PDF: {str(e)}"
#             logger.error(f"{error_msg} - URL: {url}")
#             stats.add_error(url, error_msg)
#             return None
    
#     # crawler/pdf_converter.py
#     async def download_pdf(self, url: str, session: aiohttp.ClientSession, stats) -> Optional[str]:
#         """Download existing PDF file"""
#         try:
#             logger.info(f"Downloading PDF: {url}")
            
#             # Create SSL context with certifi certificates
#             ssl_context = ssl.create_default_context(cafile=certifi.where())
            
#             async with session.get(url, ssl=ssl_context) as response:
#                 if response.status == 200:
#                     content = await response.read()
                    
#                     # Check for duplicates
#                     checksum = calculate_checksum(content)
#                     if checksum in stats.pdf_checksums:
#                         logger.info(f"Duplicate PDF skipped: {url}")
#                         stats.duplicates_skipped += 1
#                         return None
                    
#                     stats.pdf_checksums.add(checksum)
                    
#                     # Save PDF
#                     filename = generate_filename(url, is_pdf=True)
#                     filepath = config.PDFS_DIR / filename
                    
#                     async with aiofiles.open(filepath, 'wb') as f:
#                         await f.write(content)
                    
#                     logger.info(f"PDF downloaded: {filepath}")
#                     stats.pdfs_found += 1
#                     stats.pdfs_downloaded += 1
#                     return str(filepath)
#                 else:
#                     raise Exception(f"HTTP {response.status}")
                    
#         except Exception as e:
#             error_msg = f"Failed to download PDF: {str(e)}"
#             logger.error(f"{error_msg} - URL: {url}")
#             stats.add_error(url, error_msg)
#             return None
    
#     def cleanup(self):
#         """Cleanup WebDriver resources"""
#         if self.driver:
#             self.driver.quit()
#             self.driver = None


import asyncio
import aiohttp
import base64
import logging
from typing import Optional
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import aiofiles
import ssl
import certifi
from urllib.parse import urlparse
from utils.file_utils import calculate_checksum, generate_filename
from crawler.config import config

logger = logging.getLogger(__name__)

class PDFConverter:
    """Handle PDF conversion and management"""
    
    def __init__(self):
        self.driver_options = self._setup_chrome_options()
        self.driver = None
    
    def _setup_chrome_options(self) -> Options:
        """Setup Chrome options for headless browsing"""
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-gpu')
        options.add_argument('--window-size=1920,1080')
        options.add_argument('--disable-extensions')
        options.add_argument('--disable-logging')
        options.add_argument('--disable-web-security')
        options.add_argument('--allow-running-insecure-content')
        
        # PDF settings
        options.add_experimental_option('useAutomationExtension', False)
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        
        return options
    
    def _get_driver(self):
        """Get or create a WebDriver instance"""
        if self.driver is None:
            try:
                self.driver = webdriver.Chrome(options=self.driver_options)
                logger.info("Chrome WebDriver initialized successfully")
            except Exception as e:
                logger.error(f"Failed to initialize Chrome WebDriver: {e}")
                raise
        return self.driver
    
    async def convert_html_to_pdf(self, url: str, stats) -> Optional[str]:
        """Convert HTML page to PDF"""
        try:
            driver = self._get_driver()
            logger.info(f"Converting HTML to PDF: {url}")
            
            driver.get(url)
            
            # Wait for page to load
            WebDriverWait(driver, config.TIMEOUT).until(
                EC.presence_of_element_located((By.TAG_NAME, "body"))
            )
            
            # Additional wait for dynamic content
            await asyncio.sleep(3)
            
            # Execute JavaScript to get PDF
            pdf_data = driver.execute_cdp_cmd('Page.printToPDF', {
                'format': 'A4',
                'printBackground': True,
                'marginTop': 0.4,
                'marginBottom': 0.4,
                'marginLeft': 0.4,
                'marginRight': 0.4
            })
            
            # Decode base64 PDF data
            pdf_bytes = base64.b64decode(pdf_data['data'])
            
            # Check for duplicates
            checksum = calculate_checksum(pdf_bytes)
            if checksum in stats.pdf_checksums:
                logger.info(f"Duplicate PDF skipped: {url}")
                await stats.record_duplicate()
                return None
            
            stats.pdf_checksums.add(checksum)
            
            # Save PDF
            filename = generate_filename(url)
            filepath = config.PDFS_DIR / filename
            
            async with aiofiles.open(filepath, 'wb') as f:
                await f.write(pdf_bytes)
            
            logger.info(f"PDF saved: {filepath}")
            await stats.record_html_page()
            return str(filepath)
            
        except Exception as e:
            error_msg = f"Failed to convert HTML to PDF: {str(e)}"
            logger.error(f"{error_msg} - URL: {url}")
            await stats.add_error(url, error_msg)
            return None
    
    async def download_pdf(self, url: str, session: aiohttp.ClientSession, stats) -> Optional[str]:
        """Download existing PDF file"""
        try:
            logger.info(f"Downloading PDF: {url}")
            
            # Create SSL context with certifi certificates
            ssl_context = ssl.create_default_context(cafile=certifi.where())
            
            async with session.get(url, ssl=ssl_context) as response:
                if response.status == 200:
                    content = await response.read()
                    
                    # Check for duplicates
                    checksum = calculate_checksum(content)
                    if checksum in stats.pdf_checksums:
                        logger.info(f"Duplicate PDF skipped: {url}")
                        await stats.record_duplicate()
                        return None
                    
                    stats.pdf_checksums.add(checksum)
                    
                    # Save PDF
                    filename = generate_filename(url, is_pdf=True)
                    filepath = config.PDFS_DIR / filename
                    
                    async with aiofiles.open(filepath, 'wb') as f:
                        await f.write(content)
                    
                    logger.info(f"PDF downloaded: {filepath}")
                    await stats.record_pdf_found()
                    await stats.record_pdf_download()
                    return str(filepath)
                else:
                    raise Exception(f"HTTP {response.status}")
                    
        except Exception as e:
            error_msg = f"Failed to download PDF: {str(e)}"
            logger.error(f"{error_msg} - URL: {url}")
            await stats.add_error(url, error_msg)
            return None
    
    def cleanup(self):
        """Cleanup WebDriver resources"""
        if self.driver:
            self.driver.quit()
            self.driver = None