from database import get_connection, save_books, export_csv
from scraper import scrape_all


def main():
    books = scrape_all()
    conn = get_connection()
    changes = save_books(conn, books)
    total = export_csv(conn)
    print(f"{total} produtos exportados para prices.csv")
    conn.close()

    print(f"\n{len(books)} livros verificados.")
    if not changes:
        print("Nenhuma mudança de preço.")
    for c in changes:
        direction = "caiu" if c["price"] < c["old_price"] else "subiu"
        print(f"{c['title']}: £{c['old_price']:.2f} -> £{c['price']:.2f} ({direction})")


if __name__ == "__main__":
    main()