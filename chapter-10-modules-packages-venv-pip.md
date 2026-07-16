# Тема: Модули, пакеты, `if __name__`, venv, pip

## Теория

### Что это такое

До сих пор весь код жил в **одном файле** `.py`. Реальные проекты — это **десятки и сотни файлов**. Python организует код через **модули** и **пакеты**.

**Модуль** — любой файл `something.py`. Внутри — функции, классы, переменные. Подключается через `import`:

```python
import math

print(math.sqrt(16))    # 4.0
```

**Пакет** — папка с модулями и файлом `__init__.py` (или namespace package в Python 3.3+). Позволяет группировать код:

```
myproject/
    main.py
    utils/
        __init__.py
        strings.py
        math_helpers.py
```

**Стандартная библиотека** — модули, которые идут с Python: `math`, `json`, `os`, `pathlib`, `datetime`, `random` и сотни других. Устанавливать не нужно.

**Сторонние пакеты** (third-party) — код из PyPI: `requests`, `flask`, `pytest`. Ставятся через **pip** в **виртуальное окружение (venv)**.

---

### Связь с предыдущими главами

| Глава | Что уже знаешь | Как связано с модулями |
|-------|----------------|------------------------|
| 6 | Функции, scope | Функции живут **в модулях**; `import` подключает чужие функции |
| 7 | Comprehensions | `from collections import Counter` — модуль с готовыми инструментами |
| 8 | Файлы, JSON | `import json`, `from pathlib import Path` — stdlib-модули |
| 9 | Исключения | `raise` / `try` в модулях; `json.JSONDecodeError` — ошибка **из модуля** |

**Главная идея:** вместо одного файла на 500 строк — **разбей** на модули по смыслу. Каждый модуль — «глава» проекта.

```
# Было (всё в main.py — 200 строк)
def load_users(): ...
def save_users(): ...
def validate_email(): ...
def main(): ...

# Стало
storage.py      → load / save
validators.py   → validate_email
main.py         → только main() и if __name__
```

---

### `import` — способы подключения

```python
import math                          # весь модуль, math.sqrt()
from math import sqrt, pi            # только sqrt и pi
from math import sqrt as square_root # с псевдонимом
import json as j                     # модуль под коротким именем
```

| Способ | Когда использовать |
|--------|-------------------|
| `import math` | Часто — явно видно, откуда функция |
| `from math import sqrt` | Короткий код, 1–2 имени из модуля |
| `import json as j` | Длинное имя модуля |
| `from math import *` | **Избегай** — засоряет namespace |

**PEP 8 — порядок импортов:**

1. Стандартная библиотека
2. Сторонние пакеты
3. Локальные модули проекта

Между группами — пустая строка.

```python
import json
import math
from pathlib import Path

# import requests   # сторонний — после stdlib

from utils.strings import slugify   # локальный — в конце
```

---

### Как работает `import` «под капотом»

1. Python ищет модуль в **sys.path** — список папок
2. Первая папка — директория **запускаемого скрипта**
3. Потом стандартные пути Python
4. Потом site-packages (куда pip ставит пакеты)
5. Модуль **компилируется и выполняется один раз** — результат кэшируется в `sys.modules`
6. Повторный `import` того же модуля — **не выполняет файл заново**

```python
import sys
print(sys.path[:3])    # первые пути поиска
```

**Импорт = выполнение файла.** Всё на верхнем уровне модуля (не внутри функций) выполняется при первом `import`.

---

### `__name__` и `if __name__ == "__main__"`

У каждого модуля есть атрибут `__name__`:

| Как запущен файл | Значение `__name__` |
|------------------|---------------------|
| Напрямую: `python main.py` | `"__main__"` |
| Импортирован: `import main` | `"main"` (имя модуля) |

**Паттерн entry point** — код «только при прямом запуске»:

```python
def greet(name):
    print(f"Привет, {name}!")

if __name__ == "__main__":
    greet("Anna")
```

- `python mymodule.py` → выполнится `greet("Anna")`
- `import mymodule` → `greet` доступна, но блок `if` **не выполнится**

**Зачем:** один файл = и **библиотека** (импортируемые функции), и **скрипт** (точка входа).

---

### Свой модуль — просто `.py` файл

Структура:

```
lesson10/
    main.py
    helpers.py
```

**helpers.py:**

```python
def double(x):
    return x * 2

PI = 3.14159
```

**main.py:**

```python
import helpers

print(helpers.double(5))    # 10
print(helpers.PI)
```

Или:

```python
from helpers import double, PI

print(double(5))
```

**Важно:** `main.py` и `helpers.py` в **одной папке** (или пакет в sys.path).

---

### Пакеты и `__init__.py`

**Пакет** — папка с модулями. Файл `__init__.py` делает папку пакетом (может быть пустым).

```
myapp/
    __init__.py
    models.py
    services/
        __init__.py
        user_service.py
```

**Импорт из пакета:**

```python
from myapp.services.user_service import create_user
# или
from myapp import models
```

**`__init__.py`** может:
- быть пустым
- реэкспортировать удобный API:

```python
# myapp/__init__.py
from .models import User
from .services.user_service import create_user

__all__ = ["User", "create_user"]
```

Точка в `from .models` — **относительный импорт** внутри пакета.

---

### Относительный vs абсолютный импорт

| Тип | Пример | Где |
|-----|--------|-----|
| Абсолютный | `from myapp.utils import slugify` | Рекомендуется |
| Относительный | `from .utils import slugify` | Только внутри пакета |
| Относительный вверх | `from ..models import User` | Родительский пакет |

На Junior: **предпочитай абсолютные** — проще читать и дебажить.

---

### `__all__` — публичный API модуля

```python
# helpers.py
__all__ = ["double", "triple"]

def double(x):
    return x * 2

def triple(x):
    return x * 3

def _internal():
    pass    # не в __all__ — «приватная» по соглашению
```

`from helpers import *` импортирует только имена из `__all__` (если `__all__` задан).

---

### Виртуальное окружение (venv)

**Проблема без venv:** все `pip install` попадают в **глобальный** Python. Проекты конфликтуют по версиям пакетов.

**venv** — изолированная копия Python + своя папка `site-packages` для проекта.

**Создание (Windows PowerShell):**

```powershell
python -m venv venv
```

**Активация:**

```powershell
.\venv\Scripts\Activate.ps1
```

