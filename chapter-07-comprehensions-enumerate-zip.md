# Тема: List/dict comprehensions, `enumerate`, `zip`

> **Файл:** `homework_07.py`  
> **Маршрут:** ДЗ 1–5 → примеры **1–6, 11, 18, 21**. Закрывает превью из гл. 4.  
> **Дальше — гл. 8:** dict/list → **файлы и JSON**.

## Теория

### Что это такое

В главах 2 и 4 ты уже писал циклы «собери новый список»:

```python
squares = []
for x in range(1, 6):
    squares.append(x ** 2)
```

**List comprehension** — тот же смысл, **в одну строку**:

```python
squares = [x ** 2 for x in range(1, 6)]
```

Читается как: «собери список из `x ** 2` для каждого `x` в range(1, 6)».

**Dict comprehension** — то же для словарей:

```python
squares_dict = {x: x ** 2 for x in range(1, 6)}
# {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
```

**Set comprehension** — для множеств:

```python
unique_lengths = {len(word) for word in ["hi", "hello", "hi"]}
# {2, 5}
```

**`enumerate`** — цикл с **индексом и значением**:

```python
for index, value in enumerate(["a", "b", "c"]):
    print(index, value)
```

**`zip`** — «сцепляет» несколько последовательностей в пары:

```python
names = ["Anna", "Bob"]
ages = [25, 30]
for name, age in zip(names, ages):
    print(name, age)
```

---

### Синтаксис comprehensions

#### List comprehension

```python
[выражение for элемент in последовательность]
[выражение for элемент in последовательность if условие]
```

| Часть | Роль |
|-------|------|
| `выражение` | Что попадёт в результат |
| `for элемент in ...` | Откуда берём |
| `if условие` | Фильтр (опционально) |

```python
# Без фильтра
evens = [x for x in range(10) if x % 2 == 0]

# С преобразованием
upper = [w.upper() for w in ["hi", "py"]]
```

#### Вложенный comprehension

```python
matrix = [[1, 2], [3, 4]]
flat = [x for row in matrix for x in row]
# [1, 2, 3, 4]
```

Читается слева направо: «для каждой row, для каждого x в row».

#### Dict comprehension

```python
{ключ: значение for элемент in последовательность}
```

```python
words = ["apple", "banana"]
{w: len(w) for w in words}    # {'apple': 5, 'banana': 6}
```

#### Generator expression — ленивая версия

```python
gen = (x ** 2 for x in range(1000000))   # круглые скобки!
```

Не создаёт список сразу — отдаёт значения **по одному** (подробнее в продвинутых темах). Для Junior: знай, что `(x for x in ...)` — как list comprehension, но «ленивый».

---

### `enumerate` — индекс без `range(len())`

```python
# Старый способ — длиннее
for i in range(len(items)):
    print(i, items[i])

# Питоновский способ
for i, item in enumerate(items):
    print(i, item)

# Нумерация с 1
for i, item in enumerate(items, start=1):
    print(i, item)
```

`enumerate` возвращает пары `(индекс, элемент)`.

---

### `zip` — параллельный обход

```python
names = ["Anna", "Bob", "Vika"]
scores = [85, 92, 78]

pairs = list(zip(names, scores))
# [('Anna', 85), ('Bob', 92), ('Vika', 78)]
```

**Длина** — по **короткой** последовательности:

```python
list(zip([1, 2, 3], ["a", "b"]))    # [(1, 'a'), (2, 'b')]
```

**Распаковка** — «транспонирование»:

```python
pairs = [("Anna", 85), ("Bob", 92)]
names, scores = zip(*pairs)
# names = ('Anna', 'Bob'), scores = (85, 92)
```

---

### `map` и `filter` — функциональный стиль

```python
# map — применить функцию к каждому элементу
list(map(str, [1, 2, 3]))           # ['1', '2', '3']

# filter — оставить по условию
list(filter(lambda x: x > 0, [-1, 2, -3, 4]))   # [2, 4]
```

На Junior чаще используют **comprehension** — читается лучше:

```python
[str(x) for x in [1, 2, 3]]
[x for x in [-1, 2, -3, 4] if x > 0]
```

---

### `any` и `all` — проверка коллекции

```python
any([False, False, True])     # True — хоть один True
all([True, True, False])      # False — все True?

any(x > 0 for x in [-1, -2])  # False
all(x > 0 for x in [1, 2, 3])  # True
```

