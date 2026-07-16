# Тема: Списки, кортежи, множества, словари

> **Файл:** `homework_04.py`  
> **Мостик из гл. 3:** строки `split`/`join` → здесь списки слов и словари «ключ → значение».  
> **Маршрут ученика:** ДЗ 1–5 → примеры **1–10, 9**; ДЗ 6–7 → + **14, 21**; примеры 11–16 → **глава 7** (можно пропустить); 19–25 — справочник.

## Теория

### Что это такое

В первых главах ты работал с **одиночными** значениями: одно число, одна строка. В реальности данные почти всегда идут **группами**: список товаров, имена студентов, уникальные теги, словарь «логин → пароль».

Python даёт четыре главные **коллекции** (структуры данных):

| Тип | Синтаксис | Изменяемый? | Упорядоченный? | Дубликаты? |
|-----|-----------|-------------|----------------|------------|
| **list** (список) | `[1, 2, 3]` | ✅ Да | ✅ Да | ✅ Да |
| **tuple** (кортеж) | `(1, 2, 3)` | ❌ Нет | ✅ Да | ✅ Да |
| **set** (множество) | `{1, 2, 3}` | ✅ Да | ❌ Нет* | ❌ Нет |
| **dict** (словарь) | `{"a": 1}` | ✅ Да | ✅ Да** | Ключи — нет |

\* В Python 3.7+ `set` технически сохраняет порядок вставки, но **по смыслу** на него не опираются — это про уникальность.  
\** С Python 3.7+ словари сохраняют порядок добавления ключей.

---

#### Список (`list`) — изменяемая упорядоченная коллекция

Список — «контейнер» для любых объектов: числа, строки, другие списки, разные типы вперемешку.

```python
numbers = [10, 20, 30, 40]
mixed = [1, "hello", 3.14, True]
empty = []
```

**Создание:**
```python
list(range(5))          # [0, 1, 2, 3, 4]
list("abc")             # ['a', 'b', 'c']
[0] * 5                 # [0, 0, 0, 0, 0]
```

**Доступ** — как у строк: индексы, срезы, `len()`:

```python
fruits = ["яблоко", "банан", "вишня"]
print(fruits[0])         # яблоко
print(fruits[-1])        # вишня
print(fruits[1:3])       # ['банан', 'вишня']
fruits[0] = "груша"      # можно менять! (в отличие от str)
```

---

#### Кортеж (`tuple`) — неизменяемый список

```python
point = (10, 20)
colors = ("red", "green", "blue")
single = (42,)          # запятая обязательна! иначе это просто число в скобках
empty_tuple = ()
```

**Зачем кортеж, если есть список?**
- Данные **не должны меняться** (координаты, дата рождения, настройки)
- Можно использовать как **ключ словаря** (список — нельзя)
- Чуть быстрее и занимает меньше памяти
- Распаковка: `x, y = point`

```python
coords = (55.75, 37.62)
# coords[0] = 0   # TypeError — нельзя!
```

---

#### Множество (`set`) — уникальные элементы без дубликатов

```python
tags = {"python", "junior", "python"}   # {"python", "junior"} — дубль убран
unique = set([1, 2, 2, 3, 3, 3])       # {1, 2, 3}
empty_set = set()                       # НЕ {} — это пустой dict!
```

**Зачем set:**
- Убрать дубликаты
- Быстрая проверка «есть ли элемент» (`in`)
- Операции теории множеств: пересечение, объединение, разность

```python
a = {1, 2, 3}
b = {3, 4, 5}
a | b    # {1, 2, 3, 4, 5} — объединение
a & b    # {3} — пересечение
a - b    # {1, 2} — разность
```

---

#### Словарь (`dict`) — пары «ключ → значение»

```python
user = {
    "name": "Анна",
    "age": 25,
    "email": "anna@mail.com"
}

print(user["name"])       # Анна — доступ по ключу
user["age"] = 26          # изменить значение
user["city"] = "Москва"   # добавить новую пару
```

**Ключи** должны быть **неизменяемыми** (hashable): `str`, `int`, `tuple` — да; `list`, `dict` — нет.

```python
# {[1,2]: "bad"}   # TypeError — list нельзя как ключ
{(1, 2): "ok"}     # tuple — можно
```

**Зачем dict:**
- Быстрый поиск по ключу (имя → телефон, id → объект)
- JSON в Python — это `dict`
- Конфигурация приложения, кэш, счётчики

---

### Как это работает «под капотом»

#### Список — динамический массив

Список в CPython — массив **ссылок** на объекты. При `append` массив растёт; когда места не хватает — выделяется больший блок (амортизированно O(1) на добавление в конец).

```python
a = [1, 2, 3]
b = a              # b ссылается на ТОТ ЖЕ список
b.append(4)
print(a)           # [1, 2, 3, 4] — оба изменились!
```

**Важно:** `b = a` — не копия, а **общая ссылка**. Для копии: `b = a.copy()` или `b = a[:]`.

#### Кортеж — неизменяемый массив

Фиксированный размер. При «изменении» создаётся новый кортеж. Хранится в памяти компактнее списка.

#### Множество — хеш-таблица

Как `dict`, но только ключи (без значений). Поиск `x in my_set` — в среднем **O(1)** — очень быстро на больших данных.

```python
# list — O(n) для поиска
1000000 in huge_list      # медленно

# set — O(1) в среднем
1000000 in huge_set       # быстро
```

#### Словарь — хеш-таблица ключ → значение

По ключу вычисляется **хеш** — число, по которому мгновенно находится «ячейка» со значением. Поэтому `user["name"]` быстрее, чем перебор списка кортежей.

**Ключ должен быть hashable** — иметь стабильный хеш на время жизни в словаре.

#### Сравнение мутабельности (из главы 1 — теперь на практике)

| Тип | Можно `obj[i] = x`? | Методы меняют на месте? |
|-----|---------------------|-------------------------|
| `list` | ✅ | ✅ `.append()`, `.sort()` |
| `tuple` | ❌ | — |
| `set` | — (нет индексов) | ✅ `.add()`, `.remove()` |
| `dict` | — (доступ по ключу) | ✅ `d[k] = v`, `.pop()` |
| `str` | ❌ | методы возвращают новую строку |

