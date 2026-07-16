# Тема: Мутабельность, копирование, `==` vs `is`

> **Файл:** `homework_05.py`  
> **Маршрут:** ДЗ 1–5 → примеры **1–7, 13, 22**; 17–30 — углубление по желанию.  
> **Про `def` в ДЗ:** формально гл. 6 — можно отложить задачи с функциями.

## Теория

### Что это такое

В главах 1 и 4 ты уже касался этих тем. Теперь соберём их в **одну картину** — без этого Junior-код часто «ломается загадочно»: изменил одну переменную, изменилось «другое», сравнил объекты — получил неожиданный `False` или `True`.

Три кита этой главы:

1. **Мутабельность** — можно ли изменить объект «на месте»
2. **Копирование** — как получить **независимую** копию
3. **`==` vs `is`** — одинаковое **содержимое** vs один и тот же **объект в памяти**

---

#### Мутабельный (mutable) vs неизменяемый (immutable)

| Mutable — можно менять на месте | Immutable — нельзя менять на месте |
|--------------------------------|-------------------------------------|
| `list` | `int`, `float`, `bool` |
| `dict` | `str` |
| `set` | `tuple` (обычно) |
| | `None`, `frozenset` |

```python
# Mutable — меняем объект, id может остаться тем же
nums = [1, 2, 3]
nums.append(4)        # тот же list в памяти, новое содержимое

# Immutable — «изменение» = новый объект
s = "hello"
s = s + "!"           # новая строка "hello!", старая "hello" осталась
```

**Мутабельность** — про **объект**. **Имя переменной** — просто наклейка на объект.

```python
a = [1, 2]
b = a                 # две наклейки на один list
b.append(3)
print(a)              # [1, 2, 3] — a тоже изменился!
```

---

#### `==` vs `is` — две разные проверки

| Оператор | Вопрос, на который отвечает |
|----------|----------------------------|
| `==` | **Равны ли значения?** (содержимое) |
| `is` | **Это один и тот же объект?** (одинаковый id в памяти) |

```python
a = [1, 2, 3]
b = [1, 2, 3]
c = a

print(a == b)    # True  — одинаковое содержимое
print(a is b)    # False — разные list в памяти
print(a is c)    # True  — c указывает на тот же list, что и a
```

**Функция `id()`** — уникальный «адрес» объекта (номер в памяти):

```python
print(id(a))     # например 140234567890
print(id(b))     # другой номер
print(id(c))     # тот же, что id(a)
```

**Правило для Junior:**

```python
# Сравнение значений
if x == 5:
if name == "admin":

# Проверка на None — ТОЛЬКО is
if x is None:
if result is not None:

# НЕ пиши
if x == None:    # работает, но плохой стиль (PEP 8)
```

**Почему `is` для `None`?**  
`None` — синглтон: в программе существует **ровно один** объект `None`. `is` быстрее и однозначнее.

---

#### Копирование: ссылка, поверхностная, глубокая

**1. Присваивание `=` — не копия, а ссылка (alias)**

```python
original = [1, 2, 3]
alias = original      # два имени → один объект
```

**2. Поверхностная копия (shallow copy)** — копируется только **первый уровень**

```python
original = [1, 2, [3, 4]]
shallow = original.copy()        # или list(original), или original[:]

shallow[0] = 99                  # original[0] не меняется — верхний уровень независим
shallow[2].append(5)             # original[2] ТОЖЕ изменится — вложенный list общий!
```

**3. Глубокая копия (deep copy)** — рекурсивно копируется **всё**

```python
import copy
deep = copy.deepcopy(original)   # полностью независимая структура
```

| Способ | Уровень | Методы |
|--------|---------|--------|
| Ссылка | — | `b = a` |
| Shallow | 1-й | `.copy()`, `[:]`, `list()`, `dict()`, `set()` |
| Deep | все | `copy.deepcopy()` |

---

#### Immutable — но с подвохом: tuple с mutable внутри

```python
t = ([1, 2], [3, 4])    # tuple неизменяем, но list внутри — mutable!
# t[0] = [9, 9]         # TypeError — tuple менять нельзя
t[0].append(99)         # OK! внутренний list изменился
print(t)                # ([1, 2, 99], [3, 4])
```

Кортеж **неизменяем** как **набор ссылок**, но ссылки могут вести на изменяемые объекты.

---

### Как это работает «под капотом»

#### Имена и объекты — модель CPython

```
Переменная (имя)     Объект в памяти
     a    ────────→   [1, 2, 3]  (list, mutable)
     b    ────────→   тот же объект
     c    ────────→   [1, 2, 3]  (другой list, то же содержимое)
```

При `b = a` в namespace добавляется запись `b → объект_a`. Объект не копируется.

При `c = [1, 2, 3]` создаётся **новый** list-объект.

#### `==` вызывает `__eq__`

Для встроенных типов Python сравнивает **содержимое**:

```python
[1, 2] == [1, 2]     # True
{"a": 1} == {"a": 1} # True
```

Для своих классов (позже) можно переопределить `__eq__`.

#### `is` сравнивает указатели

Проверка: `id(a) == id(b)`. Никакого сравнения элементов.

#### Shallow copy — что происходит

```python
original = [[1, 2], [3, 4]]
shallow = original.copy()
```

```
original ──→ [ ref0, ref1 ]
                │     │
                ↓     ↓
              [1,2]  [3,4]

shallow  ──→ [ ref0', ref1' ]   # новый внешний list
                │     │
                ↓     ↓
              [1,2]  [3,4]      # те же внутренние объекты!
```

`ref0'` — **копия ссылки**, указывает на **тот же** `[1, 2]`.

#### Кэш малых чисел (интересный факт)

Python иногда переиспользует объекты малых `int`:

```python
a = 256
b = 256
print(a is b)    # True (часто)

a = 257
b = 257
print(a is b)    # False (не всегда кэшируется)
```

