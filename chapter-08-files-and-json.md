# Тема: Работа с файлами и JSON

> **Файл:** `homework_08.py`  
> **Мостик:** гл. 6–7 — данные в памяти (dict, list) → здесь **пишем на диск** (`Path`, `json`).  
> **Маршрут:** ДЗ 1–5 → примеры **1–12**; примеры с `try/except` — **⏳ превью гл. 9** (можно скопировать шаблон).

## Теория

### Что это такое

До сих пор данные жили **только в памяти** — при закрытии программы всё исчезало. **Файлы** позволяют **сохранять** и **загружать** данные на диск: тексты, настройки, логи, экспорт таблиц.

**Файл** — именованная область на диске. Python работает с файлами через встроенную функцию `open()`.

```python
with open("notes.txt", "w", encoding="utf-8") as f:
    f.write("Первая заметка\n")
```

**JSON** (JavaScript Object Notation) — текстовый формат для структурированных данных. В Python JSON ↔ `dict` / `list`:

```python
import json

data = {"name": "Anna", "age": 25, "skills": ["Python", "SQL"]}
json_string = json.dumps(data)    # dict → строка JSON
restored = json.loads(json_string)  # строка → dict
```

JSON — стандарт для API, конфигов, сохранения настроек приложения.

---

### Открытие и закрытие файлов

#### `open(path, mode, encoding)`

```python
f = open("file.txt", "r", encoding="utf-8")
content = f.read()
f.close()    # обязательно закрыть!
```

**Проблема:** если между `open` и `close` произойдёт ошибка — файл может **не закрыться** (утечка ресурсов).

#### Контекстный менеджер `with` — правильный способ

```python
with open("file.txt", "r", encoding="utf-8") as f:
    content = f.read()
# файл автоматически закрыт, даже при ошибке
```

`with` гарантирует вызов `close()` при выходе из блока.

---

### Режимы открытия файла (mode)

| Режим | Что делает | Файл должен существовать? | Создаёт новый? |
|-------|------------|---------------------------|----------------|
| `"r"` | Чтение (read) | Да | Нет |
| `"w"` | Запись (write), **перезаписывает** | Нет | Да (или очищает) |
| `"a"` | Добавление (append) в конец | Нет | Да |
| `"r+"` | Чтение + запись | Да | Нет |
| `"x"` | Создать только если не существует | Нет | Да (ошибка если есть) |

**Текст vs бинарный:**
- `"r"`, `"w"`, `"a"` — **текстовый** режим (строки `str`)
- `"rb"`, `"wb"` — **бинарный** (байты `bytes`) — картинки, PDF (на Junior — знай, что есть)

**Кодировка:**

```python
open("file.txt", "r", encoding="utf-8")   # всегда указывай для русского текста!
```

Без `encoding` на Windows может быть `cp1251` или системная — **кракозябры** при переносе на другой компьютер.

---

### Чтение файлов

| Метод | Что делает |
|-------|------------|
| `f.read()` | Весь файл — одна строка |
| `f.read(n)` | Первые n символов |
| `f.readline()` | Одна строка (с `\n` в конце) |
| `f.readlines()` | List всех строк |
| `for line in f:` | Построчно — **лучший для больших файлов** |

```python
with open("data.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(line.strip())   # strip убирает \n и пробелы по краям
```

**Почему `for line in f` лучше `readlines()`:**  
`readlines()` загружает **весь** файл в память. Цикл `for` читает **построчно** — экономит память на гигабайтных логах.

---

### Запись в файлы

| Метод | Что делает |
|-------|------------|
| `f.write(text)` | Записать строку (без авто-переноса!) |
| `f.writelines(list)` | Записать list строк |
| `print(..., file=f)` | print прямо в файл |

```python
with open("out.txt", "w", encoding="utf-8") as f:
    f.write("Строка 1\n")           # \n — перенос вручную
    f.write("Строка 2\n")
    print("Строка 3", file=f)       # print добавит \n
```

**Режим `"w"`** — стирает файл при открытии! Для дозаписи — `"a"`.

---

### Пути к файлам

```python
# Относительный путь — от папки, где запущен скрипт
open("data/notes.txt")

# Абсолютный путь
open("C:/Users/Admin/Documents/notes.txt")   # Windows
open("/home/user/notes.txt")                  # Linux

# pathlib — современный способ (Python 3.4+)
from pathlib import Path

file_path = Path("data") / "notes.txt"   # кроссплатформенно
file_path.exists()                        # есть ли файл?
file_path.parent.mkdir(parents=True, exist_ok=True)  # создать папку
```

---

### JSON в Python

Модуль `json` — в стандартной библиотеке.

| Функция | Направление | Описание |
|---------|-------------|----------|
| `json.dumps(obj)` | Python → **строка** | serialize |
| `json.loads(string)` | **строка** → Python | deserialize |
| `json.dump(obj, f)` | Python → **файл** | записать в файл |
| `json.load(f)` | **файл** → Python | прочитать из файла |