---

### Где это полезно и применяется в реальной разработке

| Структура | Реальный пример |
|-----------|-----------------|
| `list` | Список заказов, строки из файла, история сообщений |
| `tuple` | Координаты, `(status_code, response_body)`, возврат нескольких значений из функции |
| `set` | Уникальные user_id, теги, «кто уже видел пост» |
| `dict` | JSON API, настройки `{"theme": "dark"}`, кэш `{url: html}` |

**Типичный пайплайн:**

```python
# 1. Прочитали строки лога в список
lines = ["ERROR: disk full", "INFO: started", "ERROR: timeout"]

# 2. Отфильтровали в новый список
errors = [line for line in lines if line.startswith("ERROR")]

# 3. Посчитали уникальные типы ошибок через set
unique_msgs = set()
for line in errors:
    unique_msgs.add(line.split(":", 1)[1].strip())

# 4. Словарь-счётчик: сколько раз каждая ошибка
counts = {}
for line in errors:
    msg = line.split(":", 1)[1].strip()
    counts[msg] = counts.get(msg, 0) + 1
```

**Как выбрать структуру:**

```
Нужны пары ключ→значение?     → dict
Нужна уникальность?            → set
Порядок важен, данные меняются? → list
Данные не должны меняться?     → tuple
```

---

### Микро-моменты, нюансы, частые ошибки новичков

#### 1. `[]` — list, `{}` — dict, не set!

```python
empty_list = []
empty_dict = {}
empty_set = set()    # правильно!
# wrong_set = {}     # это dict!
```

#### 2. Кортеж из одного элемента — запятая!

```python
t = (42)      # int 42, не кортеж!
t = (42,)     # tuple с одним элементом
t = 42,       # тоже кортеж (без скобок)
```

#### 3. Ссылка vs копия списка

```python
original = [1, 2, 3]
alias = original           # одна и та же list
copy = original.copy()     # независимая копия
copy2 = original[:]        # тоже копия (срез)
```

#### 4. Вложенные списки — shallow copy

```python
matrix = [[1, 2], [3, 4]]
row = matrix[0]
row.append(99)
print(matrix)   # [[1, 2, 99], [3, 4]] — вложенные объекты общие!
```

`.copy()` копирует только **первый уровень**. Для глубокой копии — `copy.deepcopy()` (модуль `copy`, позже).

#### 5. `KeyError` при отсутствующем ключе

```python
d = {"a": 1}
# print(d["b"])        # KeyError!
print(d.get("b"))     # None — безопасно
print(d.get("b", 0))  # 0 — значение по умолчанию
```

#### 6. Изменение списка во время `for` по нему

```python
nums = [1, 2, 3, 4, 5]
for n in nums:
    if n % 2 == 0:
        nums.remove(n)   # пропустит элементы — опасно!
```

**Правильно:** новый список, или итерировать копию: `for n in nums[:]:`

#### 7. `sort()` vs `sorted()`

```python
nums = [3, 1, 2]
nums.sort()           # меняет nums на месте → [1, 2, 3]
nums = sorted([3,1,2]) # возвращает НОВЫЙ список, исходник не трогает
```

#### 8. `set` — нельзя индексировать

```python
s = {10, 20, 30}
# s[0]   # TypeError
```

#### 9. Ключи dict — только hashable

```python
# {{1, 2}: "x"}   # list/set/dict как ключ — нельзя
```

#### 10. `in` для dict — проверяет **ключи**, не значения

```python
d = {"name": "Anna"}
"name" in d      # True — ключ
"Anna" in d      # False — это значение!
"Anna" in d.values()  # True
```

#### 11. Объединение списков

```python
[1, 2] + [3, 4]     # [1, 2, 3, 4]
[1, 2] * 3          # [1, 2, 1, 2, 1, 2]
[1, 2].extend([3])  # [1, 2, 3] — extend меняет на месте
```

#### 12. `pop()` у list и dict — разное

```python
lst = [10, 20, 30]
lst.pop()      # 30 — последний (или pop(0) — первый)
lst.pop(0)     # 10

d = {"a": 1, "b": 2}
d.pop("a")     # 1 — удаляет пару по ключу
```

---

## Практика

> **Маршрут ученика:** эта глава большая — **не обязательно все 25 примеров сразу**.  
> | Цель | Достаточно примеров |
> |------|---------------------|
> | Домашка 1–5 | **1–10**, 9 (счётчик) |
> | Домашка 6–7 | + **14, 21** |
> | Превью comprehension/zip | 11–12, 15–16 — **или пропусти до гл. 7** |
> | Справочник | 19–25 по мере надобности |

### Пример 1: Создание и базовые операции со списком

```python
# Создание
fruits = ["яблоко", "банан", "вишня"]
numbers = list(range(1, 6))       # [1, 2, 3, 4, 5]
chars = list("Python")            # ['P', 'y', 't', 'h', 'o', 'n']

print(fruits)
print(len(fruits))                # 3
print(fruits[0], fruits[-1])      # яблоко вишня

# Изменение
fruits[1] = "груша"
print(fruits)                     # ['яблоко', 'груша', 'вишня']

# Срезы — как у строк
print(fruits[0:2])                # ['яблоко', 'груша']
print(numbers[::2])               # [1, 3, 5]

# Конкатенация и повторение
more = fruits + ["слива"]
print(more)
print([0] * 4)                    # [0, 0, 0, 0]
```

**Вывод консоли:**

```
['яблоко', 'банан', 'вишня']
3
яблоко вишня
['яблоко', 'груша', 'вишня']
['яблоко', 'груша']
[1, 3, 5]
['яблоко', 'груша', 'вишня', 'слива']
[0, 0, 0, 0]
```

---

### Пример 2: Методы списка — добавление и удаление

```python
items = ["хлеб"]

items.append("молоко")            # в конец
print(items)                      # ['хлеб', 'молоко']

items.insert(1, "сыр")            # на позицию 1
print(items)                      # ['хлеб', 'сыр', 'молоко']

items.extend(["яйца", "масло"])   # добавить несколько
print(items)

items.remove("сыр")               # удалить по значению (первое вхождение)
print(items)

last = items.pop()                # удалить и вернуть последний
print(f"Сняли с полки: {last}")
print(items)

items.clear()                     # очистить
print(items)                      # []
```

