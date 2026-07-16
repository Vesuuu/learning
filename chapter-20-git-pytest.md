# Тема: Git и pytest — версии кода и автотесты

> **Формат:** сначала объяснение простыми словами, потом пример с разбором.  
> Не надо зубрить всё сразу — **3 части теории + 12 примеров + 6 задач**.

---

## Цель главы

После прочтения ты понимаешь:

1. **Git** — как сохранять историю кода, работать в ветках и не бояться «сломать всё».
2. **GitHub / remote** — как отправить проект на сервер и работать в команде.
3. **pytest** — как писать автотесты и проверять, что код работает после изменений.

Без Git и тестов сложно работать в команде и проходить собеседования Junior Python.

---

# ЧАСТЬ 1. Git — основы

## 1.1. Зачем Git

Ты меняешь код каждый день. Через неделю: «а что я сломал?» «как вернуть вчерашнюю версию?»

**Git** — система контроля версий:
- **снимки** (коммиты) проекта в разные моменты,
- **ветки** — параллельные линии разработки,
- **откат** к любому коммиту,
- **слияние** изменений от нескольких людей.

---

## 1.2. Аналогия — сохранения в игре

- **Коммит** — сохранение в слот с подписью «добавил логин».
- **Ветка** — отдельная ветка сюжета: в `main` стабильно, в `feature-shop` эксперименты.
- **merge** — объединить две ветки сюжета в одну.

---

## 1.3. Репозиторий и три зоны

| Зона | Смысл |
|------|-------|
| **Working directory** | Файлы на диске, которые ты редактируешь |
| **Staging (index)** | Что **пойдёт** в следующий коммит (`git add`) |
| **Repository (.git)** | История коммитов |

Цикл:
1. Правишь файлы.
2. `git add` — выбираешь изменения.
3. `git commit` — фиксируешь снимок с сообщением.

---

## 1.4. Первые команды

```bash
git init                    # новый репозиторий в папке
git status                  # что изменено
git add file.py             # в staging
git add .                   # все изменения
git commit -m "Add login"   # коммит
git log --oneline           # история
```

**Сообщение коммита** — коротко **что** и **зачем**: `Fix crash on empty input`, не `fix` и не `asdf`.

---

## 1.5. .gitignore

Файлы, которые **не** попадают в Git:

```
__pycache__/
*.pyc
.env
venv/
.idea/
*.db
```

Секреты (`.env` с паролями) и мусор Python — в `.gitignore` **до первого коммита**.

---

## 1.6. diff — что изменилось

```bash
git diff              # unstaged изменения
git diff --staged     # что в staging
```

Перед коммитом полезно просмотреть diff — не закоммитил ли лишнее.

---

### ✅ Проверь себя — часть 1

1. `git add` — куда кладёт изменения? → **В staging**.
2. `git commit` без add новых файлов? → **Не закоммитит не добавленное**.
3. Зачем `.gitignore`? → **Не хранить в Git лишнее и секреты**.

---

# ЧАСТЬ 2. Ветки, merge и remote

## 2.1. Ветки

```bash
git branch              # список веток
git branch feature-x    # создать ветку
git checkout feature-x  # переключиться
git switch feature-x    # то же (новая команда)
git switch -c feature-x # создать и переключиться
```

Обычно:
- **`main`** (или `master`) — стабильная версия,
- **`feature/...`** — новая фича,
- после готовности — **merge** в `main`.

---

## 2.2. Merge — слияние

```bash
git switch main
git merge feature-x
```

Git объединяет истории. Если одни и те же строки меняли в двух ветках — **конфликт**.

---

## 2.3. Конфликт слияния

В файле появляются маркеры:

```
<<<<<<< HEAD
наша версия
=======
их версия
>>>>>>> feature-x
```

Ты **вручную** выбираешь итог, удаляешь маркеры, `git add`, `git commit`.

---

## 2.4. Remote и GitHub

```bash
git remote add origin https://github.com/user/repo.git
git push -u origin main     # отправить ветку на сервер
git pull                      # забрать изменения с сервера
git clone URL                 # скопировать чужой репозиторий
```

**origin** — имя удалённого репозитория по умолчанию.

---

## 2.5. Типичный workflow в команде

1. `git pull` — обновиться.
2. `git switch -c feature/add-api` — ветка под задачу.
3. Код + коммиты.
4. `git push origin feature/add-api`.
5. **Pull Request** на GitHub — ревью коллег.
6. Merge в `main`.

---

## 2.6. Полезные команды

