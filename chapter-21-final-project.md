# Тема: Финальный проект — «Мини-библиотека» (Library v1)

> **Формат:** пошаговый проект с объяснениями. Собираем навыки из глав 1–20.  
> **Цель:** один законченный учебный проект: API + SQLite + тесты + Git.  
> **Дальше:** гл. 22–23 (types/logging/FastAPI) → **гл. 24** — портфолио (мини-проекты + Library v2 / TaskFlow).  
> Эта глава = **v1**. Для найма усиливай по чеклисту гл. 24, не останавливайся только на эталоне ниже.

---

## Цель главы

Ты создаёшь **REST API мини-библиотеки**:

- книги и читатели в **SQLite**,
- **Flask**-эндпоинты (JSON),
- **pytest**-тесты,
- проект в **Git** (можно выложить на GitHub).

Это не экзамен «на скорость» — делай **по шагам**, проверяй каждый этап.

> **Обязательно из гл. 20:** `monkeypatch` + `tmp_path` для тестов (раздел 3.8). Без этого тесты проекта будут мешать друг другу.  
> **Чеклист сдачи:** `homework_21_checklist.md`  
> **Эталонный код** — в конце этой главы (можно сверяться, не копировать слепо).

---

# Что ты уже умеешь (из курса)

| Глава | Навык в проекте |
|-------|-----------------|
| 4–7 | Списки, dict, функции |
| 8 | JSON, файлы |
| 9 | Обработка ошибок |
| 10 | Структура пакета, venv |
| 15–16 | Алгоритмы, чистый код |
| 17–18 | SQL, sqlite3 |
| 19 | Flask, REST |
| 20 | Git, pytest |

---

# Описание проекта

## Сущности

**Книга (books):**
- `id` — целое, авто
- `title` — название
- `author` — автор
- `year` — год издания

**Читатель (readers):**
- `id`
- `name`

**Выдача (loans):** кто какую книгу взял
- `id`
- `book_id` → books
- `reader_id` → readers
- `loaned_at` — текст ISO даты, например `2026-07-14`

## API (минимум)

| Метод | URL | Действие |
|-------|-----|----------|
| GET | `/api/books` | Список книг |
| POST | `/api/books` | Добавить книгу |
| GET | `/api/books/<id>` | Одна книга |
| GET | `/api/readers` | Список читателей |
| POST | `/api/readers` | Добавить читателя |
| POST | `/api/loans` | Выдать книгу `{"book_id", "reader_id"}` |
| GET | `/api/loans` | Список выдач |

Коды: **200**, **201**, **400**, **404**.

---

# ЧАСТЬ 1. Структура проекта

## 1.1. Папки и файлы

```
library_project/
├── app.py              # Flask, маршруты
├── database.py         # SQLite: init, CRUD
├── requirements.txt    # flask, pytest
├── .gitignore
├── tests/
│   └── test_api.py     # pytest + test_client
└── README.md           # как запустить (кратко)
```

**Почему так:** логика БД отдельно от веба — проще тестировать и менять.

---

## 1.2. Виртуальное окружение

```bash
cd library_project
python -m venv venv
# Windows:
venv\Scripts\activate
pip install flask pytest
pip freeze > requirements.txt
```

---

## 1.3. .gitignore

```
venv/
__pycache__/
*.pyc
.pytest_cache/
library.db
.env
```

Базу `library.db` можно не коммитить — она создаётся при запуске.

---

### ✅ Проверь себя — часть 1

1. Зачем `database.py` отдельно? → **Не смешивать SQL и маршруты Flask**.
2. `library.db` в git? → **Обычно нет, в .gitignore**.
3. `requirements.txt`? → **Список зависимостей для pip install**.

---

# ЧАСТЬ 2. База данных

## 2.1. init_db — создать таблицы

В `database.py`:

