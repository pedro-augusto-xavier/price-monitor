# Price Monitor

A Python web scraper that tracks product prices over time and detects price changes.

## Features
- Crawls all 50 catalogue pages of books.toscrape.com (1,000 products), following pagination automatically
- Stores products in SQLite and records every price change in a history table
- Detects and reports price increases and drops between runs
- Exports current prices to CSV
- Polite scraping: request delay, custom User-Agent and error handling

## Tech
Python, Requests, BeautifulSoup, SQLite

## How to run
pip install -r requirements.txt
python main.py

To test change detection, run `python simulate_change.py` and then `python main.py` again.