**Что JSON поддерживает:**

| Python | JSON |
|--------|------|
| `dict` | object `{}` |
| `list` | array `[]` |
| `str` | string |
| `int`, `float` | number |
| `True`/`False` | true/false |
| `None` | null |

**Не поддерживается:** `set`, `tuple` (станет list), произвольные объекты.

```python
import json

data = {"users": [{"id": 1, "name": "Anna"}], "active": True, "meta": None}
text = json.dumps(data, ensure_ascii=False, indent=2)
print(text)
```

`ensure_ascii=False` — кириллица как есть, не `\u0410`.  
`indent=2` — красивое форматирование.

---

### Как это работает «под капотом»

#### `with` и контекстный менеджер

1. Вызывается `open()` → объект file
2. Вход в блок `with` → `f.__enter__()`
3. Тело блока
4. Выход (нормальный или ошибка) → `f.__exit__()` → **всегда** `close()`

#### Буферизация

`write()` не всегда сразу на диск — данные в **буфере**. `close()` сбрасывает буфер. Поэтому `close()` критичен без `with`.

#### Текстовый режим

Python декодирует байты → `str` (Unicode) при чтении и кодирует при записи. Кодировка = `encoding`.

#### JSON

`json.dumps` обходит структуру dict/list рекурсивно, строит строку. `json.loads` парсит текст по правилам JSON (скобки, кавычки, запятые).

---

### Где это полезно и применяется в реальной разработке

| Сценарий | Инструмент |
|----------|------------|
| Конфиг приложения | `config.json` + `json.load` |
| Логи | запись в `.log` с режимом `"a"` |
| Экспорт отчётов | CSV/TXT запись |
| Ответ API | `response.json()` → dict |
| Сохранение прогресса игры | JSON-файл |
| Чтение CSV | построчно + `split(",")` |
| Кэш данных | pickle/JSON на диск |

**Типичный паттерн — загрузка конфига:**

```python
import json
from pathlib import Path

def load_config(path="config.json"):
    config_path = Path(path)
    if not config_path.exists():
        return {}
    with config_path.open("r", encoding="utf-8") as f:
        return json.load(f)
```

---

### Микро-моменты, нюансы, частые ошибки новичков

#### 1. Забыли `encoding="utf-8"`

Кракозябры: `РџСЂРёРІРµС` вместо `Привет`.

#### 2. Забыли `\n` в `write()`

```python
f.write("строка1")
f.write("строка2")    # строка1строка2 — склеилось!
f.write("строка1\n")    # правильно
```

#### 3. Режим `"w"` случайно стёр данные

Для дозаписи — `"a"`. Для безопасного обновления — сначала прочитай, потом перезапиши.

#### 4. `FileNotFoundError`

```python
# open("нет.txt", "r")   # FileNotFoundError

from pathlib import Path
if Path("нет.txt").exists():
    ...
```

#### 5. `read()` дважды — второй раз пусто

Указатель в конце файла. После `read()` — `f.seek(0)` для перемотки (или открой заново).

#### 6. JSON — ключи только строки

В Python dict ключи могут быть int; в JSON — **только строки** в кавычках.

#### 7. Trailing comma в JSON

В JSON **нельзя**: `{"a": 1,}` — ошибка парсинга. В Python dict — можно.

#### 8. Относительный путь — от cwd

Зависит от **текущей рабочей папки**, не от места скрипта. Решение:

```python
Path(__file__).parent / "data.txt"
```

#### 9. Не закрытый файл на Windows

Иногда файл «занят» — нельзя удалить/переименовать. Используй `with`.

#### 10. `json.load` vs `json.loads`

- `load` — из **файлового объекта** `f`
- `loads` — из **строки** `s`

---

## Практика

> **Навигация:** **28 примеров**, шпаргалка, FAQ, домашка.

### Пример 1: Запись и чтение текстового файла

```python
filename = "demo_notes.txt"

# Запись
with open(filename, "w", encoding="utf-8") as f:
    f.write("Первая строка\n")
    f.write("Вторая строка\n")
    f.write("Третья строка\n")

# Чтение целиком
with open(filename, "r", encoding="utf-8") as f:
    content = f.read()

print("=== Весь файл ===")
print(content)
print(f"Символов: {len(content)}")
```

**Вывод консоли:**

```
=== Весь файл ===
Первая строка
Вторая строка
Третья строка

Символов: 42
```

**Разбор:** Режим `"w"` создаёт файл и записывает три строки, а `"r"` читает всё сразу через `read()`. Число 42 — это длина текста вместе с символами `\n` в конце строк. Конструкция `with` сама закрывает файл после блока — вручную вызывать `close()` не нужно.

*(после запуска появится файл `demo_notes.txt` в папке скрипта)*

---

### Пример 2: Построчное чтение — `for line in f`

