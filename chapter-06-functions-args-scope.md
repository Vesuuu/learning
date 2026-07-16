# Тема: Функции — аргументы, `*args`, `**kwargs`, scope

> **Файл:** `homework_06.py`  
> **Маршрут:** ДЗ 1–6 → примеры **1–5, 9, 13, 17, 20**; задача 9 — **после гл. 14**.

## Теория

### Что это такое

**Функция** — именованный блок кода, который можно **вызывать** многократно с разными данными. Вместо копипасты 10 раз одного и того же — пишешь один раз, вызываешь где нужно.

```python
def greet(name):
    return f"Привет, {name}!"

message = greet("Анна")
print(message)    # Привет, Анна!
```

**Зачем функции:**
- **Переиспользование** — DRY (Don't Repeat Yourself)
- **Читаемость** — `calculate_tax(price)` понятнее 20 строк формул
- **Тестирование** — проверяешь маленький кусок отдельно
- **Структура** — делишь программу на логические части

**Терминология:**

| Термин | Что это |
|--------|---------|
| **Параметр** | Имя в **определении** функции: `def f(x):` — `x` параметр |
| **Аргумент** | Значение при **вызове**: `f(5)` — `5` аргумент |
| **return** | Вернуть результат вызывающему коду |
| **Сигнатура** | «Лицо» функции: имя + параметры: `greet(name)` |

Функция без `return` неявно возвращает `None`:

```python
def say_hi():
    print("Hi")

result = say_hi()    # печатает Hi
print(result)        # None
```

---

### Виды аргументов

#### 1. Позиционные (positional)

Передаются **по порядку**:

```python
def introduce(name, age):
    print(f"{name}, {age} лет")

introduce("Борис", 30)    # name="Борис", age=30
```

#### 2. Именованные (keyword)

Передаются **по имени** — порядок не важен:

```python
introduce(age=30, name="Борис")    # то же самое
```

#### 3. Параметры по умолчанию (default)

```python
def greet(name, greeting="Привет"):
    print(f"{greeting}, {name}!")

greet("Анна")                  # Привет, Анна!
greet("Анна", "Здравствуй")    # Здравствуй, Анна!
```

**Правило:** параметры с default — **в конце** сигнатуры.

```python
# def bad(a=1, b):   # SyntaxError!
def good(b, a=1):    # OK
    pass
```

**Mutable default — ловушка (глава 5):**

```python
def bad(items=[]):
    items.append("x")
    return items

def good(items=None):
    if items is None:
        items = []
    items.append("x")
    return items
```

#### 4. `*args` — произвольное число позиционных аргументов

```python
def sum_all(*args):
    """args — кортеж всех лишних позиционных аргументов."""
    total = 0
    for n in args:
        total += n
    return total

print(sum_all(1, 2, 3))       # 6
print(sum_all(10, 20))        # 30
```

Имя `args` — **соглашение**, можно `*numbers`, но `*args` — стандарт.

#### 5. `**kwargs` — произвольное число именованных аргументов

```python
def show_profile(**kwargs):
    """kwargs — словарь: имя_параметра → значение."""
    for key, value in kwargs.items():
        print(f"  {key}: {value}")

show_profile(name="Anna", age=25, city="Moscow")
```

`kwargs` = **keyword arguments**.

#### 6. Полная сигнатура — порядок параметров

```python
def full(a, b, c=0, *args, d=0, **kwargs):
    pass
```

**Строгий порядок в определении:**
1. Обычные позиционные (`a`, `b`)
2. С default (`c=0`)
3. `*args`
4. **Только keyword** после `*args` (`d=0`) — keyword-only
5. `**kwargs`

```python
def connect(host, port=5432, *, ssl=True, timeout=30):
    # host, port — позиционно или по имени
    # ssl, timeout — ТОЛЬКО по имени (после *)
    pass

connect("localhost", 5432, ssl=False)
# connect("localhost", 5432, False)   # ошибка!
```

---

### Область видимости (scope) — LEGB

Python ищет имя переменной в порядке **LEGB**:

| Уровень | Расшифровка | Пример |
|---------|-------------|--------|
| **L** | Local — внутри функции | `def f(): x = 1` |
| **E** | Enclosing — во внешней функции | замыкания (глава 14) |
| **G** | Global — модуль (файл) | `x = 10` на верхнем уровне |
| **B** | Built-in — встроенные | `print`, `len`, `int` |

```python
x = "global"           # G

def outer():
    x = "enclosing"  # E
    def inner():
        x = "local"  # L
        print(x)     # local
    inner()

outer()
print(x)             # global
```

#### Локальная переменная

Присваивание внутри функции создаёт **локальное** имя:

```python
count = 0              # global

def increment():
    count = count + 1  # UnboundLocalError! count локальный, но ещё не присвоен
```

Python видит `count = ...` и считает `count` **локальным** во всей функции — правая часть обращается к ещё не созданному локальному.

**Исправление — `global`:**

```python
count = 0

def increment():
    global count
    count = count + 1
```

**Когда использовать `global`:** почти никогда на Junior. Лучше `return` новое значение.

#### `nonlocal` — для вложенных функций

```python
def counter():
    total = 0
    def add(n):
        nonlocal total
        total += n
        return total
    return add

c = counter()
print(c(1))    # 1
print(c(2))    # 3
```

---

### Как это работает «под капотом»

#### Вызов функции

1. Python находит объект-функцию по имени
2. Создаёт **новый frame** (кадр) в стеке вызовов
3. Связывает аргументы с параметрами
4. Выполняет тело
5. При `return` — кладёт значение, уничтожает frame
6. Без `return` — возвращает `None`

#### `*args` внутри

```python
def f(*args):
    print(type(args))   # <class 'tuple'>
```

Все лишние позиционные аргументы упаковываются в **tuple**.

#### `**kwargs` внутри

```python
def f(**kwargs):
    print(type(kwargs))   # <class 'dict'>
```

#### Распаковка при вызове

```python
def greet(name, age):
    print(name, age)

args = ("Anna", 25)
greet(*args)              # распаковка tuple → greet("Anna", 25)

kwargs = {"name": "Anna", "age": 25}
greet(**kwargs)           # распаковка dict → greet(name="Anna", age=25)
```

#### Локальные переменные — словарь

У каждого frame есть `locals()` — словарь локальных имён. При выходе из функции frame удаляется.

---

### Где это полезно и применяется в реальной разработке

| Паттерн | Пример |
|---------|--------|
| Валидация | `def validate_email(email): ...` |
| API-обёртки | `def get_user(user_id): ...` |
| `*args` | логгер: `log("error", "msg", timestamp, user_id)` |
| `**kwargs` | `requests.get(url, **options)` — гибкие параметры |
| Default args | `def paginate(page=1, per_page=20)` |
| Scope | изоляция — функция не ломает глобальные переменные |

**Реальный пример — конфиг:**

```python
def create_connection(host, port=5432, **options):
    timeout = options.get("timeout", 30)
    ssl = options.get("ssl", False)
    print(f"Connect {host}:{port}, ssl={ssl}, timeout={timeout}")

create_connection("db.example.com", ssl=True, timeout=60)
```

---

### Микро-моменты, нюансы, частые ошибки новичков

#### 1. Забыли `return`

```python
def add(a, b):
    a + b           # вычислили, но не вернули!

def add_ok(a, b):
    return a + b
```

#### 2. `return` завершает функцию

```python
def check(x):
    if x < 0:
        return False
    return True     # до сюда не дойдёт, если x < 0
```

#### 3. Несколько `return`

```python
def grade(score):
    if score >= 90:
        return "A"
    if score >= 75:
        return "B"
    return "C"
```

#### 4. Путаница параметр/аргумент

Не критично, но в документации: параметры в `def`, аргументы в вызове.

#### 5. Изменение mutable-аргумента

```python
def add_item(item, lst):
    lst.append(item)    # мутирует list снаружи!

data = [1, 2]
add_item(3, data)       # data → [1, 2, 3]
```

Копируй, если не хочешь менять: `lst = lst.copy()`.

#### 6. Shadowing builtins

```python
def len(items):    # перекрыл встроенный len!
    return len(items)   # бесконечная рекурсия или ошибка
```

Не называй параметры `list`, `dict`, `str`, `id`, `type`, `len`.

#### 7. Слишком много параметров

Если больше 5–6 — подумай о dict или dataclass (позже).

#### 8. `*args` + обязательный параметр

```python
def f(required, *args):
    print(required, args)

f(1, 2, 3)    # required=1, args=(2, 3)
```

#### 9. Передача функции как аргумента

```python
def apply(func, value):
    return func(value)

def double(x):
    return x * 2

print(apply(double, 5))    # 10
```

Функции в Python — **объекты первого класса**.

#### 10. Docstring — документация функции

```python
def area(width, height):
    """Вычисляет площадь прямоугольника."""
    return width * height

print(area.__doc__)
help(area)
```

---

## Практика

> **Навигация:** **30 примеров** (1–20 основной блок, 21–30 дополнение), шпаргалка, FAQ, домашка.

### Пример 1: Базовая функция

```python
def say_hello(name):
    """Приветствует пользователя по имени."""
    message = f"Привет, {name}!"
    return message

result = say_hello("Мария")
print(result)
print(type(result))

nothing = say_hello("Пётр")
# Функция без явного return в другом месте — но здесь return есть
```

**Вывод консоли:**

```
Привет, Мария!
<class 'str'>
```

---

### Пример 2: Несколько параметров и return

```python
def rectangle_info(width, height):
    area = width * height
    perimeter = 2 * (width + height)
    return area, perimeter    # tuple!

a, p = rectangle_info(5, 3)
print(f"Площадь: {a}, Периметр: {p}")

# Или целиком
info = rectangle_info(4, 4)
print(info)               # (16, 16)
print(type(info))         # <class 'tuple'>
```

**Вывод консоли:**

```
Площадь: 15, Периметр: 16
(16, 16)
<class 'tuple'>
```

---

### Пример 3: Параметры по умолчанию

```python
def power(base, exponent=2):
    """Возводит base в степень exponent. По умолчанию — квадрат."""
    return base ** exponent

print(power(5))           # 25 — exponent=2 по умолчанию
print(power(5, 3))        # 125
print(power(2, 10))       # 1024

# Именованный аргумент
print(power(base=3, exponent=4))   # 81
print(power(exponent=0, base=100)) # 1
```

**Вывод консоли:**

```
25
125
1024
81
1
```

---

### Пример 4: Позиционные vs именованные

```python
def create_user(name, email, role="user", active=True):
    return {
        "name": name,
        "email": email,
        "role": role,
        "active": active,
    }

# Только позиционные
u1 = create_user("Anna", "anna@mail.com")

# Позиционные + именованные (после позиционных!)
u2 = create_user("Bob", "bob@mail.com", role="admin")

# Только именованные (после обязательных)
u3 = create_user(
    name="Vika",
    email="vika@mail.com",
    active=False,
)

print(u1)
print(u2["role"])
print(u3["active"])
```

**Вывод консоли:**

```
{'name': 'Anna', 'email': 'anna@mail.com', 'role': 'user', 'active': True}
admin
False
```

---

### Пример 5: `*args` — сумма любого количества чисел

```python
def sum_all(*args):
    print(f"Получено args: {args}, тип: {type(args)}")
    total = 0
    for n in args:
        total += n
    return total

print(sum_all(1, 2, 3))
print(sum_all(10))
print(sum_all())          # 0 — пустой tuple
print(sum_all(1, 2, 3, 4, 5))
```

**Вывод консоли:**

```
Получено args: (1, 2, 3), тип: <class 'tuple'>
6
Получено args: (10,), тип: <class 'tuple'>
10
Получено args: (), тип: <class 'tuple'>
0
Получено args: (1, 2, 3, 4, 5), тип: <class 'tuple'>
15
```

---

### Пример 6: `**kwargs` — гибкий профиль

```python
def build_profile(name, **kwargs):
    profile = {"name": name}
    profile.update(kwargs)    # добавляем все kwargs в dict
    return profile

p1 = build_profile("Иван", age=30, city="Москва")
p2 = build_profile("Оля", hobby="Python", level="junior")

print(p1)
print(p2)
```

**Вывод консоли:**

```
{'name': 'Иван', 'age': 30, 'city': 'Москва'}
{'name': 'Оля', 'hobby': 'Python', 'level': 'junior'}
```

---

### Пример 7: `*args` + `**kwargs` вместе

```python
def mega_func(required, *args, default="ok", **kwargs):
    print(f"required: {required}")
    print(f"args: {args}")
    print(f"default: {default}")
    print(f"kwargs: {kwargs}")

mega_func(1, 2, 3, default="custom", color="red", size="L")
```

**Вывод консоли:**

```
required: 1
args: (2, 3)
default: custom
kwargs: {'color': 'red', 'size': 'L'}
```

---

### Пример 8: Распаковка при вызове

```python
def divide(a, b):
    return a / b

nums = (10, 2)
print(divide(*nums))          # divide(10, 2) → 5.0

params = {"a": 20, "b": 4}
print(divide(**params))       # divide(a=20, b=4) → 5.0

# Комбинация
def greet(greeting, name, punctuation="!"):
    print(f"{greeting}, {name}{punctuation}")

parts = ("Привет",)
details = {"name": "Анна", "punctuation": "!!!"}
greet(*parts, **details)
```

**Вывод консоли:**

```
5.0
5.0
Привет, Анна!!!
```

---

### Пример 9: Local scope — переменная внутри функции

```python
def calculate():
    x = 10              # локальная
    y = 20              # локальная
    return x + y

result = calculate()
print(result)

# print(x)              # NameError — x не существует снаружи
```

**Вывод консоли:**

```
30
```

---

### Пример 10: Global vs local — конфликт имён

```python
message = "Глобальное сообщение"

def show_message():
    message = "Локальное сообщение"    # новая локальная, global не тронут
    print("Внутри:", message)

show_message()
print("Снаружи:", message)
```

**Вывод консоли:**

```
Внутри: Локальное сообщение
Снаружи: Глобальное сообщение
```

---

### Пример 11: UnboundLocalError и `global`

```python
counter = 0

# ОШИБКА:
# def bad_increment():
#     counter = counter + 1   # UnboundLocalError

def good_increment():
    global counter
    counter = counter + 1

good_increment()
good_increment()
print("counter:", counter)
```

**Вывод консоли:**

```
counter: 2
```

**Лучший стиль без global:**

```python
def increment_pure(value):
    return value + 1

counter = 0
counter = increment_pure(counter)
counter = increment_pure(counter)
print("counter:", counter)    # 2
```

---

### Пример 12: LEGB — встроенные функции

```python
# B — Built-in
print(len([1, 2, 3]))    # 3

def demo():
    # L — Local
    text = "local"
    # использует B — len из builtins
    print(len(text))

demo()
```

**Вывод консоли:**

```
3
5
```

---

### Пример 13: Функция не мутирует, если копирует

```python
def add_tax_safe(prices, rate=0.2):
    result = prices.copy()
    for i in range(len(result)):
        result[i] = round(result[i] * (1 + rate), 2)
    return result

original = [100.0, 200.0, 50.0]
new_prices = add_tax_safe(original)

print("original:", original)
print("new:", new_prices)
```

**Вывод консоли:**

```
original: [100.0, 200.0, 50.0]
new: [120.0, 240.0, 60.0]
```

---

### Пример 14: Ранний return — guard clauses

```python
def get_discount(age, is_student):
    if age < 0:
        return 0                    # ранний выход — невалидный возраст
    if age < 12:
        return 0.5                  # дети 50%
    if is_student and age < 26:
        return 0.3                  # студенты 30%
    return 0                        # без скидки

print(get_discount(10, False))        # 0.5
print(get_discount(22, True))         # 0.3
print(get_discount(40, False))        # 0
print(get_discount(-1, False))        # 0
```

**Вывод консоли:**

```
0.5
0.3
0
0
```

---

### Пример 15: Функция как аргумент

```python
def apply_twice(func, value):
    """Применяет func к value дважды."""
    return func(func(value))

def add_three(x):
    return x + 3

def square(x):
    return x * x

print(apply_twice(add_three, 10))    # 10 → 13 → 16
print(apply_twice(square, 3))        # 3 → 9 → 81
```

**Вывод консоли:**

```
16
81
```

---

### Пример 16: Keyword-only параметры (после `*`)

```python
def send_email(to, subject, *, cc=None, priority="normal"):
    print(f"To: {to}")
    print(f"Subject: {subject}")
    print(f"CC: {cc}")
    print(f"Priority: {priority}")

send_email("anna@mail.com", "Привет", cc="boss@mail.com", priority="high")

# send_email("anna@mail.com", "Привет", "boss@mail.com")  # TypeError
```

**Вывод консоли:**

```
To: anna@mail.com
Subject: Привет
CC: boss@mail.com
Priority: high
```

---

### Пример 17: Валидация в функции

```python
def withdraw(balance, amount):
    """Снимает amount с balance. Возвращает (success, new_balance, message)."""
    if amount <= 0:
        return False, balance, "Сумма должна быть положительной"
    if amount > balance:
        return False, balance, "Недостаточно средств"
    new_balance = balance - amount
    return True, new_balance, f"Снято {amount:.2f}"

ok, bal, msg = withdraw(1000, 300)
print(ok, bal, msg)

ok, bal, msg = withdraw(1000, 1500)
print(ok, bal, msg)
```

**Вывод консоли:**

```
True 700 Снято 300.00
False 1000 Недостаточно средств
```

---

### Пример 18: `*args` для форматирования лога

```python
def log(level, message, *extra):
    parts = [f"[{level}]", message]
    for item in extra:
        parts.append(str(item))
    print(" | ".join(parts))

log("INFO", "Пользователь вошёл", "user_id=42", "ip=127.0.0.1")
log("ERROR", "Ошибка БД", "timeout", 500)
```

**Вывод консоли:**

```
[INFO] | Пользователь вошёл | user_id=42 | ip=127.0.0.1
[ERROR] | Ошибка БД | timeout | 500
```

---

### Пример 19: Docstring и help

```python
def celsius_to_fahrenheit(celsius):
    """
    Конвертирует Цельсий в Фаренгейт.

    Параметры:
        celsius (float): температура в °C

    Возвращает:
        float: температура в °F
    """
    return celsius * 9 / 5 + 32

print(celsius_to_fahrenheit.__doc__)
print(celsius_to_fahrenheit(0))     # 32.0
print(celsius_to_fahrenheit(100))   # 212.0
```

**Вывод консоли:**

```

    Конвертирует Цельсий в Фаренгейт.
    ...

32.0
212.0
```

---

### Пример 20: Мини-проект — калькулятор на функциях

```python
def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def multiply(a, b):
    return a * b

def divide(a, b):
    if b == 0:
        return None, "Деление на ноль"
    return a / b, None

OPERATIONS = {
    "+": add,
    "-": subtract,
    "*": multiply,
    "/": divide,
}

def calculate(op, a, b):
    if op not in OPERATIONS:
        return None, f"Неизвестная операция: {op}"
    func = OPERATIONS[op]
    result = func(a, b)
    if op == "/":
        return result    # (value, error) tuple
    return result, None

for op, a, b in [("+", 10, 3), ("/", 10, 2), ("/", 5, 0), ("^", 1, 2)]:
    result, err = calculate(op, a, b)
    if err:
        print(f"{a} {op} {b} → Ошибка: {err}")
    else:
        print(f"{a} {op} {b} = {result}")
```

**Вывод консоли:**

```
10 + 3 = 13
10 / 2 = 5.0
5 / 0 → Ошибка: Деление на ноль
1 ^ 2 → Ошибка: Неизвестная операция: ^
```

---

## Теория (дополнение): стек вызовов, nonlocal, аннотации

### Стек вызовов — как Python «вкладывает» функции

```python
def a():
    print("start a")
    b()
    print("end a")

def b():
    print("in b")

a()
```

| Порядок | Событие |
|---------|---------|
| 1 | Вход в `a` |
| 2 | `start a` |
| 3 | Вход в `b` |
| 4 | `in b` |
| 5 | Выход из `b` |
| 6 | `end a` |
| 7 | Выход из `a` |

**Вывод:**

```
start a
in b
end a
```

При ошибке traceback читается **снизу вверх** — последняя строка = где упало.

---

### `nonlocal` — изменение enclosing-переменной

```python
def make_accumulator():
    total = 0
    def add(x):
        nonlocal total
        total += x
        return total
    return add

acc = make_accumulator()
print(acc(10))    # 10
print(acc(5))     # 15
print(acc(100))   # 115
```

Без `nonlocal` — `UnboundLocalError` (как с `global`).

---

### Аннотации типов (type hints) — для читаемости

```python
def greet(name: str) -> str:
    return f"Привет, {name}!"

def sum_numbers(numbers: list[float]) -> float:
    return sum(numbers)
```

Python **не проверяет** типы автоматически (без mypy). Это подсказки для людей и IDE.

---

### Порядок аргументов — полная шпаргалка

```python
def example(pos1, pos2, opt1="default", *args, kwonly1, kwonly2="x", **kwargs):
    pass

# Вызов:
example(1, 2, "val", 3, 4, kwonly1=True, extra=99)
# pos1=1, pos2=2, opt1="val", args=(3,4), kwonly1=True, kwargs={'extra':99}
```

---

### Пошаговый разбор: связывание аргументов

```python
def f(a, b, c=0):
    print(a, b, c)

f(1, 2, 3)
```

| Параметр | Откуда значение |
|----------|-----------------|
| `a` | 1 (позиционный) |
| `b` | 2 (позиционный) |
| `c` | 3 (позиционный, перекрыл default) |

```python
f(1, b=2, c=3)    # OK — позиционные до именованных
# f(a=1, 2)        # SyntaxError — позиционный после именованного
```

---

## Практика — примеры 21–28 (продолжение)

### Пример 21: `nonlocal` — счётчик вызовов

```python
def make_call_counter():
    count = 0
    def wrapper():
        nonlocal count
        count += 1
        print(f"Вызов #{count}")
    return wrapper

counter = make_call_counter()
counter()
counter()
counter()
```

**Вывод консоли:**

```
Вызов #1
Вызов #2
Вызов #3
```

---

### Пример 22: Передача mutable — осознанная мутация

```python
def append_status(orders, status="new"):
    """Добавляет status каждому заказу. Мутирует orders намеренно."""
    for order in orders:
        order["status"] = status

orders = [{"id": 1}, {"id": 2}]
append_status(orders, "shipped")
print(orders)
```

**Вывод консоли:**

```
[{'id': 1, 'status': 'shipped'}, {'id': 2, 'status': 'shipped'}]
```

Документируй в docstring, если функция мутирует аргумент!

---

### Пример 23: `**kwargs` для SQL-подобного фильтра

```python
def find_users(users, **filters):
    """users — list of dict. filters — поле=значение."""
    result = []
    for user in users:
        match = True
        for key, value in filters.items():
            if user.get(key) != value:
                match = False
                break
        if match:
            result.append(user)
    return result

users = [
    {"name": "Anna", "role": "admin", "active": True},
    {"name": "Bob", "role": "user", "active": True},
    {"name": "Vika", "role": "user", "active": False},
]

print(find_users(users, role="user", active=True))
```

**Вывод консоли:**

```
[{'name': 'Bob', 'role': 'user', 'active': True}]
```

---

### Пример 24: Распаковка dict в **kwargs

```python
def create_point(x, y, z=0):
    return {"x": x, "y": y, "z": z}

coords_2d = {"x": 10, "y": 20}
coords_3d = {"x": 1, "y": 2, "z": 3}

print(create_point(**coords_2d))
print(create_point(**coords_3d))
```

**Вывод консоли:**

```
{'x': 10, 'y': 20, 'z': 0}
{'x': 1, 'y': 2, 'z': 3}
```

---

### Пример 25: Type hints в действии

```python
def full_name(first: str, last: str, middle: str = "") -> str:
    if middle:
        return f"{last} {first} {middle}"
    return f"{last} {first}"

print(full_name("Иван", "Петров"))
print(full_name("Мария", "Сидорова", "Александровна"))

# Аннотации не мешают передать «не тот» тип — Python не ругается
print(full_name(1, 2))    # работает, но плохая практика
```

**Вывод консоли:**

```
Петров Иван
Сидорова Мария Александровна
2 1
```

---

### Пример 26: Рекурсия — превью (подробнее в гл. 16)

```python
def factorial(n):
    if n < 0:
        return None
    if n <= 1:
        return 1
    return n * factorial(n - 1)

print(factorial(5))    # 120
print(factorial(0))    # 1
```

Функция вызывает **саму себя**. Нужен **базовый случай** (`n <= 1`), иначе бесконечная рекурсия → `RecursionError`.

---

### Пример 27: Обёртка (wrapper) — функция вокруг функции

```python
def log_calls(func):
    """Принимает функцию, возвращает новую с логированием."""
    def wrapper(*args, **kwargs):
        print(f"→ Вызов {func.__name__}({args}, {kwargs})")
        result = func(*args, **kwargs)
        print(f"← Результат: {result}")
        return result
    return wrapper

def multiply(a, b):
    return a * b

logged_multiply = log_calls(multiply)
logged_multiply(3, 4)
```

**Вывод консоли:**

```
→ Вызов multiply((3, 4), {})
← Результат: 12
```

*(Декораторы — глава 14; здесь — идея передачи функций)*

---

### Пример 28: Полный мини-проект — библиотека

```python
def validate_book(title, author, year):
    errors = []
    if not title or not title.strip():
        errors.append("Название пустое")
    if not author or not author.strip():
        errors.append("Автор пустой")
    if not isinstance(year, int) or year < 0 or year > 2026:
        errors.append("Некорректный год")
    return len(errors) == 0, errors

def create_book(title, author, year, **extra):
    valid, errors = validate_book(title, author, year)
    if not valid:
        return None, errors
    book = {"title": title.strip(), "author": author.strip(), "year": year}
    book.update(extra)
    return book, []

def add_book(library, **book_data):
    book, errors = create_book(**book_data)
    if errors:
        print(f"Ошибка: {', '.join(errors)}")
        return False
    library.append(book)
    print(f"Добавлено: «{book['title']}»")
    return True

def list_books(library, **filters):
    books = library
    for key, value in filters.items():
        books = [b for b in books if b.get(key) == value]
    for i, b in enumerate(books, 1):
        print(f"  {i}. {b['title']} — {b['author']} ({b['year']})")

library = []
add_book(library, title="1984", author="Оруэлл", year=1949, genre="антиутопия")
add_book(library, title="", author="X", year=2000)
add_book(library, title="Мастер и Маргарита", author="Булгаков", year=1967)
list_books(library)
list_books(library, author="Булгаков")
```

**Вывод консоли:**

```
Добавлено: «1984»
Ошибка: Название пустое
Добавлено: «Мастер и Маргарита»
  1. 1984 — Оруэлл (1949)
  2. Мастер и Маргарита — Булгаков (1967)
  1. Мастер и Маргарита — Булгаков (1967)
```

---

### Пример 29: Ошибки аргументов — что увидишь в консоли

```python
def divide(a, b, message="результат"):
    return a / b

# 1. Не хватает аргумента
try:
    divide(10)
except TypeError as e:
    print("Ошибка 1:", e)

# 2. Лишний позиционный
try:
    divide(10, 2, 3, 4)
except TypeError as e:
    print("Ошибка 2:", e)

# 3. Неизвестный именованный
try:
    divide(10, 2, unknown=5)
except TypeError as e:
    print("Ошибка 3:", e)

# 4. Правильно
print("OK:", divide(10, 2))
```

**Вывод консоли (сокращённо):**

```
Ошибка 1: divide() missing 1 required positional argument: 'b'
Ошибка 2: divide() takes from 2 to 3 positional arguments but 4 were given
Ошибка 3: divide() got an unexpected keyword argument 'unknown'
OK: 5.0
```

---

### Пример 30: `locals()` и `globals()` — отладка scope

```python
DEBUG = True

def compute(x, y):
    temp = x + y
    result = temp * 2
    if DEBUG:
        print("Локальные:", list(locals().keys()))
    return result

compute(3, 4)

def show_global():
    print("DEBUG" in globals())    # True
    print(globals().get("DEBUG"))

show_global()
```

**Вывод консоли:**

```
Локальные: ['x', 'y', 'temp', 'result']
True
True
```

*(Не злоупотребляй `globals()` в продакшене — только для обучения и отладки)*

---

## Теория (расширение): передача аргументов, комбинации, антипаттерны

### Как Python связывает аргументы — 4 шага

```python
def f(a, b, c=0, *args, **kwargs):
    pass
```

1. **Позиционные** → параметры слева направо
2. **Именованные** → по имени (остальные параметры)
3. **Лишние позиционные** → `*args`
4. **Лишние именованные** → `**kwargs`

```python
f(1, 2, 3, 4, 5, x=6, y=7)
# a=1, b=2, c=3, args=(4,5), kwargs={'x':6,'y':7}
```

---

### Комбинирование `*args` и `**kwargs` при вызове

```python
def connect(host, port, ssl=False, timeout=30):
    print(host, port, ssl, timeout)

config = {"host": "db.local", "port": 5432, "ssl": True}
extra = (30,)   # timeout как позиционный — не сработает напрямую

connect(**config, timeout=60)
# host=db.local, port=5432, ssl=True, timeout=60
```

---

### Антипаттерны — чего избегать

| Плохо | Хорошо |
|-------|--------|
| `def f(lst=[])` | `def f(lst=None)` |
| `global` везде | `return` значения |
| Функция на 200 строк | Разбить на маленькие |
| `def process(data): data.sort()` | `return sorted(data)` или копия |
| Имя `list`, `str` | `items`, `text` |
| Без docstring у публичных функций | Краткий docstring |

---

### Пошаговый разбор: вызов с `*args` распаковкой

```python
def greet(first, last, greeting="Hello"):
    print(f"{greeting}, {first} {last}")

data = ("Anna", "Smith")
greet(*data)
```

| Шаг | Действие |
|-----|----------|
| 1 | `data` → tuple `("Anna", "Smith")` |
| 2 | `*data` → `first="Anna"`, `last="Smith"` |
| 3 | `greeting` → default `"Hello"` |
| 4 | Печать |

---

### Функция как «чёрный ящик»

```
  Вход (аргументы)
        ↓
   ┌─────────────┐
   │   Функция   │  локальные переменные внутри
   └─────────────┘
        ↓
  Выход (return)
```

Вызывающий код **не должен** знать внутренности — только сигнатуру и docstring.

---

## Шпаргалка

```python
# Определение
def name(param1, param2=default, *args, kwonly, **kwargs):
    """Docstring."""
    return result

# Вызов
name(1, 2)
name(param2=2, param1=1)
name(1, 2, 3, 4, extra=5)
name(*tuple_args, **dict_kwargs)

# Scope
global var     # изменить global (избегай)
nonlocal var   # изменить enclosing

# Полезно
return a, b    # tuple
if x is None:  # проверка None
```

---

## FAQ начинающего

**В: Чем параметр отличается от аргумента?**  
Параметр — в `def`. Аргумент — при вызове. `def f(x):` — `x` параметр. `f(5)` — 5 аргумент.

**В: Обязательно ли `return`?**  
Нет. Без `return` → `None`.

**В: Можно ли вернуть несколько значений?**  
Да: `return a, b` — это tuple. Распаковка: `x, y = f()`.

**В: `*args` обязательно так называть?**  
Нет, но `*args` и `**kwargs` — стандарт. Важна звёздочка.

**В: Зачем `**kwargs`?**  
Гибкость: функция принимает любые именованные параметры (конфиг, опции, фильтры).

**В: Когда `global`?**  
Почти никогда. Предпочитай `return` или класс (позже).

**В: Позиционный после именованного?**  
Нельзя: `f(a=1, 2)` — SyntaxError.

**В: Функция внутри функции зачем?**  
Замыкания, декораторы, инкапсуляция логики.

**В: `lambda` — это функция?**  
Да, анонимная однострочная. Глава 14.

**В: Как узнать локальные переменные?**  
`locals()` внутри функции, `globals()` — глобальные (для отладки).

**В: Можно ли изменить tuple-аргумент?**  
Параметр — ссылка. Сам tuple не меняется (immutable), но `t = t + (1,)` создаст локальную ссылку на новый tuple, снаружи не видно.

**В: `return` без значения?**  
`return` или `return None` — выход с `None`.

**В: Сколько `return` допустимо?**  
Сколько нужно — ранние выходы нормальны.

**В: `*args` пустой?**  
Да — пустой tuple `()`.

**В: Порядок: можно ли `**kwargs` перед `*args` в def?**  
Нет. Строгий порядок в сигнатуре.

---

### Таблица ошибок

| Ошибка | Причина | Решение |
|--------|---------|---------|
| `TypeError: missing argument` | Не передали обязательный | Добавь аргумент или default |
| `TypeError: got multiple values` | Позиционный + именованный для одного параметра | Один способ на параметр |
| `UnboundLocalError` | Присвоение делает имя локальным | `global`/`nonlocal` или другое имя |
| `SyntaxError: non-default after default` | `def f(a=1, b)` | Default в конец |
| Возвращает `None` | Забыли `return` | Добавь `return` |

---

### Частые баги — до и после

```python
# БАГ: забыли return
def add(a, b):
    a + b
# FIX:
def add(a, b):
    return a + b

# БАГ: mutable default
def f(lst=[]):
# FIX:
def f(lst=None):
    if lst is None: lst = []

# БАГ: global без нужды
def inc():
    global x; x += 1
# FIX:
def inc(x):
    return x + 1
```

---

## Домашнее задание

**Файл:** `homework_06.py`

### Задача 1 — Лёгкая
Напиши `circle_area(radius)` — площадь круга `π * r²`. `π = 3.14159`. Верни результат. Протестируй на `r=1`, `r=5`.

<details>
<summary>Подсказка</summary>

`return 3.14159 * radius ** 2`

</details>

---

### Задача 2 — Лёгкая
Напиши `is_even(n)` → `True`/`False`. Без `if` можно: `return n % 2 == 0`.

<details>
<summary>Подсказка</summary>

Одна строка: `return n % 2 == 0`

</details>

---

### Задача 3 — Средняя
Напиши `min_max(numbers)` → tuple `(min, max)` **без** `min()`/`max()`. Пустой list → `None, None`.

<details>
<summary>Подсказка</summary>

Ранний return для `if not numbers`. Иначе цикл с накопителями.

</details>

---

### Задача 4 — Средняя
Напиши `format_name(first, last, middle="", style="normal")`:
- `style="normal"` → `"Иван Петров"`
- `style="official"` → `"Петров Иван Петрович"` (если middle пуст — без отчества)
- `style="short"` → `"И. Петров"`

<details>
<summary>Подсказка</summary>

`if/elif/elif` по `style`. Для short: `f"{first[0]}. {last}"`.

</details>

---

### Задача 5 — Средняя
Напиши `average(*args)` — среднее произвольного числа аргументов. Пустой вызов → `None`.

```python
average(10, 20, 30)    # 20.0
average()              # None
```

---

### Задача 6 — Средняя
Напиши `build_query(table, **conditions)` — строка вида:
`"SELECT * FROM users WHERE age = 25 AND city = 'Moscow'"`

Только строки и числа в conditions. Таблица — параметр `table`.

<details>
<summary>Подсказка</summary>

Собери части `f"{key} = {value}"`, для str добавь кавычки. `" AND ".join(parts)`.

</details>

---

### Задача 7 — Сложная
**Конвертер температур.** Функции:
- `celsius_to_fahrenheit(c)`
- `fahrenheit_to_celsius(f)`
- `convert(temp, from_unit, to_unit)` — `"C"` / `"F"`, вызывает нужную

При неверной unit — `return None, "ошибка"`. Используй dict функций или `if/elif`.

<details>
<summary>Подсказка</summary>

```python
CONVERTERS = {("C", "F"): celsius_to_fahrenheit, ("F", "C"): fahrenheit_to_celsius}
```

</details>

---

### Задача 8 — Сложная
Напиши `sanitize_users(users, **defaults)`:
- `users` — list of dict
- `defaults` — поля по умолчанию для каждого user
- возвращает **новый** list (не мутирует `users`!)
- каждый user — копия с применёнными defaults (нет ключа → взять из defaults)

<details>
<summary>Подсказка</summary>

`result = []`, для каждого user: `new_user = defaults.copy(); new_user.update(user); result.append(new_user)`.

</details>

---

### Задача 9 — Сложная ⏳ лучше после главы 14

> Использует **`nonlocal` и замыкания** — полный разбор в **главе 14**. Можно попробовать по Примерам 21, 27, но если туман — вернись после гл. 14.

**Счётчик с `nonlocal`.** `make_rate_limiter(max_calls)` возвращает функцию `check()`:
- каждый `check()` увеличивает счётчик
- если счётчик > max_calls → `False`
- иначе → `True`
- `make_rate_limiter(3)` → True, True, True, False, False

<details>
<summary>Подсказка</summary>

См. Примеры 21, 27. `nonlocal count` внутри `check()`.

</details>

---

### Задача 10 — Сложная (бонус)
**Меню калькулятора на функциях** (расширь Пример 20):
- `while True` меню
- `input()` для операции и чисел
- операции в dict
- выход по `q`
- деление на 0 — сообщение, не падать

---

### Задача 11 — Сложная (бонус)
Напиши `pipe(value, *functions)`:
- применяет цепочку функций слева направо
- `pipe(5, lambda x: x+1, lambda x: x*2)` → `12`

*(lambda можно заменить обычными def)*

---

### Как сдавать

- `homework_06.py`
- Задачи 7–11 — с тестовыми вызовами
- Частями: 1–5, 6–11

**Критерии зачёта:**
- Docstring хотя бы на 2 функциях
- Нет mutable default
- `*args`/`**kwargs` где уместно
- Не мутируешь вход без необходимости (задача 8!)

---

**Сделай задачи сам и пришли код на проверку. После проверки — Глава 7: *List/dict comprehensions, enumerate, zip*.**

---
Конец главы.