**Вывод:** для чисел используй `==`, **никогда** не полагайся на `is` для сравнения значений.

#### Строки: интернирование

Короткие строки-литералы иногда тоже кэшируются:

```python
a = "hello"
b = "hello"
print(a is b)    # может быть True

a = "hello world!"
b = "hello world!"
print(a is b)    # скорее False
```

Опять же: для строк сравнивай через `==`.

---

### Где это полезно и применяется в реальной разработке

| Ситуация | Что использовать |
|----------|------------------|
| Передать список в функцию, не меняя оригинал | `.copy()` или `[:]` |
| Конфиг с вложенными dict | `copy.deepcopy()` |
| Проверка «функция ничего не вернула» | `result is None` |
| Сравнение текстов, чисел, списков | `==` |
| Кэш: «уже обрабатывали этот объект?» | `is` / `id()` |
| Дефолтные аргументы функций | **не** mutable! (см. ниже) |
| Дедупликация: один объект — одна ссылка | понимание `is` |

**Ловушка дефолтных аргументов (must know для Junior):**

```python
# ОПАСНО
def add_item(item, lst=[]):
    lst.append(item)
    return lst

print(add_item("a"))    # ['a']
print(add_item("b"))    # ['a', 'b'] — сюрприз!

# ПРАВИЛЬНО
def add_item(item, lst=None):
    if lst is None:
        lst = []
    lst.append(item)
    return lst
```

Дефолтный `[]` создаётся **один раз** при определении функции — все вызовы делят один list.

**Копия перед изменением в функции:**

```python
def process(data):
    data = data.copy()    # не трогаем оригинал снаружи
    data.append("processed")
    return data
```

---

### Микро-моменты, нюансы, частые ошибки новичков

#### 1. Думали, что `=` создаёт копию

```python
a = [1, 2]
b = a
b.append(3)
# a тоже [1, 2, 3]
```

#### 2. Shallow copy при вложенности

```python
matrix = [[1, 2], [3, 4]]
copy = matrix.copy()
copy[0].append(99)
# matrix[0] тоже [1, 2, 99]
```

#### 3. `is` вместо `==` для значений

```python
a = 1000
b = 1000
if a is b:    # может быть False!
if a == b:    # True — правильно
```

#### 4. `== None` вместо `is None`

Работает, но **PEP 8** запрещает: `if x is None`.

#### 5. Путаница `is` с пустыми коллекциями

```python
[] is []     # False — разные пустые list
[] == []     # True
```

#### 6. `.copy()` у list не существует у str

```python
s = "hello"
# s.copy()   # AttributeError
s2 = s       # str immutable — просто новая ссылка на тот же объект OK
```

#### 7. `del` удаляет имя, не объект

```python
a = [1, 2]
b = a
del a        # имя a исчезло, объект [1,2] жив — на него ссылается b
```

Объект удаляется из памяти, когда на него **нет ссылок** (сборщик мусора).

#### 8. Изменяемый объект как ключ dict — нельзя

```python
# {[1,2]: "x"}   # TypeError — list unhashable
```

#### 9. `tuple` с list внутри — «полуизменяемый»

Можно менять list внутри, нельзя менять состав tuple.

#### 10. `copy()` vs `deepcopy()` для dict с вложенностью

```python
d = {"a": [1, 2]}
shallow = d.copy()
deep = copy.deepcopy(d)
```

Та же логика, что у list.

#### 11. `+=` для list — мутирует; `+` — создаёт новый

```python
a = [1, 2]
b = a
b += [3]        # то же что b.extend([3]) — меняет объект a
# a is b → True

a = [1, 2]
b = a + [3]     # новый list
# a is b → False
```

#### 12. Передача в функцию — передаётся ссылка

```python
def mutate(lst):
    lst.append(99)

data = [1, 2]
mutate(data)
# data → [1, 2, 99] — оригинал снаружи изменился
```

Immutable в функции «меняется» только локальное имя:

```python
def try_change(n):
    n = n + 1      # новый int, внешняя x не тронута

x = 5
try_change(x)
# x всё ещё 5
```

#### 13. `==` для `float('nan')` — всегда False

```python
nan = float("nan")
print(nan == nan)    # False!
print(nan is nan)    # True — тот же объект
```

NaN — особый случай: **не равен сам себе** по `==`.

#### 14. Hashable vs unhashable — почему list нельзя в set

| Hashable (можно в set, ключ dict) | Unhashable |
|-----------------------------------|------------|
| `int`, `float`, `str`, `bool` | `list`, `dict`, `set` |
| `tuple` (если элементы hashable) | `bytearray` |
| `frozenset`, `None` | |

Объект hashable = имеет `__hash__()`, hash **не меняется** за время жизни в set/dict.

---

## Практика

> **Навигация:** **30 примеров** (1–16 — «Практика», 17–30 — после доп. теории), шпаргалка, FAQ, домашка.

### Пример 1: `==` vs `is` — базовое различие

```python
x = [1, 2, 3]
y = [1, 2, 3]
z = x

print("x == y:", x == y)      # True — одинаковое содержимое
print("x is y:", x is y)      # False — разные объекты
print("x is z:", x is z)      # True — одна ссылка

print("id(x):", id(x))
print("id(y):", id(y))
print("id(z):", id(z))        # совпадает с id(x)
```

**Вывод консоли:**

```
x == y: True
x is y: False
x is z: True
id(x): 140...
id(y): 140...  (другой)
id(z): 140...  (как x)
```

---

### Пример 2: Immutable — присваивание создаёт новую ссылку

```python
a = 10
print("id до:", id(a))

a = a + 5                    # новый int 15
print("id после:", id(a))    # другой id!

s = "hi"
print(id(s))
s = s + "!"                  # новая строка
print(id(s))                 # другой id
```

**Вывод консоли (id будут числа, разные после изменения):**