```python
filename = "demo_notes.txt"

with open(filename, "r", encoding="utf-8") as f:
    print("=== Построчно ===")
    for i, line in enumerate(f, start=1):
        clean = line.strip()
        print(f"  {i}: [{clean}]")
```

**Вывод консоли:**

```
=== Построчно ===
  1: [Первая строка]
  2: [Вторая строка]
  3: [Третья строка]
```

**Разбор:** Цикл `for line in f` читает файл построчно, не загружая всё в память сразу. Метод `strip()` убирает перевод строки `\n` в конце каждой строки. `enumerate(..., start=1)` нумерует строки с единицы — удобно для отчётов и логов.

---

### Пример 3: `readline` и `readlines`

```python
filename = "demo_notes.txt"

with open(filename, "r", encoding="utf-8") as f:
    first = f.readline()
    second = f.readline()
    print("readline 1:", repr(first))
    print("readline 2:", repr(second))

with open(filename, "r", encoding="utf-8") as f:
    all_lines = f.readlines()
    print("readlines:", all_lines)
    print("Количество строк:", len(all_lines))
```

**Вывод консоли:**

```
readline 1: 'Первая строка\n'
readline 2: 'Вторая строка\n'
readlines: ['Первая строка\n', 'Вторая строка\n', 'Третья строка\n']
Количество строк: 3
```

**Разбор:** `readline()` читает по одной строке и оставляет `\n` в конце — поэтому `repr()` показывает их явно. `readlines()` сразу возвращает список всех строк файла. После двух вызовов `readline` указатель в файле стоит на третьей строке.

`repr()` показывает `\n` явно.

---

### Пример 4: Режим append — дозапись в конец

```python
filename = "demo_log.txt"

with open(filename, "w", encoding="utf-8") as f:
    f.write("Старт программы\n")

with open(filename, "a", encoding="utf-8") as f:
    f.write("Обработка данных\n")
    f.write("Завершение\n")

with open(filename, "r", encoding="utf-8") as f:
    print(f.read())
```

**Вывод консоли:**

```
Старт программы
Обработка данных
Завершение
```

**Разбор:** Режим `"w"` перезаписывает файл с нуля, а `"a"` (append) дописывает в конец, не удаляя старое. Поэтому три записи идут подряд в одном файле. При повторном запуске первый `open("w")` снова сотрёт содержимое.

---

### Пример 5: `print` в файл

```python
filename = "demo_report.txt"

with open(filename, "w", encoding="utf-8") as f:
    print("=== ОТЧЁТ ===", file=f)
    print("Строка 1", file=f)
    print("Строка 2", file=f)
    print(42, "ответ", sep=" → ", end="!\n", file=f)

with open(filename, "r", encoding="utf-8") as f:
    print(f.read())
```

**Вывод консоли:**

```
=== ОТЧЁТ ===
Строка 1
Строка 2
42 → ответ!

```

**Разбор:** Параметр `file=f` направляет `print` в файл вместо консоли. Аргументы `sep` и `end` работают так же, как при обычном выводе на экран. Сначала всё записывается в файл молча, потом мы читаем его и печатаем — поэтому вывод появляется в конце.

---

### Пример 6: `pathlib` — проверка и создание папки

```python
from pathlib import Path

data_dir = Path("my_data")
file_path = data_dir / "info.txt"

# Создать папку, если нет
data_dir.mkdir(parents=True, exist_ok=True)

print("Папка существует:", data_dir.exists())
print("Файл существует:", file_path.exists())

with file_path.open("w", encoding="utf-8") as f:
    f.write("Данные в подпапке\n")

print("После записи:", file_path.exists())
print("Абсолютный путь:", file_path.resolve())
```

**Вывод консоли (путь будет твой):**

```
Папка существует: True
Файл существует: False
После записи: True
Абсолютный путь: C:\Users\...\my_data\info.txt
```

**Разбор:** `Path.mkdir(exist_ok=True)` создаёт папку, если её ещё нет. Оператор `/` собирает путь к файлу внутри `my_data`. До записи файла не существовало (`False`), после `open("w")` он появился (`True`).

---

### Пример 7: Безопасное чтение — файл не найден

```python
from pathlib import Path

def read_text_safe(path):
    file_path = Path(path)
    if not file_path.exists():
        print(f"Файл не найден: {path}")
        return None
    with file_path.open("r", encoding="utf-8") as f:
        return f.read()

content = read_text_safe("не_существует.txt")
print(content)

content = read_text_safe("demo_notes.txt")
print(content[:20] if content else "пусто")
```

**Вывод консоли:**

```
Файл не найден: не_существует.txt
None
Первая строка
Вторая
```

**Разбор:** Перед чтением проверяем `exists()` — программа не падает с ошибкой, а сообщает о проблеме. Для несуществующего файла функция возвращает `None`, поэтому в консоли видим `None`. Для `demo_notes.txt` читаем первые 20 символов — это начало текста из примера 1.

---

### Пример 8: JSON — `dumps` и `loads`

