# Тема: HTTP, REST и веб на Flask

> **Формат:** сначала объяснение простыми словами, потом пример с разбором.  
> Не надо зубрить всё сразу — **3 части теории + 12 примеров + 6 задач**.

---

## Цель главы

После прочтения ты понимаешь:

1. **HTTP** — как браузер и сервер обмениваются запросами и ответами.
2. **REST API** — как отдавать данные в JSON для фронтенда и мобильных приложений.
3. **Flask** — минимальный веб-сервер на Python: маршруты, GET/POST, JSON.

Это мост между Python и «внешним миром»: сайты, API, мобильные клиенты.

> **Перед стартом:** `pip install flask` (лучше в venv — гл. 10).  
> **Связь с гл. 18:** мост «SQLite + Flask» в конце гл. 18 — 5 минут, если пропустил.  
> **Без браузера:** примеры через `test_client()`; `app.run()` — опционально в конце.  
> **Файл:** `homework_19.py`

---

# ЧАСТЬ 1. HTTP — основа веба

## 1.1. Клиент и сервер

Когда открываешь `https://example.com/page`:

1. **Браузер (клиент)** отправляет **HTTP-запрос**.
2. **Сервер** обрабатывает и возвращает **HTTP-ответ** (HTML, JSON, картинка).
3. Браузер показывает результат.

Python на сервере (Flask, FastAPI, Django) — программа, которая **принимает запросы** и **формирует ответы**.

---

## 1.2. Аналогия — заказ в кафе

- **Запрос** — ты говоришь официанту: «Принеси меню» (метод + адрес).
- **Ответ** — официант приносит меню или говорит «блюда нет» (код статуса + тело).

---

## 1.3. Структура HTTP-запроса

```
GET /api/users HTTP/1.1
Host: example.com
Accept: application/json
```

- **Метод** — что хотим сделать (`GET`, `POST`, ...).
- **URL / path** — куда обращаемся (`/api/users`).
- **Заголовки (headers)** — метаданные (тип ответа, авторизация).
- **Тело (body)** — данные (часто у POST/PUT), например JSON.

---

## 1.4. Методы HTTP (главные)

| Метод | Обычно для | Идемпотент* | Пример |
|-------|------------|-------------|--------|
| **GET** | Получить данные | Да | Список пользователей |
| **POST** | Создать | Нет | Регистрация |
| **PUT** | Заменить целиком | Да | Обновить профиль |
| **PATCH** | Частично обновить | Нет | Сменить email |
| **DELETE** | Удалить | Да | Удалить запись |

\*Идемпотент — повторный запрос не меняет результат сильнее первого (GET дважды — те же данные).

---

## 1.5. Коды статуса ответа

| Код | Значение | Когда |
|-----|----------|-------|
| **200** | OK | Успех |
| **201** | Created | Создали ресурс (POST) |
| **400** | Bad Request | Клиент прислал ерунду |
| **401** | Unauthorized | Нужна авторизация |
| **404** | Not Found | Маршрут или объект не найден |
| **500** | Internal Server Error | Ошибка на сервере |

Тело ответа + код статуса — то, что видит клиент (браузер, `requests`, мобильное приложение).

---

## 1.6. JSON в API

**JSON** — текстовый формат обмена данными:

```json
{"id": 1, "name": "Anna", "active": true}
```

В Python:

```python
import json

data = {"id": 1, "name": "Anna"}
text = json.dumps(data)      # dict → строка JSON
back = json.loads(text)      # строка → dict
```

API чаще отдают **JSON**, а не HTML.

---

### ✅ Проверь себя — часть 1

1. GET — для чего? → **Получить данные**.
2. Код 404? → **Не найдено**.
3. `json.loads`? → **Парсит строку JSON в Python-объект**.

---

# ЧАСТЬ 2. REST и Flask

## 2.1. Что такое REST (упрощённо)

**REST** — стиль проектирования API через HTTP:

- **Ресурсы** — сущности (`/users`, `/orders/5`).
- **Метод HTTP** — действие над ресурсом.
- **Статус-коды** — результат операции.
- **JSON** — формат данных.

Пример:
- `GET /users` — список пользователей.
- `GET /users/3` — пользователь с id=3.
- `POST /users` — создать (тело JSON с полями).
- `DELETE /users/3` — удалить.

Не «волшебный протокол» — **соглашение**, как удобно строить API.

---

## 2.2. Flask — минимальный веб-фреймворк

Установка:

```bash
pip install flask
```

Минимальное приложение:

```python
from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Hello, World!"

if __name__ == "__main__":
    app.run(debug=True)
```

- `@app.route("/")` — маршрут: URL → функция.
- `app.run()` — запуск dev-сервера (обычно `http://127.0.0.1:5000`).

---

## 2.3. Маршруты с параметрами

```python
@app.route("/users/<int:user_id>")
def get_user(user_id):
    return f"User id: {user_id}"
```

`/users/42` → `user_id = 42`.

---

## 2.4. Query-параметры (?key=value)

```python
from flask import request

@app.route("/search")
def search():
    q = request.args.get("q", "")
    return f"You searched: {q}"
```

`/search?q=python` → `q = "python"`.

---

## 2.5. JSON-ответ

```python
from flask import jsonify

@app.route("/api/status")
def status():
    return jsonify({"status": "ok", "version": 1})
```

`jsonify` — dict → ответ с заголовком `Content-Type: application/json`.

---

## 2.6. POST с JSON-телом

```python
from flask import request, jsonify

@app.route("/api/users", methods=["POST"])
def create_user():
    data = request.get_json()
    if not data or "name" not in data:
        return jsonify({"error": "name required"}), 400
    # здесь сохранили бы в БД
    return jsonify({"id": 1, "name": data["name"]}), 201
```

`methods=["POST"]` — только POST. Код **201** — создано.

---

### ✅ Проверь себя — часть 2

1. `@app.route` связывает что? → **URL и функцию-обработчик**.
2. `request.args.get("page")`? → **Query-параметр из URL**.
3. `jsonify` зачем? → **Ответ в JSON для клиента**.

---

# ЧАСТЬ 3. Клиент, тестирование API, FastAPI

## 3.1. Запросы с Python — библиотека requests

```bash
pip install requests
```

```python
import requests

r = requests.get("https://httpbin.org/get", params={"q": "test"})
print(r.status_code)
print(r.json())
```

Проверяешь своё API или чужое без браузера.

---

## 3.2. Тестовый клиент Flask — test_client

Flask даёт способ дернуть API **без запуска сервера в сеть**:

```python
with app.test_client() as client:
    response = client.get("/api/status")
    assert response.status_code == 200
```

Удобно для автотестов (связь с pytest в главе 20).

---

## 3.3. CORS (кратко)

Фронтенд на `http://localhost:3000` дергает API на `http://localhost:5000` — браузер может **заблокировать** запрос (разные origin).

Решение: заголовки CORS на сервере (расширение `flask-cors` или настройка в FastAPI). На Junior — **знать, что проблема существует**.

---

## 3.4. FastAPI — альтернатива Flask

**FastAPI** — современный фреймворк:
- автодокументация `/docs`,
- валидация через типы Pydantic,
- async из коробки.

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
```

На Junior: **начни с Flask** (проще), **знай, что FastAPI** часто в новых проектах.

---

## 3.5. Типичные ошибки Junior

| Ошибка | Проблема |
|--------|----------|
| Нет проверки `request.get_json()` на None | 500 при пустом теле |
| Все маршруты только GET | POST не принимается |
| Секреты в коде (`SECRET_KEY`) | Утечка в git |
| `debug=True` на продакшене | Дыра в безопасности |

---

### ✅ Проверь себя — часть 3

1. `requests.get` — кто клиент? → **Твой Python-скрипт**.
2. `test_client` — зачем? → **Тестировать Flask без реального HTTP**.
3. FastAPI `/docs`? → **Автоматическая документация API**.

---

# Практика — 12 примеров с разбором

---

## Пример 1. JSON dumps и loads

```python
import json