| Команда | Действие |
|---------|----------|
| `git restore file.py` | Отменить изменения в файле (до add) |
| `git restore --staged file.py` | Убрать из staging |
| `git stash` | Временно спрятать изменения |
| `git stash pop` | Вернуть спрятанное |

---

### ✅ Проверь себя — часть 2

1. Зачем ветка feature? → **Изолировать разработку от stable main**.
2. `git push`? → **Отправить коммиты на remote**.
3. Конфликт merge — кто исправляет? → **Разработчик вручную в файле**.

---

# ЧАСТЬ 3. pytest — автотесты

## 3.1. Зачем тесты

Ты поменял функцию — сломалось ли что-то ещё?  
**Автотест** — программа, которая проверяет ожидаемое поведение за секунды.

На работе: CI запускает pytest при каждом push.  
На собеседовании: «напиши функцию и тест к ней».

---

## 3.2. Установка

```bash
pip install pytest
```

Запуск:

```bash
pytest
pytest -v          # подробный вывод
pytest test_file.py
```

---

## 3.3. Первый тест

Файл `test_math.py`:

```python
def add(a, b):
    return a + b

def test_add():
    assert add(2, 3) == 5
    assert add(-1, 1) == 0
```

`assert условие` — если False, тест **падает**.  
Имена функций: **`test_`** в начале — pytest их находит сам.

---

## 3.4. Тест на исключение

```python
import pytest

def divide(a, b):
    if b == 0:
        raise ValueError("zero division")
    return a / b

def test_divide_by_zero():
    with pytest.raises(ValueError):
        divide(10, 0)
```

---

## 3.5. Параметризация — один тест, много входов

```python
import pytest

@pytest.mark.parametrize("a,b,expected", [
    (1, 2, 3),
    (0, 0, 0),
    (-1, 5, 4),
])
def test_add_many(a, b, expected):
    assert add(a, b) == expected
```

Не копируешь один и тот же тест три раза.

---

## 3.6. Тестирование Flask (связь с гл. 19)

```python
def test_ping(client):
    r = client.get("/ping")
    assert r.status_code == 200
    assert r.data == b"pong"
```

`client` — фикстура (ниже). Проверяешь API без ручного клика в браузере.

---

## 3.7. Фикстуры — подготовка данных

```python
import pytest

@pytest.fixture
def sample_list():
    return [1, 2, 3]

def test_len(sample_list):
    assert len(sample_list) == 3
```

Фикстура создаёт данные/объекты перед тестом. DRY для общего setup.

---

## 3.8. monkeypatch — подмена для тестов (нужно для гл. 21)

В **финальном проекте** тесты не должны писать в общий `library.db`. Подменяем путь к БД:

```python
import pytest

@pytest.fixture
def client(tmp_path, monkeypatch):
    import database as db
    test_db = tmp_path / "test.db"
    monkeypatch.setattr(db, "DB_PATH", str(test_db))
    db.init_db()
    from app import app
    return app.test_client()

def test_empty_books(client):
    r = client.get("/api/books")
    assert r.status_code == 200
    assert r.get_json() == []
```

**Разбор:**
- `tmp_path` — pytest даёт **чистую папку** на каждый тест.
- `monkeypatch.setattr(db, "DB_PATH", ...)` — **временно** меняем константу в модуле.
- После теста всё возвращается — другие тесты не ломаются.

Это главный инструмент **главы 21**. Потренируйся в ДЗ 6 ниже.

---

### ✅ Проверь себя — часть 3

1. Имя теста должно начинаться с? → **`test_`**.
2. `pytest.raises`? → **Проверить, что код выбрасывает исключение**.
3. `monkeypatch` зачем? → **Подменить настройки (путь к БД) в тестах**.

---

# Практика — 12 примеров с разбором

---

## Пример 1. Простая функция и assert в REPL

```python
def is_even(n):
    return n % 2 == 0

assert is_even(4) is True
assert is_even(3) is False
print("manual asserts OK")
```

**Вывод:** `manual asserts OK`

**Разбор:** assert в скрипте — мини-проверка. В проекте то же самое оформляют как `test_*` для pytest.

---

## Пример 2. pytest — тест сложения

```python
# test_calc.py
def add(a, b):
    return a + b

def test_add_positive():
    assert add(1, 1) == 2

def test_add_negative():
    assert add(-2, -3) == -5
```

Запуск: `pytest test_calc.py -v`

**Разбор:** два независимых теста. Падение одного не мешает запустить другой (pytest покажет оба результата).

---

## Пример 3. Тест с pytest.raises