```python
import json

user = {
    "id": 101,
    "name": "Анна",
    "age": 25,
    "skills": ["Python", "SQL"],
    "active": True,
    "manager": None,
}

# dict → строка
json_text = json.dumps(user, ensure_ascii=False, indent=2)
print("=== JSON строка ===")
print(json_text)

# строка → dict
restored = json.loads(json_text)
print("\n=== Восстановлено ===")
print(restored)
print(restored["name"])
print(type(restored["skills"]))
```

**Вывод консоли:**

```
=== JSON строка ===
{
  "id": 101,
  "name": "Анна",
  ...
}

=== Восстановлено ===
{'id': 101, 'name': 'Анна', ...}
Анна
<class 'list'>
```

**Разбор:** `json.dumps` превращает словарь Python в JSON-строку, `json.loads` — обратно в dict. Параметр `ensure_ascii=False` сохраняет кириллицу, `indent=2` форматирует вывод с отступами. После `loads` тип `skills` остаётся списком Python — структура данных не теряется.

---

### Пример 9: JSON — запись и чтение файла

```python
import json
from pathlib import Path

config = {
    "app_name": "MyApp",
    "version": "1.0",
    "settings": {
        "theme": "dark",
        "language": "ru",
    },
    "users": ["anna", "bob"],
}

config_path = Path("config.json")

# Запись
with config_path.open("w", encoding="utf-8") as f:
    json.dump(config, f, ensure_ascii=False, indent=2)

# Чтение
with config_path.open("r", encoding="utf-8") as f:
    loaded = json.load(f)

print("Тема:", loaded["settings"]["theme"])
print("Пользователи:", loaded["users"])
```

**Вывод консоли:**

```
Тема: dark
Пользователи: ['anna', 'bob']
```

**Разбор:** `json.dump` записывает словарь прямо в файл, `json.load` читает его обратно. Вложенный словарь `settings` доступен через цепочку ключей `loaded["settings"]["theme"]`. На диске появляется `config.json` — его можно открыть и отредактировать вручную.

*(создаётся `config.json`)*

---

### Пример 10: Обновление JSON-конфига

```python
import json
from pathlib import Path

def load_json(path):
    with Path(path).open("r", encoding="utf-8") as f:
        return json.load(f)

def save_json(path, data):
    with Path(path).open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

path = "config.json"
config = load_json(path)
config["settings"]["theme"] = "light"
config["version"] = "1.1"
save_json(path, config)
print("Обновлено:", load_json(path)["settings"])
```

**Вывод консоли:**

```
Обновлено: {'theme': 'light', 'language': 'ru'}
```

**Разбор:** Сначала загружаем конфиг в память, меняем нужные поля, затем сохраняем — файл перезаписывается целиком. Тема сменилась с `dark` на `light`, а `language` остался `ru`. Так обычно обновляют настройки приложения без переписывания всего кода.

---

### Пример 11: Парсинг простого CSV вручную

```python
csv_content = """name,age,city
Anna,25,Moscow
Bob,30,Kazan
Vika,22,Sochi"""

lines = csv_content.strip().split("\n")
headers = lines[0].split(",")
rows = [line.split(",") for line in lines[1:]]

users = [dict(zip(headers, row)) for row in rows]
for u in users:
    u["age"] = int(u["age"])

for u in users:
    print(f"{u['name']}, {u['age']} лет, {u['city']}")
```

**Вывод консоли:**

```
Anna, 25 лет, Moscow
Bob, 30 лет, Kazan
Vika, 22 лет, Sochi
```

**Разбор:** CSV разбиваем на строки, первую берём как заголовки столбцов. Функция `zip(headers, row)` собирает пары «ключ — значение» в словарь для каждой строки. `int(u["age"])` переводит возраст из строки в число — без этого это был бы текст `"25"`, а не число.

---

### Пример 12: Запись CSV в файл

```python
from pathlib import Path

users = [
    {"name": "Anna", "score": 92},
    {"name": "Bob", "score": 78},
    {"name": "Vika", "score": 95},
]

csv_path = Path("scores.csv")

with csv_path.open("w", encoding="utf-8") as f:
    f.write("name,score\n")
    for u in users:
        f.write(f"{u['name']},{u['score']}\n")

with csv_path.open("r", encoding="utf-8") as f:
    print(f.read())
```

**Вывод консоли:**

```
name,score
Anna,92
Bob,78
Vika,95

```

**Разбор:** Сначала пишем заголовок `name,score`, затем каждую запись в формате `имя,балл` через запятую. Запятая здесь — разделитель полей в простом CSV. Чтение файла в конце подтверждает, что все данные сохранились на диск правильно.

---

### Пример 13: Подсчёт слов в файле