С **generator expression** внутри — без создания списка в памяти.

---

### Как это работает «под капотом»

#### List comprehension ≈ цикл + append

```python
[x ** 2 for x in range(3)]
```

Python примерно:
1. Создаёт пустой list
2. Итерирует `range(3)`
3. Для каждого `x` вычисляет `x ** 2`
4. Если есть `if` — проверяет условие
5. Добавляет в list (оптимизировано на C-уровне — быстрее ручного append)

#### `enumerate` — генератор пар

Не создаёт список всех пар сразу — отдаёт по одной при итерации.

#### `zip` — тоже генератор

`zip(a, b)` строит кортежи «на лету» из итераторов `a` и `b`.

#### Dict comprehension и hash

Ключи dict должны быть **hashable** — как в главе 5.

---

### Где это полезно и применяется в реальной разработке

| Инструмент | Применение |
|------------|------------|
| List comprehension | Трансформация данных API, фильтрация |
| Dict comprehension | Маппинг id→объект, инверсия словаря |
| `enumerate` | Нумерованные списки, отчёты |
| `zip` | Сборка записей из колонок CSV |
| `any`/`all` | Валидация: «все поля заполнены?», «есть ошибка?» |

**Пример — ответ API → список имён:**

```python
users = [{"name": "Anna", "active": True}, {"name": "Bob", "active": False}]
active_names = [u["name"] for u in users if u["active"]]
```

**Пример — CSV-колонки → записи:**

```python
headers = ["id", "name", "score"]
rows = [[1, "Anna", 90], [2, "Bob", 85]]
records = [dict(zip(headers, row)) for row in rows]
```

---

### Микро-моменты, нюансы, частые ошибки новичков

#### 1. Comprehension ради comprehension — не усложняй

```python
# Плохо — нечитаемо
result = [x for sub in [[1,2],[3,4]] for x in sub if x % 2 == 0 if x > 1]

# Лучше — обычный цикл для сложной логики
```

**Правило:** 1–2 `for`, 1 `if` — OK. Больше — разбей на цикл или функцию.

#### 2. Побочные эффекты в comprehension — нельзя

```python
# ПЛОХО — print в comprehension
[print(x) for x in range(3)]   # создаёт [None, None, None]!

# ХОРОШО
for x in range(3):
    print(x)
```

Comprehension — для **создания** коллекции, не для действий.

#### 3. `if-else` в выражении — другой синтаксис

```python
# Фильтр (в конце)
[x for x in range(5) if x % 2 == 0]

# if-else в ВЫРАЖЕНИИ (в начале, с else)
["чёт" if x % 2 == 0 else "нечёт" for x in range(4)]
```

#### 4. Забыли `list()` вокруг `zip`/`map`

```python
z = zip([1, 2], ["a", "b"])
print(z)              # <zip object> — итератор
print(list(z))        # [(1, 'a'), (2, 'b')]
```

#### 5. `zip` обрезает по короткому

Проверяй длины, если важно не потерять данные.

#### 6. Пустой comprehension

```python
[x for x in [] if x > 0]    # []
{x: x for x in []}          # {}
```

#### 7. Переменная цикла «утекает»?

В Python 3 переменная comprehension **остаётся** после:

```python
[x for x in range(3)]
print(x)    # 2 — последнее значение!
```

Используй осмысленные имена; для одноразовых — `_` не всегда защищает в старых версиях.

#### 8. Dict comprehension — дубликаты ключей

```python
{x % 3: x for x in range(6)}    # ключи 0,1,2 — последний побеждает
```

#### 9. `enumerate` не копирует данные

Работает с итератором — лениво.

#### 10. `all([])` → `True`, `any([])` → `False`

Пустая коллекция: all «вакуумно истинно», any — ложно.

---

## Практика

> **Навигация:** **30 примеров**, шпаргалка, FAQ, домашка.

### Пример 1: Базовый list comprehension

```python
# Циклом
squares_loop = []
for x in range(1, 6):
    squares_loop.append(x ** 2)

# Comprehension
squares = [x ** 2 for x in range(1, 6)]

print(squares_loop)
print(squares)
print(squares_loop == squares)    # True
```

**Вывод консоли:**

```
[1, 4, 9, 16, 25]
[1, 4, 9, 16, 25]
True
```

---

### Пример 2: Comprehension с фильтром `if`

