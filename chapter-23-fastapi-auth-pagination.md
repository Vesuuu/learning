# Тема: FastAPI, пагинация и простая auth

> **Формат:** 3 части + 12 примеров + 6 задач.  
> **Зачем:** в вакансиях junior backend часто **FastAPI** (или Django), а не только Flask.  
> **Перед стартом:** `pip install fastapi uvicorn` (в venv).  
> **Файл:** `homework_23.py`  
> **База:** гл. 19 (HTTP/REST), гл. 22 (hints, env, logging).

---

## Цель главы

После прочтения ты умеешь:

1. Поднять **REST API на FastAPI** с автоматической документацией `/docs`.
2. Делать **пагинацию** списков (`limit` / `offset` + `total`).
3. Защищать эндпоинты **API Key** и понимать идею **JWT** (без глубокого crypto).

Flask из гл. 19 **не выбрасываем** — оба стека полезны. FastAPI = современный рынок + type hints «из коробки».

---

# ЧАСТЬ 1. FastAPI за 20 минут

## 1.1. Почему FastAPI на junior

| Плюс | Смысл |
|------|--------|
| **Pydantic-модели** | Валидация JSON автоматически |
| **OpenAPI /docs** | Живая документация API |
| **Type hints** | Параметры = контракт |
| **async-ready** | Потом проще расти |
| **Рынок** | Много вакансий 2024–2026 |

Для обучения sync-функций достаточно (как в Flask).

---

## 1.2. Минимальный сервер

```python
from fastapi import FastAPI

app = FastAPI(title="Demo API")


@app.get("/ping")
def ping() -> dict[str, str]:
    return {"message": "pong"}
```

Запуск:

```bash
uvicorn homework_23:app --reload
```

Открой: http://127.0.0.1:8000/docs

---

## 1.3. Path и Query параметры

```python
from fastapi import FastAPI, Query

app = FastAPI()


@app.get("/hello/{name}")
def hello(name: str) -> dict[str, str]:
    return {"hello": name}


@app.get("/items")
def items(limit: int = Query(10, ge=1, le=100)) -> dict[str, int]:
    return {"limit": limit}
```

- `{name}` — path.
- `limit` — query: `/items?limit=5`.
- `ge=1, le=100` — валидация: иначе **422**.

---

## 1.4. Body через Pydantic

```python
from pydantic import BaseModel, Field


class BookIn(BaseModel):
    title: str = Field(min_length=1)
    author: str = Field(min_length=1)
    year: int | None = None


class BookOut(BookIn):
    id: int


@app.post("/api/books", status_code=201)
def create_book(body: BookIn) -> BookOut:
    return BookOut(id=1, **body.model_dump())
```

Пустой `title` → FastAPI сам вернёт **422** с описанием ошибки (удобнее ручных `if not title` в Flask).

---

## 1.5. HTTPException — свои 404/400

```python
from fastapi import HTTPException


@app.get("/api/books/{book_id}")
def get_book(book_id: int) -> dict:
    book = storage.get(book_id)  # None если нет
    if book is None:
        raise HTTPException(status_code=404, detail="book not found")
    return book
```

Клиент увидит JSON с `detail`.

---

## 1.6. TestClient (pytest)

```python
from fastapi.testclient import TestClient

client = TestClient(app)

def test_ping():
    r = client.get("/ping")
    assert r.status_code == 200
    assert r.json()["message"] == "pong"
```

`pip install httpx` — зависимость TestClient (часто ставится с fastapi).

---

### ✅ Проверь себя — часть 1

1. Где смотреть docs? → **`/docs` (Swagger UI)**.
2. Невалидное body? → **Обычно 422**.
3. Свой 404? → **`raise HTTPException(404, detail=...)`**.

---

# ЧАСТЬ 2. Пагинация и полный CRUD

## 2.1. Зачем пагинация

`GET /api/books` без лимита при 100_000 записей — тормоз и большой JSON.

Паттерн junior-уровня:

```http
GET /api/books?limit=10&offset=0
```

Ответ:

```json
{
  "items": [ ... ],
  "total": 42,
  "limit": 10,
  "offset": 0
}
```

- **limit** — сколько вернуть.
- **offset** — сколько пропустить с начала.
- **total** — всего записей (для UI «страница 1 из N»).

---

## 2.2. Реализация на списке в памяти

```python
def paginate(rows: list, limit: int, offset: int) -> dict:
    total = len(rows)
    slice_ = rows[offset : offset + limit]
    return {
        "items": slice_,
        "total": total,
        "limit": limit,
        "offset": offset,
    }
```

В SQL:

```sql
SELECT ... FROM books ORDER BY id LIMIT ? OFFSET ?
```

И отдельно: `SELECT COUNT(*) FROM books`.

---