```python
import sqlite3

DB_PATH = "library.db"

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year INTEGER
            );
            CREATE TABLE IF NOT EXISTS readers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS loans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                reader_id INTEGER NOT NULL,
                loaned_at TEXT NOT NULL,
                FOREIGN KEY (book_id) REFERENCES books(id),
                FOREIGN KEY (reader_id) REFERENCES readers(id)
            );
        """)
        conn.commit()
```

**Разбор:** `IF NOT EXISTS` — повторный запуск не падает. FOREIGN KEY связывает выдачу с книгой и читателем.

---

## 2.2. add_book — параметризованный INSERT

```python
def add_book(title, author, year):
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO books (title, author, year) VALUES (?, ?, ?)",
            (title, author, year),
        )
        conn.commit()
        return cur.lastrowid
```

**Разбор:** `?` — без SQL injection. `lastrowid` — id новой книги для ответа API.

---

## 2.3. list_books

```python
def list_books():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, title, author, year FROM books ORDER BY id"
        ).fetchall()
        return [dict(r) for r in rows]
```

**Разбор:** `dict(r)` — JSON-friendly структура для `jsonify`.

---

### ✅ Проверь себя — часть 2

1. Плейсхолдеры в INSERT? → **`?` и кортеж значений**.
2. `lastrowid`? → **id только что вставленной строки**.
3. Зачем `row_factory = Row`? → **Доступ к столбцам по имени**.

---

# ЧАСТЬ 3. Flask API

## 3.1. Каркас app.py

```python
from flask import Flask, request, jsonify
import database as db

app = Flask(__name__)

@app.before_request
def setup():
    pass  # init_db() лучше вызвать один раз при старте

def create_app(test_config=None):
    db.init_db()
    return app
```

На практике:

```python
if __name__ == "__main__":
    db.init_db()
    app.run(debug=True)
```

---

## 3.2. GET /api/books

```python
@app.route("/api/books", methods=["GET"])
def get_books():
    return jsonify(db.list_books())
```

---

## 3.3. POST /api/books

```python
@app.route("/api/books", methods=["POST"])
def post_book():
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    author = data.get("author")
    if not title or not author:
        return jsonify({"error": "title and author required"}), 400
    year = data.get("year")
    book_id = db.add_book(title, author, year)
    return jsonify({"id": book_id, "title": title, "author": author, "year": year}), 201
```

**Разбор:** валидация → 400. Успех → 201 и тело с id.

---

## 3.4. POST /api/loans — бизнес-правило

Перед выдачей проверь:
- книга существует,
- читатель существует,
- (опционально) книга ещё не выдана.

Иначе **404** или **400** с понятным `{"error": "..."}`.

---

### ✅ Проверь себя — часть 3

1. POST без JSON? → **400, не 500**.
2. Код при создании книги? → **201**.
3. Где валидация? → **В маршруте Flask до вызова БД**.

---

# ЧАСТЬ 4. Тесты и Git

## 4.1. Тест с временной БД

В тестах используй **отдельный файл** БД или monkeypatch `DB_PATH`:

```python
import pytest
from app import app
import database as db

@pytest.fixture
def client(tmp_path, monkeypatch):
    test_db = tmp_path / "test.db"
    monkeypatch.setattr(db, "DB_PATH", str(test_db))
    db.init_db()
    return app.test_client()

def test_list_books_empty(client):
    r = client.get("/api/books")
    assert r.status_code == 200
    assert r.get_json() == []
```

**Разбор:** `tmp_path` — чистая папка на каждый тест. Не трогаем реальную `library.db`.

---

## 4.2. Минимальный набор тестов

Напиши минимум **5** тестов:

1. GET `/api/books` — пустой список.
2. POST `/api/books` — 201, книга в списке.
3. POST без title — 400.
4. GET `/api/books/999` — 404.
5. POST `/api/loans` — успешная выдача.

`pytest tests/ -v` — все зелёные.

---

## 4.3. Git и GitHub

