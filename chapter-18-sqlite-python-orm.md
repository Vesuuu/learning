# Тема: SQLite и Python — работа с базой из кода

> **Формат:** сначала объяснение простыми словами, потом пример с разбором.  
> Не надо зубрить всё сразу — **3 части теории + 12 примеров + 6 задач**.

---

## Цель главы

После прочтения ты понимаешь:

1. **sqlite3** — как подключиться к БД, выполнить SQL и прочитать результат.
2. **Безопасные запросы** — параметры вместо склейки строк (защита от SQL injection).
3. **ORM (обзор)** — зачем SQLAlchemy и как выглядит код без ручного SQL.

Глава 17 дала язык SQL. Здесь — **применяем его из Python**.

---

# ЧАСТЬ 1. SQLite и модуль sqlite3

## 1.1. Что такое SQLite

**SQLite** — встраиваемая база данных:
- один **файл** на диске (например `shop.db`),
- не нужен отдельный сервер (в отличие от PostgreSQL),
- встроена в Python через модуль **`sqlite3`**.

Идеально для:
- обучения,
- прототипов,
- небольших приложений,
- локального кэша данных.

---

## 1.2. Аналогия

PostgreSQL — как ресторан с официантами: отдельное здание, много посетителей.  
SQLite — как блокнот в кармане: открыл, записал, закрыл. Для Junior-проектов блокнота часто хватает.

---

## 1.3. Подключение и курсор

```python
import sqlite3

conn = sqlite3.connect("shop.db")   # файл создастся, если нет
cursor = conn.cursor()

cursor.execute("SELECT 1")
print(cursor.fetchone())            # (1,)

conn.close()
```

- **`connect`** — соединение с БД (файл или `":memory:"` для RAM).
- **`cursor`** — объект, через который отправляем SQL.
- **`execute`** — выполнить один запрос.
- **`fetchone` / `fetchall`** — забрать результат SELECT.

---

## 1.4. Контекстный менеджер — правильное закрытие

```python
import sqlite3

with sqlite3.connect("shop.db") as conn:
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT)")
    conn.commit()
```

`with` закроет соединение автоматически.  
**`commit()`** — сохранить изменения (INSERT/UPDATE/DELETE). Без commit данные могут не записаться.

---

## 1.5. CREATE и INSERT из Python

```python
import sqlite3

with sqlite3.connect(":memory:") as conn:
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL
        )
    """)
    cur.execute("INSERT INTO users (name) VALUES (?)", ("Anna",))
    cur.execute("INSERT INTO users (name) VALUES (?)", ("Bob",))
    conn.commit()

    cur.execute("SELECT id, name FROM users")
    print(cur.fetchall())
```

**Вывод:** `[(1, 'Anna'), (2, 'Bob')]`

`?` — **плейсхолдер** для параметра. Значение передаётся отдельным кортежем.

---

### ✅ Проверь себя — часть 1

1. Файл БД SQLite — это что? → **Один файл на диске**.
2. Зачем `commit()`? → **Сохранить изменения в БД**.
3. `fetchall()` после SELECT? → **Список всех строк результата**.

---

# ЧАСТЬ 2. Безопасность и практика CRUD

## 2.1. SQL injection — почему нельзя склеивать строки

**Плохо:**

```python
name = user_input
cursor.execute(f"SELECT * FROM users WHERE name = '{name}'")
```

Если `user_input = "'; DROP TABLE users; --"`, злоумышленник может испортить БД.

**Хорошо — параметризованный запрос:**

```python
cursor.execute("SELECT * FROM users WHERE name = ?", (name,))
```

БД сама экранирует значение. **Всегда** используй `?` и кортеж параметров в sqlite3.

---

## 2.2. SELECT с параметрами

```python
cursor.execute("SELECT id, name FROM users WHERE id = ?", (user_id,))
row = cursor.fetchone()
```

`fetchone()` — одна строка или `None`.  
`fetchall()` — список кортежей.

---

## 2.3. row_factory — словари вместо кортежей

```python
conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()
# ...
row = cursor.fetchone()
print(row["name"])   # доступ по имени столбца
```

Удобнее для чтения кода.

---

## 2.4. UPDATE и DELETE

```python
cursor.execute("UPDATE users SET name = ? WHERE id = ?", ("Anna K.", 1))
cursor.execute("DELETE FROM users WHERE id = ?", (2,))
conn.commit()
```