```
id до: ...
id после: ...
...
...
```

---

### Пример 3: Mutable — изменение на месте, id тот же

```python
nums = [1, 2, 3]
print("id до append:", id(nums))

nums.append(4)
print("id после append:", id(nums))    # тот же!
print("nums:", nums)

nums[0] = 99
print("id после nums[0]=99:", id(nums))  # всё ещё тот же list
```

**Вывод консоли:**

```
id до append: 140...
id после append: 140...  (тот же)
nums: [1, 2, 3, 4]
id после nums[0]=99: 140...  (тот же)
```

---

### Пример 4: Ссылка — две переменные, один объект

```python
shopping = ["хлеб", "молоко"]
also_shopping = shopping       # ссылка, не копия!

also_shopping.append("сыр")
print("shopping:", shopping)           # ['хлеб', 'молоко', 'сыр']
print("also_shopping:", also_shopping) # то же
print("Один объект?", shopping is also_shopping)  # True
```

**Вывод консоли:**

```
shopping: ['хлеб', 'молоко', 'сыр']
also_shopping: ['хлеб', 'молоко', 'сыр']
Один объект? True
```

---

### Пример 5: Поверхностная копия list

```python
original = [1, 2, 3]

# Три способа shallow copy
copy1 = original.copy()
copy2 = list(original)
copy3 = original[:]

copy1.append(4)
print("original:", original)   # [1, 2, 3] — не тронут
print("copy1:", copy1)         # [1, 2, 3, 4]

print("copy2 is original:", copy2 is original)  # False
```

**Вывод консоли:**

```
original: [1, 2, 3]
copy1: [1, 2, 3, 4]
copy2 is original: False
```

---

### Пример 6: Shallow copy ловушка — вложенный list

```python
original = [[1, 2], [3, 4]]
shallow = original.copy()

print("До изменения:")
print("  original:", original)
print("  shallow:", shallow)

shallow[0].append(99)          # меняем ВНУТРЕННИЙ list

print("После shallow[0].append(99):")
print("  original:", original)   # [[1, 2, 99], [3, 4]] — изменился!
print("  shallow:", shallow)     # тоже
print("  Внутренние list одни?", original[0] is shallow[0])  # True
```

**Вывод консоли:**

```
До изменения:
  original: [[1, 2], [3, 4]]
  shallow: [[1, 2], [3, 4]]
После shallow[0].append(99):
  original: [[1, 2, 99], [3, 4]]
  shallow: [[1, 2, 99], [3, 4]]
  Внутренние list одни? True
```

---

### Пример 7: deepcopy — полная независимость

```python
import copy

original = [[1, 2], [3, 4]]
deep = copy.deepcopy(original)

deep[0].append(99)

print("original:", original)     # [[1, 2], [3, 4]] — цел
print("deep:", deep)             # [[1, 2, 99], [3, 4]]
print("Внутренние разные?", original[0] is deep[0])  # False
```

**Вывод консоли:**

```
original: [[1, 2], [3, 4]]
deep: [[1, 2, 99], [3, 4]]
Внутренние разные? True
```

---

### Пример 8: dict — ссылка, copy, deepcopy

```python
import copy

config = {
    "name": "app",
    "ports": [8080, 9090],
}

alias = config
alias["name"] = "hacked"
print(config["name"])          # hacked — ссылка

config = {"name": "app", "ports": [8080, 9090]}
shallow = config.copy()
shallow["ports"].append(3000)
print(config["ports"])         # [8080, 9090, 3000] — вложенный list общий!

config = {"name": "app", "ports": [8080, 9090]}
deep = copy.deepcopy(config)
deep["ports"].append(3000)
print(config["ports"])         # [8080, 9090] — цел
```

**Вывод консоли:**

```
hacked
[8080, 9090, 3000]
[8080, 9090]
```

---

### Пример 9: Проверка на None — только `is`

```python
def find_user(user_id):
    # имитация: пользователь не найден
    return None

result = find_user(999)

# Правильно
if result is None:
    print("Пользователь не найден")

# Работает, но плохой стиль
if result == None:
    print("Тоже сработает, но не пиши так")

# Проверка «что-то вернулось»
data = find_user(1)
if data is not None:
    print("Есть данные")
else:
    print("Пусто")
```

**Вывод консоли:**

```
Пользователь не найден
Тоже сработает, но не пиши так
Пусто
```

---

### Пример 10: Пустые коллекции — `==` vs `is`

```python
a = []
b = []
c = a

print(a == b)     # True — оба пустые
print(a is b)     # False — разные объекты!
print(a is c)     # True

print([] is [])   # False
print(() is ())   # True для пустого tuple! (кэшируется интерпретатором)
```

**Вывод консоли:**

```
True
False
True
False
True
```

*(пустой `tuple` — синглтон в CPython)*

---

### Пример 11: str immutable — «изменение» через новый объект

```python
text = "hello"
print("id:", id(text))

text = text.replace("hello", "HELLO")   # replace возвращает НОВУЮ строку
print("после replace:", text)
print("id:", id(text))                  # другой id

# Исходная не менялась бы, если бы сохранили
original = "hello"
new = original.replace("l", "L")
print("original:", original)            # hello
print("new:", new)                      # heLLo
```

**Вывод консоли:**

```
id: ...
после replace: HELLO
id: ...  (другой)
original: hello
new: heLLo
```

---

### Пример 12: tuple — нельзя менять, но list внутри можно

```python
record = ("Иван", [85, 90, 78])

# record[0] = "Пётр"     # TypeError
record[1].append(95)       # list внутри — mutable!

print(record)              # ('Иван', [85, 90, 78, 95])

# tuple как ключ dict — OK (если элементы hashable)
# но list внутри делает tuple unhashable если бы list был прямым... 
# (1, [2]) — unhashable! (list внутри)
locations = {(55.75, 37.62): "Москва"}   # OK — только числа
```

