# Тема: Type hints, logging и конфиг через env

> **Формат:** 3 части теории + 12 примеров + 6 задач.  
> **Зачем:** на junior-собеседованиях и в реальных API ждут не только «работает», а **читаемый, безопасный, отлаживаемый** код.  
> **Файл:** `homework_22.py`  
> **Перед стартом:** Python 3.10+ (синтаксис `list[str]`, `X | None`).

---

## Цель главы

После прочтения ты умеешь:

1. **Аннотировать** функции и данные type hints (`list[str]`, `dict[str, int]`, `X | None`).
2. **Логировать** через модуль `logging` вместо `print` в «боевом» коде.
3. **Хранить секреты и настройки** в переменных окружения (`.env`), а не в коде.

Это «production hygiene» — то, чего не хватает после глав 1–21 для уверенного junior.

---

# ЧАСТЬ 1. Type hints

## 1.1. Зачем аннотации

Без подсказок:

```python
def add_user(name, age):
    ...
```

Через месяц: `name` — строка или dict? `age` — int или str из JSON?

**Type hints** — подсказки для тебя, IDE и (опционально) mypy:

```python
def add_user(name: str, age: int) -> dict[str, str | int]:
    return {"name": name, "age": age}
```

Python **не проверяет** типы в runtime (в отличие от Java). Это документация + помощь редактору.

---

## 1.2. Базовые аннотации

| Аннотация | Смысл | Пример |
|-----------|--------|--------|
| `str`, `int`, `float`, `bool` | Примитивы | `x: int = 1` |
| `list[str]` | Список строк | `names: list[str]` |
| `dict[str, int]` | Словарь str→int | `scores: dict[str, int]` |
| `tuple[int, str]` | Кортеж фиксированной формы | `(1, "ok")` |
| `set[int]` | Множество | `{1, 2}` |
| `X \| None` | Значение или None | `user: dict \| None` |
| `Any` | «Что угодно» (избегай) | редко |

В Python **3.9+** пиши `list[str]`, не `List[str]` из `typing` (старый стиль ещё встречается).

---

## 1.3. Функции: параметры и return

```python
def full_name(first: str, last: str) -> str:
    return f"{first} {last}"


def find_user(users: list[dict], user_id: int) -> dict | None:
    for u in users:
        if u["id"] == user_id:
            return u
    return None
```

`-> None` — функция ничего полезного не возвращает (side effects: печать, запись в файл).

---

## 1.4. Optional и значения по умолчанию

```python
def greet(name: str, title: str | None = None) -> str:
    if title is None:
        return f"Hello, {name}"
    return f"Hello, {title} {name}"
```

`title: str | None = None` — либо строка, либо «не передали».

---

## 1.5. TypedDict — форма dict (без классов)

Когда JSON-объект фиксированной формы, но ещё не хочешь Pydantic/dataclass:

```python
from typing import TypedDict


class BookDict(TypedDict):
    id: int
    title: str
    author: str


def book_to_line(book: BookDict) -> str:
    return f"{book['id']}: {book['title']} — {book['author']}"
```

---

## 1.6. Когда hints обязательны на junior

| Место | Делай |
|-------|--------|
| Публичные функции API/БД | параметры + `->` |
| Сложные dict-структуры | TypedDict или dataclass |
| Внутренние 3-строчные хелперы | можно без, но лучше с |
| `*args` / `**kwargs` | можно проще: не усложняй |

---

### ✅ Проверь себя — часть 1

1. Проверяет ли Python типы сам? → **Нет, только подсказки**.
2. Как записать «int или None»? → **`int | None`**.
3. `list[str]` vs `List[str]`? → **В 3.9+ предпочтительно `list[str]`**.

---

# ЧАСТЬ 2. Logging

## 2.1. Почему не print

`print` хорош для обучения. В API / скриптах на сервере:

- нельзя отключить «шум» без правки кода;
- нет **уровней** (DEBUG / INFO / WARNING / ERROR);
- нет времени, модуля, единого формата;
- в проде логи часто идут в файл или систему сбора логов.

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger(__name__)

logger.info("Server started")
logger.warning("Disk almost full")
logger.error("Failed to open DB: %s", "library.db")
```

---

## 2.2. Уровни

| Уровень | Когда |
|---------|--------|
| **DEBUG** | Детали для отладки (тело запроса, SQL) |
| **INFO** | Нормальные события (старт, «user created») |
| **WARNING** | Странно, но живём (deprecated, retry) |
| **ERROR** | Операция не удалась |
| **CRITICAL** | Система падает |

В разработке часто `DEBUG` или `INFO`. В проде — `INFO` или `WARNING`.

---

## 2.3. Logger на модуль

```python
# database.py
import logging

logger = logging.getLogger(__name__)  # "database"


def init_db() -> None:
    logger.info("Initializing database")
    ...