```bash
git init
git add .
git commit -m "Initial library API with tests"
git branch -M main
git remote add origin https://github.com/YOUR_USER/library_project.git
git push -u origin main
```

В **README.md** укажи:
- как установить зависимости,
- как запустить `python app.py`,
- как запустить тесты.

---

### ✅ Проверь себя — часть 4

1. Зачем отдельная test.db? → **Изоляция тестов**.
2. `monkeypatch`? → **Подменить DB_PATH в тестах**.
3. README зачем? → **Чтобы другой (и ты через месяц) запустил проект**.

---

# ЧАСТЬ 5. Эталонная реализация (полный код)

Ниже — **рабочий минимум** проекта. Можно сверяться по шагам или взять за основу и доработать самому.

---

## 5.1. Полный `database.py` (~80 строк)

```python
"""Слой работы с SQLite для мини-библиотеки."""
import sqlite3
from datetime import date

DB_PATH = "library.db"


def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    with get_connection() as conn:
        conn.executescript("""
            CREATE TABLE IF NOT EXISTS books (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                author TEXT NOT NULL,
                year INTEGER
            );
            CREATE TABLE IF NOT EXISTS readers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS loans (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                book_id INTEGER NOT NULL,
                reader_id INTEGER NOT NULL,
                loaned_at TEXT NOT NULL,
                FOREIGN KEY (book_id) REFERENCES books(id),
                FOREIGN KEY (reader_id) REFERENCES readers(id)
            );
        """)
        conn.commit()


def add_book(title, author, year=None):
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO books (title, author, year) VALUES (?, ?, ?)",
            (title, author, year),
        )
        conn.commit()
        return cur.lastrowid


def list_books():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, title, author, year FROM books ORDER BY id"
        ).fetchall()
        return [dict(r) for r in rows]


def get_book(book_id):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, title, author, year FROM books WHERE id = ?",
            (book_id,),
        ).fetchone()
        return dict(row) if row else None


def add_reader(name):
    with get_connection() as conn:
        cur = conn.execute(
            "INSERT INTO readers (name) VALUES (?)",
            (name,),
        )
        conn.commit()
        return cur.lastrowid


def list_readers():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT id, name FROM readers ORDER BY id"
        ).fetchall()
        return [dict(r) for r in rows]


def get_reader(reader_id):
    with get_connection() as conn:
        row = conn.execute(
            "SELECT id, name FROM readers WHERE id = ?",
            (reader_id,),
        ).fetchone()
        return dict(row) if row else None


def create_loan(book_id, reader_id):
    loaned_at = date.today().isoformat()
    with get_connection() as conn:
        cur = conn.execute(
            """INSERT INTO loans (book_id, reader_id, loaned_at)
               VALUES (?, ?, ?)""",
            (book_id, reader_id, loaned_at),
        )
        conn.commit()
        return cur.lastrowid


def list_loans():
    with get_connection() as conn:
        rows = conn.execute(
            """SELECT l.id, l.book_id, l.reader_id, l.loaned_at,
                      b.title AS book_title, r.name AS reader_name
               FROM loans l
               JOIN books b ON b.id = l.book_id
               JOIN readers r ON r.id = l.reader_id
               ORDER BY l.id"""
        ).fetchall()
        return [dict(r) for r in rows]
```

**Разбор:** один модуль — вся SQL-логика. `get_book` / `get_reader` возвращают `None`, если id не найден — удобно для 404 в Flask. `list_loans` с JOIN — читабельный ответ API.

---

## 5.2. Полный `app.py` (~80 строк)