**Вывод консоли:**

```
('Иван', [85, 90, 78, 95])
```

---

### Пример 13: Ловушка mutable default argument

```python
# ПЛОХО — один list на все вызовы
def broken_add(item, bucket=[]):
    bucket.append(item)
    return bucket

print(broken_add("яблоко"))    # ['яблоко']
print(broken_add("банан"))     # ['яблоко', 'банан'] — ой!

# ХОРОШО
def good_add(item, bucket=None):
    if bucket is None:
        bucket = []
    bucket.append(item)
    return bucket

print(good_add("яблоко"))      # ['яблоко']
print(good_add("банан"))       # ['банан'] — независимо
```

**Вывод консоли:**

```
['яблоко']
['яблоко', 'банан']
['яблоко']
['банан']
```

---

### Пример 14: Функция не должна мутировать аргумент без предупреждения

```python
def add_tax(prices):
    """Плохо: меняет список снаружи."""
    for i in range(len(prices)):
        prices[i] = round(prices[i] * 1.2, 2)
    return prices

def add_tax_safe(prices):
    """Хорошо: работает с копией."""
    result = prices.copy()
    for i in range(len(result)):
        result[i] = round(result[i] * 1.2, 2)
    return result

original = [100.0, 200.0, 50.0]
print("До:", original)

add_tax(original)
print("После add_tax (плохо):", original)   # изменился!

original = [100.0, 200.0, 50.0]
new_prices = add_tax_safe(original)
print("После add_tax_safe:", original)      # [100, 200, 50] — цел
print("Новые цены:", new_prices)
```

**Вывод консоли:**

```
До: [100.0, 200.0, 50.0]
После add_tax (плохо): [120.0, 240.0, 60.0]
После add_tax_safe: [100.0, 200.0, 50.0]
Новые цены: [120.0, 240.0, 60.0]
```

---

### Пример 15: Сравнение вложенных структур через `==`

```python
a = {"users": [{"id": 1, "name": "Anna"}]}
b = {"users": [{"id": 1, "name": "Anna"}]}

print(a == b)    # True — рекурсивное сравнение содержимого
print(a is b)    # False

# Изменим b — копия не связана
b["users"][0]["name"] = "Bob"
print(a == b)    # False
print(a)         # Anna не тронута
```

**Вывод консоли:**

```
True
False
False
{'users': [{'id': 1, 'name': 'Anna'}]}
```

---

### Пример 16: Практика — безопасное редактирование вложенного dict

```python
import copy

template = {
    "title": "Отчёт",
    "data": {"sales": 1000, "items": [1, 2, 3]},
}

# Отчёт за январь — не трогаем шаблон
january = copy.deepcopy(template)
january["title"] = "Январь"
january["data"]["sales"] = 1500
january["data"]["items"].append(4)

# Отчёт за февраль — из того же шаблона
february = copy.deepcopy(template)
february["title"] = "Февраль"
february["data"]["sales"] = 800

print("template:", template)
print("january:", january)
print("february:", february)
```

**Вывод консоли:**

```
template: {'title': 'Отчёт', 'data': {'sales': 1000, 'items': [1, 2, 3]}}
january: {'title': 'Январь', 'data': {'sales': 1500, 'items': [1, 2, 3, 4]}}
february: {'title': 'Февраль', 'data': {'sales': 800, 'items': [1, 2, 3]}}
```

---

## Теория (дополнение): дерево решений, разборы, set/frozenset

### Дерево: нужна ли копия?

```
Меняешь данные?
│
├─ НЕТ → ссылка b = a — OK
│
└─ ДА → Есть вложенные list/dict/set?
         │
         ├─ НЕТ → shallow: .copy(), [:], dict(), list()
         │
         └─ ДА → нужна полная независимость?
                  │
                  ├─ ДА → copy.deepcopy()
                  └─ НЕТ (только верхний уровень) → shallow
```

### Дерево: `==` или `is`?

```
Что проверяешь?
│
├─ None → is None / is not None
├─ Одинаковое содержимое? → ==
├─ Тот же объект в памяти? → is (редко нужно явно)
└─ Числа/строки по значению? → == (НИКОГДА не is для значений)
```

---

### Пошаговый разбор: shallow vs deep

```python
orig = {"a": [1]}
shallow = orig.copy()
deep = copy.deepcopy(orig)
```

| Действие | `orig` | `shallow` | `deep` |
|----------|--------|-----------|--------|
| `shallow["a"].append(2)` | `[1,2]` | `[1,2]` | `[1]` |
| `deep["a"].append(3)` | `[1,2]` | `[1,2]` | `[1,3]` |

---

### set — mutable, но элементы immutable

```python
s = {1, 2, 3}
s.add(4)              # OK

# s.add([1, 2])       # TypeError — list unhashable
s.add((1, 2))         # OK — tuple hashable (если элементы hashable)
```

Множество хранит **hash** каждого элемента. Mutable объекты меняют hash → нельзя.

---

### frozenset — immutable set

```python
normal = {1, 2, 3}
frozen = frozenset([1, 2, 3])

# normal.add(4)       # OK
# frozen.add(4)     # AttributeError

# frozenset как ключ dict
cache = {frozen: "данные"}
```

---

### `del` — удаление имени

```python
x = [1, 2, 3]
y = x
del x              # имя x исчезло
print(y)           # [1, 2, 3] — объект жив
del y              # ссылок нет → объект будет собран GC
```

---

## Практика — примеры 17–22 (продолжение)

### Пример 17: Копирование set

```python
original = {1, 2, 3}
alias = original
alias.add(4)
print(original)           # {1, 2, 3, 4}

original = {1, 2, 3}
copied = original.copy()  # или set(original)
copied.add(4)
print(original)           # {1, 2, 3}
print(copied)             # {1, 2, 3, 4}
print(original is copied) # False
```

