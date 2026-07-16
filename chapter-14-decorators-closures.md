# Тема: Замыкания и декораторы

> **Формат:** сначала объяснение простыми словами, потом пример с разбором.  
> Не надо зубрить 45 примеров — **3 части теории + 12 примеров + 6 задач**.

---

## Цель главы

После прочтения ты понимаешь:

1. **Замыкание** — внутренняя функция «помнит» переменные внешней.
2. **Декоратор** — обёртка вокруг функции: логика до/после без копипасты.
3. **`@имя`** — короткая запись; `@property` из главы 13 — тот же механизм.

---

# ЧАСТЬ 1. Функции как объекты и замыкания

## 1.1. Функция — это тоже «вещь»

В Python функцию можно **положить в переменную**, передать аргументом, вернуть из другой функции:

```python
def greet(name):
    return f"Привет, {name}!"

say = greet          # say теперь ссылается на ту же функцию
print(say("Anna"))   # Привет, Anna!
```

Это основа декораторов: декоратор — функция, которая **принимает функцию** и **возвращает другую функцию**.

---

## 1.2. Функция внутри функции

```python
def outer():
    def inner():
        print("Я внутри inner")
    inner()

outer()
```

`inner` видна только внутри `outer`. Снаружи `inner()` вызвать нельзя — это локальное имя.

---

## 1.3. Замыкание — «помнит» внешние переменные

```python
def make_multiplier(n):
    def multiply(x):
        return x * n    # n взяли из внешней функции
    return multiply

double = make_multiplier(2)
triple = make_multiplier(3)

print(double(5))   # 10
print(triple(5))   # 15
```

**Замыкание (closure)** — `multiply` «замкнула» на себе значение `n`.  
Даже когда `make_multiplier` уже завершилась, `double` всё ещё помнит `n = 2`.

**Аналогия:** фабрика печатает калькуляторы. Один всегда умножает на 2, другой на 3. Настройка `n` «зашита» внутрь.

---

## 1.4. Зачем замыкания Junior-разработчику

- **Декораторы** построены на замыканиях.
- **Фабрики функций** — одна настройка, много похожих функций (`double`, `triple`).
- **Счётчики и кэш** — внутреннее состояние без глобальных переменных.

---

## 1.5. `nonlocal` — изменить переменную внешней функции

```python
def counter():
    count = 0
    def inc():
        nonlocal count
        count += 1
        return count
    return inc

c = counter()
print(c(), c(), c())   # 1, 2, 3
```

Без `nonlocal` Python создал бы **новую локальную** `count` в `inc` и упал бы с ошибкой при `count += 1`.

---

## 1.6. Типичные ошибки

| Ошибка | Что происходит |
|--------|----------------|
| Забыли `return inner` | Фабрика возвращает `None`, вызов падает |
| Путают `n` при цикле без замыкания | Все lambda берут последнее значение (см. пример 4) |
| Мутируют замкнутый список неожиданно | Один список на все вызовы — используй осторожно |

---

### ✅ Проверь себя — часть 1

1. `double = make_multiplier(2)` — что внутри `double`? → **Функция multiply с n=2**.
2. Замыкание «живёт» после выхода из `outer`? → **Да**, если на него есть ссылка.
3. Зачем `nonlocal`? → **Изменить переменную внешней функции из внутренней**.

---

# ЧАСТЬ 2. Декораторы

## 2.1. Идея декоратора

Нужно **перед каждым вызовом** функции печатать лог. Плохо:

```python
def add(a, b):
    print("вызов add")      # копипаста
    return a + b

def sub(a, b):
    print("вызов sub")      # снова копипаста
    return a - b
```

Хорошо — **одна обёртка** для всех функций:

```python
def log_calls(func):
    def wrapper(*args, **kwargs):
        print(f"Вызов {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
```

---

## 2.2. Как применить декоратор вручную

```python
def greet(name):
    return f"Привет, {name}!"

greet = log_calls(greet)
greet("Bob")
```

`log_calls(greet)` возвращает `wrapper`. Имя `greet` теперь указывает на `wrapper`, который внутри вызывает **оригинальный** `greet`.

---

## 2.3. Синтаксис `@`

```python
@log_calls
def greet(name):
    return f"Привет, {name}!"
```

Полностью то же самое, что `greet = log_calls(greet)` **до** определения тела.  
Читается: «определи `greet` и сразу оберни в `log_calls`».

---

## 2.4. `*args` и `**kwargs` в wrapper

Декоратор должен работать с **любой** сигнатурой:

```python
def wrapper(*args, **kwargs):
    ...
    return func(*args, **kwargs)
```