```python
import pytest

def parse_age(s):
    age = int(s)
    if age < 0:
        raise ValueError("age must be non-negative")
    return age

def test_valid():
    assert parse_age("25") == 25

def test_negative():
    with pytest.raises(ValueError):
        parse_age("-1")
```

**Разбор:** валидный ввод и граничный случай — отрицательный возраст должен бросать ValueError.

---

## Пример 4. parametrize

```python
import pytest

def slugify(text):
    return text.lower().replace(" ", "-")

@pytest.mark.parametrize("inp,out", [
    ("Hello World", "hello-world"),
    ("Python", "python"),
    ("", ""),
])
def test_slugify(inp, out):
    assert slugify(inp) == out
```

**Разбор:** три кейса — один тестовый шаблон. В отчёте pytest три строки.

---

## Пример 5. Фикстура списка

```python
import pytest

@pytest.fixture
def numbers():
    return [10, 20, 30]

def test_sum(numbers):
    assert sum(numbers) == 60

def test_max(numbers):
    assert max(numbers) == 30
```

**Разбор:** `numbers` создаётся для каждого теста. Не дублируем `[10, 20, 30]` в каждой функции.

---

## Пример 6. Тест функции из «домашки» — palindrome

```python
def is_palindrome(s):
    left, right = 0, len(s) - 1
    while left < right:
        if s[left] != s[right]:
            return False
        left += 1
        right -= 1
    return True

def test_palindrome_true():
    assert is_palindrome("radar") is True

def test_palindrome_false():
    assert is_palindrome("python") is False
```

**Разбор:** тесты к алгоритму из главы 16. Регрессия: если сломаешь функцию — pytest сразу покажет.

---

## Пример 7. Git status (что увидишь в терминале)

```bash
# После правки файла без add:
git status
# On branch main
# Changes not staged for commit:
#   modified:   app.py

git add app.py
git status
# Changes to be committed:
#   modified:   app.py
```

**Разбор:** два состояния — «изменён» и «готов к коммиту». Понимание status избавляет от «я закоммитил, но ничего не ушло».

---

## Пример 8. .gitignore для Python-проекта

```
# .gitignore
__pycache__/
*.py[cod]
venv/
.env
.pytest_cache/
*.db
```

**Разбор:** `__pycache__` и `venv` не нужны в репозитории — у каждого своя копия. `.pytest_cache` — кэш pytest.

---

## Пример 9. Сообщения коммитов — хорошо и плохо

```
# Плохо:
fix
update
asdf
wip

# Хорошо:
Add user registration endpoint
Fix IndexError when list is empty
Update README with install steps
```

**Разбор:** через месяц `git log` должен быть **читаемой историей**, а не загадкой.

---

## Пример 10. Ветка feature — сценарий команд

```bash
git switch main
git pull
git switch -c feature/task-api
# ... правки кода ...
git add .
git commit -m "Add GET /api/tasks endpoint"
git push -u origin feature/task-api
```

**Разбор:** изолированная ветка → коммит → push → Pull Request. `main` остаётся рабочим.

---

## Пример 11. Flask + pytest фикстура client

```python
import pytest
from flask import Flask

@pytest.fixture
def app():
    app = Flask(__name__)

    @app.route("/ping")
    def ping():
        return "pong"

    return app

@pytest.fixture
def client(app):
    return app.test_client()

def test_ping(client):
    r = client.get("/ping")
    assert r.status_code == 200
    assert r.data.decode() == "pong"
```

**Разбор:** фикстура `app` строит приложение, `client` — тестовый HTTP-клиент. Тест из главы 19 в автоматическом виде.

---

## Пример 12. Мини-CI в голове — порядок перед push

```
1. pytest -v          # тесты зелёные
2. git status           # нет лишних файлов
3. git diff             # осознанные изменения
4. git commit -m "..."
5. git push
```

**Разбор:** привычка «тесты → коммит → push» экономит время команды и нервы на ревью.

---

# Шпаргалка

### Git
| Команда | Действие |
|---------|----------|
| `git init` | Новый репо |
| `git add .` | В staging |
| `git commit -m "msg"` | Коммит |
| `git branch` / `git switch` | Ветки |
| `git merge` | Слить ветку |
| `git pull` / `git push` | Синхрон с remote |

### pytest
| Элемент | Смысл |
|---------|-------|
| `def test_...` | Тестовая функция |
| `assert` | Проверка |
| `pytest.raises` | Ожидаемое исключение |
| `@pytest.mark.parametrize` | Много входов |
| `@pytest.fixture` | Общий setup |

---

# FAQ

**Git обязателен?**  
Да, для любой командной разработки.