**Вывод консоли:**

```
{1, 2, 3, 4}
{1, 2, 3}
{1, 2, 3, 4}
False
```

---

### Пример 18: bool — singleton True и False

```python
a = True
b = True
print(a is b)        # True — один объект True в Python

flag = 5 > 3
print(flag is True)  # может быть True, но сравнивай flag == True или просто if flag:
```

**Вывод консоли:**

```
True
True
```

---

### Пример 19: Список list comprehension — всегда новый объект

```python
a = [1, 2, 3]
b = [1, 2, 3]
c = [x for x in a]

print(a == b == c)    # True
print(a is b)         # False
print(a is c)         # False — comprehension создаёт новый list
```

**Вывод консоли:**

```
True
False
False
```

---

### Пример 20: Копия перед сортировкой — не ломай исходник

```python
data = [3, 1, 4, 1, 5]

# Плохо для исходных данных:
# data.sort()  # меняет data

# Хорошо — sorted или copy
sorted_data = sorted(data)
print("original:", data)         # [3, 1, 4, 1, 5]
print("sorted:", sorted_data)    # [1, 1, 3, 4, 5]

# Или
copy = data.copy()
copy.sort()
print("original:", data)
print("sorted copy:", copy)
```

**Вывод консоли:**

```
original: [3, 1, 4, 1, 5]
sorted: [1, 1, 3, 4, 5]
original: [3, 1, 4, 1, 5]
sorted copy: [1, 1, 3, 4, 5]
```

---

### Пример 21: Мини-проект — история изменений (copy discipline)

```python
import copy

def save_version(document, history):
    """Сохраняет deep copy в историю — откат возможен."""
    history.append(copy.deepcopy(document))

def show(doc):
    print(f"  title={doc['title']}, body={doc['body']}")

document = {"title": "Черновик", "body": ["строка 1"]}
history = []

save_version(document, history)

document["title"] = "Версия 2"
document["body"].append("строка 2")
save_version(document, history)

document["body"].append("строка 3 — забыли сохранить")

print("Текущий:")
show(document)

print("История (откат):")
for i, snap in enumerate(history):
    print(f"  v{i}:", end=" ")
    show(snap)

# Откат к v0
restored = copy.deepcopy(history[0])
print("После отката к v0:")
show(restored)
```

**Вывод консоли:**

```
Текущий:
  title=Версия 2, body=['строка 1', 'строка 2', 'строка 3 — забыли сохранить']
История (откат):
  v0:   title=Черновик, body=['строка 1']
  v1:   title=Версия 2, body=['строка 1', 'строка 2']
После отката к v0:
  title=Черновик, body=['строка 1']
```

---

### Пример 22: Квиз в коде — угадай вывод

```python
def quiz():
    tests = []

    # 1
    a = [1, 2]
    b = a
    b += [3]
    tests.append(("1", a, b, a is b))

    # 2
    a = [1, 2]
    b = a + [3]
    tests.append(("2", a, b, a is b))

    # 3
    a = (1, 2)
    b = a + (3,)
    tests.append(("3", a, b, a is b))

    for num, a, b, same in tests:
        print(f"Тест {num}: a={a}, b={b}, a is b={same}")

quiz()
```

**Вывод консоли:**

```
Тест 1: a=[1, 2, 3], b=[1, 2, 3], a is b=True
Тест 2: a=[1, 2], b=[1, 2, 3], a is b=False
Тест 3: a=(1, 2), b=(1, 2, 3), a is b=False
```

**Разбор:**
- Тест 1: `+=` для list **мутирует** на месте → `a` и `b` один объект
- Тест 2: `+` создаёт **новый** list
- Тест 3: `+` для tuple создаёт **новый** tuple (immutable)

---

## Теория (расширение): передача в функции, GC, таблицы `==`/`is`

### Аргументы функций — «передача по ссылке на объект»

В Python нет «передачи по значению» для объектов. Передаётся **ссылка**:

```python
def add_tag(user, tag):
    user["tags"].append(tag)   # мутирует dict снаружи

profile = {"name": "Anna", "tags": ["python"]}
add_tag(profile, "junior")
print(profile)   # tags изменился!
```

**Защита:** копируй в начале функции, если не хочешь менять снаружи:

```python
def add_tag_safe(user, tag):
    user = user.copy()                    # shallow — верхний уровень
    user["tags"] = user["tags"].copy()    # и list внутри!
    user["tags"].append(tag)
    return user
```

---

### Сборщик мусора (GC) — простыми словами

Объект живёт, пока на него есть **хотя бы одна ссылка** (имя переменной, элемент list, ключ dict...).

```python
x = [1, 2, 3]     # list существует
y = x             # 2 ссылки
del x             # 1 ссылка (y)
del y             # 0 ссылок → GC удалит объект (когда-нибудь)
```

Тебе не нужно вручную «освобождать память» — Python сам.

---

### Полная таблица: когда `==` True, а `is` False

| Выражение | `==` | `is` | Почему |
|-----------|------|------|--------|
| `[1,2] == [1,2]` | True | False | Одинаковое содержимое, разные list |
| `256 == 256` | True | часто True | Кэш малых int |
| `1000 == 1000` | True | не гарантировано | Большие int — разные объекты |
| `None is None` | True | True | Синглтон |
| `[] == []` | True | False | Два пустых list |
| `"a" * 1000 == "a" * 1000` | True | не гарантировано | Длинные строки |

**Золотое правило:** для сравнения данных — **`==`**. Для `None` — **`is`**.

---

### `__eq__` по типам — что именно сравнивается

| Тип | `==` сравнивает |
|-----|-----------------|
| `list` | Элементы по порядку, рекурсивно |
| `dict` | Ключи и значения (порядок не важен для равенства) |
| `set` | Содержимое (порядок не важен) |
| `str` | Символ за символом |
| `tuple` | Элементы по порядку |