**Вывод консоли:**

```
['хлеб', 'молоко']
['хлеб', 'сыр', 'молоко']
['хлеб', 'сыр', 'молоко', 'яйца', 'масло']
['хлеб', 'молоко', 'яйца', 'масло']
Сняли с полки: масло
['хлеб', 'молоко', 'яйца']
[]
```

---

### Пример 3: sort, reverse, count, index

```python
scores = [85, 92, 78, 92, 60, 92]

print(scores.count(92))           # 3 — сколько раз 92
print(scores.index(78))           # 2 — индекс первого 78

scores.sort()                     # по возрастанию, меняет на месте
print(scores)                     # [60, 78, 85, 92, 92, 92]

scores.sort(reverse=True)         # по убыванию
print(scores)

words = ["банан", "яблоко", "груша"]
words.sort(key=len)               # по длине слова
print(words)                      # ['груша', 'банан', 'яблоко']

# sorted — не меняет исходник
original = [3, 1, 2]
sorted_copy = sorted(original)
print(original)                   # [3, 1, 2]
print(sorted_copy)                # [1, 2, 3]
```

**Вывод консоли:**

```
3
2
[60, 78, 85, 92, 92, 92]
[92, 92, 92, 85, 78, 60]
['груша', 'банан', 'яблоко']
[3, 1, 2]
[1, 2, 3]
```

---

### Пример 4: Ссылка vs копия — ловушка новичка

```python
original = [1, 2, 3]

# ОШИБКА: думаем, что это копия
alias = original
alias.append(4)
print("original:", original)      # [1, 2, 3, 4] — изменился!

# ПРАВИЛЬНО: независимая копия
original = [1, 2, 3]
copy = original.copy()
copy.append(99)
print("original:", original)      # [1, 2, 3]
print("copy:", copy)              # [1, 2, 3, 99]
```

**Вывод консоли:**

```
original: [1, 2, 3, 4]
original: [1, 2, 3]
copy: [1, 2, 3, 99]
```

---

### Пример 5: Кортежи — создание и распаковка

```python
point = (10, 20)
rgb = (255, 128, 0)
single = (42,)                    # кортеж из одного элемента

print(point[0], point[1])         # 10 20
print(len(rgb))                   # 3

# Распаковка
x, y = point
print(f"x={x}, y={y}")

# Обмен переменных — питоновская магия через tuple
a, b = 1, 2
a, b = b, a                       # справа создаётся кортеж (2, 1)
print(a, b)                       # 2 1

# Кортеж как ключ словаря
locations = {
    (55.75, 37.62): "Москва",
    (59.93, 30.31): "Санкт-Петербург"
}
print(locations[(55.75, 37.62)])
```

**Вывод консоли:**

```
10 20
3
x=10, y=20
2 1
Москва
```

---

### Пример 6: Множества — уникальность и операции

```python
# Дубликаты убираются автоматически
tags = {"python", "java", "python", "go"}
print(tags)                       # порядок может отличаться

# Из списка с дублями
nums = [1, 2, 2, 3, 3, 3, 4]
unique = set(nums)
print(unique)                     # {1, 2, 3, 4}
print(list(unique))               # обратно в list (порядок не гарантирован как в исходнике)

# Операции
a = {1, 2, 3, 4}
b = {3, 4, 5, 6}

print(a | b)    # объединение: {1, 2, 3, 4, 5, 6}
print(a & b)    # пересечение: {3, 4}
print(a - b)    # разность: {1, 2}
print(a ^ b)    # симметричная разность: {1, 2, 5, 6}

# add / remove
tags.add("rust")
tags.remove("java")               # KeyError если нет — осторожно
tags.discard("cobol")             # discard — без ошибки если нет
print(tags)
```

**Вывод консоли (порядок set может отличаться):**

```
{'java', 'python', 'go'}
{1, 2, 3, 4}
[1, 2, 3, 4]
{1, 2, 3, 4, 5, 6}
{3, 4}
{1, 2}
{1, 2, 5, 6}
{'rust', 'python', 'go'}
```

---

### Пример 7: Словарь — создание, доступ, изменение

```python
user = {
    "id": 101,
    "name": "Анна",
    "email": "anna@mail.com",
    "active": True
}

# Доступ
print(user["name"])               # Анна
print(user.get("phone"))          # None — нет ключа
print(user.get("phone", "не указан"))  # не указан

# Изменение и добавление
user["age"] = 25                  # новый ключ
user["active"] = False
print(user)

# Удаление
removed = user.pop("email")       # удалить и вернуть значение
print(f"Удалили email: {removed}")

# del user["id"]                  # альтернатива pop

print(len(user))                  # количество пар
print("name" in user)             # True — проверка ключа
print("Анна" in user)             # False — значение не ищется так
```

**Вывод консоли:**

```
Анна
None
не указан
{'id': 101, 'name': 'Анна', 'email': 'anna@mail.com', 'active': False, 'age': 25}
Удалили email: anna@mail.com
4
True
False
```

---

### Пример 8: keys(), values(), items() — перебор словаря

```python
prices = {
    "яблоко": 89.90,
    "банан": 69.50,
    "вишня": 199.00
}

print("Ключи:", list(prices.keys()))
print("Цены:", list(prices.values()))

print("--- Чек ---")
total = 0
for product, price in prices.items():   # пары (ключ, значение)
    print(f"  {product}: {price:.2f} руб.")
    total += price
print(f"Итого: {total:.2f} руб.")
```

**Вывод консоли:**

```
Ключи: ['яблоко', 'банан', 'вишня']
Цены: [89.9, 69.5, 199.0]
--- Чек ---
  яблоко: 89.90 руб.
  банан: 69.50 руб.
  вишня: 199.00 руб.
Итого: 358.40 руб.
```

---

### Пример 9: Словарь-счётчик (частый паттерн)

```python
votes = ["яблоко", "банан", "яблоко", "вишня", "яблоко", "банан"]

# Подсчёт голосов
counts = {}
for fruit in votes:
    counts[fruit] = counts.get(fruit, 0) + 1
    # get(fruit, 0) — если ключа нет, вернёт 0

print(counts)                     # {'яблоко': 3, 'банан': 2, 'вишня': 1}

# Победитель
winner = None
max_votes = 0
for fruit, count in counts.items():
    if count > max_votes:
        max_votes = count
        winner = fruit
print(f"Победитель: {winner} ({max_votes} голосов)")
```