Проверяй `cursor.rowcount` — сколько строк затронуто.

---

## 2.5. Транзакции и откат

```python
try:
    cursor.execute("INSERT INTO accounts (balance) VALUES (?)", (100,))
    cursor.execute("INSERT INTO accounts (balance) VALUES (?)", (-200,))  # ошибка бизнес-логики
    conn.commit()
except Exception:
    conn.rollback()
    raise
```

**rollback()** — отменить незакершённую транзакцию. Важно для переводов денег: либо оба шага, либо ни одного.

---

## 2.6. executemany — много вставок

```python
users = [("Anna",), ("Bob",), ("Vika",)]
cursor.executemany("INSERT INTO users (name) VALUES (?)", users)
conn.commit()
```

Быстрее, чем execute в цикле.

---

### ✅ Проверь себя — часть 2

1. f-string в SQL с пользовательским вводом? → **Опасно (SQL injection)**.
2. Плейсхолдер в sqlite3? → **`?` и кортеж параметров**.
3. `rollback()` когда? → **При ошибке, чтобы отменить незавершённые изменения**.

---

# ЧАСТЬ 3. Связка SQLite + Flask (мост к гл. 19)

## 3.1. Один файл — БД и простой API

После этой главы ты умеешь хранить данные. В **главе 19** отдашь их в JSON. Промежуточный шаг:

```python
import sqlite3
from flask import Flask, jsonify

app = Flask(__name__)

def get_books():
    with sqlite3.connect("books.db") as conn:
        conn.row_factory = sqlite3.Row
        rows = conn.execute("SELECT id, title FROM books").fetchall()
        return [dict(r) for r in rows]

@app.route("/api/books")
def api_books():
    return jsonify(get_books())
```

**Разбор:** `database.py` + `app.py` в гл. 21 — та же идея, только больше таблиц и тестов.  
Сначала освой **sqlite3** из частей 1–2; Flask — в следующей главе.

---

### ✅ Проверь себя — часть 3

1. Где жить SQL на первом проходе? → **В `sqlite3`, не в ORM**.
2. Зачем мост к Flask? → **Снять скачок 18 → 19**.

---

# БОНУС. ORM (SQLAlchemy) — можно пропустить на Junior

> **На первом проходе** достаточно частей 1–2 и моста выше. ORM — «как делают в больших проектах», вернёшься позже.

## БОНУС 1. Проблема ручного SQL

Много таблиц, связей, CRUD — код на чистом SQL разрастается:
- дублирование запросов,
- сложно менять схему,
- легко ошибиться в JOIN.

**ORM** (Object-Relational Mapping) — библиотека, которая связывает **классы Python** с **таблицами БД**.

---

## БОНУС 2. SQLAlchemy — стандарт для Python

```python
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    name = Column(String)

engine = create_engine("sqlite:///shop.db")
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
```

Класс `User` = таблица `users`. Поля класса = столбцы.

---

## БОНУС 3. CRUD через ORM (идея)

```python
session = Session()

# Create
u = User(name="Anna")
session.add(u)
session.commit()

# Read
users = session.query(User).filter(User.name == "Anna").all()

# Update
u.name = "Anna K."
session.commit()

# Delete
session.delete(u)
session.commit()
session.close()
```

На Junior: **умей sqlite3 вручную** + **понимай, что ORM делает то же самое**, но через объекты.

---

## БОНУС 4. Когда sqlite3, когда ORM

| Ситуация | Выбор |
|----------|-------|
| Учеба, скрипт, 1–2 таблицы | `sqlite3` |
| Flask/FastAPI проект, много моделей | SQLAlchemy |
| Сложная аналитика, отчёты | Часто чистый SQL |
| Миграции схемы | Alembic (с SQLAlchemy) |

---

## БОНУС 5. Установка SQLAlchemy (когда понадобится)

```bash
pip install sqlalchemy
```

В примерах ниже основной фокус — **sqlite3** (встроен, запускается сразу). ORM — обзор для картины.

---

### ✅ Проверь себя — бонус ORM

1. ORM связывает что с чем? → **Классы Python ↔ таблицы БД**.
2. ORM обязателен на Junior? → **Нет**, сначала sqlite3.
3. ORM заменяет SQL? → **Нет**.

---

# Практика — 12 примеров с разбором

Все примеры можно запустить: `python chapter_18_examples.py` или копировать в REPL.  
Используем `":memory:"` — БД в оперативной памяти, файл не нужен.