```python
"""Flask REST API мини-библиотеки."""
from flask import Flask, request, jsonify
import database as db

app = Flask(__name__)


@app.route("/api/books", methods=["GET"])
def get_books():
    return jsonify(db.list_books())


@app.route("/api/books", methods=["POST"])
def post_book():
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    author = data.get("author")
    if not title or not author:
        return jsonify({"error": "title and author required"}), 400
    year = data.get("year")
    book_id = db.add_book(title, author, year)
    return jsonify({
        "id": book_id, "title": title, "author": author, "year": year
    }), 201


@app.route("/api/books/<int:book_id>", methods=["GET"])
def get_book_by_id(book_id):
    book = db.get_book(book_id)
    if book is None:
        return jsonify({"error": "book not found"}), 404
    return jsonify(book)


@app.route("/api/readers", methods=["GET"])
def get_readers():
    return jsonify(db.list_readers())


@app.route("/api/readers", methods=["POST"])
def post_reader():
    data = request.get_json(silent=True) or {}
    name = data.get("name")
    if not name:
        return jsonify({"error": "name required"}), 400
    reader_id = db.add_reader(name)
    return jsonify({"id": reader_id, "name": name}), 201


@app.route("/api/loans", methods=["GET"])
def get_loans():
    return jsonify(db.list_loans())


@app.route("/api/loans", methods=["POST"])
def post_loan():
    data = request.get_json(silent=True) or {}
    book_id = data.get("book_id")
    reader_id = data.get("reader_id")
    if book_id is None or reader_id is None:
        return jsonify({"error": "book_id and reader_id required"}), 400
    if db.get_book(book_id) is None:
        return jsonify({"error": "book not found"}), 404
    if db.get_reader(reader_id) is None:
        return jsonify({"error": "reader not found"}), 404
    loan_id = db.create_loan(book_id, reader_id)
    return jsonify({
        "id": loan_id,
        "book_id": book_id,
        "reader_id": reader_id,
    }), 201


if __name__ == "__main__":
    db.init_db()
    app.run(debug=True)
```

**Разбор:** маршруты тонкие — валидация и коды ответа здесь, SQL в `database.py`. Перед `create_loan` проверяем существование книги и читателя → предсказуемые 404.

---

### ✅ Проверь себя — часть 5

1. Где хранится путь к БД? → **`DB_PATH` в `database.py`**.
2. Что вернёт `get_book(999)`? → **`None` → маршрут отдаст 404**.
3. Зачем `request.get_json(silent=True) or {}`? → **Не падать на пустом теле POST**.

---

# Примеры — 16 фрагментов с разбором

Примеры 1–12 — короткие куски из частей 1–5. Примеры 13–16 — тесты, ручная проверка и README.

---

## Пример 1. Структура `requirements.txt`

```
flask>=3.0
pytest>=8.0
```

**Разбор:** зафиксируй версии после `pip freeze`, если сдаёшь на GitHub — так проект воспроизводим.

---

## Пример 2. Минимальный `.gitignore`

```
venv/
__pycache__/
*.pyc
.pytest_cache/
library.db
.env
```

**Разбор:** локальная БД и venv не должны попадать в репозиторий.

---

## Пример 3. `get_connection` с `Row`

```python
conn = sqlite3.connect(DB_PATH)
conn.row_factory = sqlite3.Row
```

**Разбор:** без `Row` строки — кортежи по индексу; с `Row` — `row["title"]` и `dict(row)` для JSON.

---

## Пример 4. Параметризованный INSERT

```python
conn.execute(
    "INSERT INTO books (title, author, year) VALUES (?, ?, ?)",
    (title, author, year),
)
```

**Разбор:** никогда не вставляй значения через f-string в SQL — только `?` и кортеж.

---

## Пример 5. `lastrowid` после INSERT

```python
cur = conn.execute("INSERT INTO readers (name) VALUES (?)", (name,))
conn.commit()
return cur.lastrowid
```

**Разбор:** id новой строки нужен клиенту API в ответе 201.

---

## Пример 6. GET списка книг

```python
@app.route("/api/books", methods=["GET"])
def get_books():
    return jsonify(db.list_books())
```

**Разбор:** Flask сериализует список dict в JSON-массив.

---

## Пример 7. Валидация POST — 400

```python
if not title or not author:
    return jsonify({"error": "title and author required"}), 400
```