```python
# Только чётные
evens = [x for x in range(20) if x % 2 == 0]
print(evens)

# Только длинные слова
words = ["hi", "python", "go", "javascript"]
long_words = [w for w in words if len(w) > 2]
print(long_words)

# Только положительные
nums = [-3, -1, 0, 2, 5, -7]
positive = [n for n in nums if n > 0]
print(positive)
```

**Вывод консоли:**

```
[0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
['python', 'go', 'javascript']
[2, 5]
```

---

### Пример 3: Преобразование элементов

```python
names = ["anna", "boris", "vika"]
capitalized = [name.capitalize() for name in names]
print(capitalized)

prices_str = ["100", "250", "75"]
prices = [int(p) for p in prices_str]
print(prices)

# С условием в выражении (if-else)
labels = ["чёт" if n % 2 == 0 else "нечёт" for n in range(5)]
print(labels)
```

**Вывод консоли:**

```
['Anna', 'Boris', 'Vika']
[100, 250, 75]
['чёт', 'нечёт', 'чёт', 'нечёт', 'чёт']
```

---

### Пример 4: Вложенный comprehension — flatten

```python
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]

# Развернуть в один list
flat = [x for row in matrix for x in row]
print(flat)

# Только чётные из матрицы
evens = [x for row in matrix for x in row if x % 2 == 0]
print(evens)
```

**Вывод консоли:**

```
[1, 2, 3, 4, 5, 6, 7, 8, 9]
[2, 4, 6, 8]
```

---

### Пример 5: Dict comprehension

```python
# Квадраты
squares = {n: n ** 2 for n in range(1, 6)}
print(squares)

# Длины слов
words = ["apple", "banana", "cherry"]
lengths = {w: len(w) for w in words}
print(lengths)

# Инверсия (значения уникальны!)
original = {"a": 1, "b": 2, "c": 3}
inverted = {v: k for k, v in original.items()}
print(inverted)

# Фильтр — только длинные слова
long_only = {w: len(w) for w in words if len(w) > 5}
print(long_only)
```

**Вывод консоли:**

```
{1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
{'apple': 5, 'banana': 6, 'cherry': 6}
{1: 'a', 2: 'b', 3: 'c'}
{'banana': 6, 'cherry': 6}
```

---

### Пример 6: Set comprehension

```python
text = "hello world hello"
unique_chars = {c for c in text if c != " "}
print(unique_chars)

# Уникальные длины слов
words = ["hi", "hello", "hi", "py", "hello"]
unique_lengths = {len(w) for w in words}
print(unique_lengths)
```

**Вывод консоли (порядок set может отличаться):**

```
{'h', 'e', 'l', 'o', 'w', 'r', 'd'}
{2, 5}
```

---

### Пример 7: `enumerate` — базовое использование

```python
fruits = ["яблоко", "банан", "вишня"]

print("С нуля:")
for i, fruit in enumerate(fruits):
    print(f"  {i}: {fruit}")

print("С единицы:")
for i, fruit in enumerate(fruits, start=1):
    print(f"  {i}. {fruit}")
```

**Вывод консоли:**

```
С нуля:
  0: яблоко
  1: банан
  2: вишня
С единицы:
  1. яблоко
  2. банан
  3. вишня
```

---

### Пример 8: `enumerate` — найти индекс элемента

```python
def find_index(items, target):
    for i, item in enumerate(items):
        if item == target:
            return i
    return -1

nums = [10, 20, 30, 20, 40]
print(find_index(nums, 30))    # 2
print(find_index(nums, 99))    # -1

# Первое вхождение 20
print(find_index(nums, 20))    # 1
```

**Вывод консоли:**

```
2
-1
1
```

---

### Пример 9: `zip` — параллельный обход

```python
names = ["Анна", "Борис", "Вика"]
ages = [25, 30, 22]
cities = ["Москва", "Казань", "Сочи"]

print("Профили:")
for name, age, city in zip(names, ages, cities):
    print(f"  {name}, {age} лет, {city}")

# В list кортежей
pairs = list(zip(names, ages))
print(pairs)
```

**Вывод консоли:**

```
Профили:
  Анна, 25 лет, Москва
  Борис, 30 лет, Казань
  Вика, 22 лет, Сочи
[('Анна', 25), ('Борис', 30), ('Вика', 22)]
```

---

### Пример 10: `zip` — разная длина

