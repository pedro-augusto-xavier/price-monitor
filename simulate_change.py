import sqlite3

conn = sqlite3.connect("prices.db")
conn.execute("UPDATE products SET price = 99.99 WHERE title = 'A Light in the Attic'")
conn.commit()
conn.close()
print("Preço alterado no banco.")