**Разбор:** ошибка клиента (неполные данные) — код 400, не 500.

---

## Пример 8. 404 для одной книги

```python
book = db.get_book(book_id)
if book is None:
    return jsonify({"error": "book not found"}), 404
```

**Разбор:** «не найдено» — всегда 404 с понятным `error`.

---

## Пример 9. Дата выдачи ISO

```python
from datetime import date
loaned_at = date.today().isoformat()  # "2026-07-14"
```

**Разбор:** TEXT в SQLite + ISO-строка — простой формат для Junior.

---

## Пример 10. JOIN в `list_loans`

```sql
SELECT l.id, b.title AS book_title, r.name AS reader_name
FROM loans l
JOIN books b ON b.id = l.book_id
JOIN readers r ON r.id = l.reader_id
```

**Разбор:** в ответе API сразу видно название книги и имя читателя, не только id.

---

## Пример 11. Проверка перед loan

```python
if db.get_book(book_id) is None:
    return jsonify({"error": "book not found"}), 404
```

**Разбор:** бизнес-правило в Python, даже если FOREIGN KEY в SQLite отключён.

---

## Пример 12. Запуск сервера

```python
if __name__ == "__main__":
    db.init_db()
    app.run(debug=True)
```

**Разбор:** `init_db()` при старте создаёт таблицы; `debug=True` только для разработки.

---

## Пример 13. Фикстура `client` для pytest

Полный файл `tests/conftest.py` (или в начале `test_api.py`):

```python
import pytest
from app import app
import database as db


@pytest.fixture
def client(tmp_path, monkeypatch):
    """Flask test_client с изолированной БД в tmp_path."""
    test_db = tmp_path / "test.db"
    monkeypatch.setattr(db, "DB_PATH", str(test_db))
    db.init_db()
    with app.test_client() as c:
        yield c
```

**Разбор:** `tmp_path` — уникальная папка на каждый тест. `monkeypatch` подменяет `DB_PATH`, чтобы не трогать `library.db` в корне проекта. `yield` — фикстура отдаёт клиент и после теста корректно завершается.

---

## Пример 14. Образец pytest-теста

```python
def test_post_book_then_list(client):
    r = client.post(
        "/api/books",
        json={"title": "1984", "author": "Orwell", "year": 1949},
    )
    assert r.status_code == 201
    body = r.get_json()
    assert body["title"] == "1984"
    assert "id" in body

    r2 = client.get("/api/books")
    assert r2.status_code == 200
    books = r2.get_json()
    assert len(books) == 1
    assert books[0]["author"] == "Orwell"


def test_post_book_missing_title_returns_400(client):
    r = client.post("/api/books", json={"author": "Orwell"})
    assert r.status_code == 400
    assert "error" in r.get_json()
```

**Разбор:** `client.post(..., json=...)` сам ставит `Content-Type: application/json`. Проверяем и код, и тело. Второй тест — негативный сценарий (обязательное поле).

---

## Пример 15. Ручная проверка: `test_client` и curl

**В Python (REPL или скрипт):**

```python
from app import app
import database as db

db.init_db()
client = app.test_client()

# Книга
r = client.post("/api/books", json={
    "title": "Мастер и Маргарита",
    "author": "Булгаков",
    "year": 1967,
})
print("POST book:", r.status_code, r.get_json())

# Читатель
r = client.post("/api/readers", json={"name": "Анна"})
print("POST reader:", r.status_code, r.get_json())

# Выдача
r = client.post("/api/loans", json={"book_id": 1, "reader_id": 1})
print("POST loan:", r.status_code, r.get_json())

# Список выдач
r = client.get("/api/loans")
print("GET loans:", r.get_json())
```

**Через curl** (сервер запущен: `python app.py`):

```bash
curl -s http://127.0.0.1:5000/api/books

curl -s -X POST http://127.0.0.1:5000/api/books \
  -H "Content-Type: application/json" \
  -d "{\"title\":\"1984\",\"author\":\"Orwell\",\"year\":1949}"

curl -s http://127.0.0.1:5000/api/loans
```