**Вывод консоли:**

```
{'яблоко': 3, 'банан': 2, 'вишня': 1}
Победитель: яблоко (3 голосов)
```

---

### Пример 10: Вложенные структуры — список словарей

```python
# Типичный формат данных из API
students = [
    {"name": "Иван", "score": 85},
    {"name": "Мария", "score": 92},
    {"name": "Пётр", "score": 78},
]

# Средний балл
total = 0
for student in students:
    print(f"{student['name']}: {student['score']}")
    total += student["score"]

average = total / len(students)
print(f"Средний балл: {average:.1f}")
```

**Вывод консоли:**

```
Иван: 85
Мария: 92
Пётр: 78
Средний балл: 85.0
```

---

### Пример 11: list comprehension — создание списка в одну строку

> **Превью:** list/dict comprehension разбираем **подробно в главе 7**. Здесь — первое знакомство.

```python
# Квадраты чисел 1–10
squares = [x ** 2 for x in range(1, 11)]
print(squares)

# Только чётные
evens = [x for x in range(20) if x % 2 == 0]
print(evens)

# Из строк
words = ["hello", "world", "python"]
upper_words = [w.upper() for w in words]
print(upper_words)

# С преобразованием
prices_str = ["100", "250", "75"]
prices = [int(p) for p in prices_str]
print(prices)
```

**Вывод консоли:**

```
[1, 4, 9, 16, 25, 36, 49, 64, 81, 100]
[0, 2, 4, 6, 8, 10, 12, 14, 16, 18]
['HELLO', 'WORLD', 'PYTHON']
[100, 250, 75]
```

**Читается как:** «собери список из `x ** 2` для каждого `x` в range(1, 11)».

---

### Пример 12: dict comprehension

> **Превью:** dict comprehension подробно — **глава 7**. Здесь — краткое знакомство.

```python
# Квадраты как словарь
squares_dict = {x: x ** 2 for x in range(1, 6)}
print(squares_dict)               # {1: 1, 2: 4, 3: 9, 4: 16, 5: 25}

# Инверсия словаря (значения → ключи), если значения уникальны
original = {"a": 1, "b": 2, "c": 3}
inverted = {v: k for k, v in original.items()}
print(inverted)                   # {1: 'a', 2: 'b', 3: 'c'}

# Фильтр: только дорогие товары
prices = {"яблоко": 50, "вишня": 200, "банан": 60}
expensive = {k: v for k, v in prices.items() if v > 80}
print(expensive)                  # {'вишня': 200}
```

**Вывод консоли:**

```
{1: 1, 2: 4, 3: 9, 4: 16, 5: 25}
{1: 'a', 2: 'b', 3: 'c'}
{'вишня': 200}
```

---

### Пример 13: set для быстрой проверки членства

```python
# Плохо: список — медленный поиск на больших данных
banned_list = ["spammer1", "spammer2", "spammer3"] * 1000

# Хорошо: set
banned_set = set(banned_list)

username = "spammer2"
if username in banned_set:
    print(f"{username} заблокирован")
else:
    print("Доступ разрешён")

# Уникальные слова в тексте
text = "python is great and python is fun"
unique_words = set(text.split())
print(unique_words)
print(f"Уникальных слов: {len(unique_words)}")
```

**Вывод консоли:**

```
spammer2 заблокирован
{'fun', 'python', 'and', 'great', 'is'}
Уникальных слов: 5
```

---

### Пример 14: Фильтрация списка — с циклом и comprehension

```python
temperatures = [22, 35, 18, 40, 15, 28, 33]

# Способ 1: цикл + новый список
hot_days = []
for t in temperatures:
    if t > 30:
        hot_days.append(t)
print("Жаркие:", hot_days)

# Способ 2: list comprehension (короче)
hot_days2 = [t for t in temperatures if t > 30]
print("Жаркие:", hot_days2)

# Убрать дубликаты температур
unique_temps = list(set(temperatures))
print("Уникальные:", sorted(unique_temps))
```

**Вывод консоли:**

```
Жаркие: [35, 40, 33]
Жаркие: [35, 40, 33]
Уникальные: [15, 18, 22, 28, 33, 35, 40]
```

---

### Пример 15: zip — объединить несколько списков

> **Превью:** `zip` и `enumerate` — **глава 7**, здесь первое применение.

```python
names = ["Анна", "Борис", "Вика"]
ages = [25, 30, 22]
cities = ["Москва", "Казань", "Сочи"]

# zip создаёт пары (кортежи)
for name, age, city in zip(names, ages, cities):
    print(f"{name}, {age} лет, г. {city}")

# Собрать список словарей — частый паттерн
users = [
    {"name": n, "age": a, "city": c}
    for n, a, c in zip(names, ages, cities)
]
print(users)
```

**Вывод консоли:**

```
Анна, 25 лет, г. Москва
Борис, 30 лет, г. Казань
Вика, 22 лет, г. Сочи
[{'name': 'Анна', 'age': 25, 'city': 'Москва'}, {'name': 'Борис', 'age': 30, 'city': 'Казань'}, {'name': 'Вика', 'age': 22, 'city': 'Сочи'}]
```

---

### Пример 16: enumerate — индекс + элемент в цикле

```python
tasks = ["купить хлеб", "позвонить маме", "сделать дз"]

print("Список дел:")
for i, task in enumerate(tasks, start=1):   # start=1 → нумерация с 1
    print(f"  {i}. {task}")

# Без enumerate (длиннее):
for i in range(len(tasks)):
    print(f"  {i + 1}. {tasks[i]}")
```

**Вывод консоли:**

```
Список дел:
  1. купить хлеб
  2. позвонить маме
  3. сделать дз
  1. купить хлеб
  2. позвонить маме
  3. сделать дз
```

---

### Пример 17: Опасность remove в цикле — и правильное решение