```python
from pathlib import Path

def count_words_in_file(path):
    counts = {}
    with Path(path).open("r", encoding="utf-8") as f:
        for line in f:
            for word in line.lower().split():
                word = word.strip(".,!?;:")
                if word:
                    counts[word] = counts.get(word, 0) + 1
    return counts

text = "Python python is great. Python is fun!"
Path("words.txt").write_text(text, encoding="utf-8")

counts = count_words_in_file("words.txt")
for word, count in sorted(counts.items(), key=lambda x: -x[1]):
    print(f"  {word}: {count}")
```

**Вывод консоли:**

```
  python: 3
  is: 2
  great: 1
  fun: 1
```

---

### Пример 14: Логгер в файл (append)

```python
from datetime import datetime
from pathlib import Path

LOG_FILE = Path("app.log")

def log(level, message):
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{timestamp}] [{level}] {message}\n"
    with LOG_FILE.open("a", encoding="utf-8") as f:
        f.write(line)

log("INFO", "Приложение запущено")
log("INFO", "Загрузка конфига")
log("ERROR", "Файл не найден: data.csv")
log("INFO", "Завершение")

print("=== Лог ===")
print(LOG_FILE.read_text(encoding="utf-8"))
```

**Вывод консоли:**

```
=== Лог ===
[2026-07-14 ...] [INFO] Приложение запущено
[2026-07-14 ...] [INFO] Загрузка конфига
[2026-07-14 ...] [ERROR] Файл не найден: data.csv
[2026-07-14 ...] [INFO] Завершение
```

---

### Пример 15: JSON — ошибка парсинга ⏳ (превью гл. 9)

> Синтаксис `try/except` — **глава 9**. Здесь смотри **идею**: битый JSON не должен ронять программу.

```python
import json

bad_json = '{"name": "Anna", "age": 25,}'   # лишняя запятая — невалидный JSON

try:
    data = json.loads(bad_json)
except json.JSONDecodeError as e:
    print("Ошибка JSON:", e)
    print("Позиция:", e.pos)

good_json = '{"name": "Anna", "age": 25}'
data = json.loads(good_json)
print("OK:", data)
```

**Вывод консоли:**

```
Ошибка JSON: Expecting property name enclosed in double quotes: ...
Позиция: ...
OK: {'name': 'Anna', 'age': 25}
```

---

### Пример 16: Сохранение list of dict — типичный экспорт

```python
import json
from pathlib import Path

students = [
    {"id": 1, "name": "Anna", "score": 92},
    {"id": 2, "name": "Bob", "score": 78},
    {"id": 3, "name": "Vika", "score": 95},
]

path = Path("students.json")
with path.open("w", encoding="utf-8") as f:
    json.dump(students, f, ensure_ascii=False, indent=2)

with path.open("r", encoding="utf-8") as f:
    loaded = json.load(f)

avg = sum(s["score"] for s in loaded) / len(loaded)
print(f"Загружено {len(loaded)} студентов, средний балл: {avg:.1f}")
```

**Вывод консоли:**

```
Загружено 3 студентов, средний балл: 88.3
```

---

## Теория (дополнение): seek, контекст, типичные паттерны

### `seek` — перемотка в файле

```python
with open("file.txt", "r", encoding="utf-8") as f:
    part1 = f.read(5)
    f.seek(0)           # в начало
    full = f.read()
```

| `seek(offset, whence)` | whence |
|------------------------|--------|
| `f.seek(0)` | начало |
| `f.seek(0, 2)` | конец |

На Junior достаточно знать: после `read()` указатель в конце.

---

### Паттерн: read-modify-write

```python
import json
from pathlib import Path

path = Path("counter.json")

# Прочитать
if path.exists():
    with path.open("r", encoding="utf-8") as f:
        data = json.load(f)
else:
    data = {"count": 0}

# Изменить
data["count"] += 1

# Записать
with path.open("w", encoding="utf-8") as f:
    json.dump(data, f)
```

**Осторожно:** при одновременном доступе двух программ — race condition. На Junior — OK для простых скриптов.

---

### `Path.read_text` / `Path.write_text` — короткая запись

```python
from pathlib import Path

Path("short.txt").write_text("Привет!\n", encoding="utf-8")
text = Path("short.txt").read_text(encoding="utf-8")
print(text)
```

Для **маленьких** файлов — удобно. Для больших — `open` + цикл.

---

### JSON и API — связь

```python
# Имитация ответа API (в реале: requests.get(url).json())
api_response = '{"status": "ok", "data": {"id": 1, "name": "Anna"}}'

import json
parsed = json.loads(api_response)
if parsed["status"] == "ok":
    user = parsed["data"]
    print(user["name"])
```

---

## Практика — примеры 17–28 (продолжение)

### Пример 17: Копирование файла

```python
from pathlib import Path
import shutil

source = Path("demo_notes.txt")
dest = Path("demo_notes_copy.txt")

shutil.copy(source, dest)
print("Скопировано:", dest.read_text(encoding="utf-8")[:30])
```

**Вывод:** содержимое копии совпадает с оригиналом.

---

### Пример 18: Фильтрация строк при чтении