```

`__name__` → в логе видно, **из какого файла** сообщение.

---

## 2.4. Не логируй секреты

```python
# ПЛОХО
logger.info("Login: password=%s", password)

# ХОРОШО
logger.info("Login attempt for user_id=%s", user_id)
```

Токены, пароли, API keys — **никогда** в логи.

---

## 2.5. Ошибки с traceback

```python
try:
    data = load_json(path)
except Exception:
    logger.exception("Cannot load %s", path)  # + traceback
    raise
```

`logger.exception(...)` внутри `except` пишет ERROR **и** стек вызовов.

---

### ✅ Проверь себя — часть 2

1. Чем logging лучше print? → **Уровни, формат, можно отключать**.
2. Какой logger создавать в модуле? → **`logging.getLogger(__name__)`**.
3. Как залогировать traceback? → **`logger.exception(...)`**.

---

# ЧАСТЬ 3. Конфиг и .env

## 3.1. 12-factor: конфиг из окружения

Секреты и настройки **не** хардкодятся:

```python
# ПЛОХО
API_KEY = "sk-super-secret"
DB_PATH = "C:/Users/Admin/secret.db"
```

```python
# ХОРОШО
import os

API_KEY = os.environ.get("API_KEY", "")
DB_PATH = os.environ.get("DB_PATH", "library.db")
```

На сервере / в CI ключи задают как переменные окружения. В git попадает только `.env.example` **без** секретов.

---

## 3.2. Файл .env (локально)

Файл `.env` в корне проекта (в `.gitignore`!):

```
API_KEY=dev-secret-key
DB_PATH=library.db
DEBUG=1
```

Чтение через `python-dotenv`:

```bash
pip install python-dotenv
```

```python
import os
from dotenv import load_dotenv

load_dotenv()  # подхватывает .env

API_KEY = os.getenv("API_KEY", "")
DEBUG = os.getenv("DEBUG", "0") == "1"
```

---

## 3.3. .env.example — шаблон для GitHub

```
API_KEY=change-me
DB_PATH=library.db
DEBUG=0
```

В README: «Скопируй `.env.example` → `.env` и заполни».

---

## 3.4. Мини-модуль config.py

```python
"""config.py — единая точка настроек."""
import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    API_KEY: str = os.getenv("API_KEY", "dev-key")
    DB_PATH: str = os.getenv("DB_PATH", "app.db")
    DEBUG: bool = os.getenv("DEBUG", "0") == "1"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
```

Использование:

```python
from config import Config

print(Config.DB_PATH)
```

---

## 3.5. Связка logging + env

```python
import logging
from config import Config

logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL, logging.INFO),
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
```

Меняешь `LOG_LEVEL=DEBUG` в `.env` — без правки кода.

---

### ✅ Проверь себя — часть 3

1. Почему API key не в коде? → **Утечка через GitHub / скрин / share**.
2. `.env` в git? → **Нет, только `.env.example`**.
3. `os.getenv("X", "default")` — что если переменной нет? → **Вернёт `"default"`**.

---

# Примеры — 12 с разбором

## Пример 1. Аннотация списка

```python
def average(nums: list[float]) -> float:
    if not nums:
        raise ValueError("empty list")
    return sum(nums) / len(nums)
```

**Разбор:** IDE подскажет, что `nums` — числа; `-> float` — результат.

---

## Пример 2. dict | None

```python
def get_item(store: dict[str, int], key: str) -> int | None:
    return store.get(key)
```

**Разбор:** `.get` может вернуть `None` — тип это отражает.

---

## Пример 3. TypedDict для JSON-ответа

```python
from typing import TypedDict


class ErrorBody(TypedDict):
    error: str


def make_error(msg: str) -> ErrorBody:
    return {"error": msg}
```

**Разбор:** единый формат `{"error": "..."}` как в твоём Flask API.

---

## Пример 4. dataclass + hints

```python
from dataclasses import dataclass


@dataclass
class Book:
    id: int
    title: str
    author: str
    year: int | None = None
```

**Разбор:** dataclass (гл. 11) + type hints = понятная модель без ORM.

---

## Пример 5. basicConfig один раз

```python
import logging

logging.basicConfig(level=logging.DEBUG)
logging.debug("only once at program start")
```

**Разбор:** `basicConfig` вызывай **в точке входа** (`if __name__ == "__main__"` или `app.py`), не в каждом модуле.

---

## Пример 6. Лог с плейсхолдерами

```python
logger.info("Created book id=%s title=%s", book_id, title)
```

**Разбор:** `%s` + аргументы — лучше, чем f-string: сообщение **не** форматируется, если уровень отключён.

---

## Пример 7. WARNING при странных данных

```python
if year is not None and year < 0:
    logger.warning("Suspicious year=%s for book %s", year, title)
```

**Разбор:** не падаем, но фиксируем аномалию.

---

## Пример 8. os.environ

```python
import os