```python
nums = [1, 2, 3, 4, 5, 6]

# НЕПРАВИЛЬНО — пропустит элементы
# for n in nums:
#     if n % 2 == 0:
#         nums.remove(n)

# ПРАВИЛЬНО — новый список
odds = [n for n in nums if n % 2 != 0]
print("Нечётные:", odds)

# ИЛИ — итерация по копии
nums2 = [1, 2, 3, 4, 5, 6]
for n in nums2[:]:                # срез [:] — копия
    if n % 2 == 0:
        nums2.remove(n)
print("Только нечётные:", nums2)
```

**Вывод консоли:**

```
Нечётные: [1, 3, 5]
Только нечётные: [1, 3, 5]
```

---

### Пример 18: Мини-проект — инвентарь магазина

```python
# Словарь: товар → {цена, количество}
inventory = {
    "яблоко": {"price": 89.90, "qty": 50},
    "банан": {"price": 69.50, "qty": 30},
    "вишня": {"price": 199.00, "qty": 10},
}

def show_inventory(inv):
    print("\n=== Склад ===")
    total_value = 0
    for product, info in inv.items():
        value = info["price"] * info["qty"]
        total_value += value
        print(f"  {product}: {info['qty']} шт. × {info['price']:.2f} = {value:.2f} руб.")
    print(f"Общая стоимость склада: {total_value:.2f} руб.")

def sell(inv, product, amount):
    if product not in inv:
        print(f"Товар '{product}' не найден")
        return
    if inv[product]["qty"] < amount:
        print(f"Недостаточно: есть {inv[product]['qty']}, нужно {amount}")
        return
    inv[product]["qty"] -= amount
    cost = inv[product]["price"] * amount
    print(f"Продано {amount} × {product} на {cost:.2f} руб.")

show_inventory(inventory)
sell(inventory, "яблоко", 5)
sell(inventory, "вишня", 100)     # ошибка — мало на складе
sell(inventory, "киви", 1)        # нет товара
show_inventory(inventory)

# Товары, которых осталось < 20
low_stock = [p for p, info in inventory.items() if info["qty"] < 20]
print(f"Заканчиваются: {low_stock}")
```

**Вывод консоли:**

```

=== Склад ===
  яблоко: 50 шт. × 89.90 = 4495.00 руб.
  банан: 30 шт. × 69.50 = 2085.00 руб.
  вишня: 10 шт. × 199.00 = 1990.00 руб.
Общая стоимость склада: 8570.00 руб.
Продано 5 × яблоко на 449.50 руб.
Недостаточно: есть 10, нужно 100
Товар 'киви' не найден

=== Склад ===
  яблоко: 45 шт. × 89.90 = 4045.50 руб.
  банан: 30 шт. × 69.50 = 2085.00 руб.
  вишня: 10 шт. × 199.00 = 1990.00 руб.
Общая стоимость склада: 8120.50 руб.
Заканчиваются: ['вишня']
```

---

## Теория (дополнение): память, вложенность, пошаговые разборы

### Как list живёт в памяти — пошагово

```python
a = [1, 2, 3]
b = a
b.append(4)
```

| Шаг | Код | Что в памяти |
|-----|-----|--------------|
| 1 | `a = [1, 2, 3]` | Объект list `[1,2,3]`, имя `a` → на него |
| 2 | `b = a` | Имя `b` → **тот же** list |
| 3 | `b.append(4)` | List стал `[1,2,3,4]`, оба имени видят это |

```python
a = [1, 2, 3]
b = a.copy()
b.append(4)
```

| Шаг | Результат |
|-----|-----------|
| После copy | Два **разных** list в памяти |
| `a` | `[1, 2, 3]` |
| `b` | `[1, 2, 3, 4]` |

**Запомни:** `=`, `copy()`, `[:]`, `list()` — копия первого уровня. Вложенные list внутри — **общие** (shallow copy).

---

### Вложенные структуры — «матрёшка» данных

Реальные данные почти никогда не плоские:

```python
# list внутри list — матрица, таблица
matrix = [
    [1, 2, 3],
    [4, 5, 6],
    [7, 8, 9],
]
print(matrix[1][2])    # 6 — строка 1, столбец 2

# dict внутри list — ответ API
users = [
    {"id": 1, "name": "Anna"},
    {"id": 2, "name": "Bob"},
]

# list внутри dict — группировка
groups = {
    "фрукты": ["яблоко", "банан"],
    "овощи": ["морковь", "лук"],
}

# dict внутри dict — вложенные настройки
config = {
    "database": {"host": "localhost", "port": 5432},
    "cache": {"enabled": True, "ttl": 300},
}
```

**Доступ:** цепочка `[ ]` и `.get()`:

```python
print(config["database"]["host"])           # localhost
print(config.get("redis", {}).get("host"))   # None — безопасно
```

---

### Все способы создать dict

```python
# 1. Литерал
d1 = {"a": 1, "b": 2}

# 2. dict() от пар
d2 = dict([("a", 1), ("b", 2)])

# 3. zip
keys = ["a", "b"]
vals = [1, 2]
d3 = dict(zip(keys, vals))

# 4. dict comprehension
d4 = {x: x**2 for x in range(1, 4)}

# 5. fromkeys — одинаковое значение всем ключам
d5 = dict.fromkeys(["x", "y", "z"], 0)   # {'x': 0, 'y': 0, 'z': 0}

# 6. Копия
d6 = d1.copy()
```

---

### Объединение словарей

```python
defaults = {"theme": "light", "lang": "ru"}
user_prefs = {"theme": "dark", "font_size": 14}

# update — меняет словарь слева
merged = defaults.copy()
merged.update(user_prefs)
print(merged)   # theme перезаписан на dark

# Python 3.9+ — оператор |
final = defaults | user_prefs
print(final)
```

---

### set comprehension и frozenset

```python
# set comprehension — как list, но результат множество
squares = {x**2 for x in range(-3, 4)}
print(squares)    # {0, 1, 4, 9} — без дублей, порядок не важен

# frozenset — неизменяемое множество (можно ключ dict)
frozen = frozenset([1, 2, 3])
valid_keys = {frozen: "ok"}
```

На Junior `frozenset` редко нужен — просто знай, что существует.

---

### Возврат нескольких значений — на самом деле tuple