Иначе обёртка сломает функции с разным числом аргументов (из главы 6).

---

## 2.5. `functools.wraps` — сохранить имя функции

Без `wraps`:

```python
print(greet.__name__)   # wrapper  — неудобно для отладки
```

С `wraps`:

```python
from functools import wraps

def log_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Вызов {func.__name__}")
        return func(*args, **kwargs)
    return wrapper
```

`@wraps(func)` копирует `__name__`, `__doc__` с оригинала на `wrapper`.

---

## 2.6. Связь с главой 13

`@property`, `@staticmethod`, `@classmethod` — **встроенные декораторы**.  
Ты уже пользовался ими. Теперь знаешь механизм: «взять функцию → вернуть обёртку с другим поведением».

---

### ✅ Проверь себя — часть 2

1. `@log_calls` над `def f` — что происходит? → **`f = log_calls(f)`**.
2. Зачем `*args, **kwargs` в wrapper? → **Принять любые аргументы оригинала**.
3. `@property` — это декоратор? → **Да**.

---

# ЧАСТЬ 3. Практические декораторы

## 3.1. Таймер — измерить время

```python
import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        elapsed = time.perf_counter() - start
        print(f"{func.__name__}: {elapsed:.4f} сек")
        return result
    return wrapper
```

Поведение **после** вызова: замерили время, вернули результат оригинала.

---

## 3.2. Retry — повтор при ошибке

Идея из главы 9: если функция упала — попробовать ещё раз:

```python
def retry(times=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            last_error = None
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    last_error = e
                    print(f"Попытка {attempt}/{times} не удалась: {e}")
            raise last_error
        return wrapper
    return decorator
```

Здесь **два уровня** функций — разберём в примере 11.

---

## 3.3. Декоратор с параметрами — три уровня

| Уровень | Что делает |
|---------|------------|
| `retry(times=3)` | Принимает настройку, возвращает **декоратор** |
| `decorator(func)` | Принимает функцию, возвращает **wrapper** |
| `wrapper(...)` | Вызывается вместо функции |

Использование:

```python
@retry(times=2)
def unstable():
    ...
```

Эквивалент: `unstable = retry(times=2)(unstable)`.

---

## 3.4. Несколько декораторов — порядок снизу вверх

```python
@timer
@log_calls
def work():
    pass
```

Это: `work = timer(log_calls(work))`.  
Сначала `log_calls`, потом `timer` оборачивает уже обёрнутую функцию.

---

## 3.5. Когда декоратор уместен

| Ситуация | Декоратор |
|----------|-----------|
| Логирование вызовов | `@log_calls` |
| Замер времени | `@timer` |
| Повтор при сбое | `@retry` |
| Проверка прав / auth | `@require_login` |
| Кэш результата | `@lru_cache` (stdlib) |

Не декорируй всё подряд — если логика **только в одной** функции, проще написать внутри неё.

---

### ✅ Проверь себя — часть 3

1. `@retry(times=2)` — сколько уровней функций? → **Три** (фабрика → декоратор → wrapper).
2. `@a` `@b` над `f` — что ближе к `f`? → **`b` применяется первым**.
3. `lru_cache` откуда? → **`functools`**, готовый декоратор кэша**.

---

# Практика — 12 примеров с разбором

---

## Пример 1. Функция в переменной

```python
def square(x):
    return x * x

op = square
print(op(4))
print(square is op)
```

**Вывод:**
```
16
True
```

**Разбор:** `op` и `square` — одна и та же функция в памяти (`is` → True). Декораторы используют эту идею: передаём `func` в другую функцию.

---

## Пример 2. Простое замыкание

```python
def make_greeter(prefix):
    def greet(name):
        return f"{prefix}, {name}!"
    return greet

hello = make_greeter("Привет")
formal = make_greeter("Здравствуйте")

print(hello("Anna"))
print(formal("Anna"))
```

**Вывод:**
```
Привет, Anna!
Здравствуйте, Anna!
```

**Разбор:** одна фабрика `make_greeter`, два замыкания с разным `prefix`. `prefix` не глобальный — у каждого greeter свой.

---

## Пример 3. Счётчик на nonlocal

```python
def make_counter(start=0):
    count = start
    def inc(step=1):
        nonlocal count
        count += step
        return count
    return inc

c = make_counter(10)
print(c())
print(c(5))
print(c())
```

**Вывод:**
```
11
16
17
```

**Разбор:** состояние `count` живёт в замыкании, не в глобальной переменной. Каждый `make_counter()` — отдельный счётчик.

---