```python
{"a": 1, "b": 2} == {"b": 2, "a": 1}   # True — порядок ключей не важен
[1, 2] == [2, 1]                        # False — порядок важен!
```

---

### Ручная глубокая копия без `deepcopy` (для понимания)

```python
def manual_deep_copy_list(lst):
    """Копия list с рекурсией на один уровень вложенности list."""
    result = []
    for item in lst:
        if isinstance(item, list):
            result.append(manual_deep_copy_list(item))
        else:
            result.append(item)
    return result
```

`copy.deepcopy()` делает это **для любой глубины** и любых типов — используй его в реальном коде.

---

### Пошаговый разбор: передача list в функцию

```python
def mystery(lst):
    lst.append(4)
    lst = [9, 9, 9]    # локальное имя lst теперь на другой объект
    lst.append(1)

data = [1, 2, 3]
mystery(data)
print(data)
```

| Шаг | `data` снаружи | `lst` внутри функции |
|-----|----------------|----------------------|
| Вход | `[1,2,3]` | ссылка на тот же |
| `append(4)` | `[1,2,3,4]` | тот же объект |
| `lst = [9,9,9]` | `[1,2,3,4]` | **новый** list, data не тронут |
| `append(1)` | `[1,2,3,4]` | `[9,9,9,1]` |
| Выход | `[1,2,3,4]` | локальное имя уничтожено |

**Вывод:** `[1, 2, 3, 4]` — переприсваивание `lst = ...` **не** откатывает append.

---

## Практика — примеры 23–30 (продолжение)

### Пример 23: `+=` vs `+` для list — детально

```python
# += мутирует
a = [1, 2]
b = a
print("id до +=:", id(a), id(b))
b += [3]
print("после +=:", a, b)
print("id после +=:", id(a), id(b), "same?", a is b)

print("---")

# + создаёт новый
a = [1, 2]
b = a
b = b + [3]
print("после +:", a, b)
print("same?", a is b)
```

**Вывод консоли:**

```
id до +=: ... ... 
после +=: [1, 2, 3] [1, 2, 3]
id после +=: ... ... same? True
---
после +: [1, 2] [1, 2, 3]
same? False
```

---

### Пример 24: Передача в функцию — mutate vs reassign

```python
def mutate(lst):
    lst.append("X")

def reassign(lst):
    lst = ["полностью", "новый"]

data = ["a", "b"]
mutate(data)
print("after mutate:", data)       # ['a', 'b', 'X']

data = ["a", "b"]
reassign(data)
print("after reassign:", data)     # ['a', 'b'] — не изменился
```

**Вывод консоли:**

```
after mutate: ['a', 'b', 'X']
after reassign: ['a', 'b']
```

---

### Пример 25: Immutable int в функции

```python
def increment(n):
    print(f"  внутри до: id={id(n)}, n={n}")
    n = n + 1
    print(f"  внутри после: id={id(n)}, n={n}")

x = 100
print(f"снаружи до: id={id(x)}, x={x}")
increment(x)
print(f"снаружи после: id={id(x)}, x={x}")
```

**Вывод консоли:**

```
снаружи до: id=..., x=100
  внутри до: id=..., n=100
  внутри после: id=..., n=101   (другой id)
снаружи после: id=..., x=100    (x не изменился)
```

---

### Пример 26: dict — `==` не зависит от порядка ключей

```python
a = {"name": "Anna", "age": 25, "city": "Moscow"}
b = {"city": "Moscow", "name": "Anna", "age": 25}

print(a == b)    # True
print(a is b)    # False

# list — порядок важен!
la = ["Anna", 25, "Moscow"]
lb = ["Moscow", "Anna", 25]
print(la == lb)  # False
```

**Вывод консоли:**

```
True
False
False
```

---

### Пример 27: Копирование вложенного dict вручную (shallow + list copy)

```python
def safe_update_user(user, new_tags):
    """Не мутирует исходный user."""
    updated = user.copy()
    updated["tags"] = user["tags"].copy()   # копия list внутри
    updated["tags"].extend(new_tags)
    return updated

original = {"name": "Bob", "tags": ["python"]}
new_user = safe_update_user(original, ["django"])

new_user["tags"].append("flask")
print("original:", original)     # tags не тронуты
print("new_user:", new_user)
```

**Вывод консоли:**

```
original: {'name': 'Bob', 'tags': ['python']}
new_user: {'name': 'Bob', 'tags': ['python', 'django', 'flask']}
```

---

### Пример 28: `is` с пустыми и непустыми — полный тест

```python
tests = [
    ([], []),
    ([1], [1]),
    ("", ""),
    ("a", "a"),
    (None, None),
    (True, True),
    ({}, {}),
    (set(), set()),
]

for a, b in tests:
    print(f"{repr(a):12} == {repr(b):12} → {a == b:5}  |  is → {a is b}")
```

**Вывод консоли (примерный):**

```
[]           == []           → True   |  is → False
[1]          == [1]          → True   |  is → False
''           == ''           → True   |  is → False
'a'          == 'a'          → True   |  is → True  (интернирование)
None         == None         → True   |  is → True
True         == True         → True   |  is → True
{}           == {}           → True   |  is → False
set()        == set()        → True   |  is → False
```

---

### Пример 29: Отладка «почему изменилось» — чеклист в коде

```python
def debug_refs(label, obj, other=None):
    print(f"\n=== {label} ===")
    print(f"  value: {obj}")
    print(f"  id:    {id(obj)}")
    if other is not None:
        print(f"  other id: {id(other)}")
        print(f"  same object? {obj is other}")

a = [[1, 2]]
b = a
debug_refs("1. a и b — ссылка", a, b)

c = a.copy()
debug_refs("2. c — shallow", a, c)
print(f"  inner same? {a[0] is c[0]}")

import copy
d = copy.deepcopy(a)
debug_refs("3. d — deep", a, d)
print(f"  inner same? {a[0] is d[0]}")
```

