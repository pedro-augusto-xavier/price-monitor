import csv
import sqlite3
from datetime import datetime

DB_PATH = "prices.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS products (
            url TEXT PRIMARY KEY,
            title TEXT NOT NULL,
            price REAL NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS price_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT NOT NULL,
            old_price REAL,
            new_price REAL NOT NULL,
            changed_at TEXT NOT NULL
        )
    """)
    return conn


def save_books(conn, books):
    now = datetime.now().isoformat(timespec="seconds")
    changes = []
    for book in books:
        row = conn.execute(
            "SELECT price FROM products WHERE url = ?", (book["url"],)
        ).fetchone()
        if row is None:
            conn.execute(
                "INSERT INTO products (url, title, price, updated_at) VALUES (?, ?, ?, ?)",
                (book["url"], book["title"], book["price"], now),
            )
        elif row[0] != book["price"]:
            conn.execute(
                "UPDATE products SET price = ?, updated_at = ? WHERE url = ?",
                (book["price"], now, book["url"]),
            )
            conn.execute(
                "INSERT INTO price_history (url, old_price, new_price, changed_at) VALUES (?, ?, ?, ?)",
                (book["url"], row[0], book["price"], now),
            )
            changes.append({**book, "old_price": row[0]})
    conn.commit()
    return changes
def export_csv(conn, path="prices.csv"):
    rows = conn.execute(
        "SELECT title, price, url, updated_at FROM products ORDER BY title"
    ).fetchall()
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["title", "price", "url", "updated_at"])
        writer.writerows(rows)
    return len(rows)