**Разбор:** `test_client` — без сети, идеально для отладки. curl — проверка «как снаружи», когда сервер реально слушает порт 5000.

---

## Пример 16. Шаблон README.md

```markdown
# Library API — мини-библиотека

REST API на Flask + SQLite: книги, читатели, выдачи.

## Требования

- Python 3.10+
- pip

## Установка

```bash
git clone https://github.com/YOUR_USER/library_project.git
cd library_project
python -m venv venv
# Windows:
venv\Scripts\activate
pip install -r requirements.txt
```

## Запуск

```bash
python app.py
```

Сервер: http://127.0.0.1:5000

## Тесты

```bash
pytest tests/ -v
```

## Эндпоинты

| Метод | URL | Описание |
|-------|-----|----------|
| GET | `/api/books` | Список книг |
| POST | `/api/books` | Добавить книгу |
| GET | `/api/books/<id>` | Одна книга |
| GET/POST | `/api/readers` | Читатели |
| GET/POST | `/api/loans` | Выдачи |

## Автор

Имя Фамилия — курс Junior Python Developer
```

**Разбор:** README — первая страница репозитория. Укажи установку, запуск, тесты и таблицу API — ревьюеру не придётся угадывать команды.

---

# Практика — 8 шагов с разбором

---

## Шаг 1. Создай папку и venv

```bash
mkdir library_project
cd library_project
python -m venv venv
```

**Разбор:** изолированные зависимости — стандарт для Python-проектов.

---

## Шаг 2. database.py — init_db

Скопируй схему из части 2. Проверь:

```python
# в REPL или маленьком скрипте
import database as db
db.init_db()
print("OK")
```

**Разбор:** файл `library.db` появится рядом — значит SQLite работает.

---

## Шаг 3. CRUD для books

Реализуй `add_book`, `list_books`, `get_book(book_id)`.

```python
book_id = db.add_book("1984", "Orwell", 1949)
print(db.list_books())
print(db.get_book(book_id))
```

**Разбор:** сначала БД без Flask — проще отлаживать SQL.

---

## Шаг 4. readers и loans

`add_reader`, `list_readers`, `create_loan`, `list_loans`.

При выдаче запиши `loaned_at`:

```python
from datetime import date
today = date.today().isoformat()
```

**Разбор:** дата строкой — простой вариант для Junior (без datetime в SQLite).

---

## Шаг 5. Flask-маршруты

Подключи все эндпоинты из таблицы в начале главы.

Проверь вручную через `test_client` или Postman / curl.

**Разбор:** один ресурс за раз — сначала books, потом readers, потом loans.

---

## Шаг 6. Обработка ошибок

- нет книги → 404 `{"error": "book not found"}`,
- пустой JSON на POST → 400,
- неверный `book_id` при loan → 404.

**Разбор:** API должен **предсказуемо** отвечать, а не падать с traceback клиенту.

---

## Шаг 7. tests/test_api.py

Фикстура `client` с `tmp_path`. Пять тестов из части 4.

```bash
pytest tests/ -v
```

**Разбор:** тесты — доказательство, что проект работает. Ревьюер на GitHub увидит CI-ready код.

---

## Шаг 8. Git push и README

Короткий README на русском или английском:

```markdown
# Library API

## Install
pip install -r requirements.txt

## Run
python app.py

## Test
pytest tests/ -v
```

**Разбор:** репозиторий с README + тестами — сильная строка в резюме Junior.

---

# Критерии «проект сдан»

| # | Критерий |
|---|----------|
| 1 | Есть `database.py` с init и CRUD |
| 2 | Flask отдаёт JSON, коды 200/201/400/404 |
| 3 | SQLite на диске, параметры `?` в SQL |
| 4 | Минимум 5 pytest-тестов, все passed |
| 5 | `.gitignore`, `requirements.txt` |
| 6 | README с инструкцией запуска |
| 7 | Репозиторий на GitHub (желательно) |

