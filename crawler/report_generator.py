import json
from datetime import datetime
from pathlib import Path
from crawler.config import config
import logging

logger = logging.getLogger(__name__)

class ReportGenerator:
    """Generate reports for crawl operations"""
    
    @staticmethod
    def generate_html_report(stats_dict) -> str:
        """Generate HTML report from stats dictionary"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = config.REPORTS_DIR / f"crawl_report_{timestamp}.html"
        
        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>Crawl Report - {timestamp}</title>
            <style>
                body {{ font-family: Arial, sans-serif; margin: 20px; }}
                .header {{ background-color: #f0f0f0; padding: 20px; border-radius: 5px; }}
                .stats {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 20px 0; }}
                .stat-box {{ background-color: #e7f3ff; padding: 15px; border-radius: 5px; text-align: center; }}
                .errors {{ background-color: #ffe7e7; padding: 15px; border-radius: 5px; margin: 20px 0; }}
                .error-item {{ margin: 10px 0; padding: 10px; background-color: white; border-radius: 3px; }}
            </style>
        </head>
        <body>
            <div class="header">
                <h1>Website Crawler Report</h1>
                <p>Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
                <p>Duration: {stats_dict['duration_minutes']:.2f} minutes</p>
            </div>
            
            <div class="stats">
                <div class="stat-box">
                    <h3>{stats_dict['pages_crawled']}</h3>
                    <p>Pages Crawled</p>
                </div>
                <div class="stat-box">
                    <h3>{stats_dict['pdfs_found']}</h3>
                    <p>PDFs Found</p>
                </div>
                <div class="stat-box">
                    <h3>{stats_dict['pdfs_downloaded']}</h3>
                    <p>PDFs Downloaded</p>
                </div>
                <div class="stat-box">
                    <h3>{stats_dict['duplicates_skipped']}</h3>
                    <p>Duplicates Skipped</p>
                </div>
                <div class="stat-box">
                    <h3>{stats_dict['errors_count']}</h3>
                    <p>Errors</p>
                </div>
            </div>
            
            {"<div class='errors'><h2>Errors</h2>" + 
             "".join([
                 f"<div class='error-item'><strong>URL:</strong> {error['url']}<br>"
                 f"<strong>Error:</strong> {error['error']}<br>"
                 f"<strong>Time:</strong> {error['timestamp']}</div>" 
                 for error in stats_dict['errors']
             ]) + "</div>" 
             if stats_dict['errors'] else ""}
        </body>
        </html>
        """
        
        with open(report_file, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        logger.info(f"HTML report generated: {report_file}")
        return str(report_file)
    
    @staticmethod
    def generate_json_report(stats_dict) -> str:
        """Generate JSON report from stats dictionary"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        report_file = config.REPORTS_DIR / f"crawl_report_{timestamp}.json"
        
        with open(report_file, 'w', encoding='utf-8') as f:
            json.dump(stats_dict, f, indent=2, default=str)
        
        logger.info(f"JSON report generated: {report_file}")
        return str(report_file)