```python
nums = [1, 2, 3, 4, 5]
letters = ["a", "b", "c"]

print(list(zip(nums, letters)))
# [(1, 'a'), (2, 'b'), (3, 'c')] — обрезано по 3

# Проверка длин
if len(nums) != len(letters):
    print(f"Внимание: {len(nums)} чисел, {len(letters)} букв")
```

**Вывод консоли:**

```
[(1, 'a'), (2, 'b'), (3, 'c')]
Внимание: 5 чисел, 3 букв
```

---

### Пример 11: `zip` + dict — сборка записей

```python
keys = ["id", "name", "score"]
values_list = [
    [1, "Anna", 92],
    [2, "Bob", 78],
    [3, "Vika", 95],
]

students = [dict(zip(keys, row)) for row in values_list]
for s in students:
    print(s)
```

**Вывод консоли:**

```
{'id': 1, 'name': 'Anna', 'score': 92}
{'id': 2, 'name': 'Bob', 'score': 78}
{'id': 3, 'name': 'Vika', 'score': 95}
```

---

### Пример 12: Распаковка `zip(*...)`

```python
pairs = [("Anna", 25), ("Bob", 30), ("Vika", 22)]

names, ages = zip(*pairs)
print(names)    # ('Anna', 'Bob', 'Vika')
print(ages)     # (25, 30, 22)
print(type(names))   # tuple
```

**Вывод консоли:**

```
('Anna', 'Bob', 'Vika')
(25, 30, 22)
<class 'tuple'>
```

---

### Пример 13: `any` и `all`

```python
nums = [2, 4, 6, 8]
print(any(n > 5 for n in nums))     # True
print(all(n > 0 for n in nums))     # True
print(all(n % 2 == 0 for n in nums))  # True

nums2 = [1, 2, 3, 4]
print(any(n > 10 for n in nums2))   # False
print(all(n > 2 for n in nums2))    # False

# Пустой
print(any([]))    # False
print(all([]))    # True!
```

**Вывод консоли:**

```
True
True
True
False
False
False
True
```

---

### Пример 14: `map` vs comprehension

```python
nums = [1, 2, 3, 4, 5]

# map
doubled_map = list(map(lambda x: x * 2, nums))

# comprehension — предпочтительнее на Junior
doubled = [x * 2 for x in nums]

print(doubled_map)
print(doubled)

# str для всех
strings = [str(n) for n in nums]
print(strings)
```

**Вывод консоли:**

```
[2, 4, 6, 8, 10]
[2, 4, 6, 8, 10]
['1', '2', '3', '4', '5']
```

---

### Пример 15: `filter` vs comprehension

```python
nums = [-3, -1, 0, 2, 5, -7]

# filter
positive_f = list(filter(lambda x: x > 0, nums))

# comprehension
positive = [x for x in nums if x > 0]

print(positive_f)
print(positive)
```

**Вывод консоли:**

```
[2, 5]
[2, 5]
```

---

### Пример 16: Комбо — обработка данных пользователей

```python
users = [
    {"name": "anna", "age": 17, "active": True},
    {"name": "boris", "age": 25, "active": False},
    {"name": "vika", "age": 22, "active": True},
    {"name": "den", "age": 16, "active": True},
]

# Активные совершеннолетние — имена с заглавной
adults = [
    u["name"].capitalize()
    for u in users
    if u["active"] and u["age"] >= 18
]
print("Активные 18+:", adults)

# Есть ли несовершеннолетние активные?
has_minors = any(u["active"] and u["age"] < 18 for u in users)
print("Есть несовершеннолетние:", has_minors)

# Все ли имена в нижнем регистре в данных?
all_lower = all(u["name"] == u["name"].lower() for u in users)
print("Все имена lower:", all_lower)
```

**Вывод консоли:**

```
Активные 18+: ['Vika']
Есть несовершеннолетние: True
Все имена lower: True
```

---

### Пример 17: Таблица через zip и enumerate

```python
headers = ["#", "Товар", "Цена", "Кол-во"]
rows = [
    ["яблоко", 89.90, 3],
    ["молоко", 69.50, 1],
    ["сыр", 350.00, 2],
]

print(" | ".join(headers))
print("-" * 40)
for i, row in enumerate(rows, start=1):
    name, price, qty = row
    print(f"{i} | {name} | {price:.2f} | {qty}")
```

**Вывод консоли:**