port = int(os.environ.get("PORT", "5000"))
```

**Разбор:** env всегда **строки** — приведи к `int` явно.

---

## Пример 9. load_dotenv

```python
from dotenv import load_dotenv
import os

load_dotenv()
assert os.getenv("API_KEY"), "Set API_KEY in .env"
```

**Разбор:** `assert` на старте — fail-fast, если секрет забыли.

---

## Пример 10. Проверка API key (идея auth)

```python
from flask import request, jsonify
from config import Config

def require_api_key():
    key = request.headers.get("X-API-Key", "")
    if key != Config.API_KEY:
        return jsonify({"error": "unauthorized"}), 401
    return None
```

**Разбор:** простейшая защита POST. Полноценный JWT — в гл. 23.

---

## Пример 11. Единый старт приложения

```python
# app.py
import logging
from config import Config

logging.basicConfig(level=Config.LOG_LEVEL)
logger = logging.getLogger(__name__)

def main() -> None:
    logger.info("Starting app db=%s debug=%s", Config.DB_PATH, Config.DEBUG)
    ...

if __name__ == "__main__":
    main()
```

**Разбор:** config → logging → business logic.

---

## Пример 12. Аннотированный CRUD-хелпер

```python
def add_book(title: str, author: str, year: int | None = None) -> int:
    """Insert book, return new id."""
    ...
    return new_id
```

**Разбор:** сигнатура = контракт. В финальном проекте так оформляй `database.py`.

---

# Практика — 6 задач

> Решения пиши в `homework_22.py`. В конце файла — блок `if __name__ == "__main__"` с **assert**-проверками.

---

## Задача 1. Аннотируй функции

Напиши и аннотируй:

```python
def clamp(value: float, low: float, high: float) -> float:
    """Ограничить value диапазоном [low, high]."""
    ...

def word_count(text: str) -> dict[str, int]:
    """Счётчик слов (нижний регистр, split по пробелам)."""
    ...
```

**Проверка:**

```python
assert clamp(15, 0, 10) == 10
assert clamp(-1, 0, 10) == 0
assert word_count("A a b") == {"a": 2, "b": 1}
```

---

## Задача 2. TypedDict User

```python
class User(TypedDict):
    id: int
    name: str
    active: bool

def active_names(users: list[User]) -> list[str]:
    ...
```

**Проверка:** только `active: True`, имена по порядку.

---

## Задача 3. Logger вместо print

Функция `safe_divide(a: float, b: float) -> float | None`:

- при `b == 0` — `logger.error(...)`, вернуть `None`;
- иначе — результат деления и `logger.debug`.

В `main` настрой `logging.basicConfig(level=logging.DEBUG)`.

---

## Задача 4. config из env

Модуль/класс:

- `get_settings() -> dict[str, str | bool]` с ключами `app_name`, `debug` из env:
  - `APP_NAME` (default `"homework22"`)
  - `DEBUG` (`"1"` → True)

Без python-dotenv можно: `os.environ` + в тесте `os.environ["DEBUG"] = "1"`.

---

## Задача 5. .env.example текст

Функция `env_example_text() -> str` возвращает **многострочный** шаблон:

```
APP_NAME=homework22
DEBUG=0
API_KEY=change-me
LOG_LEVEL=INFO
```

(ровно такой текст, можно с финальным `\n`).

---

## Задача 6. Мини-сервис с hygiene

Собери в одном файле:

1. `Config`-подобные константы из env (`API_KEY`, default `"dev"`).
2. `logger = logging.getLogger("hw22")`.
3. `def create_note(text: str, api_key: str) -> dict[str, str | int]:`
   - если `api_key != Config.API_KEY` → `logger.warning` + `raise PermissionError`;
   - если пустой `text` → `raise ValueError("text required")`;
   - иначе `logger.info` и `{"id": 1, "text": text}`.

**Проверка assert-ами** happy path + `pytest.raises` **или** `try/except` в main.

---

# Критерии зачёта гл. 22

- [ ] Задачи 1–3: type hints на всех публичных функциях
- [ ] Задача 3: есть `logging`, не только print
- [ ] Задачи 4–5: env / шаблон без секретов в «коде шаблона»
- [ ] Задача 6: отказ при неверном key + лог
- [ ] `python homework_22.py` без traceback (asserts зелёные)

---

# FAQ

**Q: Нужен mypy?**  
A: На junior достаточно hints в коде. mypy — плюс: `pip install mypy` → `mypy homework_22.py`.

**Q: Pydantic?**  
A: Удобен с FastAPI (гл. 23). Здесь хватит TypedDict + ручная валидация.

**Q: Куда вставить в library_project?**  
A: `config.py` + `logging.basicConfig` в `app.py` + аннотации в `database.py` — уже выглядит как junior, не как «скрипт из туториала».

---

# Что дальше

- **Гл. 23** — FastAPI, пагинация, API key / идея JWT.  
- **Гл. 24** — портфолио: 4 мини-проекта + усиленный capstone.