```python
def min_max(nums):
    smallest = min(nums)
    largest = max(nums)
    return smallest, largest    # это tuple!

result = min_max([3, 1, 4, 1, 5])
print(result)       # (1, 5)
print(type(result)) # <class 'tuple'>

lo, hi = min_max([3, 1, 4])   # распаковка
print(lo, hi)       # 1 4
```

---

### Пошаговый разбор: словарь-счётчик

```python
words = ["яблоко", "банан", "яблоко"]
counts = {}

for word in words:
    counts[word] = counts.get(word, 0) + 1
```

| Итерация | word | counts до | get(word, 0) | counts после |
|----------|------|-----------|--------------|--------------|
| 1 | яблоко | `{}` | 0 | `{"яблоко": 1}` |
| 2 | банан | `{"яблоко": 1}` | 0 | `{"яблоко": 1, "банан": 1}` |
| 3 | яблоко | `...` | 1 | `{"яблоко": 2, "банан": 1}` |

---

### Пошаговый разбор: почему remove в цикле ломается

Задача: из `[1, 2, 2, 3]` удалить все **чётные**, ожидаем `[1, 3]`.

```python
for n in nums:
    if n % 2 == 0:
        nums.remove(n)
```

| Шаг | nums сейчас | n | Действие |
|-----|-------------|---|----------|
| 1 | `[1, 2, 2, 3]` | 1 | нечётное — пропуск |
| 2 | `[1, 2, 2, 3]` | 2 | `remove(2)` → `[1, 2, 3]` |
| 3 | `[1, 2, 3]` | 3 | нечётное — пропуск |

**Итог:** `[1, 2, 3]` — вторая двойка **осталась**! Итератор «перепрыгнул» через неё после первого удаления.

**Правильно:** `nums = [n for n in nums if n % 2 != 0]` или цикл по копии `nums[:]`.

---

## Практика — примеры 19–25 (продолжение)

### Пример 19: Двумерный список — таблица / матрица

```python
# Таблица оценок: строка = студент, столбец = предмет
grades = [
    [85, 90, 78],   # студент 0
    [92, 88, 95],   # студент 1
    [60, 75, 80],   # студент 2
]

subjects = ["Математика", "Физика", "История"]

# Оценка студента 1 по физике
print(grades[1][1])               # 88

# Средняя по каждому студенту
for i, student_grades in enumerate(grades):
    avg = sum(student_grades) / len(student_grades)
    print(f"Студент {i}: средняя {avg:.1f}")

# Средняя по каждому предмету (по столбцам)
for j, subject in enumerate(subjects):
    column = [grades[i][j] for i in range(len(grades))]
    avg = sum(column) / len(column)
    print(f"{subject}: средняя {avg:.1f}")
```

**Вывод консоли:**

```
88
Студент 0: средняя 84.3
Студент 1: средняя 91.7
Студент 2: средняя 71.7
Математика: средняя 79.0
Физика: средняя 84.3
История: средняя 84.3
```

---

### Пример 20: Shallow copy — ловушка вложенных списков

```python
original = [[1, 2], [3, 4]]

# Поверхностная копия
shallow = original.copy()

shallow[0].append(99)     # меняем ВНУТРЕННИЙ list
print("original:", original)   # [[1, 2, 99], [3, 4]] — изменился!
print("shallow:", shallow)     # тоже

# Решение для Junior: копируй вложенность явно
original = [[1, 2], [3, 4]]
deep_manual = [row.copy() for row in original]
deep_manual[0].append(99)
print("original:", original)       # [[1, 2], [3, 4]] — цел
print("deep_manual:", deep_manual) # [[1, 2, 99], [3, 4]]
```

**Вывод консоли:**

```
original: [[1, 2, 99], [3, 4]]
shallow: [[1, 2, 99], [3, 4]]
original: [[1, 2], [3, 4]]
deep_manual: [[1, 2, 99], [3, 4]]
```

---

### Пример 21: Группировка элементов в dict of lists

```python
# Сгруппировать слова по первой букве
words = ["apple", "banana", "apricot", "blueberry", "avocado", "cherry"]

groups = {}
for word in words:
    first = word[0]
    if first not in groups:
        groups[first] = []          # создаём пустой список для буквы
    groups[first].append(word)

for letter in sorted(groups):
    print(f"{letter}: {groups[letter]}")
```

**Вывод консоли:**

```
a: ['apple', 'apricot', 'avocado']
b: ['banana', 'blueberry']
c: ['cherry']
```

**Паттерн:** `dict` со значением-списком — классическая группировка.

---

### Пример 22: set — пересечение интересов двух пользователей

```python
alice_hobbies = {"чтение", "python", "плавание", "музыка"}
bob_hobbies = {"python", "игры", "музыка", "бег"}

common = alice_hobbies & bob_hobbies
only_alice = alice_hobbies - bob_hobbies
all_hobbies = alice_hobbies | bob_hobbies

print(f"Общие: {common}")
print(f"Только у Alice: {only_alice}")
print(f"Всего уникальных: {len(all_hobbies)}")
print(f"Совместимость: {len(common) / len(all_hobbies) * 100:.0f}%")
```

**Вывод консоли (порядок set может отличаться):**

```
Общие: {'python', 'музыка'}
Только у Alice: {'плавание', 'чтение'}
Всего уникальных: 6
Совместимость: 33%
```

---

### Пример 23: Парсинг CSV-строки в list of dicts

```python
# Как часто приходят данные из файла/Excel
raw_lines = [
    "id,name,score",
    "1,Анна,92",
    "2,Борис,78",
    "3,Вика,95",
]

header = raw_lines[0].split(",")
students = []

for line in raw_lines[1:]:
    values = line.split(",")
    student = {}
    for i, key in enumerate(header):
        student[key] = values[i]
    student["score"] = int(student["score"])   # приводим тип
    students.append(student)

for s in students:
    print(f"#{s['id']} {s['name']}: {s['score']}")
```

**Вывод консоли:**

```
#1 Анна: 92
#2 Борис: 78
#3 Вика: 95
```

---

### Пример 24: Функция возвращает tuple — множественный результат