## Пример 4. Ловушка lambda в цикле (и исправление)

```python
# ПЛОХО — все lambda возьмут последний i
funcs_bad = []
for i in range(3):
    funcs_bad.append(lambda: i)

print([f() for f in funcs_bad])

# ХОРОШО — замыкание с аргументом по умолчанию
funcs_good = []
for i in range(3):
    funcs_good.append(lambda i=i: i)

print([f() for f in funcs_good])
```

**Вывод:**
```
[2, 2, 2]
[0, 1, 2]
```

**Разбор:** в плохом варианте все lambda ссылаются на **одну** переменную `i`, которая в конце цикла = 2. Исправление: `i=i` фиксирует значение в момент создании lambda.

---

## Пример 5. Декоратор без `@`

```python
def shout(func):
    def wrapper(*args, **kwargs):
        print("=== START ===")
        result = func(*args, **kwargs)
        print("=== END ===")
        return result
    return wrapper

def add(a, b):
    return a + b

add = shout(add)
print(add(2, 3))
```

**Вывод:**
```
=== START ===
=== END ===
5
```

**Разбор:** `add` теперь `wrapper`. При вызове `add(2, 3)` выполняется обёртка, внутри — оригинальный `add`. Результат 5 возвращается наружу.

---

## Пример 6. Синтаксис `@`

```python
def shout(func):
    def wrapper(*args, **kwargs):
        print(">>>", func.__name__)
        return func(*args, **kwargs)
    return wrapper

@shout
def multiply(a, b):
    return a * b

print(multiply(3, 4))
```

**Вывод:**
```
>>> multiply
12
```

**Разбор:** `@shout` = `multiply = shout(multiply)`. Имя в логе — пока ещё `multiply` (до `wraps` в следующем примере wrapper бы назывался `wrapper`).

---

## Пример 7. functools.wraps

```python
from functools import wraps

def shout(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs)
    return wrapper

@shout
def divide(a, b):
    """Делит a на b."""
    return a / b

print(divide.__name__)
print(divide.__doc__)
```

**Вывод:**
```
divide
Делит a на b.
```

**Разбор:** без `@wraps(func)` было бы `wrapper` и пустой docstring. Для отладки и `help()` важно сохранять метаданные.

---

## Пример 8. Логирование аргументов

```python
from functools import wraps

def log_args(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"args={args}, kwargs={kwargs}")
        return func(*args, **kwargs)
    return wrapper

@log_args
def power(base, exp=2):
    return base ** exp

print(power(3))
print(power(2, exp=5))
```

**Вывод:**
```
args=(3,), kwargs={}
9
args=(2,), kwargs={'exp': 5}
32
```

**Разбор:** декоратор видит и позиционные, и именованные аргументы. Оригинальная сигнатура `exp=2` сохраняется.

---

## Пример 9. Декоратор-таймер (упрощённый)

```python
import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.perf_counter()
        result = func(*args, **kwargs)
        print(f"{func.__name__}: {time.perf_counter() - start:.6f} s")
        return result
    return wrapper

@timer
def slow_sum(n):
    return sum(range(n))

print(slow_sum(1_000_000))
```

**Вывод (примерно):**
```
slow_sum: 0.045123 s
499999500000
```

**Разбор:** время печатаем, но **возвращаем** результат оригинала — иначе сломаем вызывающий код.

---

## Пример 10. Retry при ошибке

```python
from functools import wraps

def retry(times=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, times + 1):
                try:
                    return func(*args, **kwargs)
                except ValueError as e:
                    print(f"попытка {attempt}: {e}")
            raise ValueError("все попытки исчерпаны")
        return wrapper
    return decorator

attempt = 0

@retry(times=3)
def flaky():
    global attempt
    attempt += 1
    if attempt < 3:
        raise ValueError("сбой")
    return "OK"

print(flaky())
```

**Вывод:**
```
попытка 1: сбой
попытка 2: сбой
OK
```

**Разбор:** первые два вызова внутри `flaky` падают, третий успешен. Декоратор **не глотает** ошибку бесконечно — после 3 попыток пробрасывает дальше.

---

## Пример 11. Три уровня — разбор по шагам

```python
def repeat(n):
    print(f"1) repeat({n}) вызван — возвращаю decorator")
    def decorator(func):
        print(f"2) decorator получил {func.__name__}")
        def wrapper(*args, **kwargs):
            print(f"3) wrapper вызывает {func.__name__}")
            return func(*args, **kwargs)
        return wrapper
    return decorator

@repeat(1)
def hello():
    return "hi"

hello()
```