```python
from pathlib import Path

log_content = """INFO: start
INFO: processing
ERROR: disk full
INFO: retry
ERROR: timeout
"""

Path("filter_log.txt").write_text(log_content, encoding="utf-8")

errors = []
with Path("filter_log.txt").open("r", encoding="utf-8") as f:
    for line in f:
        if "ERROR" in line:
            errors.append(line.strip())

print("Ошибки:")
for e in errors:
    print(f"  {e}")
```

**Вывод консоли:**

```
Ошибки:
  ERROR: disk full
  ERROR: timeout
```

---

### Пример 19: JSON — список настроек по умолчанию

```python
import json
from pathlib import Path

DEFAULTS = {
    "theme": "light",
    "font_size": 14,
    "notifications": True,
}

def get_settings(path="settings.json"):
    p = Path(path)
    if not p.exists():
        return DEFAULTS.copy()
    with p.open("r", encoding="utf-8") as f:
        saved = json.load(f)
    result = DEFAULTS.copy()
    result.update(saved)
    return result

print("Без файла:", get_settings("no_settings.json"))
```

**Вывод консоли:**

```
Без файла: {'theme': 'light', 'font_size': 14, 'notifications': True}
```

---

### Пример 20: Запись нумерованного списка в файл

```python
from pathlib import Path

tasks = ["Выучить файлы", "Сделать JSON", "Сдать домашку"]

with Path("todo.txt").open("w", encoding="utf-8") as f:
    for i, task in enumerate(tasks, start=1):
        f.write(f"{i}. {task}\n")

print(Path("todo.txt").read_text(encoding="utf-8"))
```

**Вывод консоли:**

```
1. Выучить файлы
2. Сделать JSON
3. Сдать домашку

```

---

### Пример 21: Объединение двух JSON-файлов

```python
import json
from pathlib import Path

users1 = [{"id": 1, "name": "Anna"}]
users2 = [{"id": 2, "name": "Bob"}]

Path("users1.json").write_text(json.dumps(users1), encoding="utf-8")
Path("users2.json").write_text(json.dumps(users2), encoding="utf-8")

def load_users(path):
    with Path(path).open("r", encoding="utf-8") as f:
        return json.load(f)

merged = load_users("users1.json") + load_users("users2.json")
print(merged)
```

**Вывод консоли:**

```
[{'id': 1, 'name': 'Anna'}, {'id': 2, 'name': 'Bob'}]
```

---

### Пример 22: Валидация JSON-структуры

```python
import json

def validate_user(data):
    """Проверяет, что data — корректный user dict."""
    errors = []
    if not isinstance(data, dict):
        return False, ["Ожидался dict"]
    if "name" not in data or not data["name"]:
        errors.append("Нет name")
    if "age" not in data or not isinstance(data["age"], int):
        errors.append("Некорректный age")
    return len(errors) == 0, errors

tests = [
    {"name": "Anna", "age": 25},
    {"name": "", "age": 25},
    {"age": "25"},
]

for t in tests:
    ok, errs = validate_user(t)
    print(f"{t} → OK={ok}, errors={errs}")
```

**Вывод консоли:**

```
{'name': 'Anna', 'age': 25} → OK=True, errors=[]
{'name': '', 'age': 25} → OK=False, errors=['Нет name']
{'age': '25'} → OK=False, errors=['Нет name', 'Некорректный age']
```

---

### Пример 23: Чтение файла с обработкой пустых строк

```python
from pathlib import Path

content = "строка 1\n\nстрока 3\n   \nстрока 5\n"
Path("sparse.txt").write_text(content, encoding="utf-8")

non_empty = []
with Path("sparse.txt").open("r", encoding="utf-8") as f:
    for line in f:
        stripped = line.strip()
        if stripped:
            non_empty.append(stripped)

print(non_empty)
```

**Вывод консоли:**

```
['строка 1', 'строка 3', 'строка 5']
```

---

### Пример 24: Backup перед перезаписью

```python
import json
import shutil
from pathlib import Path
from datetime import datetime

def safe_save_json(path, data):
    p = Path(path)
    if p.exists():
        backup = p.with_suffix(f".{datetime.now():%Y%m%d_%H%M%S}.bak.json")
        shutil.copy(p, backup)
        print(f"Бэкап: {backup}")
    with p.open("w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

safe_save_json("config.json", {"version": 2})
```

---

### Пример 25: Мини-проект — заметки (CRUD в файле)

```python
import json
from pathlib import Path

NOTES_FILE = Path("notes.json")

def load_notes():
    if not NOTES_FILE.exists():
        return []
    with NOTES_FILE.open("r", encoding="utf-8") as f:
        return json.load(f)

def save_notes(notes):
    with NOTES_FILE.open("w", encoding="utf-8") as f:
        json.dump(notes, f, ensure_ascii=False, indent=2)

def add_note(text):
    notes = load_notes()
    notes.append({"id": len(notes) + 1, "text": text})
    save_notes(notes)

def list_notes():
    for note in load_notes():
        print(f"  [{note['id']}] {note['text']}")

add_note("Купить молоко")
add_note("Сделать дз по Python")
print("Заметки:")
list_notes()
```