После активации в начале строки терминала появится `(venv)`.

**Деактивация:**

```powershell
deactivate
```

**Что внутри venv:**
- `Scripts/python.exe` — интерпретатор
- `Scripts/pip.exe` — pip для этого окружения
- `Lib/site-packages/` — установленные пакеты

**Правило:** один проект = один venv. Папку `venv/` **не коммитят** в Git (добавляют в `.gitignore`).

---

### pip — менеджер пакетов

**pip** устанавливает пакеты с [PyPI](https://pypi.org).

| Команда | Что делает |
|---------|------------|
| `pip install requests` | Установить пакет |
| `pip install requests==2.31.0` | Конкретная версия |
| `pip uninstall requests` | Удалить |
| `pip list` | Список установленных |
| `pip show requests` | Информация о пакете |
| `pip freeze` | Список с версиями для requirements |
| `pip install -r requirements.txt` | Установить всё из файла |

**requirements.txt** — список зависимостей проекта:

```
requests==2.31.0
flask>=3.0.0
pytest
```

Команды для фиксации окружения:

```powershell
pip freeze > requirements.txt
pip install -r requirements.txt
```

**Всегда активируй venv** перед `pip install`.

#### Дополнительные команды pip (полезно знать)

| Команда | Зачем |
|---------|-------|
| `pip install --upgrade pip` | Обновить сам pip |
| `pip install "flask>=3.0,<4.0"` | Диапазон версий |
| `pip install -r requirements.txt --upgrade` | Обновить все зависимости |
| `python -m pip install requests` | То же, но явно через текущий Python |
| `pip cache purge` | Очистить кэш скачанных пакетов |

**requirements.txt vs requirements-dev.txt:**
- `requirements.txt` — для продакшена / деплоя
- `requirements-dev.txt` — pytest, black, линтеры (только для разработки)

---

### Стандартная библиотека — модули, которые стоит знать Junior

| Модуль | Для чего | Пример |
|--------|----------|--------|
| `math` | Математика | `math.sqrt`, `math.ceil` |
| `random` | Случайные числа | `random.randint`, `random.choice` |
| `datetime` | Даты и время | `datetime.now()`, `timedelta` |
| `json` | JSON ↔ Python | `json.loads`, `json.dump` |
| `pathlib` | Пути к файлам | `Path("data") / "file.txt"` |
| `os` | ОС, cwd, env | `os.getcwd()`, `os.environ` |
| `sys` | Интерпретатор | `sys.argv`, `sys.path`, `sys.executable` |
| `collections` | Расширенные структуры | `Counter`, `defaultdict` |
| `re` | Регулярные выражения | `re.search`, `re.findall` |
| `itertools` | Итераторы | `chain`, `combinations` |
| `functools` | Декораторы, partial | `functools.wraps` (гл. 14) |
| `typing` | Подсказки типов | `list[str]`, `Optional[int]` |
| `logging` | Логи вместо print | `logging.info(...)` |
| `argparse` | CLI-аргументы | `--file`, `--verbose` |
| `unittest` / `pytest`* | Тесты | `assert`, `pytest` — сторонний |

\* `pytest` ставится через pip, не встроен.

**Как найти модуль:** [docs.python.org/3/library](https://docs.python.org/3/library/) — полный список stdlib.

---

### Типичная структура Python-проекта (Junior → Middle)

**Маленький скрипт (1–3 файла):**

```
my_script/
    main.py
    helpers.py
    requirements.txt
    venv/              ← не в Git
    .gitignore
```

**Мини-приложение с пакетом:**

```
todo_app/
    README.md
    requirements.txt
    .gitignore
    .env.example       ← шаблон переменных (без секретов!)
    main.py            ← точка входа
    todo_app/          ← пакет приложения
        __init__.py
        models.py
        storage.py
        validators.py
    tests/
        __init__.py
        test_validators.py
    data/
        tasks.json
```

**Правила именования:**
- Файлы и папки: `snake_case`
- Пакет приложения: короткое имя без дефисов (`todo_app`, не `todo-app`)
- Точка входа: `main.py` или `cli.py`

**Папка `tests/`** — отдельный пакет с тестами. Импортирует код из проекта:

```python
from todo_app.validators import validate_task
```

---

### `__pycache__` и `.pyc` — что это

При первом `import` Python компилирует `.py` → **байт-код** `.pyc` и кладёт в `__pycache__/`.

```
myapp/
    helpers.py
    __pycache__/
        helpers.cpython-312.pyc
```

- Ускоряет повторный запуск
- **Не редактируй** `.pyc` вручную
- **Не коммить** `__pycache__/` в Git
- При изменении `.py` Python перекомпилирует автоматически

Удалить кэш: просто удали папки `__pycache__` — безвредно.

---

### `PYTHONPATH` — добавить папку в поиск модулей

По умолчанию Python ищет модули в `sys.path`. Можно добавить папку через переменную окружения:

```powershell
$env:PYTHONPATH = "C:\projects\shared_libs"
python main.py
```

Или в коде (редко, для скриптов):

```python
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent / "lib"))
```

На Junior **лучше** правильная структура пакета, чем хаки с `sys.path`.

---

### Где это применяется в реальной разработке

| Ситуация | Решение |
|----------|---------|
| Разбить большой скрипт | Модули `utils/`, `models/` |
| Переиспользуемые функции | Свой пакет + `import` |
| Тесты отдельно от кода | `pytest` в venv, `tests/` пакет |
| Деплой на сервер | `requirements.txt` + `pip install -r` |
| CLI-утилита | `if __name__ == "__main__"` + `argparse` |
| Flask/FastAPI проект | Пакет `app/` с `__init__.py` |

---

### Микро-моменты, нюансы, частые ошибки новичков

#### 1. Запуск файла не из той папки

```powershell
cd C:\projects\myapp
python main.py    # OK — main.py и helpers.py рядом
```

Если `cd` в другую папку — `import helpers` может не найтись.

#### 2. Имя файла = имя модуля

`my-utils.py` — **нельзя** импортировать нормально (дефис). Используй `my_utils.py`.

#### 3. Не путай модуль и переменную

```python
import json
json = {"a": 1}    # затёр модуль! json.dumps сломается
```

#### 4. Циклический импорт

`a.py` импортирует `b.py`, `b.py` импортирует `a.py` → `ImportError`. Решение: вынести общее в третий модуль.

#### 5. `from module import *` — плохая практика

Неясно, какие имена появились в namespace. Явные импорты лучше.

#### 6. venv не активирован — pip ставит «не туда»

Проверка: `where python` (Windows) — путь должен быть внутри `venv\Scripts\`.

#### 7. Коммитить venv в Git — нельзя

Тяжёлая папка, привязана к ОС. Коммить `requirements.txt`.

#### 8. `if __name__` — не обязателен, но стандарт

Без него при `import` выполнится весь код файла — тесты, print, side effects.

#### 9. `python -m package.module`

Запуск модуля как скрипта с правильным `sys.path`:

```powershell
python -m myapp.main
```

#### 10. Встроенные vs установленные

`math`, `json` — встроены. `requests` — нужен `pip install requests`.

#### 11. Имя `main.py` vs имя пакета

Если и пакет, и файл называются `todo_app` — путаница. Решение: `main.py` снаружи, пакет `todo_app/` внутри.

#### 12. Импорт из родительской папки без пакета

```python
# Не сработает, если main.py в корне, а utils/ не в sys.path
from utils.helpers import double   # ModuleNotFoundError
```

Запускай из корня проекта или оформи `utils/` как пакет с `__init__.py`.

#### 13. Дублирование имени модуля

Файл `json.py` в проекте **затрёт** стандартный `json` при `import json`. Не называй модули как stdlib.

#### 14. `pip freeze` тянет ВСЁ

В freeze попадают транзитивные зависимости (зависимости зависимостей). Для учебного проекта — OK. В проде иногда чистят вручную.

#### 15. Активация venv в CMD vs PowerShell

| Shell | Активация |
|-------|-----------|
| PowerShell | `.\venv\Scripts\Activate.ps1` |
| CMD | `venv\Scripts\activate.bat` |
| Git Bash | `source venv/Scripts/activate` |

Если PowerShell блокирует скрипт — `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`.

---

## Практика

> **Маршрут ученика:** 38 примеров — **не всё сразу**.  
> | Цель | Достаточно примеров |
> |------|---------------------|
> | Домашка 1–5 | **1–12** |
> | venv, pip (задачи 6–7) | **22–26** + раздел теории venv |
> | Пакеты (задачи 8+) | **13–21**, **27** (todo_mini) |
> | re, logging, argparse | справочно, не для первого прохода |

### Пример 1: `import math` — стандартная библиотека

```python
import math

print(math.sqrt(25))
print(math.pi)
print(math.ceil(4.2))
print(math.floor(4.8))
```

**Вывод консоли:**

```
5.0
3.141592653589793
5
4
```

**Разбор:** Модуль `math` входит в стандартную библиотеку Python — его не нужно устанавливать отдельно. `sqrt(25)` даёт 5.0, `ceil` округляет вверх (4.2 → 5), `floor` — вниз (4.8 → 4). Константа `pi` хранится в модуле и доступна как `math.pi`.

---

### Пример 2: `from math import ...` — выборочный импорт

```python
from math import sqrt, pow, pi

print(sqrt(9))
print(pow(2, 10))
print(round(pi, 4))
```

**Вывод консоли:**

```
3.0
1024.0
3.1416
```

**Разбор:** Конструкция `from math import sqrt, pow, pi` подтягивает только нужные имена — пишем `sqrt(9)` без префикса `math.`. `pow(2, 10)` возводит 2 в степень 10 и даёт 1024.0. Такой импорт удобен, когда функций немного и конфликтов имён нет.

---

### Пример 3: Псевдоним модуля — `import json as j`

```python
import json as j

data = {"name": "Anna", "skills": ["Python", "SQL"]}
text = j.dumps(data, ensure_ascii=False)
restored = j.loads(text)

print(text)
print(restored["skills"])
```

**Вывод консоли:**

```
{"name": "Anna", "skills": ["Python", "SQL"]}
['Python', 'SQL']
```

**Разбор:** Запись `import json as j` задаёт короткий псевдоним — дальше вызываем `j.dumps` и `j.loads`. `dumps` превращает словарь в JSON-строку, `loads` восстанавливает его обратно. Список `skills` после `loads` остаётся обычным списком Python.

---

### Пример 4: Несколько модулей в одном скрипте

```python
import math
import random
from datetime import datetime

numbers = [random.randint(1, 100) for _ in range(5)]
print("Числа:", numbers)
print("Сумма:", sum(numbers))
print("Макс:", max(numbers))
print("√макс:", round(math.sqrt(max(numbers)), 2))
print("Сейчас:", datetime.now().strftime("%Y-%m-%d %H:%M"))
```

**Вывод консоли (примерно):**

```
Числа: [42, 17, 88, 3, 61]
Сумма: 211
Макс: 88
√макс: 9.38
Сейчас: 2026-07-14 15:30
```

**Разбор:** В одном скрипте спокойно сочетают модули из стандартной библиотеки: `random` генерирует числа, `math` считает корень, `datetime` форматирует время. Сумма и максимум считаются из уже сгенерированного списка. Дата и время в выводе зависят от момента запуска.

---

### Пример 5: `dir()` и `help()` — исследование модуля

```python
import math

print("sqrt" in dir(math))
print([name for name in dir(math) if not name.startswith("_")][:8])
help(math.sqrt)
```

**Вывод консоли (сокращённо):**

```
True
['acos', 'acosh', 'asin', 'asinh', 'atan', 'atan2', 'atanh', 'ceil']
Help on built-in function sqrt in module math:
...
```

**Разбор:** Функция `dir(math)` показывает все имена внутри модуля — фильтр убирает служебные, начинающиеся с `_`. Проверка `"sqrt" in dir(math)` подтверждает, что функция там есть. `help()` выводит встроенную документацию прямо в консоль — полезно, когда забыли сигнатуру.

---

### Пример 6: `__name__` при прямом запуске

```python
print(f"Текущий модуль: __name__ = {__name__!r}")

if __name__ == "__main__":
    print("Файл запущен напрямую")
else:
    print("Файл импортирован как модуль")
```

**Вывод консоли (при `python example06.py`):**

```
Текущий модуль: __name__ = '__main__'
Файл запущен напрямую
```

**Разбор:** При прямом запуске файла переменная `__name__` равна `'__main__'`. Условие `if __name__ == "__main__"` срабатывает только в этом случае. Если тот же файл импортировать как модуль, выполнилась бы ветка `else` — код демо не запустился бы сам.

---

### Пример 7: Паттерн `if __name__ == "__main__"` — функции + main

```python
def celsius_to_fahrenheit(c):
    return c * 9 / 5 + 32

def fahrenheit_to_celsius(f):
    return (f - 32) * 5 / 9

def demo():
    for c in [0, 20, 37]:
        f = celsius_to_fahrenheit(c)
        print(f"{c}°C = {f:.1f}°F")

if __name__ == "__main__":
    demo()
```

**Вывод консоли:**

```
0°C = 32.0°F
20°C = 68.0°F
37°C = 98.6°F
```

**Разбор:** Функции перевода определены на уровне модуля, а `demo()` вызывается только при запуске файла напрямую. Формула °C→°F: умножить на 9/5 и прибавить 32. Так отделяют переиспользуемый код от демонстрации и тестов.

---

### Пример 8: `random` — модуль для случайных чисел

```python
import random

random.seed(42)    # фиксируем для воспроизводимости

print(random.randint(1, 6))
print(random.choice(["орёл", "решка"]))
print(random.sample(range(1, 11), 3))
print(round(random.uniform(0, 1), 3))
```

**Вывод консоли:**

```
1
решка
[1, 2, 10]
0.864
```

**Разбор:** Вызов `random.seed(42)` фиксирует последовательность — при том же seed вывод повторится. `randint`, `choice`, `sample` и `uniform` — разные способы получить случайные значения. Без `seed` результаты менялись бы при каждом запуске.

---

### Пример 9: `datetime` — даты и время

```python
from datetime import datetime, date, timedelta

today = date.today()
print("Сегодня:", today)

now = datetime.now()
print("Сейчас:", now.strftime("%d.%m.%Y %H:%M:%S"))

deadline = today + timedelta(days=14)
print("Через 2 недели:", deadline)
```

**Вывод консоли (дата зависит от запуска):**

```
Сегодня: 2026-07-14
Сейчас: 14.07.2026 15:30:00
Через 2 недели: 2026-07-28
```

**Разбор:** `date.today()` возвращает только дату, `datetime.now()` — дату и время вместе. Метод `strftime` форматирует вывод по шаблону (`%d.%m.%Y` и т.д.). `timedelta(days=14)` прибавляет 14 дней к сегодняшней дате — удобно для дедлайнов.

---

### Пример 10: `collections.Counter` — подсчёт элементов

```python
from collections import Counter

words = ["apple", "banana", "apple", "cherry", "banana", "apple"]
counts = Counter(words)

print(counts)
print("Самое частое:", counts.most_common(1))
print("Только apple:", counts["apple"])
```

**Вывод консоли:**

```
Counter({'apple': 3, 'banana': 2, 'cherry': 1})
Самое частое: [('apple', 3)]
Только apple: 3
```

**Разбор:** Класс `Counter` считает, сколько раз встретился каждый элемент списка. `most_common(1)` возвращает самый частый элемент — здесь `apple` с тремя вхождениями. Обращение `counts["apple"]` сразу даёт готовое число без ручного подсчёта в цикле.

---

### Пример 11: `pathlib` — работа с путями (модуль)

```python
from pathlib import Path

script_dir = Path(__file__).parent
data_file = script_dir / "data" / "notes.txt"

data_file.parent.mkdir(parents=True, exist_ok=True)
data_file.write_text("Заметка из pathlib\n", encoding="utf-8")

print("Путь:", data_file)
print("Существует:", data_file.exists())
print("Содержимое:", data_file.read_text(encoding="utf-8").strip())
```

**Вывод консоли:**

```
Путь: ...\data\notes.txt
Существует: True
Содержимое: Заметка из pathlib
```

**Разбор:** Выражение `Path(__file__).parent` указывает на папку, где лежит скрипт. Оператор `/` собирает путь `data/notes.txt` относительно неё. `mkdir` создаёт папку, `write_text` записывает файл, `read_text` читает его обратно — всё через один объект `Path`.

---

### Пример 12: `os` и `sys` — системная информация

```python
import os
import sys

print("Платформа:", sys.platform)
print("Версия Python:", sys.version.split()[0])
print("Текущая папка (cwd):", os.getcwd())
print("Аргументы командной строки:", sys.argv)
```

**Вывод консоли (примерно):**

```
Платформа: win32
Версия Python: 3.12.x
Текущая папка (cwd): C:\Users\...
Аргументы командной строки: ['example12.py']
```

**Разбор:** `sys.platform` показывает операционную систему (`win32` на Windows). `sys.version` — версия интерпретатора Python. `os.getcwd()` возвращает текущую рабочую папку, а `sys.argv` — список аргументов командной строки (первый элемент — имя скрипта).

---

### Пример 13: Свой модуль — структура двух файлов

**Файл `text_utils.py`:**

```python
def slugify(text):
    return text.lower().strip().replace(" ", "-")

def truncate(text, max_len=50):
    if len(text) <= max_len:
        return text
    return text[: max_len - 3] + "..."
```

**Файл `main_13.py` (в той же папке):**

```python
import text_utils

title = "  Hello Python World  "
print(text_utils.slugify(title))
print(text_utils.truncate("A" * 60, 20))
```

**Вывод консоли:**

```
hello-python-world
AAAAAAAAAAAAAAAAA...
```

---

### Пример 14: `from module import function` — короткий синтаксис

```python
# Предположим text_utils.py из Примера 13 рядом

from text_utils import slugify, truncate

print(slugify("Junior Python Developer"))
print(truncate("Модули упрощают структуру проекта", 15))
```

**Вывод консоли:**

```
junior-python-developer
Модули упроща...
```

---

### Пример 15: Импорт с псевдонимом функции

```python
from datetime import datetime as dt

def log(message):
    timestamp = dt.now().strftime("%H:%M:%S")
    print(f"[{timestamp}] {message}")

log("Приложение запущено")
log("Обработка данных")
```

**Вывод консоли:**

```
[15:30:01] Приложение запущено
[15:30:01] Обработка данных
```

---

### Пример 16: `sys.path` — где Python ищет модули

```python
import sys

print("Первые 4 пути поиска модулей:")
for i, path in enumerate(sys.path[:4]):
    print(f"  {i}: {path}")

print("\n'math' в sys.modules:", "math" in sys.modules)
import math
print("После import math:", "math" in sys.modules)
```

**Вывод консоли (пути зависят от системы):**

```
Первые 4 пути поиска модулей:
  0: C:\...\lesson10
  1: C:\...\Python312\python312.zip
  ...

'math' в sys.modules: False
После import math: True
```

---

### Пример 17: Повторный import не выполняет модуль заново

```python
# counter_mod.py — отдельный файл:
# _counter = 0
# _counter += 1
# print(f"counter_mod загружен, счётчик = {_counter}")

import counter_mod
import counter_mod
import counter_mod

print("Импортировали три раза — сообщение выше одно")
```

**Вывод консоли (если есть counter_mod.py):**

```
counter_mod загружен, счётчик = 1
Импортировали три раза — сообщение выше одно
```

*(Для демо создай `counter_mod.py` с кодом из комментария)*

---

### Пример 18: `__all__` — контроль `from module import *`

**Файл `greeters.py`:**

```python
__all__ = ["hello", "bye"]

def hello(name):
    return f"Привет, {name}!"

def bye(name):
    return f"Пока, {name}!"

def _secret():
    return "не для export"
```

**Файл `main_18.py`:**

```python
from greeters import *

print(hello("Anna"))
print(bye("Bob"))
try:
    print(_secret())
except NameError as e:
    print("NameError:", e)
```

**Вывод консоли:**

```
Привет, Anna!
Пока, Bob!
NameError: name '_secret' is not defined
```

---

### Пример 19: Пакет — структура папок

```
shop/
    __init__.py
    products.py
    cart.py
```

**`shop/products.py`:**

```python
PRODUCTS = {
    1: {"name": "Книга", "price": 500},
    2: {"name": "Ручка", "price": 50},
}

def get_product(product_id):
    return PRODUCTS.get(product_id)
```

**`shop/cart.py`:**

```python
def total(items):
    return sum(item["price"] * item["qty"] for item in items)
```

**`shop/__init__.py`:**

```python
from .products import get_product, PRODUCTS
from .cart import total
```

**`main_19.py`:**

```python
from shop import get_product, total

item = get_product(1)
items = [{"name": item["name"], "price": item["price"], "qty": 2}]
print(f"Товар: {item['name']}, сумма: {total(items)} руб.")
```

**Вывод консоли:**

```
Товар: Книга, сумма: 1000 руб.
```

---

### Пример 20: Относительный импорт внутри пакета

**`shop/inventory.py`:**

```python
from .products import PRODUCTS

def list_names():
    return [p["name"] for p in PRODUCTS.values()]
```

**`main_20.py`:**

```python
from shop.inventory import list_names

print("На складе:", ", ".join(list_names()))
```

**Вывод консоли:**

```
На складе: Книга, Ручка
```

---

### Пример 21: `if __name__` в модуле-библиотеке

**`calculator.py`:**

```python
def add(a, b):
    return a + b

def mul(a, b):
    return a * b

def _run_self_test():
    assert add(2, 3) == 5
    assert mul(4, 5) == 20
    print("Все тесты calculator.py пройдены")

if __name__ == "__main__":
    _run_self_test()
```

**Запуск:**

```powershell
python calculator.py    # тесты
```

**Импорт:**

```python
from calculator import add
print(add(10, 1))    # тесты НЕ запускаются
```

**Вывод при `python calculator.py`:**

```
Все тесты calculator.py пройдены
```

---

### Пример 22: `sys.argv` — аргументы командной строки

```python
import sys

def main():
    if len(sys.argv) < 2:
        print("Использование: python greet_cli.py <имя>")
        return
    name = sys.argv[1]
    print(f"Привет, {name}!")

if __name__ == "__main__":
    main()
```

**Запуск:**

```powershell
python greet_cli.py Anna
```

**Вывод консоли:**

```
Привет, Anna!
```

---

### Пример 23: Опциональный импорт — graceful fallback

```python
try:
    import rich
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

def print_status(message, level="info"):
    if HAS_RICH:
        rich.print(f"[bold]{level}[/bold]: {message}")
    else:
        print(f"{level.upper()}: {message}")

print_status("Модуль rich не обязателен", "info")
print("HAS_RICH =", HAS_RICH)
```

**Вывод консоли (без rich):**

```
INFO: Модуль rich не обязателен
HAS_RICH = False
```

---

### Пример 24: `importlib` — динамический импорт по имени

```python
import importlib

module_name = "math"
math = importlib.import_module(module_name)

print(math.sqrt(64))
print(type(math))
```

**Вывод консоли:**

```
8.0
<class 'module'>
```

---

### Пример 25: `requirements.txt` — формат и смысл

**Файл `requirements.txt`:**

```
# Зависимости проекта todo-api
requests>=2.28.0,<3.0.0
python-dotenv==1.0.0
pytest>=7.0.0
```

**Команды (в активированном venv):**

```powershell
pip install -r requirements.txt
pip freeze > requirements-lock.txt
```

Смысл:
- `==` — точная версия (воспроизводимость)
- `>=` — минимум
- `package>=1.0,<2.0` — диапазон

---

### Пример 26: Создание venv — пошагово (терминал)

```powershell
# 1. Перейти в папку проекта
cd C:\projects\myapp

# 2. Создать venv
python -m venv venv

# 3. Активировать (Windows PowerShell)
.\venv\Scripts\Activate.ps1

# 4. Обновить pip (опционально)
python -m pip install --upgrade pip

# 5. Установить пакет
pip install requests

# 6. Проверить
pip show requests
python -c "import requests; print(requests.__version__)"
```

**Признак успеха:** `where python` указывает на `...\myapp\venv\Scripts\python.exe`.

---

### Пример 27: Мини-проект — разбиение на модули

**Структура:**

```
todo_mini/
    main.py
    storage.py
    validators.py
```

**`validators.py`:**

```python
class ValidationError(Exception):
    pass

def validate_task(title):
    title = title.strip()
    if not title:
        raise ValidationError("Название не может быть пустым")
    if len(title) > 100:
        raise ValidationError("Максимум 100 символов")
    return title
```

**`storage.py`:**

```python
import json
from pathlib import Path

DATA_FILE = Path(__file__).parent / "tasks.json"

def load_tasks():
    if not DATA_FILE.exists():
        return []
    return json.loads(DATA_FILE.read_text(encoding="utf-8"))

def save_tasks(tasks):
    DATA_FILE.write_text(
        json.dumps(tasks, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
```

**`main.py`:**

```python
from storage import load_tasks, save_tasks
from validators import validate_task, ValidationError

def add_task(title):
    try:
        title = validate_task(title)
    except ValidationError as e:
        print(f"Ошибка: {e}")
        return
    tasks = load_tasks()
    tasks.append({"id": len(tasks) + 1, "title": title, "done": False})
    save_tasks(tasks)
    print(f"Добавлено: {title}")

if __name__ == "__main__":
    add_task("  Изучить модули Python  ")
    add_task("")
    print("Все задачи:", load_tasks())
```

**Вывод консоли:**

```
Добавлено: Изучить модули Python
Ошибка: Название не может быть пустым
Все задачи: [{'id': 1, 'title': 'Изучить модули Python', 'done': False}]
```

---

### Пример 28: `.gitignore` для Python-проекта

**Файл `.gitignore` (фрагмент):**

```
# Виртуальное окружение
venv/
.venv/
env/

# Кэш Python
__pycache__/
*.py[cod]

# Локальные данные
*.json
!tasks.example.json

# IDE
.idea/
.vscode/
```

**Смысл:** в Git — код и `requirements.txt`, **не** venv и `__pycache__`.

---

### Пример 29: `__file__` — путь к текущему модулю

```python
from pathlib import Path

def get_module_dir():
    return Path(__file__).resolve().parent

module_dir = get_module_dir()
config_path = module_dir / "config" / "settings.json"

print("Модуль лежит в:", module_dir)
print("Конфиг рядом с кодом:", config_path)
```

**Вывод консоли (пути зависят от запуска):**

```
Модуль лежит в: C:\projects\myapp
Конфиг рядом с кодом: C:\projects\myapp\config\settings.json
```

**Зачем:** относительные пути `"data/file.txt"` зависят от cwd. Путь через `__file__` — **от папки модуля**, стабильнее.

---

### Пример 30: Полный пайплайн — venv + pip + import стороннего пакета

**Шаг 1 — терминал:**

```powershell
mkdir weather_app
cd weather_app
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install requests
pip freeze > requirements.txt
```

**Шаг 2 — `weather_app/client.py`:**

```python
import sys

def check_requests():
    try:
        import requests
    except ImportError:
        print("Установи: pip install requests")
        print("Python:", sys.executable)
        return None
    print("requests", requests.__version__)
    print("Python:", sys.executable)
    return requests

if __name__ == "__main__":
    check_requests()
```

**Вывод консоли (в активированном venv):**

```
requests 2.32.x
Python: C:\...\weather_app\venv\Scripts\python.exe
```

**Шаг 3 — `requirements.txt` (создан pip freeze):**

```
requests==2.32.3
certifi==2024.x.x
...
```

На другом ПК: `pip install -r requirements.txt` — те же версии.

---

### Пример 31: `re` — регулярные выражения (модуль stdlib)

```python
import re

text = "Email: anna@mail.com и bob@test.org"

emails = re.findall(r"[\w.+-]+@[\w-]+\.[\w.-]+", text)
print("Emails:", emails)

match = re.search(r"(\w+)@(\w+)", "user@domain.com")
if match:
    print("Логин:", match.group(1))
    print("Домен:", match.group(2))
```

**Вывод консоли:**

```
Emails: ['anna@mail.com', 'bob@test.org']
Логин: user
Домен: domain
```

---

### Пример 32: `itertools` — цепочка и комбинации

```python
from itertools import chain, combinations

list1 = [1, 2]
list2 = [3, 4]
merged = list(chain(list1, list2))
print("chain:", merged)

pairs = list(combinations(["A", "B", "C"], 2))
print("combinations:", pairs)
```

**Вывод консоли:**

```
chain: [1, 2, 3, 4]
combinations: [('A', 'B'), ('A', 'C'), ('B', 'C')]
```

---

### Пример 33: `functools.partial` — частичное применение

```python
from functools import partial

def power(base, exponent):
    return base ** exponent

square = partial(power, exponent=2)
cube = partial(power, exponent=3)

print(square(5))
print(cube(5))
```

**Вывод консоли:**

```
25
125
```

---

### Пример 34: `argparse` — CLI с аргументами

```python
import argparse

def main():
    parser = argparse.ArgumentParser(description="Приветствие по имени")
    parser.add_argument("name", help="Имя пользователя")
    parser.add_argument("--loud", action="store_true", help="Крикнуть")
    args = parser.parse_args(["Anna", "--loud"])

    message = f"Привет, {args.name}!"
    if args.loud:
        message = message.upper()
    print(message)

if __name__ == "__main__":
    main()
```

**Вывод консоли:**

```
ПРИВЕТ, ANNA!
```

*(В реальном запуске: `python greet.py Anna --loud`)*

---

### Пример 35: `logging` — логи вместо print

```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    datefmt="%H:%M:%S",
)

def process_data(items):
    logging.info("Старт обработки, элементов: %d", len(items))
    if not items:
        logging.warning("Пустой список!")
        return []
    logging.debug("Детали: %s", items)
    return [x * 2 for x in items]

process_data([1, 2, 3])
process_data([])
```

**Вывод консоли:**

```
15:30:01 [INFO] Старт обработки, элементов: 3
15:30:01 [INFO] Старт обработки, элементов: 0
15:30:01 [WARNING] Пустой список!
```

---

### Пример 36: Структура `tests/` — тесты отдельным пакетом

**`calc.py`:**

```python
def add(a, b):
    return a + b

def divide(a, b):
    if b == 0:
        raise ValueError("Делитель не может быть 0")
    return a / b
```

**`tests/test_calc.py`:**

```python
from calc import add, divide

def test_add():
    assert add(2, 3) == 5

def test_divide():
    assert divide(10, 2) == 5

def test_divide_by_zero():
    try:
        divide(1, 0)
        assert False, "Ожидали ValueError"
    except ValueError as e:
        assert "0" in str(e)

if __name__ == "__main__":
    test_add()
    test_divide()
    test_divide_by_zero()
    print("Все тесты пройдены")
```

**Вывод консоли:**

```
Все тесты пройдены
```

---

### Пример 37: Циклический импорт — проблема и решение

**Плохо — `a.py` импортирует `b.py`, `b.py` импортирует `a.py`:**

```
a.py → import b → b.py → import a → a ещё не готов → ImportError
```

**Хорошо — вынести общее в `common.py`:**

**`common.py`:**

```python
TAX_RATE = 0.2

def apply_tax(price):
    return price * (1 + TAX_RATE)
```

**`cart.py`:**

```python
from common import apply_tax

def total(prices):
    return sum(apply_tax(p) for p in prices)
```

**`invoice.py`:**

```python
from common import TAX_RATE, apply_tax

def format_invoice(price):
    return f"Итого с НДС {TAX_RATE*100:.0f}%: {apply_tax(price):.2f}"
```

**`main_37.py`:**

```python
from cart import total
from invoice import format_invoice

prices = [100, 200]
print("Сумма:", total(prices))
print(format_invoice(100))
```

**Вывод консоли:**

```
Сумма: 360.0
Итого с НДС 20%: 120.00
```

---

### Пример 38: Полный каркас проекта — все части вместе

```
bookstore/
    .gitignore
    requirements.txt
    README.md
    main.py
    bookstore/
        __init__.py
        models.py
        catalog.py
    tests/
        test_catalog.py
```

**`bookstore/models.py`:**

```python
class Book:
    def __init__(self, title, price):
        self.title = title
        self.price = price
```

**`bookstore/catalog.py`:**

```python
from .models import Book

_catalog = []

def add_book(title, price):
    _catalog.append(Book(title, price))

def list_books():
    return [(b.title, b.price) for b in _catalog]
```

**`bookstore/__init__.py`:**

```python
from .catalog import add_book, list_books
from .models import Book

__all__ = ["Book", "add_book", "list_books"]
```

**`main.py`:**

```python
from bookstore import add_book, list_books

def main():
    add_book("Python Crash Course", 1500)
    add_book("Clean Code", 1200)
    for title, price in list_books():
        print(f"  {title}: {price} руб.")

if __name__ == "__main__":
    main()
```

**`.gitignore`:**

```
venv/
__pycache__/
*.pyc
.env
```

**`requirements.txt`:**

```
# Пока только stdlib — файл для привычки структуры
```

**Вывод консоли:**

```
  Python Crash Course: 1500 руб.
  Clean Code: 1200 руб.
```

**Это шаблон** — так выглядит «настоящий» мини-проект перед Flask/FastAPI.

---

## Шпаргалка

```python
import math
from math import sqrt
from math import sqrt as sq
import json as j

if __name__ == "__main__":
    main()

# Свой модуль: file.py рядом → import file
# Пакет: folder/__init__.py → from folder import module

__all__ = ["public_func"]

# Терминал
# python -m venv venv
# .\venv\Scripts\Activate.ps1    # Windows
# pip install package
# pip freeze > requirements.txt
# pip install -r requirements.txt
```

| Команда | Назначение |
|---------|------------|
| `python -m venv venv` | Создать окружение |
| `.\venv\Scripts\Activate.ps1` | Активировать (Win) |
| `deactivate` | Выйти из venv |
| `pip install pkg` | Установить пакет |
| `pip freeze` | Список с версиями |
| `python -m pip install -r requirements.txt` | Установить зависимости |

### Таблица: какой import когда

| Ситуация | Рекомендация |
|----------|--------------|
| 1–2 функции из модуля | `from math import sqrt, pi` |
| Много вызовов из модуля | `import math` |
| Конфликт имён | `import json as j` |
| Публичный API пакета | Реэкспорт в `__init__.py` |
| Скрипт + библиотека | `if __name__ == "__main__"` |
| Сторонний пакет | venv + `pip install` |

### Таблица: что в Git, что нет

| Коммитить | Не коммитить |
|-----------|--------------|
| `.py` файлы | `venv/`, `.venv/` |
| `requirements.txt` | `__pycache__/`, `*.pyc` |
| `README.md`, `.gitignore` | `.env` (секреты!) |
| `tests/` | `*.log`, локальные `data/*.json` с личными данными |

---

## FAQ начинающего

**В: Чем модуль отличается от пакета?**  
Модуль = один `.py`. Пакет = папка с модулями (+ обычно `__init__.py`).

**В: Зачем venv, если Python уже установлен?**  
Изоляция зависимостей. Проект A — Flask 2, проект B — Flask 3. Без venv — конфликт.

**В: `pip` не найден?**  
`python -m pip install ...` — надёжнее, чем просто `pip`.

**В: Куда ставится пакет после `pip install`?**  
В `site-packages` **активного** Python (venv или глобальный).

**В: Можно ли импортировать файл с пробелом в имени?**  
Практически нет. Переименуй в `snake_case.py`.

**В: `import helpers` vs `from helpers import double`?**  
Первый — namespace `helpers.double`. Второй — `double` сразу. Оба OK.

**В: Что коммитить в Git?**  
Код, `requirements.txt`, README. Не venv, не `__pycache__`.

**В: `python main.py` vs `python -m myapp.main`?**  
`-m` запускает модуль пакета с корректным путём — полезно в больших проектах.

**В: Как узнать версию установленного пакета?**  
`pip show requests` или `python -c "import requests; print(requests.__version__)"`.

**В: Нужен ли `__init__.py` в Python 3?**  
Для явного пакета — да (или namespace package без него, но на Junior проще с `__init__.py`).

**В: ModuleNotFoundError — что делать?**  
1) Файл в той же папке? 2) Есть `__init__.py` в пакете? 3) Запуск из правильной директории? 4) Пакет установлен через pip?

**В: ImportError: cannot import name 'X' from 'Y'?**  
Часто циклический импорт или опечатка. Или функция `X` ещё не определена в `Y` на момент импорта.

**В: Зачем `requirements.txt`, если есть `pip freeze`?**  
`freeze` — **всё** установленное. `requirements.txt` — **только нужное** проекту, часто пишут вручную или чистят после freeze.

**В: Можно ли несколько venv в одном проекте?**  
Обычно один. Исключение — разные версии Python (`venv39`, `venv312`) — редко на Junior.

**В: `logging` vs `print`?**  
`print` — для учебы и быстрых скриптов. `logging` — уровни (INFO/WARNING/ERROR), формат, запись в файл — в реальных проектах.

**В: Где хранить секреты (API-ключи)?**  
В `.env` + `python-dotenv`, файл `.env` в `.gitignore`. В коде — только `os.environ["KEY"]`.

**В: Что такое `site-packages`?**  
Папка внутри Python/venv, куда pip кладёт установленные пакеты. Путь: `venv/Lib/site-packages/` (Windows).

**В: `python main.py` из другой папки — import ломается?**  
`sys.path[0]` = папка скрипта, но относительные пути к **файлам данных** могут сломаться. Используй `Path(__file__).parent`.

---

### Частые баги

```python
# БАГ — импорт после использования
print(sqrt(4))
from math import sqrt

# БАГ — свой файл json.py ломает import json
# json.py в проекте → import json импортирует ТВОЙ файл

# БАГ — циклический импорт a ↔ b
# a.py: from b import foo
# b.py: from a import bar

# БАГ — pip без venv
# Flask 3 в проекте A, Flask 2 в проекте B — конфликт в глобальном Python

# БАГ — забыли Activate.ps1, но думаете что в venv
import sys
print(sys.executable)   # проверяй всегда!

# БАГ — код вне if __name__ при импорте
# helpers.py:
print("Загрузка...")    # выполнится при import helpers!
def double(x): ...

# FIX — структура
# myapp/
#   main.py              ← if __name__
#   myapp/__init__.py
#   myapp/utils.py
#   requirements.txt
#   .gitignore           ← venv/, __pycache__/, .env
```

### Типичные ошибки терминала

| Ошибка | Причина | Решение |
|--------|---------|---------|
| `ModuleNotFoundError: No module named 'requests'` | Пакет не установлен или не тот venv | `pip install requests`, проверь `sys.executable` |
| `Activate.ps1 cannot be loaded` | Политика PowerShell | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| `pip: command not found` | pip не в PATH | `python -m pip install ...` |
| `ERROR: Could not find a version` | Опечатка в имени пакета | Проверь на pypi.org |

---

## Домашнее задание

**Файл:** `homework_10.py` (задачи 6+ — папки/модули по заданию)

### Задача 1 — Лёгкая
Создай файл `greetings.py` с функциями `hello(name)` и `goodbye(name)`.  
Создай `main.py`, который импортирует и вызывает обе функции.

---

### Задача 2 — Лёгкая
Напиши скрипт `explore_math.py`: импортируй `math`, выведи 5 разных функций/констант с пояснением (print).

---

### Задача 3 — Средняя
Создай `stats_utils.py` с функциями `mean(numbers)` и `median(numbers)`.  
В `main.py` импортируй их и посчитай для списка `[10, 20, 30, 40, 50]`.

<details>
<summary>Подсказка</summary>

`median` — отсортированный список, средний элемент (для нечётной длины).

</details>

---

### Задача 4 — Средняя
Добавь в `stats_utils.py` блок `if __name__ == "__main__":` с 2–3 `assert` для `mean` и `median`.  
Покажи: `python stats_utils.py` — тесты; `import stats_utils` — тесты **не** запускаются.

---

### Задача 5 — Средняя
Создай пакет `converter/`:
- `converter/temperature.py` — `celsius_to_fahrenheit`, `fahrenheit_to_celsius`
- `converter/__init__.py` — реэкспорт обеих функций
- `main.py` — импорт `from converter import celsius_to_fahrenheit`

---

### Задача 6 — Сложная
Создай мини-проект `phonebook/`:
- `models.py` — `Contact(name, phone)`
- `storage.py` — `load()` / `save()` в JSON
- `main.py` — меню: добавить / показать все / выход
- `if __name__ == "__main__"` только в `main.py`

---

### Задача 7 — Сложная
Создай venv в папке проекта, активируй, установи `requests`, выведи:
- путь к `python` (`sys.executable`)
- версию `requests`
- содержимое `pip freeze` (можно в файл)

<details>
<summary>Подсказка</summary>

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install requests
python -c "import sys; print(sys.executable)"
```

</details>

---

### Задача 8 — Сложная
Создай `requirements.txt` с `requests` и `python-dotenv`.  
Напиши в комментарии к ДЗ команды: как создать venv с нуля и установить зависимости на другом компьютере.

---

### Задача 9 — Сложная (бонус)
Модуль `config.py` читает переменные из `.env` через `python-dotenv` (если установлен).  
Если пакет не установлен — fallback на `os.environ` с дефолтами.  
Паттерн как в Примере 23.

---

### Задача 10 — Сложная (бонус)
Проект `log_parser/`:
- `parser.py` — `parse_line(line)` → dict или raise `ValueError`
- `report.py` — `summarize(lines)` → статистика
- `cli.py` — `sys.argv[1]` путь к файлу, `if __name__`
- `tests/test_parser.py` — 3 теста через `assert` (pytest пока не обязателен)

---

### Задача 11 — Сложная (бонус)
Создай пакет `texttools/` с модулями `slugify.py` и `counter.py`.  
В `__init__.py` реэкспортируй `slugify` и `word_count`.  
Добавь `__all__`. Напиши `tests/test_texttools.py` с 4 `assert`.

<details>
<summary>Подсказка</summary>

См. Примеры 18, 36, 38 — структура пакета + тесты.

</details>

---

### Задача 12 — Сложная (бонус)
**Мини-каталог книг** по шаблону Примера 38:
- пакет `bookstore/` с `models`, `catalog`
- `main.py`, `.gitignore`, `requirements.txt`, `README.md`
- добавь функцию `find_by_title(title)` → книга или `None`
- в `README.md` — команды: создать venv, установить зависимости, запустить

---

### Как сдавать

- Папка `homework_10/` со структурой файлов **или** архив
- Для задач 7–8 — скрин или текст вывода терминала (`pip freeze`, `sys.executable`)
- Задачи 1–5 — первая часть, 6–10 — вторая, 11–12 — бонус
- Файл `README.txt` — как запускать каждый скрипт

**Критерии:**
- Импорты по PEP 8 (группы, без `import *`)
- `if __name__ == "__main__"` в точках входа
- Пакеты с `__init__.py`
- venv не в архиве, есть `requirements.txt`
- Имена файлов в `snake_case`

---

**Сделай задачи сам и пришли код на проверку. После проверки — Глава 11: *ООП — классы и объекты*.**

---
Конец главы.