---

## Пример 1. Подключение и простой SELECT

```python
import sqlite3

with sqlite3.connect(":memory:") as conn:
    cur = conn.cursor()
    cur.execute("SELECT 10 + 5 AS result")
    print(cur.fetchone())
```

**Вывод:** `(15,)`

**Разбор:** SQLite умеет считать выражения без таблицы. `fetchone()` — одна строка, один столбец.

---

## Пример 2. CREATE TABLE + INSERT

```python
import sqlite3

with sqlite3.connect(":memory:") as conn:
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            price REAL
        )
    """)
    cur.execute("INSERT INTO products (name, price) VALUES (?, ?)", ("Laptop", 1200.0))
    cur.execute("INSERT INTO products (name, price) VALUES (?, ?)", ("Mouse", 25.5))
    conn.commit()

    cur.execute("SELECT name, price FROM products")
    print(cur.fetchall())
```

**Вывод:** `[('Laptop', 1200.0), ('Mouse', 25.5)]`

**Разбор:** `AUTOINCREMENT` сам нумерует `id`. Параметры `(?, ?)` — безопасная вставка.

---

## Пример 3. SELECT с WHERE

```python
import sqlite3

with sqlite3.connect(":memory:") as conn:
    cur = conn.cursor()
    cur.execute("CREATE TABLE products (id INTEGER PRIMARY KEY, name TEXT, price REAL)")
    for row in [("A", 100), ("B", 500), ("C", 1500)]:
        cur.execute("INSERT INTO products (name, price) VALUES (?, ?)", row)
    conn.commit()

    cur.execute("SELECT name, price FROM products WHERE price > ?", (1000,))
    print(cur.fetchall())
```

**Вывод:** `[('C', 1500)]`

**Разбор:** `1000` передано как параметр `(1000,)`. Условие из главы 17 — здесь из Python.

---

## Пример 4. fetchone и проверка «не найдено»

```python
import sqlite3

with sqlite3.connect(":memory:") as conn:
    cur = conn.cursor()
    cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
    cur.execute("INSERT INTO users (name) VALUES (?)", ("Anna",))
    conn.commit()

    cur.execute("SELECT name FROM users WHERE id = ?", (1,))
    print(cur.fetchone())

    cur.execute("SELECT name FROM users WHERE id = ?", (99,))
    print(cur.fetchone())
```

**Вывод:**
```
('Anna',)
None
```

**Разбор:** id=1 есть → кортеж. id=99 нет → `None`. В коде проверяй `if row is None`.

---

## Пример 5. row_factory = Row

```python
import sqlite3

conn = sqlite3.connect(":memory:")
conn.row_factory = sqlite3.Row
cur = conn.cursor()
cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
cur.execute("INSERT INTO users (name) VALUES (?)", ("Bob",))
conn.commit()

cur.execute("SELECT * FROM users WHERE id = 1")
row = cur.fetchone()
print(row["name"])
conn.close()
```

**Вывод:** `Bob`

**Разбор:** `row["name"]` читабельнее, чем `row[1]`. Удобно в API и шаблонах.

---

## Пример 6. executemany — пакетная вставка

```python
import sqlite3

with sqlite3.connect(":memory:") as conn:
    cur = conn.cursor()
    cur.execute("CREATE TABLE cities (name TEXT)")
    data = [("Moscow",), ("Kazan",), ("Sochi",)]
    cur.executemany("INSERT INTO cities (name) VALUES (?)", data)
    conn.commit()

    cur.execute("SELECT COUNT(*) FROM cities")
    print(cur.fetchone()[0])
```

**Вывод:** `3`

**Разбор:** три кортежа вставлены одним вызовом. `fetchone()[0]` — число из COUNT.

---

## Пример 7. UPDATE и rowcount

```python
import sqlite3

with sqlite3.connect(":memory:") as conn:
    cur = conn.cursor()
    cur.execute("CREATE TABLE items (id INTEGER PRIMARY KEY, price REAL)")
    cur.execute("INSERT INTO items (price) VALUES (?)", (100,))
    cur.execute("INSERT INTO items (price) VALUES (?)", (200,))
    conn.commit()

    cur.execute("UPDATE items SET price = price * 1.1 WHERE id = ?", (1,))
    conn.commit()
    print("updated rows:", cur.rowcount)

    cur.execute("SELECT price FROM items WHERE id = 1")
    print(cur.fetchone())
```