**Вывод консоли:**

```
Заметки:
  [1] Купить молоко
  [2] Сделать дз по Python
```

---

### Пример 26: Статистика по текстовому файлу

```python
from pathlib import Path

def file_stats(path):
    lines = words = chars = 0
    with Path(path).open("r", encoding="utf-8") as f:
        for line in f:
            lines += 1
            chars += len(line)
            words += len(line.split())
    return {"lines": lines, "words": words, "chars": chars}

text = "Hello world\nPython is great\n"
Path("stats.txt").write_text(text, encoding="utf-8")
print(file_stats("stats.txt"))
```

**Вывод консоли:**

```
{'lines': 2, 'words': 5, 'chars': 32}
```

---

### Пример 27: Экспорт dict в «красивый» JSON

```python
import json

report = {
    "period": "2026-Q1",
    "revenue": 150000.50,
    "departments": {
        "sales": 90000,
        "support": 60000,
    },
    "closed": True,
}

output = json.dumps(
    report,
    ensure_ascii=False,
    indent=4,
    sort_keys=True,
)
print(output)
```

**Вывод консоли:**

```json
{
    "closed": true,
    "departments": {
        "sales": 90000,
        "support": 60000
    },
    "period": "2026-Q1",
    "revenue": 150000.5
}
```

---

### Пример 28: Полный пайплайн — CSV → обработка → JSON

```python
import json
from pathlib import Path

csv_data = """product,qty,price
яблоко,10,89.90
молоко,5,69.50
сыр,2,350.00"""

Path("sales.csv").write_text(csv_data, encoding="utf-8")

# Читаем CSV
lines = Path("sales.csv").read_text(encoding="utf-8").strip().split("\n")
headers = lines[0].split(",")
items = []
for line in lines[1:]:
    vals = line.split(",")
    row = dict(zip(headers, vals))
    row["qty"] = int(row["qty"])
    row["price"] = float(row["price"])
    row["total"] = row["qty"] * row["price"]
    items.append(row)

# Сохраняем JSON
report = {
    "items": items,
    "grand_total": sum(i["total"] for i in items),
}
Path("sales_report.json").write_text(
    json.dumps(report, ensure_ascii=False, indent=2),
    encoding="utf-8",
)
print(json.dumps(report, ensure_ascii=False, indent=2))
```

**Вывод консоли:**

```json
{
  "items": [
    {"product": "яблоко", "qty": 10, "price": 89.9, "total": 899.0},
    ...
  ],
  "grand_total": 2216.2
}
```

---

## Шпаргалка

```python
# Текстовый файл
with open("f.txt", "r", encoding="utf-8") as f:
    text = f.read()
    for line in f:
        ...

with open("f.txt", "w", encoding="utf-8") as f:
    f.write("text\n")

with open("f.txt", "a", encoding="utf-8") as f:
    f.write("append\n")

# pathlib
from pathlib import Path
p = Path("data/file.txt")
p.exists()
p.read_text(encoding="utf-8")
p.write_text("hi", encoding="utf-8")
p.parent.mkdir(parents=True, exist_ok=True)

# JSON
import json
s = json.dumps(obj, ensure_ascii=False, indent=2)
obj = json.loads(s)
json.dump(obj, f, ensure_ascii=False, indent=2)
obj = json.load(f)
```

---

## FAQ начинающего

**В: Зачем `with`?**  
Автоматически закрывает файл. Безопаснее `open` + `close`.

**В: `r` или `rb`?**  
Текст → `r`. Бинарные данные → `rb`. Для .txt, .json, .csv — `r` + encoding.

**В: Почему кракозябры?**  
Нет `encoding="utf-8"` или файл в другой кодировке.

**В: `json.dump` vs `json.dumps`?**  
`dump` → в файл. `dumps` → в строку (string).

**В: Можно ли JSON с комментариями?**  
Нет. Используй `.jsonc` только в редакторах — `json.load` не примет.

**В: Как узнать путь к скрипту?**  
`Path(__file__).parent`

**В: `w` удаляет файл?**  
Очищает содержимое (или создаёт пустой). Данные теряются!

**В: Большой файл — как читать?**  
`for line in f:` построчно, не `read()`.

**В: Модуль `csv` — нужен?**  
Для простого CSV хватит `split`. Модуль `csv` — для кавычек и запятых внутри полей (позже).

**В: `Path` vs `open`?**  
Оба OK. `Path` — удобнее для путей и `exists()`. `open` — классика.

**В: Где лежит файл при `open("a.txt")`?**  
В **текущей рабочей папке** (cwd), не обязательно рядом со скриптом.

---

### Таблица: какой метод чтения когда