**Вывод:**
```
1) repeat(1) вызван — возвращаю decorator
2) decorator получил hello
3) wrapper вызывает hello
```

**Разбор:** строки 1–2 печатаются **при определении** функции (импорт/загрузка модуля). Строка 3 — при **каждом вызове** `hello()`. Цепочка: `hello = repeat(1)(hello)`.

---

## Пример 12. Несколько декораторов

```python
from functools import wraps

def bold(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return f"**{func(*args, **kwargs)}**"
    return wrapper

def italic(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        return f"_{func(*args, **kwargs)}_"
    return wrapper

@bold
@italic
def title():
    return "Python"

print(title())
```

**Вывод:** `_**Python**_`

**Разбор:** порядок: сначала `italic(title)`, потом `bold(...)`. Внутри `bold` вызывает уже обёрнутый `italic`, который вызывает `title`. Результат: курсив снаружи, жирный внутри.

---

# Шпаргалка

| Понятие | Суть |
|---------|------|
| Замыкание | Внутренняя функция помнит переменные внешней |
| `nonlocal` | Менять переменную внешней функции |
| Декоратор | `def deco(func): ... return wrapper` |
| `@deco` | `func = deco(func)` |
| `@wraps(func)` | Сохранить `__name__`, `__doc__` |
| Декоратор с args | `deco(arg)` → возвращает `decorator` → `wrapper` |
| Несколько `@` | Снизу вверх: `@a @b` → `a(b(f))` |

---

# FAQ

**Декоратор обязателен на Junior?**  
Понимать замыкания и простой `@decorator` — да. Трёхуровневые — на собеседовании могут спросить идею.

**Чем декоратор лучше просто вызова `log(f())`?**  
Оригинальная функция вызывается в **одном месте** — в wrapper. Не забудешь лог в одной из 20 функций.

**Можно декорировать класс?**  
Да, но реже. Чаще декорируют функции и методы. Класс-декоратор — через `__call__` (продвинутый уровень).

**@lru_cache когда?**  
Чистая функция с дорогим вычислением и повторяющимися аргументами — кэш из `functools`.

**Декоратор vs наследование?**  
Декоратор добавляет **поведение вокруг** вызова. Наследование — **тип объекта**. Разные задачи.

---

# Домашнее задание

**Файл:** `homework_14.py`

---

## Задача 1. Замыкание multiply

Напиши `make_multiplier(n)`, возвращает функцию `multiply(x) = x * n`.

Проверь: `make_multiplier(5)(4)` → `20`

---

## Задача 2. Счётчик

Напиши `make_counter()`, возвращает `inc()` без аргументов. Каждый вызов `inc()` даёт 1, 2, 3…

Проверь три вызова подряд.

**Должно вывести:** `1`, `2`, `3`

---

## Задача 3. Декоратор uppercase

Напиши декоратор `@uppercase_result`: если функция возвращает **строку** — вернуть `.upper()`, иначе как есть.

```python
@uppercase_result
def greet(name):
    return f"hello, {name}"
```

**Должно:** `greet("anna")` → `"HELLO, ANNA"`

---

## Задача 4. Декоратор с @wraps

Скопируй задачу 3, добавь `@wraps(func)`.  
Выведи `greet.__name__`.

**Должно вывести:** `greet`

---

## Задача 5. Декоратор `run_twice`

Напиши `@run_twice` — оригинальная функция вызывается **два раза**, возвращается результат **второго** вызова.

```python
@run_twice
def say():
    print("hi")
    return 42
```

**Должно вывести:** `hi` два раза, return `42`

---

## Задача 6. Мини-проект: лог + таймер

1. Напиши `@log_calls` (печатает имя функции перед вызовом).
2. Напиши `@timer` (печатает время после вызова).
3. Повесь **оба** на функцию `work()` с `return sum(range(100_000))`.
4. Вызови `work()` один раз.

**Должно:** в консоли имя `work`, время, результат `4999950000`

Подсказка: порядок декораторов — `@timer` сверху, `@log_calls` снизу (сначала лог, потом таймер вокруг).

---

## Как сдать

- Файл `homework_14.py`
- Сдавай 1–3, потом 4–6
- Пришли код — проверю

---

# Итог

1. **Замыкание** — функция + «запомненные» переменные внешней области.
2. **Декоратор** — `wrapper` вокруг `func`, `@` — синтаксический сахар.
3. **`wraps`** — не терять имя и docstring.
4. **Декоратор с параметрами** — фабрика возвращает декоратор.

**Следующая глава 15:** алгоритмы — сложность, поиск, сортировка.

---
Конец главы.