user = {"id": 1, "name": "Anna", "tags": ["python", "sql"]}
s = json.dumps(user, ensure_ascii=False)
print(s)
print(json.loads(s)["name"])
```

**Вывод:**
```
{"id": 1, "name": "Anna", "tags": ["python", "sql"]}
Anna
```

**Разбор:** `dumps` — Python → строка для сети/файла. `loads` — обратно. `ensure_ascii=False` — кириллица читаема.

---

## Пример 2. Минимальный Flask — текстовый ответ

```python
from flask import Flask

app = Flask(__name__)

@app.route("/hello")
def hello():
    return "Привет из Flask!"

# Запуск вручную: app.run()
# Тест без сервера:
with app.test_client() as client:
    r = client.get("/hello")
    print(r.data.decode())
```

**Вывод:** `Привет из Flask!`

**Разбор:** `client.get` имитирует GET-запрос. `r.data` — байты ответа.

---

## Пример 3. Статус-код 404

```python
from flask import Flask

app = Flask(__name__)

@app.route("/only-this")
def only_this():
    return "OK"

with app.test_client() as client:
    print(client.get("/only-this").status_code)
    print(client.get("/missing").status_code)
```

**Вывод:**
```
200
404
```

**Разбор:** несуществующий маршрут — Flask сам отдаёт 404.

---

## Пример 4. Маршрут с int-параметром

```python
from flask import Flask, jsonify

app = Flask(__name__)
USERS = {1: "Anna", 2: "Bob"}

@app.route("/users/<int:user_id>")
def user_detail(user_id):
    name = USERS.get(user_id)
    if name is None:
        return jsonify({"error": "not found"}), 404
    return jsonify({"id": user_id, "name": name})

with app.test_client() as client:
    print(client.get("/users/1").get_json())
    print(client.get("/users/99").status_code)
```

**Вывод:**
```
{'id': 1, 'name': 'Anna'}
404
```

**Разбор:** REST-стиль: ресурс `/users/1`, JSON, 404 если нет в «БД» (словаре).

---

## Пример 5. Query-параметры

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/search")
def search():
    q = request.args.get("q", "")
    limit = request.args.get("limit", 10, type=int)
    return jsonify({"query": q, "limit": limit})

with app.test_client() as client:
    r = client.get("/search?q=flask&limit=5")
    print(r.get_json())
```

**Вывод:** `{'query': 'flask', 'limit': 5}`

**Разбор:** `type=int` превращает строку `"5"` в число. Второй аргумент `get` — значение по умолчанию.

---

## Пример 6. GET — список ресурсов

```python
from flask import Flask, jsonify

app = Flask(__name__)
BOOKS = [
    {"id": 1, "title": "Python"},
    {"id": 2, "title": "SQL"},
]

@app.route("/api/books", methods=["GET"])
def list_books():
    return jsonify(BOOKS)

with app.test_client() as client:
    print(client.get("/api/books").get_json())
```

**Вывод:** `[{'id': 1, 'title': 'Python'}, {'id': 2, 'title': 'SQL'}]`

**Разбор:** классический `GET /api/books` — отдать коллекцию JSON.

---

## Пример 7. POST — создать ресурс

```python
from flask import Flask, request, jsonify

app = Flask(__name__)
next_id = 3
BOOKS = []

@app.route("/api/books", methods=["POST"])
def add_book():
    global next_id
    data = request.get_json()
    if not data or "title" not in data:
        return jsonify({"error": "title required"}), 400
    book = {"id": next_id, "title": data["title"]}
    next_id += 1
    BOOKS.append(book)
    return jsonify(book), 201

with app.test_client() as client:
    r = client.post("/api/books", json={"title": "Flask Guide"})
    print(r.status_code, r.get_json())
```

