```markdown
# Website Crawler & PDF Converter

> Automated web crawler that converts HTML pages to PDFs and downloads existing PDFs with scheduling, smart filtering, and detailed reporting.

This robust solution crawls websites recursively, converts HTML content to PDF, downloads existing PDFs, detects duplicates, and generates comprehensive reports. Ideal for web archiving, compliance documentation, and content preservation.

## 🚀 Features

- **Smart Web Crawling**: Configurable depth and page limits
- **PDF Conversion**: HTML → PDF using headless Chrome
- **PDF Downloading**: Direct PDF retrieval with duplicate detection
- **Scheduled Execution**: Automatic periodic crawling
- **Detailed Reporting**: HTML + JSON reports with statistics
- **Error Tracking**: Comprehensive error logging
- **Smart Filtering**: URL validation and exclusion rules

## ⚙️ Installation

1. Clone the repository:
```bash
git clone https://github.com/abdurrahimcs50/website_crawler_pdf_converter_project.git
cd website_crawler_pdf_converter_project
```

2. Create virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# .\.venv\Scripts\activate  # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment:
```bash
cp .env.example .env
```

## ⚡ Configuration

Edit `.env` file:
```ini
BASE_URLS="https://example.com"
MAX_DEPTH=3
MAX_PAGES=100
DELAY_BETWEEN_REQUESTS=1.0
MAX_CONCURRENT=5
OUTPUT_DIR="crawler_output"
SCHEDULE_HOURS=12
```

## 🛠️ Usage

```bash
# Single crawl
python app.py crawl

# Scheduled crawls (every 6 hours)
python app.py schedule --hours=6

# Run tests
python app.py test
```

## 📊 Sample Report
![Report Preview](https://via.placeholder.com/800x400?text=Crawl+Report+Example)

```json
{
  "start_time": "2025-06-18T20:36:30.237455",
  "end_time": "2025-06-18T20:37:10.394819",
  "duration_minutes": 0.67,
  "pages_crawled": 5,
  "pdfs_found": 3,
  "pdfs_downloaded": 3,
  "duplicates_skipped": 2,
  "errors_count": 0
}
```

## 📂 Project Structure
```
website_crawler_pdf_converter_project/
├── crawler/               # Core functionality
│   ├── config.py          # Configuration loader
│   ├── crawl_stats.py     # Statistics tracker
│   ├── pdf_converter.py   # PDF processor
│   ├── report_generator.py# Report creator
│   ├── scheduler.py       # Job scheduler
│   └── web_crawler.py     # Crawler logic
├── utils/                 # Helpers
│   ├── file_utils.py      # File operations
│   ├── logging_utils.py   # Log setup
│   └── url_utils.py       # URL handlers
├── .env.example           # Config template
├── requirements.txt       # Dependencies
├── app.py                 # Main entry point
└── LICENSE
```

## 🤝 Contributing
Contributions welcome! Please follow these steps:
1. Fork the repository
2. Create your feature branch (`git checkout -b feature/your-feature`)
3. Commit changes (`git commit -am 'Add feature'`)
4. Push to branch (`git push origin feature/your-feature`)
5. Open a pull request

## 📄 License
Distributed under the MIT License - see [LICENSE](LICENSE) for details.