**Сколько тестов писать?**  
Сначала — на ключевую логику и граничные случаи. 100% coverage не цель Junior.

**unittest vs pytest?**  
В индустрии чаще **pytest** — проще синтаксис. unittest в stdlib, тоже полезно знать.

**Коммитить в main напрямую?**  
В учебе — да. В команде — через ветки и PR.

**Что если забыл .gitignore и закоммитил .env?**  
Смени пароли, удали из истории (git filter / BFG), добавь в .gitignore. Профилактика важнее.

**pytest не находит тесты?**  
Имена `test_*`, файлы `test_*.py` или `*_test.py`.

---

# Домашнее задание

**Файлы:** `homework_20.py` (код функций) и `test_homework_20.py` (тесты pytest)

---

## Задача 1. Функция reverse_string

Напиши `reverse_string(s)`, возвращает строку задом наперёд **без** `s[::-1]` — используй цикл или два указателя.

Проверка вручную: `reverse_string("abc")` → `"cba"`.

---

## Задача 2. Тесты для reverse_string

В `test_homework_20.py` напиши минимум **2** теста:
- обычная строка `"hello"` → `"olleh"`
- пустая строка `""` → `""`

Запуск: `pytest test_homework_20.py -v` — оба зелёные.

---

## Задача 3. Функция unique_sorted

Скопируй логику из главы 16: `unique_sorted(arr)` — уникальные из **отсортированного** списка, один проход.

Тест: `unique_sorted([1, 1, 2, 3, 3])` → `[1, 2, 3]`.

---

## Задача 4. parametrize для unique_sorted

Один тест с `@pytest.mark.parametrize` — минимум **3** набора вход/выход.

Пример строки параметров: `([], [])`, `([5], [5])`, `([1,1,2], [1,2])`.

---

## Задача 5. Функция с ошибкой — clamp

```python
def clamp(value, min_val, max_val):
    """Ограничить value между min_val и max_val."""
    if value < min_val:
        return min_val
    if value > max_val:
        return max_val
    return value
```

Тест `test_clamp_raises` не нужен. Напиши тесты:
- `clamp(5, 0, 10) == 5`
- `clamp(-1, 0, 10) == 0`
- `clamp(99, 0, 10) == 10`

---

## Задача 6. Git на практике + monkeypatch + вывод

**Часть A — Git руками (обязательно):**

1. Создай папку `git_practice/` рядом с домашками.
2. Положи туда `hello.txt` с текстом `hello`.
3. В терминале выполни **реально**:
   ```bash
   cd git_practice
   git init
   git add hello.txt
   git commit -m "First commit"
   git switch -c feature/tests
   ```
4. В `homework_20.py` в комментариях выпиши **эти 4 команды** и вывод `git log --oneline` (1–2 строки).

**Часть B — monkeypatch (обязательно перед гл. 21):** в `test_homework_20.py`:

```python
def test_monkeypatch_db_path(tmp_path, monkeypatch):
    DB_PATH = "MOCK_DB_PATH"
    monkeypatch.setattr("builtins.DB_PATH", DB_PATH, raising=False)  # не сработает — см. ниже
```

Правильный вариант — маленький модуль `demo_db.py`:

```python
# demo_db.py
DB_PATH = "real.db"
```

```python
# в test_homework_20.py
import demo_db

def test_monkeypatch_sets_path(tmp_path, monkeypatch):
    fake = str(tmp_path / "test.db")
    monkeypatch.setattr(demo_db, "DB_PATH", fake)
    assert demo_db.DB_PATH == fake
```

Создай `demo_db.py` рядом с тестом. Это **тот же приём**, что `monkeypatch.setattr(db, "DB_PATH", ...)` в гл. 21.

**Часть C.** В `if __name__ == "__main__":` выведи:
```
reverse_string('abc')
unique_sorted([1, 1, 2, 3, 3])
clamp(99, 0, 10)
```

**Должно вывести:**
```
cba
[1, 2, 3]
10
```

---

## Как сдать

- `homework_20.py` + `test_homework_20.py`
- `pytest test_homework_20.py -v` — все passed
- Сдавай 1–3, потом 4–6

---

# Итог

1. **Git** — add, commit, branch, merge, push, pull, `.gitignore`.
2. **Коммиты** — маленькие, с понятным сообщением.
3. **pytest** — `test_*`, assert, parametrize, fixtures.
4. **Тесты + Git** — основа работы в команде над Python-проектом.

**Следующая глава 21:** финальный проект курса — собрать всё вместе (API + БД + тесты + Git).

---
Конец главы.