## 2.3. Фильтр + пагинация

```python
@app.get("/api/books")
def list_books(
    q: str | None = None,
    limit: int = Query(10, ge=1, le=100),
    offset: int = Query(0, ge=0),
) -> dict:
    rows = all_books()
    if q:
        q_low = q.lower()
        rows = [b for b in rows if q_low in b["title"].lower()]
    return paginate(rows, limit, offset)
```

`?q=orwell&limit=5` — поиск + страница.

---

## 2.4. PUT / PATCH / DELETE

| Метод | Смысл |
|-------|--------|
| **PUT** | Заменить ресурс целиком (все поля) |
| **PATCH** | Частично (только переданные поля) |
| **DELETE** | Удалить → часто **204** без тела или **200** + сообщение |

```python
@app.delete("/api/books/{book_id}", status_code=204)
def delete_book(book_id: int) -> None:
    if not remove(book_id):
        raise HTTPException(404, detail="book not found")
```

---

## 2.5. Код 409 Conflict

Бизнес-конфликт, не «не найдено»:

- книга **уже выдана**;
- email **уже зарегистрирован**;
- short code **занят**.

```python
raise HTTPException(status_code=409, detail="book already loaned")
```

На собеседовании 409 отделяют от 400/404 — хороший знак junior.

---

### ✅ Проверь себя — часть 2

1. Зачем `total` в ответе? → **UI пагинации / клиент знает размер**.
2. `offset=10, limit=10` — какая «страница»? → **Вторая (записи 11–20)**.
3. Книга уже выдана — какой код? → **409**, не 400/404.

---

# ЧАСТЬ 3. Auth basics

## 3.1. Зачем auth

Без защиты любой в интернете сделает `POST /api/books`.  
Минимум junior: **отличать «кто угодно» и «кто знает секрет»**.

Уровни (от простого к сложному):

1. **API Key** в заголовке — для сервисов и учебы.
2. **Login + session cookie** — классика сайтов.
3. **JWT Bearer token** — типичный REST/mobile.

В этой главе: **API Key** (must) + **идея JWT** (теория + крошечный demo).

---

## 3.2. API Key в заголовке

Клиент:

```http
GET /api/secret
X-API-Key: dev-secret-key
```

Сервер:

```python
from fastapi import Header, HTTPException, Depends
import os

API_KEY = os.getenv("API_KEY", "dev-secret-key")


def verify_api_key(x_api_key: str | None = Header(default=None)) -> None:
    if x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="invalid or missing API key")


@app.post("/api/books", status_code=201, dependencies=[Depends(verify_api_key)])
def create_book(body: BookIn) -> BookOut:
    ...
```

- **401** — не авторизован (нет/неверный ключ).
- **403** — авторизован, но **нельзя** (роль user ≠ admin) — позже.

---

## 3.3. Идея JWT (без полной реализации crypto)

**JWT** — строка из трёх частей: `header.payload.signature`.

1. Клиент: `POST /auth/login` с email/password.
2. Сервер проверяет пароль (хеш!), отдаёт token.
3. Клиент: `Authorization: Bearer <token>` на защищённых маршрутах.
4. Сервер проверяет подпись и expiry, достаёт `user_id`.

**Важно для junior:**

- пароль **никогда** не хранить plaintext → `bcrypt` / `argon2`;
- secret для подписи JWT — только в env;
- access token короткий (15–60 мин).

Библиотеки: `PyJWT`, `python-jose`, в FastAPI часто `OAuth2PasswordBearer`.

Полный JWT+password — **бонус / capstone гл. 24**, здесь достаточно API Key + понимание схемы.

---

## 3.4. Что логировать при auth

```python
logger.info("Auth failed for path=%s", request.url.path)
# НЕ: logger.info("key=%s", x_api_key)
```

---

### ✅ Проверь себя — часть 3

1. Неверный API key → **401**.
2. Где хранить API_KEY? → **env / .env, не в git**.
3. JWT где передают? → **Заголовок `Authorization: Bearer ...`**.

---

# Примеры — 12 с разбором

## Пример 1. app + ping

```python
from fastapi import FastAPI
app = FastAPI()

@app.get("/ping")
def ping():
    return {"message": "pong"}
```

**Разбор:** минимальная проверка, что uvicorn видит `app`.

---

## Пример 2. Модель In/Out

```python
class NoteIn(BaseModel):
    text: str = Field(min_length=1)

class NoteOut(NoteIn):
    id: int
```

**Разбор:** не отдаём «лишнее»; id только в ответе.

---

## Пример 3. In-memory storage

```python
_notes: dict[int, dict] = {}
_next_id = 1

def add_note(text: str) -> dict:
    global _next_id
    note = {"id": _next_id, "text": text}
    _notes[_next_id] = note
    _next_id += 1
    return note
```