**Вывод:**
```
updated rows: 1
(110.0,)
```

**Разбор:** цена 100 выросла на 10% → 110. `rowcount` — одна строка обновлена.

---

## Пример 8. DELETE с WHERE

```python
import sqlite3

with sqlite3.connect(":memory:") as conn:
    cur = conn.cursor()
    cur.execute("CREATE TABLE logs (id INTEGER PRIMARY KEY, msg TEXT)")
    cur.executemany("INSERT INTO logs (msg) VALUES (?)", [("a",), ("b",), ("c",)])
    conn.commit()

    cur.execute("DELETE FROM logs WHERE id = ?", (2,))
    conn.commit()

    cur.execute("SELECT id, msg FROM logs")
    print(cur.fetchall())
```

**Вывод:** `[(1, 'a'), (3, 'c')]`

**Разбор:** удалили только id=2. Без WHERE удалили бы всё.

---

## Пример 9. JOIN из Python

```python
import sqlite3

with sqlite3.connect(":memory:") as conn:
    cur = conn.cursor()
    cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
    cur.execute("CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER, total REAL)")
    cur.execute("INSERT INTO users (name) VALUES (?)", ("Anna",))
    cur.execute("INSERT INTO orders (user_id, total) VALUES (?, ?)", (1, 50.0))
    cur.execute("INSERT INTO orders (user_id, total) VALUES (?, ?)", (1, 30.0))
    conn.commit()

    cur.execute("""
        SELECT u.name, o.total
        FROM users u
        INNER JOIN orders o ON u.id = o.user_id
    """)
    print(cur.fetchall())
```

**Вывод:** `[('Anna', 50.0), ('Anna', 30.0)]`

**Разбор:** SQL JOIN из главы 17 — выполняется через тот же `execute`. Два заказа Anna — две строки.

---

## Пример 10. Функция «найти пользователя по имени»

```python
import sqlite3

def find_user_by_name(conn, name):
    cur = conn.cursor()
    cur.execute("SELECT id, name FROM users WHERE name = ?", (name,))
    return cur.fetchone()

with sqlite3.connect(":memory:") as conn:
    cur = conn.cursor()
    cur.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
    cur.execute("INSERT INTO users (name) VALUES (?)", ("Vika",))
    conn.commit()

    print(find_user_by_name(conn, "Vika"))
    print(find_user_by_name(conn, "Unknown"))
```

**Вывод:**
```
(1, 'Vika')
None
```

**Разбор:** логика вынесена в функцию. Параметр `name` всегда через `?` — безопасно.

---

## Пример 11. rollback при ошибке

```python
import sqlite3

with sqlite3.connect(":memory:") as conn:
    cur = conn.cursor()
    cur.execute("CREATE TABLE balance (id INTEGER PRIMARY KEY, amount INTEGER)")
    cur.execute("INSERT INTO balance (amount) VALUES (?)", (100,))
    conn.commit()

    try:
        cur.execute("UPDATE balance SET amount = amount - 150 WHERE id = 1")
        if cur.execute("SELECT amount FROM balance WHERE id = 1").fetchone()[0] < 0:
            raise ValueError("Negative balance")
        conn.commit()
    except ValueError:
        conn.rollback()

    cur.execute("SELECT amount FROM balance WHERE id = 1")
    print(cur.fetchone())
```

**Вывод:** `(100,)`

**Разбор:** списание 150 с баланса 100 — ошибка. `rollback()` вернул 100. Деньги не «пропали».

---

## Пример 12. Мини-скрипт: создать БД в файле

```python
import sqlite3
import os

DB_PATH = "demo_shop.db"

with sqlite3.connect(DB_PATH) as conn:
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            price REAL
        )
    """)
    cur.execute("INSERT INTO products (name, price) VALUES (?, ?)", ("Book", 15.0))
    conn.commit()
    cur.execute("SELECT name, price FROM products")
    print(cur.fetchall())

# Удалим демо-файл после примера
if os.path.exists(DB_PATH):
    os.remove(DB_PATH)
```

**Вывод:** `[('Book', 15.0)]`

**Разбор:** `shop.db` — реальный файл рядом со скриптом. `IF NOT EXISTS` — не падаем при повторном запуске. В конце удалили файл для чистоты.

---

# Шпаргалка