**Вывод:** `201 {'id': 3, 'title': 'Flask Guide'}`

**Разбор:** `client.post(..., json=...)` — тело как JSON. Ответ 201 Created.

---

## Пример 8. DELETE — удалить

```python
from flask import Flask, jsonify

app = Flask(__name__)
BOOKS = [{"id": 1, "title": "A"}, {"id": 2, "title": "B"}]

@app.route("/api/books/<int:book_id>", methods=["DELETE"])
def delete_book(book_id):
    global BOOKS
    before = len(BOOKS)
    BOOKS = [b for b in BOOKS if b["id"] != book_id]
    if len(BOOKS) == before:
        return jsonify({"error": "not found"}), 404
    return "", 204

with app.test_client() as client:
    print(client.delete("/api/books/1").status_code)
    print(len(BOOKS))
```

**Вывод:**
```
204
1
```

**Разбор:** **204 No Content** — успех без тела. В списке осталась одна книга.

---

## Пример 9. Обработка неверного JSON

```python
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/api/echo", methods=["POST"])
def echo():
    data = request.get_json(silent=True)
    if data is None:
        return jsonify({"error": "invalid json"}), 400
    return jsonify(data)

with app.test_client() as client:
    r = client.post("/api/echo", data="not json", content_type="application/json")
    print(r.status_code, r.get_json())
```

**Вывод:** `400 {'error': 'invalid json'}`

**Разбор:** `silent=True` — не падать с 500, вернуть None. Отдаём 400 клиенту.

---

## Пример 10. requests — внешний GET

```python
import requests

r = requests.get("https://httpbin.org/get", params={"course": "python"}, timeout=5)
print(r.status_code)
print(r.json()["args"])
```

**Вывод (примерно):**
```
200
{'course': 'python'}
```

**Разбор:** httpbin — тестовый сервис. `timeout=5` — не висеть вечно. Нужен интернет.

---

## Пример 11. REST: сводка маршрутов

```python
# Учебная «карта» API магазина:
ROUTES = """
GET    /api/products      — список товаров
GET    /api/products/<id> — один товар
POST   /api/products      — создать
PUT    /api/products/<id> — обновить
DELETE /api/products/<id> — удалить
"""
print(ROUTES.strip())
```

**Разбор:** перед кодом полезно набросать **контракт API** — что клиент может вызывать. Так делают в команде.

---

## Пример 12. Flask + sqlite3 (идея связи с гл. 18)

```python
import sqlite3
from flask import Flask, jsonify

app = Flask(__name__)

def get_db():
    conn = sqlite3.connect(":memory:")
    conn.row_factory = sqlite3.Row
    conn.execute("CREATE TABLE items (id INTEGER PRIMARY KEY, name TEXT)")
    conn.execute("INSERT INTO items (name) VALUES (?)", ("Apple",))
    conn.commit()
    return conn

@app.route("/api/items")
def items():
    conn = get_db()
    rows = conn.execute("SELECT id, name FROM items").fetchall()
    conn.close()
    return jsonify([dict(r) for r in rows])

with app.test_client() as client:
    print(client.get("/api/items").get_json())
```

**Вывод:** `[{'id': 1, 'name': 'Apple'}]`

**Разбор:** веб-слой (Flask) + данные (SQLite). В реальном проекте соединение и БД живут дольше одного запроса.

---

# Шпаргалка

| Задача | Инструмент |
|--------|------------|
| Маршрут | `@app.route("/path", methods=[...])` |
| Query | `request.args.get("key")` |
| JSON тело | `request.get_json()` |
| JSON ответ | `jsonify({...})` |
| Код ошибки | `return jsonify(...), 400` |
| Тест без сети | `app.test_client()` |
| Внешний запрос | `requests.get/post` |