**Разбор:** для учёбы OK; в проде — БД (гл. 18/21).

---

## Пример 4. paginate

```python
def paginate(items: list, limit: int, offset: int) -> dict:
    return {
        "items": items[offset: offset + limit],
        "total": len(items),
        "limit": limit,
        "offset": offset,
    }
```

**Разбор:** одна функция — переиспользуй в books/notes/tasks.

---

## Пример 5. Query ge/le

```python
limit: int = Query(10, ge=1, le=50)
```

**Разбор:** `limit=0` или `9999` отрежутся валидацией.

---

## Пример 6. 404

```python
raise HTTPException(status_code=404, detail="note not found")
```

**Разбор:** `detail` может быть str или dict.

---

## Пример 7. 409

```python
if email in registered:
    raise HTTPException(409, detail="email taken")
```

**Разбор:** конфликт состояния, не «кривой JSON».

---

## Пример 8. Depends API key

```python
@app.get("/private", dependencies=[Depends(verify_api_key)])
def private():
    return {"ok": True}
```

**Разбор:** `dependencies` не добавляет параметр в функцию — только проверка.

---

## Пример 9. Header вручную

```python
def verify(x_api_key: str | None = Header(default=None)):
    if x_api_key != API_KEY:
        raise HTTPException(401, detail="unauthorized")
```

**Разбор:** имя `x_api_key` → заголовок `X-Api-Key` (FastAPI конвертирует).

---

## Пример 10. TestClient POST

```python
r = client.post("/api/notes", json={"text": "hi"})
assert r.status_code == 201
assert r.json()["text"] == "hi"
```

**Разбор:** как Flask `test_client`, но `.json()` метод ответа.

---

## Пример 11. Тест 401

```python
r = client.post("/api/notes", json={"text": "x"})  # без ключа
assert r.status_code == 401
```

**Разбор:** негативные тесты = junior-мышление.

---

## Пример 12. Тест с ключом

```python
r = client.post(
    "/api/notes",
    json={"text": "x"},
    headers={"X-API-Key": "dev-secret-key"},
)
assert r.status_code == 201
```

**Разбор:** headers в TestClient — как у настоящего клиента.

---

# Практика — 6 задач

> Код в `homework_23.py`. Внизу — `if __name__ == "__main__"`: прогон через `TestClient` + assert (uvicorn не обязателен для сдачи).

---

## Задача 1. Ping + docs-ready app

- `app = FastAPI(title="HW23")`
- `GET /ping` → `{"message": "pong"}`

---

## Задача 2. Notes API (CRUD-lite)

In-memory:

| Метод | URL | Поведение |
|-------|-----|-----------|
| GET | `/api/notes` | пагинация `limit` (default 10), `offset` (default 0) → `items/total/limit/offset` |
| POST | `/api/notes` | body `{"text": "..."}` → 201 + id |
| GET | `/api/notes/{id}` | 200 или 404 |
| DELETE | `/api/notes/{id}` | 204 или 404 |

Pydantic-модель для POST.

---

## Задача 3. Поиск `q`

`GET /api/notes?q=flask` — только notes, где `q` входит в `text` (без регистра), **потом** paginate.

---

## Задача 4. API Key на запись

- `POST` и `DELETE` требуют заголовок `X-API-Key` = `dev-secret-key` (или из env).
- `GET` — публичные.
- Без ключа / неверный → **401**.

---

## Задача 5. Конфликт (симуляция)

`POST /api/notes/unique` body `{"text": "..."}`:

- если note с таким `text` уже есть → **409** `detail` содержит `"exists"`;
- иначе создаёт как обычный note.

---

## Задача 6. Автотесты в main

Через `TestClient` минимум:

1. ping 200  
2. post без key → 401  
3. post с key → 201  
4. list total == 1  
5. get missing → 404  
6. unique duplicate → 409  

```bash
python homework_23.py
```

Все assert проходят.

---

# Критерии зачёта гл. 23

- [ ] FastAPI app + Pydantic на POST
- [ ] Пагинация с `total`
- [ ] API Key на мутациях
- [ ] 404 и 409 в нужных местах
- [ ] 6 проверок TestClient зелёные

---

# FAQ

**Q: Flask или FastAPI на собесе?**  
A: Знай оба на уровне CRUD. В резюме: «Flask (курс) + FastAPI (гл. 23 / портфолио)».

**Q: Нужен async?**  
A: Для junior CRUD — нет. `async def` + БД async — следующий уровень.

**Q: Заменить library_project на FastAPI?**  
A: Да, как **вариант B** в гл. 24 — сильный плюс к портфолио.

---

# Что дальше

**Глава 24** — не теория, а **портфолио**: 4 мини-проекта + один capstone «я junior».