```
# | Товар | Цена | Кол-во
----------------------------------------
1 | яблоко | 89.90 | 3
2 | молоко | 69.50 | 1
3 | сыр | 350.00 | 2
```

---

### Пример 18: Dict из двух list через zip

```python
keys = ["name", "age", "city"]
values = ["Дима", 28, "Омск"]

user = dict(zip(keys, values))
print(user)

# Несколько пользователей
names = ["Anna", "Bob"]
ages = [25, 30]
users = [dict(zip(["name", "age"], pair)) for pair in zip(names, ages)]
print(users)
```

**Вывод консоли:**

```
{'name': 'Дима', 'age': 28, 'city': 'Омск'}
[{'name': 'Anna', 'age': 25}, {'name': 'Bob', 'age': 30}]
```

---

## Теория (дополнение): когда что использовать, вложенность, производительность

### Comprehension vs цикл — таблица решений

| Ситуация | Рекомендация |
|----------|--------------|
| Простая трансформация / фильтр | Comprehension |
| Побочные эффекты (`print`, запись в файл) | `for` |
| Несколько веток логики | `for` или функция |
| Вложенность 3+ уровней | `for` |
| Нужен `break` / `continue` сложный | `for` |

---

### Вложенные comprehensions — матрица

```python
# Создать матрицу 3x3 нулей
matrix = [[0 for _ in range(3)] for _ in range(3)]
print(matrix)

# Таблица умножения
table = {i: {j: i * j for j in range(1, 6)} for i in range(1, 6)}
print(table[3])    # {1: 3, 2: 6, 3: 9, 4: 12, 5: 15}
```

**Осторожно с ловушкой:**

```python
# НЕПРАВИЛЬНО — одна ссылка на list!
bad = [[0] * 3] * 3
bad[0][0] = 1
print(bad)    # [[1,0,0], [1,0,0], [1,0,0]] — все строки связаны!

# ПРАВИЛЬНО
good = [[0 for _ in range(3)] for _ in range(3)]
```

---

### Generator expression — экономия памяти

```python
import sys

lst = [x ** 2 for x in range(10000)]      # list в памяти
gen = (x ** 2 for x in range(10000))      # генератор

print(sys.getsizeof(lst))    # десятки KB
print(sys.getsizeof(gen))    # ~200 байт

# sum принимает итератор
total = sum(x for x in range(1000) if x % 3 == 0)
print(total)
```

---

### Пошаговый разбор: `[x*2 for x in a if x>0]`

```python
a = [-1, 2, -3, 4]
```

| x | x > 0? | x*2 | В результат? |
|---|--------|-----|--------------|
| -1 | False | — | нет |
| 2 | True | 4 | да |
| -3 | False | — | нет |
| 4 | True | 8 | да |

Результат: `[4, 8]`

---

## Практика — примеры 19–30 (продолжение)

### Пример 19: Подсчёт через dict comprehension + условие

```python
words = ["apple", "banana", "apple", "cherry", "banana", "apple"]

# Обычный способ — цикл + get
counts = {}
for w in words:
    counts[w] = counts.get(w, 0) + 1

# Через set уникальных + dict comp (для понимания)
unique = set(words)
counts2 = {w: words.count(w) for w in unique}
print(counts)
print(counts2)
```

**Вывод консоли:**

```
{'apple': 3, 'banana': 2, 'cherry': 1}
{'cherry': 1, 'banana': 2, 'apple': 3}
```

---

### Пример 20: Фильтрация и сортировка в одной цепочке

```python
grades = [85, 92, 78, 60, 100, 55, 88]

# Прошедшие (>= 70), отсортированные
passed = sorted([g for g in grades if g >= 70], reverse=True)
print("Сдали:", passed)

# Статистика одной строкой
failed_count = len([g for g in grades if g < 60])
print("Не сдали:", failed_count)
```

**Вывод консоли:**

```
Сдали: [100, 92, 88, 85, 78]
Не сдали: 1
```

---

### Пример 21: enumerate + zip — нумерованный список пар

```python
questions = ["Имя?", "Возраст?", "Город?"]
answers = ["Anna", "25", "Moscow"]

print("Анкета:")
for i, (q, a) in enumerate(zip(questions, answers), start=1):
    print(f"  {i}. {q} → {a}")
```

**Вывод консоли:**

```
Анкета:
  1. Имя? → Anna
  2. Возраст? → 25
  3. Город? → Moscow
```