**Вывод консоли:**

```
=== 1. a и b — ссылка ===
  value: [[1, 2]]
  id:    ...
  other id: ...
  same object? True

=== 2. c — shallow ===
  ...
  same object? False
  inner same? True

=== 3. d — deep ===
  ...
  same object? False
  inner same? False
```

---

### Пример 30: Мини-проект — undo/redo с копиями

```python
import copy

class SimpleEditor:
    def __init__(self, text):
        self.text = text
        self.history = [copy.deepcopy(text)]
        self.position = 0

    def edit(self, new_text):
        self.text = new_text
        # обрезаем «будущее» при новом редактировании
        self.history = self.history[: self.position + 1]
        self.history.append(copy.deepcopy(new_text))
        self.position += 1

    def undo(self):
        if self.position > 0:
            self.position -= 1
            self.text = copy.deepcopy(self.history[self.position])
            print(f"Undo → '{self.text}'")
        else:
            print("Нечего отменять")

    def show(self):
        print(f"Текст: '{self.text}' (шаг {self.position}/{len(self.history)-1})")

editor = SimpleEditor("Привет")
editor.show()

editor.edit("Привет, мир")
editor.edit("Привет, Python")
editor.show()

editor.undo()
editor.undo()
editor.show()

editor.edit("Новая ветка")
editor.show()
```

**Вывод консоли:**

```
Текст: 'Привет' (шаг 0/0)
Текст: 'Привет, Python' (шаг 2/2)
Undo → 'Привет, мир'
Undo → 'Привет'
Текст: 'Привет' (шаг 0/2)
Текст: 'Новая ветка' (шаг 1/1)
```

*(Для str `deepcopy` избыточен — str immutable; здесь для единообразия и если бы text был list символов)*

---

## Шпаргалка

```python
# Сравнение
a == b          # равны ли значения
a is b          # тот же объект?
a is None       # проверка на None
id(a)           # «адрес» объекта

# Копии list
lst.copy()
lst[:]
list(lst)

# Копии dict
d.copy()
dict(d)

# Копии set
s.copy()
set(s)

# Глубокая копия
import copy
copy.deepcopy(obj)

# Mutable
list, dict, set     # .append, [i]=, .add

# Immutable
int, float, str, bool, tuple, frozenset, None
```

---

## FAQ начинающего

**В: Когда нужен deepcopy?**  
Когда структура **вложенная** (list в list, dict в dict) и ты меняешь внутренности, не затрагивая оригинал.

**В: `b = a[:]` — это копия?**  
Shallow (поверхностная). Для плоского list — полная независимость. Для вложенного — нет.

**В: Почему `if x:` не заменяет `if x is None`?**  
`if x:` ловит все falsy (0, "", [], None). `if x is None` — **только** None.

**В: `==` для float 0.1 + 0.2?**  
Помни главу 1 — лучше с допуском. `is` здесь вообще не при чём.

**В: Копировать tuple нужно?**  
Обычно нет — immutable. Но если внутри mutable — копируй внутренности.

**В: Как проверить, что два dict независимы?**  
Измени один — смотри второй. Или `id(d1["key"]) != id(d2["key"])` для вложенных.

**В: `list()` и `.copy()` — разница?**  
Для list — оба shallow copy. `.copy()` читаемее.

**В: Зачем вообще `is`?**  
В основном `is None`, иногда singletons, иногда оптимизация/идентичность в продвинутом коде.

**В: `a = b` и `a is b` после присваивания?**  
Всегда `True` — одно имя переназначили на объект другого.

**В: Можно ли `is` для пустой строки?**  
`"" is ""` может быть True (интернирование). Не полагайся — используй `==` или `if not s`.

**В: `copy.copy()` vs `.copy()`?**  
`copy.copy(x)` — shallow, как `.copy()` для list/dict. `copy.deepcopy(x)` — глубокая.

**В: Зачем копировать перед `for item in big_list: item...`?**  
Если `item` — ссылка на mutable и ты меняешь `item`, меняется оригинал. Копируй: `for item in [x.copy() for x in big_list]:` или работай с копией внутри.

**В: `tuple(sorted_list)` — новый объект?**  
Да, `tuple()` всегда создаёт новый tuple.

**В: Два dict с одинаковыми ключами — `is`?**  
`is` False. `==` True если пары совпадают.

**В: Как отлаживать «откуда изменение»?**  
`print(id(obj))` до и после, `print(obj is other)`, breakpoints на `.append`, `.update`.

---

### Таблица операций: мутирует или создаёт новое?

| Операция | list | str | tuple | dict |
|----------|------|-----|-------|------|
| `+=` | мутирует* | новый str | новый tuple | — |
| `+` | новый | новый | новый | — |
| `.append()` | мутирует | — | — | — |
| `[i] = x` | мутирует | ошибка | ошибка | мутирует |
| `.copy()` | shallow | — | — | shallow |
| `sorted(x)` | новый list | — | — | — |
| `.sort()` | мутирует | — | — | — |

\* `list += iterable` вызывает `extend` на месте.

---

### Частые баги — до и после

```python
# БАГ: думали, что копия
b = a
b.append(1)

# FIX
b = a.copy()

# БАГ: is для чисел
if x is 5:

# FIX
if x == 5:

# БАГ: shallow для матрицы
m2 = m1.copy()
m2[0].append(99)

# FIX
m2 = copy.deepcopy(m1)

# БАГ: def f(lst=[])
def f(lst=None):
    if lst is None:
        lst = []
```

---

## Домашнее задание

**Файл:** `homework_05.py`

### Задача 1 — Лёгкая
Создай `a = [1, 2, 3]`, `b = [1, 2, 3]`, `c = a`. Выведи для каждой пары: `==`, `is`, `id()`.  
В комментарии объясни каждый результат своими словами.