---

# FAQ

**Flask или Django?**  
Flask — минимализм, учёба, маленькие API. Django — «всё включено» (админка, ORM). Junior часто начинает с Flask/FastAPI.

**Где хранить данные в учебном API?**  
Список в памяти, потом SQLite (глава 18).

**Почему 201, а не 200 на POST?**  
201 явно говорит: **ресурс создан**. Клиенту понятнее.

**Нужен ли HTML?**  
Для API — нет, JSON. HTML — если рендеришь страницы (`render_template`).

**Как запустить Flask?**  
`python app.py` или `flask --app app run`. `debug=True` только локально.

---

# Домашнее задание

**Файл:** `homework_19.py`

Используй Flask и `test_client` — **сервер вручную запускать не обязательно**.

---

## Задача 1. Маршрут /ping

Создай Flask-приложение с маршрутом `GET /ping`, возвращает строку `"pong"`.  
Через `test_client` выведи тело ответа.

**Должно вывести:** `pong`

---

## Задача 2. JSON /api/info

Маршрут `GET /api/info` возвращает JSON: `{"course": "Python Junior", "chapter": 19}`.

**Должно вывести:** словарь с этими ключами (проверь `get_json()`).

---

## Задача 3. Параметр в URL

Маршрут `GET /hello/<name>` — ответ `Hello, <name>!`.  
Проверь `/hello/Anna`.

**Должно вывести:** `Hello, Anna!`

---

## Задача 4. Query limit

Маршрут `GET /api/items` возвращает JSON-список из 10 имён `item_0` … `item_9`.  
Query-параметр `limit` (int) — вернуть только первые `limit` элементов.  
По умолчанию `limit=10`. Проверь `?limit=3`.

**Должно вывести:** 3 элемента в списке.

---

## Задача 5. POST /api/notes

В памяти список `notes`.  
`POST /api/notes` принимает JSON `{"text": "..."}`. Если нет `text` — 400.  
Иначе добавь заметку с полями `id` (автоинкремент) и `text`, верни 201 и объект.

Проверь POST с `{"text": "learn Flask"}`.

**Должно:** status 201, в JSON есть `"text": "learn Flask"` и `"id"`.

---

## Задача 6. Мини-API «задачи»

Реализуй в одном файле:

| Метод | URL | Действие |
|-------|-----|----------|
| GET | `/api/tasks` | список всех задач |
| POST | `/api/tasks` | создать `{"title": "..."}` |
| DELETE | `/api/tasks/<id>` | удалить по id |

Храни задачи в списке словарей `{"id", "title", "done": False}`.

В `if __name__ == "__main__":` через `test_client`:
1. POST задачу `"Buy milk"`
2. GET — вывести количество задач (должно быть 1)
3. DELETE id=1
4. GET — количество (должно быть 0)

**Должно вывести две строки:** `1` затем `0`

---

## Задача 7. Бонус — Flask + SQLite (мост гл. 18)

`GET /api/books` читает книги из SQLite `:memory:` (создай таблицу при старте, вставь 1–2 книги).  
Верни JSON-список через `jsonify`. Проверь через `test_client`.

**Должно:** status 200, в JSON хотя бы одна книга с полями `id`, `title`.

Подсказка: мост в **гл. 18 часть 3** + **пример 12** в этой главе.

---

## Как сдать

- `pip install flask` если ещё нет
- `python homework_19.py`
- Сдавай 1–3, потом 4–6; задача 7 — бонус после 6

---

# Итог

1. **HTTP** — метод, URL, заголовки, тело, код статуса.
2. **REST** — ресурсы + HTTP-методы + JSON.
3. **Flask** — маршруты, `jsonify`, `test_client` для проверки.
4. Данные из **SQLite** (глава 18) можно отдавать через API.

**Следующая глава 20:** Git и pytest — версии кода и автотесты.

---
Конец главы.