---

### Пример 22: Валидация формы через `all`

```python
def validate_form(fields):
    """
    fields — dict поле→значение.
    Все строковые поля не пустые после strip?
    """
    checks = [
        isinstance(v, str) and len(v.strip()) > 0
        for v in fields.values()
    ]
    return all(checks)

print(validate_form({"name": "Anna", "email": "a@b.com"}))   # True
print(validate_form({"name": "  ", "email": "a@b.com"}))    # False
print(validate_form({"name": "Bob", "email": ""}))         # False
```

**Вывод консоли:**

```
True
False
False
```

---

### Пример 23: Поиск ошибок в логах через `any`

```python
log_lines = [
    "INFO: started",
    "INFO: processing",
    "ERROR: connection failed",
    "INFO: retry",
]

has_error = any("ERROR" in line for line in log_lines)
error_lines = [line for line in log_lines if "ERROR" in line]

print("Есть ошибки:", has_error)
print("Ошибки:", error_lines)
```

**Вывод консоли:**

```
Есть ошибки: True
Ошибки: ['ERROR: connection failed']
```

---

### Пример 24: Транспонирование матрицы через zip

```python
matrix = [
    [1, 2, 3],
    [4, 5, 6],
]

# Строки → столбцы
transposed = [list(col) for col in zip(*matrix)]
print("Исходная:", matrix)
print("Транспонированная:", transposed)
```

**Вывод консоли:**

```
Исходная: [[1, 2, 3], [4, 5, 6]]
Транспонированная: [[1, 4], [2, 5], [3, 6]]
```

---

### Пример 25: Generator expression в функциях

```python
# max/min/sum принимают итератор
data = [1, 5, 3, 9, 2, 7]

max_even = max(x for x in data if x % 2 == 0)
min_positive = min(x for x in data if x > 0)
sum_big = sum(x for x in data if x > 5)

print(max_even, min_positive, sum_big)
```

**Вывод консоли:**

```
8 1 16
```

---

### Пример 26: Словарь группировки через comprehension (упрощённо)

```python
words = ["apple", "banana", "apricot", "blueberry", "avocado"]

# Группировка по первой букве — через цикл понятнее, но покажем идею
letters = {w[0] for w in words}
grouped = {letter: [w for w in words if w[0] == letter] for letter in letters}

for letter in sorted(grouped):
    print(f"{letter}: {grouped[letter]}")
```

**Вывод консоли:**

```
a: ['apple', 'apricot', 'avocado']
b: ['banana', 'blueberry']
```

---

### Пример 27: Замена вложенного цикла — cartesian product

```python
colors = ["red", "green"]
sizes = ["S", "M"]

# Все комбинации
combinations = [(c, s) for c in colors for s in sizes]
print(combinations)

# С фильтром — только red
red_combos = [(c, s) for c in colors for s in sizes if c == "red"]
print(red_combos)
```

**Вывод консоли:**

```
[('red', 'S'), ('red', 'M'), ('green', 'S'), ('green', 'M')]
[('red', 'S'), ('red', 'M')]
```

---

### Пример 28: `enumerate` + условие — только чётные индексы

```python
data = ["a", "b", "c", "d", "e", "f"]

selected = [item for i, item in enumerate(data) if i % 2 == 0]
print(selected)

# Или
for i, item in enumerate(data):
    if i % 2 == 0:
        print(f"  [{i}] {item}")
```

**Вывод консоли:**

```
['a', 'c', 'e']
  [0] a
  [2] c
  [4] e
```

---

### Пример 29: Мини-проект — отчёт по продажам

```python
sales = [
    {"product": "яблоко", "qty": 10, "price": 89.90},
    {"product": "молоко", "qty": 5, "price": 69.50},
    {"product": "сыр", "qty": 2, "price": 350.00},
    {"product": "яблоко", "qty": 3, "price": 89.90},
]

# Сумма по каждой строке
totals = [
    {**s, "total": round(s["qty"] * s["price"], 2)}
    for s in sales
]

# Общая выручка
revenue = sum(t["total"] for t in totals)

# Товары с выручкой > 500
big = [t["product"] for t in totals if t["total"] > 500]

# Таблица
print(f"{'#':<3} {'Товар':<10} {'Сумма':>10}")
for i, t in enumerate(totals, start=1):
    print(f"{i:<3} {t['product']:<10} {t['total']:>10.2f}")
print(f"{'ИТОГО':<14} {revenue:>10.2f}")
print("Крупные (>500):", big)
```