```python
def analyze_scores(scores):
    """Возвращает (min, max, avg) — tuple из трёх значений."""
    if not scores:
        return None, None, None

    total = sum(scores)
    smallest = scores[0]
    largest = scores[0]

    for s in scores:
        if s < smallest:
            smallest = s
        if s > largest:
            largest = s

    average = total / len(scores)
    return smallest, largest, average

data = [85, 92, 78, 60, 100]
lo, hi, avg = analyze_scores(data)

print(f"Мин: {lo}, Макс: {hi}, Средняя: {avg:.1f}")
```

**Вывод консоли:**

```
Мин: 60, Макс: 100, Средняя: 83.0
```

---

### Пример 25: Полная мини-программа — TODO-список

```python
"""
TODO на list of dict — типичная структура для Junior-проектов.
Каждая задача: {text, done}
"""

todos = []

def add_task(text):
    todos.append({"text": text.strip(), "done": False})
    print(f"Добавлено: {text}")

def show_tasks():
    if not todos:
        print("Список пуст!")
        return
    for i, task in enumerate(todos, start=1):
        mark = "[x]" if task["done"] else "[ ]"
        print(f"  {i}. {mark} {task['text']}")

def complete_task(index):
    if 1 <= index <= len(todos):
        todos[index - 1]["done"] = True
        print(f"Выполнено: {todos[index - 1]['text']}")
    else:
        print("Неверный номер")

def stats():
    done = sum(1 for t in todos if t["done"])
    print(f"Всего: {len(todos)}, выполнено: {done}, осталось: {len(todos) - done}")

# Демо
add_task("Выучить list и dict")
add_task("Сделать домашку гл.4")
add_task("Повторить tuple и set")
show_tasks()
complete_task(1)
complete_task(2)
show_tasks()
stats()
```

**Вывод консоли:**

```
Добавлено: Выучить list и dict
Добавлено: Сделать домашку гл.4
Добавлено: Повторить tuple и set
  1. [ ] Выучить list и dict
  2. [ ] Сделать домашку гл.4
  3. [ ] Повторить tuple и set
Выполнено: Выучить list и dict
Выполнено: Сделать домашку гл.4
  1. [x] Выучить list и dict
  2. [x] Сделать домашку гл.4
  3. [ ] Повторить tuple и set
Всего: 3, выполнено: 2, осталось: 1
```

---

## Теория (дополнение): шпаргалка, FAQ, выбор структуры

### Шпаргалка — методы list

```python
lst.append(x)       # в конец
lst.extend(iter)    # несколько в конец
lst.insert(i, x)    # на позицию i
lst.remove(x)       # удалить первое x
lst.pop()           # снять последний
lst.pop(i)          # снять по индексу
lst.clear()
lst.sort()          # на месте
lst.reverse()       # на месте
lst.count(x)
lst.index(x)
lst.copy()          # поверхностная копия
```

### Шпаргалка — set

```python
s.add(x)
s.remove(x)         # KeyError если нет
s.discard(x)        # без ошибки
s.clear()
a | b   # union
a & b   # intersection
a - b   # difference
a ^ b   # symmetric_difference
x in s
```

### Шпаргалка — dict

```python
d[key]              # доступ (KeyError если нет)
d.get(key, default)
d[key] = value      # добавить/изменить
d.pop(key)
d.popitem()         # удалить последнюю пару
d.clear()
d.update(other)
d.keys(), d.values(), d.items()
key in d            # проверка ключа
```

### Какую структуру выбрать — таблица решений

| Задача | Структура |
|--------|-----------|
| Список покупок по порядку | `list` |
| Убрать повторы из списка | `set(list)` |
| Настройки приложения | `dict` |
| Координаты (x, y) | `tuple` |
| Подсчёт слов в тексте | `dict` (слово → счётчик) |
| Проверка «забанен ли юзер» | `set` |
| Таблица студентов | `list` of `dict` |

---

### FAQ начинающего

**В: list или tuple для списка студентов?**  
`list` — если добавляешь/удаляешь. `tuple` — если фиксированный состав.

**В: Как объединить два списка?**  
`a + b` или `a.extend(b)` (extend меняет `a` на месте).

**В: Как удалить элемент по индексу?**  
`del lst[i]` или `lst.pop(i)`.

**В: `sorted()` или `.sort()`?**  
Нужен новый список → `sorted()`. Менять текущий → `.sort()`.

**В: Как проверить, пуст ли список?**  
`if not lst:` или `if len(lst) == 0:`

**В: Два ключа одно значение в dict?**  
`d = dict.fromkeys(["a", "b", "c"], 0)` → все ключи с 0.

**В: Как перебрать dict в порядке ключей?**  
`for k in sorted(d):` или с Python 3.7+ `for k in d:` уже в порядке вставки.

**В: list comprehension обязателен?**  
Нет, но очень полезен. Сначала освой цикл + append, потом comprehension.

**В: Можно ли отсортировать dict?**  
Напрямую — нет. `sorted(d)` даёт **ключи**. `sorted(d.items())` — пары. `sorted(d, key=d.get)` — по значениям.

**В: Как удалить элемент из set по индексу?**  
Никак — у set нет индексов. Только `remove(value)` или `discard(value)`.

**В: list.pop() без аргумента — что удаляет?**  
Последний элемент. `pop(0)` — первый.

**В: Чем extend отличается от append?**  
`append([1,2])` → один элемент-список внутри. `extend([1,2])` → добавляет 1 и 2 по отдельности.

```python
a = [1]
a.append([2, 3])    # [1, [2, 3]]
b = [1]
b.extend([2, 3])    # [1, 2, 3]
```

**В: Как скопировать set или dict?**  
`s.copy()` или `set(s)`. `d.copy()` или `dict(d)`.

**В: Пустой list — falsy?**  
Да: `if not []:` → True. Как пустая строка.

---

### Сравнение append vs extend vs + — таблица

| Операция | Исходный `a` | Результат |
|----------|--------------|-----------|
| `a.append(5)` | `[1, 2]` | `[1, 2, 5]` |
| `a.extend([5, 6])` | `[1, 2]` | `[1, 2, 5, 6]` |
| `a + [5, 6]` | `[1, 2]` | **новый** `[1, 2, 5, 6]`, `a` не меняется |
| `a.append([5, 6])` | `[1, 2]` | `[1, 2, [5, 6]]` — вложенный list! |

