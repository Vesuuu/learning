# Лаборатория — Глава 17 (мост к главе 18)
# Запуск: python lab_sql_17.py

import sqlite3

with sqlite3.connect(":memory:") as conn:
    cur = conn.cursor()
    cur.executescript("""
        CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT);
        CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER, total REAL);
    """)
    cur.execute("INSERT INTO users (name) VALUES (?)", ("Anna",))
    cur.execute("INSERT INTO orders (user_id, total) VALUES (?, ?)", (1, 120.0))
    conn.commit()

    cur.execute("""
        SELECT u.name, o.total
        FROM users u
        INNER JOIN orders o ON u.id = o.user_id
    """)
    print("JOIN:", cur.fetchall())

    cur.execute("SELECT COUNT(*) FROM users")
    print("COUNT:", cur.fetchone()[0])