| Действие | Код |
|----------|-----|
| Подключение | `sqlite3.connect("file.db")` |
| В памяти | `sqlite3.connect(":memory:")` |
| Выполнить SQL | `cursor.execute(sql, params)` |
| Все строки | `cursor.fetchall()` |
| Одна строка | `cursor.fetchone()` |
| Сохранить | `conn.commit()` |
| Откат | `conn.rollback()` |
| Много INSERT | `cursor.executemany(sql, list)` |
| Строки как dict | `conn.row_factory = sqlite3.Row` |

---

# FAQ

**Нужно ли ставить SQLite отдельно?**  
Нет, `sqlite3` встроен в Python.

**Почему кортеж `(name,)` с запятой?**  
`(name)` — просто скобки вокруг переменной. `(name,)` — кортеж из одного элемента. execute ждёт кортеж параметров.

**Когда вызывать close()?**  
`with sqlite3.connect(...) as conn` закрывает сам. Иначе — `conn.close()` в `finally`.

**ORM обязателен на работе?**  
Многие проекты на Flask/Django/FastAPI используют ORM. Но собеседования часто спрашивают чистый SQL и sqlite3.

**Асинхронная БД?**  
`aiosqlite` + FastAPI — позже. Сначала синхронный sqlite3.

**Как посмотреть таблицы в файле?**  
Программы DB Browser for SQLite, расширения VS Code, или `sqlite3 shop.db` в терминале.

---

# Домашнее задание

**Файл:** `homework_18.py`

Все задачи выполняй с `sqlite3.connect(":memory:")` — файл на диске не нужен.  
В конце каждой задачи — `print()` с ожидаемым результатом.

---

## Задача 1. Таблица и вставка

Создай таблицу `books (id INTEGER PRIMARY KEY AUTOINCREMENT, title TEXT, year INTEGER)`.  
Вставь две книги: `("Python Basics", 2024)` и `("SQL Guide", 2023)`.  
Выведи все строки `SELECT * FROM books`.

**Должно вывести (id могут быть 1 и 2):**
```
[(1, 'Python Basics', 2024), (2, 'SQL Guide', 2023)]
```

---

## Задача 2. SELECT с WHERE

На тех же данных выведи книги с `year >= 2024`.

**Должно вывести:**
```
[(1, 'Python Basics', 2024)]
```

---

## Задача 3. Функция count_rows

Напиши функцию `count_rows(conn, table_name)`, которая возвращает число строк в таблице.  
Используй `SELECT COUNT(*) FROM ...` — **имя таблицы только из доверенного кода**, не от пользователя.

Проверь на таблице `books` из задачи 1.

**Должно вывести:** `2`

---

## Задача 4. UPDATE

Добавь книгу `("Old Book", 2010)`. Обнови ей `year` на `2015` WHERE `title = 'Old Book'`.  
Выведи `title, year` этой книги.

**Должно вывести:** `('Old Book', 2015)`

---

## Задача 5. JOIN двух таблиц

Создай:
- `authors (id, name)` — вставь `("Tolstoy",)`
- `books2 (id, title, author_id)` — вставь `("War and Peace", 1)`

Напиши INNER JOIN: вывести `author_name, book_title`.

**Должно вывести:** `[('Tolstoy', 'War and Peace')]`

---

## Задача 6. Мини-модуль «библиотека»

Сделай в одном файле:

1. Функция `init_db(conn)` — создаёт таблицу `readers (id, name)` если нет.
2. Функция `add_reader(conn, name)` — INSERT с параметром `?`.
3. Функция `list_readers(conn)` — возвращает список имён.

В `if __name__ == "__main__":`:
- создай `:memory:` соединение,
- `init_db`, добавь `"Anna"` и `"Bob"`,
- выведи `list_readers(conn)`.

**Должно вывести:** `['Anna', 'Bob']`

---

## Как сдать

- Файл `homework_18.py`
- Запуск: `python homework_18.py` без ошибок
- Сдавай 1–3, потом 4–6

---

# Итог

1. **sqlite3** — connect, execute, fetch, commit, close.
2. Параметры **`?`** — защита от SQL injection.
3. **executemany**, **row_factory**, **rollback** — практические инструменты.
4. **ORM** (SQLAlchemy) — объекты вместо ручного SQL в больших проектах.

**Следующая глава 19:** HTTP, REST и веб на Flask — как отдать данные из Python в браузер.

---
Конец главы.