import time
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

START_URL = "https://books.toscrape.com/catalogue/page-1.html"
HEADERS = {"User-Agent": "price-monitor/1.0 (portfolio project)"}


def parse_page(html, page_url):
    soup = BeautifulSoup(html, "html.parser")
    books = []
    for card in soup.select("article.product_pod"):
        link = card.h3.a
        books.append({
            "title": link["title"],
            "price": float(card.select_one(".price_color").text.replace("£", "")),
            "url": urljoin(page_url, link["href"]),
        })
    next_link = soup.select_one("li.next a")
    next_url = urljoin(page_url, next_link["href"]) if next_link else None
    return books, next_url


def scrape_all():
    url = START_URL
    all_books = []
    while url:
        response = requests.get(url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        response.encoding = "utf-8"
        books, url = parse_page(response.text, response.url)
        all_books.extend(books)
        print(f"{len(all_books)} livros coletados...")
        time.sleep(0.5)
    return all_books


if __name__ == "__main__":
    books = scrape_all()
    print(f"Total: {len(books)} livros")
    print(books[0])