| Задача | Метод |
|--------|-------|
| Весь маленький файл | `read()` |
| Построчно, большой файл | `for line in f` |
| Одна строка | `readline()` |
| Все строки в list (малый файл) | `readlines()` |
| Быстро прочитать маленький | `Path.read_text()` |

---

### Context Manager — что ещё поддерживает `with`

Кроме файлов: блокировки, сетевые соединения, транзакции БД. Паттерн один: `__enter__` / `__exit__`.

---

### Частые баги

```python
# БАГ: нет encoding
open("f.txt", "r")

# БАГ: нет \n
f.write("a"); f.write("b")

# БАГ: w вместо a для лога
open("log.txt", "a")

# БАГ: json.loads с файлом
json.loads(f)   # нужен f.read() или json.load(f)

# БАГ: не проверили exists
Path("f.txt").read_text()   # FileNotFoundError
```

---

## Домашнее задание

**Файл:** `homework_08.py`

### Задача 1 — Лёгкая
Создай файл `greeting.txt` с 3 строками приветствия (режим `"w"`). Прочитай и выведи содержимое.

---

### Задача 2 — Лёгкая
Допиши 2 строки в `greeting.txt` режимом `"a"`. Выведи итоговый файл.

---

### Задача 3 — Средняя
Напиши `count_lines(path)` → количество строк в файле. Используй `for line in f`, не `readlines()`.

<details>
<summary>Подсказка</summary>

Счётчик +1 на каждую итерацию цикла.

</details>

---

### Задача 4 — Средняя
Создай `profile.json` с полями: `name`, `age`, `city`, `hobbies` (list). Прочитай и выведи хобби через запятую.

---

### Задача 5 — Средняя
Напиши `merge_json_files(file1, file2, output)` — объединяет два JSON-массива в один и сохраняет в `output`.

<details>
<summary>Подсказка</summary>

`merged = json.load(f1) + json.load(f2)` — если оба list.

</details>

---

### Задача 6 — Сложная
**Текстовая статистика.** Функция `analyze_text_file(path)` возвращает dict:
- `lines`, `words`, `chars`
- `longest_line` (строка)
- `most_common_word` (без учёта регистра, убрать пунктуацию простым `strip(".,!?")`)

<details>
<summary>Подсказка</summary>

См. Пример 13. Счётчик слов + `max(counts, key=counts.get)`.

</details>

---

### Задача 7 — Сложная
**Дневник на JSON.** Функции:
- `add_entry(date, text)` — добавляет `{"date": date, "text": text}` в `diary.json`
- `list_entries()` — печатает все записи
- `search_entries(keyword)` — возвращает записи, где keyword в text

Файл — list of dict. Создай 3 записи, протестируй поиск.

<details>
<summary>Подсказка</summary>

См. Пример 25. load → append → save. Поиск: list comprehension по `keyword in entry["text"]`.

</details>

---

### Задача 8 — Сложная
**Конвертер CSV → JSON.** Функция `csv_to_json(csv_path, json_path)`:
- первая строка CSV — заголовки
- остальные — данные
- числовые поля (`age`, `score`) — преобразуй в `int`
- сохрани JSON с `indent=2`, `ensure_ascii=False`

Тестовый CSV создай сам.

<details>
<summary>Подсказка</summary>

См. Пример 28. `int()` для age/score в try/except или проверкой `.isdigit()`.

</details>

---

### Задача 9 — Сложная (бонус)
**Менеджер задач в файле.** `todo.json` — list задач `{id, text, done}`.
- `add_task(text)`
- `complete_task(id)`
- `list_tasks(show_done=True)` — параметр фильтрует выполненные
- `show_stats()` — сколько всего / выполнено / осталось

Меню `while True` в main.

<details>
<summary>Подсказка</summary>

Структура как Пример 25 + фильтр `[t for t in tasks if not t["done"]]` при `show_done=False`.

</details>

---

### Задача 10 — Сложная (бонус)
Напиши `safe_read_json(path, default=None)`:
- если файла нет → `default`
- если JSON битый → печатает ошибку, возвращает `default`
- иначе → данные

Протестируй на: несуществующий файл, битый JSON, корректный JSON.

<details>
<summary>Подсказка</summary>

```python
try:
    with open(path) as f:
        return json.load(f)
except FileNotFoundError:
    return default
except json.JSONDecodeError as e:
    print(e)
    return default
```

</details>

---

### Как сдавать

- `homework_08.py` + созданные `.txt`/`.json` при необходимости
- Запускай из папки с файлами или используй `Path(__file__).parent`
- Частями: 1–5, 6–10

**Критерии:**
- Везде `encoding="utf-8"`
- Везде `with` (или `Path` методы)
- JSON с `ensure_ascii=False` для русского
- Обработка «файл не найден» где уместно

---

**Сделай задачи сам и пришли код на проверку. После проверки — Глава 9: *Исключения — try/except/finally*.**

---
Конец главы.