<details>
<summary>Подсказка</summary>

Три print-блока: `a vs b`, `a vs c`, `b vs c`.

</details>

---

### Задача 2 — Лёгкая
Докажи, что `str` immutable: сохрани `id` до и после «изменения» строки (`+=` или `.upper()` в переприсваивании).

<details>
<summary>Подсказка</summary>

```python
s = "test"
old_id = id(s)
s = s + "!"   # или s = s.upper()
print(old_id, id(s), old_id == id(s))
```

</details>

---

### Задача 3 — Средняя
```python
matrix = [[1, 2], [3, 4]]
```
1. Сделай `shallow = matrix.copy()`
2. В `shallow[0]` добавь `99`
3. Выведи `matrix` и `shallow`
4. Объясни, почему `matrix` изменился
5. Повтори с `copy.deepcopy()` — `matrix` должен остаться прежним

<details>
<summary>Подсказка</summary>

См. Примеры 6–7. После shallow: `matrix[0] is shallow[0]` → True. После deep → False.

</details>

---

### Задача 4 — Средняя
Исправь функцию:

```python
def broken(items=[]):
    items.append("new")
    return items
```

Перепиши безопасно. Покажи 3 вызова, доказывающие, что баг исправлен.

<details>
<summary>Подсказка</summary>

См. Пример 13. Паттерн: `if items is None: items = []`.

</details>

---

### Задача 5 — Средняя
Напиши функцию `safe_merge(base, updates)`, которая:
- возвращает **новый** dict (не меняет `base`)
- применяет ключи из `updates`
- если значение — list, **копирует** list (shallow), не ссылается на оригинал

Тест:
```python
base = {"tags": ["a", "b"], "count": 1}
updates = {"tags": ["x"], "name": "test"}
result = safe_merge(base, updates)
result["tags"].append("y")
# base["tags"] должен остаться ["a", "b"]
```

<details>
<summary>Подсказка</summary>

`result = base.copy()`, потом для каждого ключа из `updates`: если значение `list` → `value.copy()`, иначе как есть. См. Пример 27.

</details>

---

### Задача 6 — Сложная
Напиши функцию `is_palindrome_list(lst)`, которая:
- **не меняет** исходный list
- сравнивает с reversed-копией через `==`
- для проверки используй копию: `lst.copy()` или срез

Протестируй на `[1, 2, 1]` и `[1, 2, 3]`. Покажи, что исходник не изменился.

<details>
<summary>Подсказка</summary>

`copy = lst.copy()`, `return copy == copy[::-1]`. Не вызывай `.reverse()` — он мутирует!

</details>

---

### Задача 7 — Сложная
**Система снимков настроек.**

```python
default_settings = {
    "theme": "light",
    "notifications": {"email": True, "push": False},
    "filters": ["all"],
}
```

Реализуй:
- `create_profile(settings)` → deep copy
- `apply_filter(profile, new_filter)` → добавляет в `filters` копии
- `reset_to_default(profile, default)` → deep copy из default

Докажи тестами, что `default_settings` **никогда** не меняется.

<details>
<summary>Подсказка</summary>

Везде `copy.deepcopy`. После каждой операции: `print(default_settings)` — байт-в-байт как в начале. См. Примеры 16, 21, 30.

</details>

---

### Задача 8 — Сложная (бонус)
Напиши «карточную колоду»:
- `create_deck()` → list из 52 строк `"2♥"`, `"3♥"`, ... (можно упрощённо `["2H", "3H", ...]`)
- `shuffle_and_deal(deck, hands=4)` → **не меняет** исходный deck (работай с копией!), возвращает list из 4 list по 13 карт

Используй `.copy()` и срезы. `random.shuffle` на копии — OK (`import random`).

<details>
<summary>Подсказка</summary>

`working = deck.copy()`, `random.shuffle(working)`, раздай срезами `working[0:13]` и т.д. Исходный `deck` не трогай.

</details>

---

### Задача 9 — Сложная (бонус)
**Найди баг** в коде ниже. Объясни и исправь:

```python
def process_users(users):
    cache = []
    for user in users:
        entry = user
        entry["processed"] = True
        cache.append(entry)
    return cache

original = [{"name": "Anna"}, {"name": "Bob"}]
result = process_users(original)
print(original)
print(result)
```

<details>
<summary>Подсказка</summary>

`entry = user` — **ссылка**, не копия! `original` мутируется. Fix: `entry = user.copy()` или `copy.deepcopy(user)`.

</details>

---

### Задача 10 — Сложная (бонус)
Пройди **квиз** — напиши программу, которая выводит `==` и `is` для пар:

```python
pairs = [
    ([1, 2], [1, 2]),
    ((1, 2), (1, 2)),
    (None, None),
    (100, 100),
    (1000, 1000),
]
```

Для каждой пары: объясни результат **в комментарии** (2–3 предложения).  
Сравни с Примером 28.

---

### Задача 11 — Сложная (бонус)
Реализуй `clone(data, deep=False)`:
- `deep=False` → `copy()` / `dict()` / `set()` по типу
- `deep=True` → `copy.deepcopy(data)`
- поддержи: `list`, `dict`, `set`, `str`, `int` (для int/str просто верни значение)

Протестируй на `{"a": [1, [2, 3]]}` — при `deep=False` внутренний `[2,3]` общий, при `deep=True` — нет.

---

### Как сдавать

- `homework_05.py` или по файлу на задачу
- Задачи 3, 7, 9 — обязательно комментарии «почему»
- Частями: 1–5, потом 6–11

**Критерии зачёта:**
- Правильно: `==` для значений, `is` для `None`
- Копия там, где данные меняются
- `deepcopy` при вложенности
- Нет mutable default args

---

**Сделай задачи сам и пришли код на проверку. После проверки — Глава 6: *Функции — аргументы, `*args`, `**kwargs`, scope*.**

---
Конец главы.