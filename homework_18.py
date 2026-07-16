# Домашнее задание — Глава 18
# SQLite из Python
#
# Используй sqlite3.connect(":memory:")
# Задания текстом — в файле chapter-18-sqlite-python-orm.md
# Запуск: python homework_18.py


# ========== ЗАДАЧА 1. Таблица books + INSERT ==========
# SELECT *  →  [(1, 'Python Basics', 2024), (2, 'SQL Guide', 2023)]



# ========== ЗАДАЧА 2. WHERE year >= 2024 ==========
#  →  [(1, 'Python Basics', 2024)]



# ========== ЗАДАЧА 3. count_rows(conn, table_name) ==========
# count_rows на books  →  2



# ========== ЗАДАЧА 4. UPDATE Old Book ==========
#  →  ('Old Book', 2015)



# ========== ЗАДАЧА 5. JOIN authors + books2 ==========
#  →  [('Tolstoy', 'War and Peace')]



# ========== ЗАДАЧА 6. init_db, add_reader, list_readers ==========
# list_readers  →  ['Anna', 'Bob']
# См. задание 6 в главе