---

# Домашнее задание (финальное)

**Папка:** `library_project/` (создай сам в `python-learning/` или отдельно)

> **Чеклист сдачи:** перед отправкой пройди все пункты в файле [`homework_21_checklist.md`](homework_21_checklist.md) — 6 обязательных проверок.

---

## Задача 1. Схема БД

Три таблицы: `books`, `readers`, `loans` с FOREIGN KEY.  
`init_db()` создаёт их при первом запуске.

**Проверка:** после `init_db()` в SQLite есть 3 таблицы.

---

## Задача 2. API книг

`GET /api/books`, `POST /api/books`, `GET /api/books/<id>`.

POST: обязательны `title`, `author`; `year` опционален.

**Проверка:** POST → 201, GET списка содержит книгу.

---

## Задача 3. API читателей и выдач

`GET/POST /api/readers`, `GET/POST /api/loans`.

Loan: тело `{"book_id": 1, "reader_id": 1}`.

**Проверка:** после loan в `GET /api/loans` одна запись.

---

## Задача 4. Тесты

Файл `tests/test_api.py`, минимум 5 тестов, `pytest -v` — green.

---

## Задача 5. README + Git

README: установка, запуск, тесты.  
Минимум 3 осмысленных коммита, например:
- `Add database layer`
- `Add Flask routes`
- `Add API tests`

---

## Задача 6. Дополнительно (по желанию)

Реализуй **одно** на выбор:
- `DELETE /api/books/<id>`,
- поиск книг `GET /api/books?q=orwell`,
- проверка «книга уже выдана» при повторном loan.

Опиши в README, что сделал.

---

## Как сдать

- Ссылка на GitHub **или** zip папки `library_project`
- Скриншот / текст вывода `pytest tests/ -v`
- Кратко: что было сложнее всего

---

# FAQ по проекту

**Сервер не стартует — ModuleNotFoundError: flask**  
Активируй venv и выполни `pip install -r requirements.txt`.

**pytest падает — база не пустая**  
В тестах обязательно подменяй `DB_PATH` через `tmp_path` и `monkeypatch`. Не используй общий `library.db` в тестах.

**POST возвращает 415 Unsupported Media Type**  
Клиент должен слать заголовок `Content-Type: application/json`. В `test_client`: `client.post(url, json={...})`.

**FOREIGN KEY не работает в SQLite**  
По умолчанию SQLite может не проверять FK. Для учебного проекта достаточно проверять существование book/reader в Python перед INSERT в loans.

**Как проверить API вручную без Postman**  
```python
with app.test_client() as c:
    print(c.post("/api/books", json={"title": "Test", "author": "Me"}).get_json())
```

**Сколько времени на проект**  
Ориентир: 2–4 вечера по 2–3 часа, если делать по шагам из этой главы.

---

# Частые ошибки Junior (и как исправить)

| Симптом | Причина | Решение |
|---------|---------|---------|
| 500 на POST | `request.get_json()` без проверки на None | `data = request.get_json(silent=True) or {}` |
| Пустой список после INSERT | Забыли `commit()` | `conn.commit()` после execute |
| Тесты влияют друг на друга | Одна БД на все тесты | `tmp_path` + отдельный файл БД |
| `library.db` в git | Нет в .gitignore | Добавь `*.db` |
| CORS ошибка в браузере | Фронт на другом порту | На Junior достаточно тестировать через `test_client` |

---

# Итог курса

Ты прошёл путь от **переменных и циклов** до **веб-API с базой и тестами**.

Дальше самостоятельно:
- **FastAPI** + async,
- **Docker**,
- **PostgreSQL** вместо SQLite,
- **аутентификация** (JWT),
- pet-проекты в портфолио.

**Поздравляю с завершением курса Junior Python Developer!**

---
Конец главы. Конец курса.