**Вывод консоли:**

```
#   Товар           Сумма
1   яблоко         899.00
2   молоко         347.50
3   сыр            700.00
4   яблоко         269.70
ИТОГО            2216.20
Крупные (>500): ['яблоко', 'сыр', 'яблоко']
```

**Разбор `{**s, "total": ...}`:** «скопируй все ключи из словаря `s` и добавь поле `total`».  
Это распаковка dict — на Junior достаточно знать: **новый словарь = старые поля + одно новое**.  
Эквивалент без `**`: `{"product": s["product"], "qty": s["qty"], "price": s["price"], "total": ...}`.

---

### Пример 30: Антипаттерн vs чистый код

```python
# ПЛОХО — нечитаемо
result_bad = [str(y) for x in [[1,2],[3,4]] for y in x if y > 1 if y % 2 == 0]

# ХОРОШО — явный цикл
result_good = []
for sublist in [[1, 2], [3, 4]]:
    for y in sublist:
        if y > 1 and y % 2 == 0:
            result_good.append(str(y))

print(result_bad)
print(result_good)

# СРЕДНЕ — однострочник, но ещё читаемо
result_ok = [str(y) for sub in [[1,2],[3,4]] for y in sub if y > 1 and y % 2 == 0]
print(result_ok)
```

**Вывод консоли:**

```
['2', '4']
['2', '4']
['2', '4']
```

---

## Шпаргалка

```python
# List
[x * 2 for x in range(5)]
[x for x in data if x > 0]
["чёт" if x % 2 == 0 else "нечёт" for x in range(4)]
[x for row in matrix for x in row]

# Dict
{k: v for k, v in items}
{w: len(w) for w in words}

# Set
{len(w) for w in words}

# Generator (ленивый)
(x ** 2 for x in range(10))
sum(x for x in data if x > 0)

# enumerate
for i, x in enumerate(lst, start=1): ...

# zip
for a, b in zip(list1, list2): ...
dict(zip(keys, values))
names, ages = zip(*pairs)

# any / all
any(x > 0 for x in data)
all(x.valid for x in users)
```

---

## FAQ начинающего

**В: Comprehension всегда лучше цикла?**  
Нет. Лучше — **читаемее**. Простые случаи — comprehension.

**В: Можно ли `break` в comprehension?**  
Нет. Используй цикл.

**В: `zip` возвращает list?**  
В Python 3 — итератор. `list(zip(...))` для списка.

**В: `enumerate` копирует list?**  
Нет, итерирует лениво.

**В: Зачем `_` в `for _ in range(3)`?**  
Показывает: переменная цикла не используется.

**В: Dict comp — порядок ключей?**  
С 3.7+ — порядок вставки (как в обычном dict).

**В: `all([])` почему True?**  
Матемическая конвенция «для всех элементов пустого множества». Запомни.

**В: Разница `[x for x in a]` и `list(a)`?**  
Для простого копирования list — `a.copy()` или `a[:]`. Comprehension — если есть фильтр/маппинг.

**В: Несколько `if` в comprehension?**  
`[x for x in a if a_cond if b_cond]` — редко. Обычно `if a_cond and b_cond`.

**В: Walrus `:=` в comprehension?**  
Python 3.8+: `[y for x in data if (y := f(x)) > 0]` — продвинуто, на Junior не обязательно.

**В: `zip` с dict?**  
`zip(d.keys(), d.values())` — пары ключ-значение. Проще: `d.items()`.

---

### Сравнение: цикл vs comprehension vs map/filter

| Задача | Цикл | Comprehension | map/filter |
|--------|------|---------------|------------|
| Удвоить числа | 5 строк | 1 строка | `map` |
| Только > 0 | 6 строк | 1 строка | `filter` |
| Сложная логика | ✅ лучший | ❌ | ❌ |
| Читаемость Junior | OK | ✅ часто | средне |

---

### Встроенные функции — связь с главой 7

| Функция | Что делает | Аналог comprehension |
|---------|------------|----------------------|
| `len(x)` | Длина | — |
| `range(n)` | Числа 0..n-1 | — |
| `enumerate(x)` | Индекс + элемент | — |
| `zip(a, b)` | Пары | — |
| `sum(iter)` | Сумма | `sum(x for x in ...)` |
| `min`/`max` | Мин/макс | `max(x for x in ...)` |
| `sorted(x)` | Сортировка | `sorted([... for ...])` |
| `any`/`all` | Логика на коллекции | с generator expr |