---

### Частые баги — до и после

```python
# БАГ: {} для пустого set
s = {}           # dict!
s = set()        # ✓

# БАГ: (42) — не кортеж
t = (42,)        # ✓

# БАГ: думали, что .append возвращает список
lst = [1, 2]
lst = lst.append(3)   # lst теперь None!
lst = [1, 2]
lst.append(3)         # ✓

# БАГ: KeyError
d = {"a": 1}
# x = d["b"]
x = d.get("b", 0)     # ✓

# БАГ: искали значение в dict через in
"Anna" in {"name": "Anna"}           # False
"name" in {"name": "Anna"}           # ✓
```

---

## Домашнее задание

**Файл:** `homework_04.py`

### Задача 1 — Лёгкая
Создай список из 5 любимых фильмов. Выведи первый, последний, весь список. Добавь 6-й фильм через `append`, вставь фильм на 2-ю позицию через `insert`. Удали один фильм через `remove`.

<details>
<summary>Подсказка</summary>

`insert(1, "фильм")` — вставка на индекс 1 (второе место). `remove` ищет по **значению**, не по индексу.

</details>

---

### Задача 2 — Лёгкая
Дан список чисел:

```python
nums = [4, 2, 8, 2, 9, 4, 1, 8, 2]
```

Выведи: длину, сумму (циклом), максимум **без** `max()`, количество двоек (`count`), отсортированный список **без** изменения исходного (`sorted`).

<details>
<summary>Подсказка</summary>

Максимум: `best = nums[0]`, цикл `if n > best: best = n`. После `sorted(nums)` проверь, что `nums` не изменился.

</details>

---

### Задача 3 — Средняя
Дан текст:

```python
text = "python java python go java python rust go"
```

Получи:
1. Список всех слов
2. Множество уникальных языков
3. Словарь «язык → сколько раз встретился»

<details>
<summary>Подсказка</summary>

`text.split()` → список слов. `set(words)` → уникальные. Счётчик — как в Примере 9: `counts[w] = counts.get(w, 0) + 1`.

</details>

---

### Задача 4 — Средняя
Напиши функцию `invert_dict(d)`, которая меняет ключи и значения местами.  
Пример: `{"a": 1, "b": 2}` → `{1: "a", 2: "b"}`.  
Что произойдёт с `{"a": 1, "b": 1}`? Добавь в комментарий объяснение.

<details>
<summary>Подсказка</summary>

`{v: k for k, v in d.items()}`. При дублях значений останется **последний** ключ — ключи dict уникальны.

</details>

---

### Задача 5 — Средняя
Список оценок:

```python
grades = [85, 92, 78, 92, 60, 85, 92, 100, 55, 78]
```

Найди:
- средний балл
- самую частую оценку (модa) — через словарь-счётчик
- список уникальных оценок, отсортированный

<details>
<summary>Подсказка</summary>

Мода: в счётчике найди ключ с максимальным значением. Уникальные: `sorted(set(grades))`.

</details>

---

### Задача 6 — Сложная
**Телефонная книга.** Реализуй на `dict`:
- добавить контакт (`имя` → `телефон`)
- найти телефон по имени
- удалить контакт
- показать все контакты
- меню в `while True` (как в главе 2)

Имена храни в нижнем регистре (`.lower()`), чтобы «Анна» и «анна» — один контакт.

<details>
<summary>Подсказка</summary>

`contacts = {}` снаружи цикла. Добавление: `contacts[name.lower()] = phone`. Поиск: `contacts.get(name.lower(), "не найден")`.

</details>

---

### Задача 7 — Сложная
Даны два списка:

```python
keys = ["name", "age", "city"]
values = ["Дима", 28, "Омск"]
```

Собери словарь **тремя способами**:
1. Цикл и присваивание
2. `zip(keys, values)`
3. dict comprehension

Затем добавь ключ `"email"` со значением от `input()`.

---

### Задача 8 — Сложная (бонус)
**Анализ корзины покупок.** Список словарей:

```python
cart = [
    {"name": "хлеб", "price": 45.00, "qty": 2},
    {"name": "молоко", "price": 89.90, "qty": 1},
    {"name": "сыр", "price": 350.00, "qty": 1},
    {"name": "хлеб", "price": 45.00, "qty": 1},
]
```

1. Общая сумма корзины
2. Самый дорогой товар (по `price`)
3. Сколько **уникальных** наименований
4. Объедини одинаковые товары в один (суммируй `qty`) — итоговый список без дублей по `name`
5. Если итог > 500 — скидка 5%, выведи `final_total`

<details>
<summary>Подсказка</summary>

Для объединения дублей: новый `list`, dict `merged = {}` по `name`, накапливай `qty`. См. Пример 18 (инвентарь).

</details>

---

### Задача 9 — Сложная (бонус)
Дана матрица 3×3:

```python
matrix = [
    [8, 1, 6],
    [3, 5, 7],
    [4, 9, 2],
]
```

1. Выведи главную диагональ (`[8, 5, 2]`)
2. Выведи сумму каждой **строки**
3. Выведи сумму каждого **столбца**
4. Найди максимальный элемент **без** `max()` — двойной цикл

---

### Задача 10 — Сложная (бонус)
**Группировка заказов.** Список словарей:

```python
orders = [
    {"city": "Москва", "amount": 1200},
    {"city": "Омск", "amount": 800},
    {"city": "Москва", "amount": 500},
    {"city": "Казань", "amount": 300},
    {"city": "Омск", "amount": 1500},
]
```

Построй `dict`: город → сумма всех заказов из этого города.  
Выведи города, где сумма > 1000.  
*(См. Пример 21 — группировка.)*

---

### Как сдавать

- Файл `homework_04.py` или по файлу на задачу.
- Задачи 6–8 — с вызовом и тестовыми данными.
- Можно частями: 1–4, потом 5–8.

**Критерии зачёта:**
- Правильный выбор структуры (list/set/dict)
- Нет путаницы ссылка/копия там, где меняешь данные
- `get()` вместо ловли KeyError где уместно
- Код запускается

---

**Сделай задачи сам и пришли код на проверку. После проверки — Глава 5: *Мутабельность, копирование, == vs is*.**

---
Конец главы.