---

### Частые баги

```python
# БАГ: print в comprehension
[print(x) for x in a]   # [None, None, ...]

# БАГ: [[0]*3]*3
[[0 for _ in range(3)] for _ in range(3)]

# БАГ: забыли list() при нужде в списке
z = zip(a, b)   # итератор — один проход!

# БАГ: if-else перепутали местами
# фильтр:  [x for x in a if cond]
# ветвление: [a if cond else b for x in ...]
```

---

## Домашнее задание

**Файл:** `homework_07.py`

### Задача 1 — Лёгкая
Создай list квадратов чисел 1–20, делящихся на 3.

<details>
<summary>Подсказка</summary>

`[x**2 for x in range(1, 21) if x % 3 == 0]`

</details>

---

### Задача 2 — Лёгкая
Дан `words = ["Python", "is", "awesome"]`. Одной строкой comprehension: list длин слов.

---

### Задача 3 — Средняя
Дан `text = "hello world from python world"`. Получи:
1. list уникальных слов (без set в исходнике — можно `list(set(...))` в результате)
2. dict `{слово: количество}`

<details>
<summary>Подсказка</summary>

`words = text.split()`. Счётчик: цикл + get или `{w: words.count(w) for w in set(words)}`.

</details>

---

### Задача 4 — Средняя
Две list одинаковой длины: `names`, `scores`. Собери `list` of `dict` через `zip`. Выведи только тех, у кого score >= 80.

<details>
<summary>Подсказка</summary>

`[dict(zip(["name","score"], pair)) for pair in zip(names, scores) if pair[1] >= 80]`

</details>

---

### Задача 5 — Средняя
Напиши `numbered_list(items)` → list строк `"1. item"` через `enumerate`.

```python
numbered_list(["a", "b", "c"])
# ['1. a', '2. b', '3. c']
```

<details>
<summary>Подсказка</summary>

`[f"{i}. {item}" for i, item in enumerate(items, start=1)]`

</details>

---

### Задача 6 — Сложная
Матрица 4×4 случайных чисел 1–9 (или заданная). Без numpy:
1. Создай через вложенный comprehension
2. Транспонируй через `zip`
3. Сумма каждой **строки** — list из 4 чисел
4. Сумма каждого **столбца** — list из 4 чисел

<details>
<summary>Подсказка</summary>

Матрица: `[[... for _ in range(4)] for _ in range(4)]`. Столбцы: `zip(*matrix)`, сумма: `sum(col)`.

</details>

---

### Задача 7 — Сложная
Дан list словарей заказов (как в Примере 29). Верни dict `{product: total_qty}` — суммарное количество по каждому товару.

<details>
<summary>Подсказка</summary>

Цикл + dict-счётчик, или `collections.Counter` (если знаешь). Без Counter: `totals.get(product, 0) + qty`.

</details>

---

### Задача 8 — Сложная
`validate_passwords(passwords)` → list of tuple `(password, is_valid, errors)`:
- длина >= 8
- есть цифра (`any(c.isdigit() for c in pwd)`)
- нет пробелов

Используй comprehension для финального списка результатов.

---

### Задача 9 — Сложная (бонус)
Напиши `pivot_csv(headers, rows)`:
- `headers` — list строк
- `rows` — list of list
- возвращает `list` of `dict` через zip
- затем фильтрует записи, где поле `"active"` == `"yes"` (строка)

---

### Задача 10 — Сложная (бонус)
**Cartesian menu:** `categories = ["пицца", "напитки"]`, `items = {"пицца": ["Маргарита", "Пепперони"], "напитки": ["Кола", "Вода"]}`.  
Собери все пары `(категория, товар)` через comprehension. Выведи нумерованный меню через `enumerate`.

---

### Как сдавать

- `homework_07.py`
- Задачи 6–10 — с тестовыми данными
- Частями: 1–5, 6–10

**Критерии:**
- Comprehension там, где код читается
- Цикл там, где логика сложная
- `zip`/`enumerate` уместно
- Нет побочных эффектов в comprehension

---

**Сделай задачи сам и пришли код на проверку. После проверки — Глава 8: *Работа с файлами и JSON*.**

---
Конец главы.