# Тема: Исключения — `try`/`except`/`finally`, свои ошибки

> **Файл:** `homework_09.py`  
> **Мостик из гл. 8:** теперь разбираем `FileNotFoundError`, `JSONDecodeError`, `safe_read_json` — то, что видел в превью.  
> **Задача 9 (retry-декоратор):** только **после гл. 14**.

## Теория

### Что это такое

**Исключение (exception)** — способ Python сказать: «что-то пошло не так, я не могу продолжить **эту** операцию нормально».

Без обработки программа **падает** с traceback:

```python
print(10 / 0)    # ZeroDivisionError: division by zero
```

**Обработка исключений** — перехватить ошибку и **решить**, что делать: показать сообщение, повторить, записать в лог, вернуть значение по умолчанию.

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Нельзя делить на ноль!")
    result = None
```

Программа **не падает** — продолжает работу после `except`.

---

### Синтаксис: `try` / `except` / `else` / `finally`

```python
try:
    # код, который может вызвать ошибку
    risky_operation()
except SomeError:
    # что делать, если поймали SomeError
    handle_error()
else:
    # выполнится, если в try НЕ было исключения
    on_success()
finally:
    # выполнится ВСЕГДА — и при ошибке, и без
    cleanup()
```

| Блок | Когда выполняется |
|------|-------------------|
| `try` | Пробуем опасный код |
| `except` | Поймали указанную ошибку |
| `else` | `try` завершился **без** исключения |
| `finally` | **Всегда** в конце |

**Минимальная форма** (90% случаев на Junior):

```python
try:
    do_something()
except SomeError as e:
    print(f"Ошибка: {e}")
```

`as e` — объект исключения с сообщением.

---

### Иерархия исключений — главные типы

Все исключения наследуются от `BaseException` → `Exception`.

| Исключение | Когда возникает |
|------------|-----------------|
| `ZeroDivisionError` | Деление на 0 |
| `ValueError` | Неверное значение (`int("abc")`) |
| `TypeError` | Неверный тип (`"a" + 5`) |
| `IndexError` | Индекс за границей list |
| `KeyError` | Нет ключа в dict |
| `FileNotFoundError` | Файл не найден |
| `PermissionError` | Нет прав на файл |
| `AttributeError` | Нет атрибута у объекта |
| `NameError` | Переменная не определена |
| `SyntaxError` | Ошибка синтаксиса (до запуска) |
| `json.JSONDecodeError` | Битый JSON |
| `StopIteration` | Итератор закончился |

```python
# Иерархия (упрощённо)
# BaseException
#   ├── KeyboardInterrupt
#   ├── SystemExit
#   └── Exception
#         ├── ValueError
#         ├── TypeError
#         ├── KeyError
#         ├── FileNotFoundError
#         └── ...
```

**Ловить конкретный тип** лучше, чем всё подряд:

```python
# Хорошо
except ValueError:
    ...

# Плохо (слишком широко)
except Exception:
    ...
```

---

### `raise` — выбросить исключение самому

```python
def withdraw(balance, amount):
    if amount <= 0:
        raise ValueError("Сумма должна быть положительной")
    if amount > balance:
        raise ValueError("Недостаточно средств")
    return balance - amount
```

**Зачем:** сообщить вызывающему коду, что операция **невозможна** — он обработает через `try/except`.

**Повторный выброс:**

```python
try:
    risky()
except ValueError as e:
    log(e)
    raise    # пробросить дальше после логирования
```

---

### Свои исключения (custom exceptions)

```python
class InsufficientFundsError(Exception):
    """Недостаточно денег на счёте."""
    pass

class ValidationError(Exception):
    def __init__(self, field, message):
        self.field = field
        self.message = message
        super().__init__(f"{field}: {message}")

def withdraw(balance, amount):
    if amount > balance:
        raise InsufficientFundsError(f"Нужно {amount}, есть {balance}")
```

Наследуй от `Exception` (не от `BaseException`).

---

### EAFP vs LBYL — два стиля

| Стиль | Расшифровка | Пример |
|-------|-------------|--------|
| **EAFP** | Easier to Ask Forgiveness than Permission | `try: x = d[key]` |
| **LBYL** | Look Before You Leap | `if key in d: x = d[key]` |

Python-идиоматичен **EAFP** для многих случаев:

```python
# EAFP — питоновски
try:
    value = int(user_input)
except ValueError:
    print("Введите число")

# LBYL — тоже OK
if user_input.isdigit():
    value = int(user_input)
```

---

### Как это работает «под капотом»

1. Python выполняет код в `try`
2. Если возникает исключение — **прерывает** выполнение `try`
3. Ищет подходящий `except` (сверху вниз по типам)
4. Если нашёл — выполняет `except`, продолжает после всей конструкции
5. Если не нашёл — исключение **всплывает** наверх (программа падает)
6. `finally` выполняется **перед** выходом из конструкции в любом случае

**Traceback** — стек вызовов от места ошибки до верха. Читай **снизу вверх**: последняя строка — тип и сообщение.

---

### Где это полезно и применяется в реальной разработке

| Сценарий | Обработка |
|----------|-----------|
| Ввод пользователя | `ValueError` при `int()` |
| Файлы | `FileNotFoundError` |
| API / JSON | `JSONDecodeError`, `KeyError` |
| БД | свои исключения драйвера |
| Валидация бизнес-логики | `raise CustomError` |
| Логирование + retry | `except` + повтор |

**Паттерн — безопасное преобразование ввода:**

```python
def get_positive_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value <= 0:
                raise ValueError("Число должно быть > 0")
            return value
        except ValueError as e:
            print(f"Ошибка: {e}. Попробуйте снова.")
```

---

### Микро-моменты, нюансы, частые ошибки новичков

#### 1. Голый `except:` — никогда!

```python
except:           # ловит ВСЁ, даже KeyboardInterrupt
except Exception:  # широко, но лучше конкретный тип
```

#### 2. Пустой `except: pass` — глотает ошибки

```python
try:
    important()
except Exception:
    pass    # ошибка проглочена — дебаг ад!
```

#### 3. Порядок `except` — от конкретного к общему

```python
try:
    ...
except ValueError:      # сначала конкретный
    ...
except Exception:      # потом общий
    ...
```

#### 4. `else` без `except` — нельзя

`else` только вместе с `except`.

#### 5. `return` в `finally` — перезаписывает return из try

На Junior — не делай `return` в `finally`.

#### 6. `KeyError` vs `dict.get()`

```python
# KeyError
value = d["missing"]

# Без исключения
value = d.get("missing", 0)
```

#### 7. `raise` без аргумента — внутри except

```python
except ValueError:
    log()
    raise    # пробросить то же исключение
```

#### 8. `assert` — не замена валидации в продакшене

```python
assert x > 0, "x должен быть положительным"   # для отладки
```

При `python -O` assert отключаются.

#### 9. Не всё ловить — программные ошибки должны падать

`NameError`, `SyntaxError` — баги в коде, не скрывай их.

#### 10. Сообщение в raise — информативное

```python
raise ValueError("age must be 0-150, got {age}")   # хорошо
raise ValueError()                                  # плохо
```

---

## Практика

> **Навигация:** **28 примеров**, шпаргалка, FAQ, домашка.

### Пример 1: Базовый try/except

```python
try:
    result = 10 / 0
except ZeroDivisionError:
    print("Поймали: деление на ноль")
    result = None

print("Программа продолжает работу, result =", result)
```

**Вывод консоли:**

```
Поймали: деление на ноль
Программа продолжает работу, result = None
```

**Разбор:** Выражение `10 / 0` вызывает `ZeroDivisionError`, но блок `except` перехватывает её — программа не завершается аварийно. В `except` задаём `result = None`, чтобы было понятно, что деление не удалось. Код после `try/except` выполняется в любом случае — в этом главный смысл обработки ошибок.

---

### Пример 2: `as e` — сообщение исключения

```python
try:
    number = int("не число")
except ValueError as e:
    print(f"Тип: {type(e).__name__}")
    print(f"Сообщение: {e}")
```

**Вывод консоли:**

```
Тип: ValueError
Сообщение: invalid literal for int() with base 10: 'не число'
```

**Разбор:** Функция `int("не число")` не может преобразовать текст в число и бросает `ValueError`. Конструкция `as e` даёт доступ к самому объекту исключения и его текстовому сообщению. `type(e).__name__` показывает имя класса ошибки — удобно для логов и отладки.

---

### Пример 3: Несколько типов исключений

```python
def safe_divide(a, b):
    try:
        return a / b
    except ZeroDivisionError:
        print("Ошибка: деление на ноль")
        return None
    except TypeError:
        print("Ошибка: нужны числа")
        return None

print(safe_divide(10, 2))      # 5.0
print(safe_divide(10, 0))      # None
print(safe_divide(10, "2"))    # None
```

**Вывод консоли:**

```
5.0
Ошибка: деление на ноль
None
Ошибка: нужны числа
None
```

**Разбор:** Каждый блок `except` ловит свой тип ошибки: деление на ноль и неверный тип аргумента. Успешное деление `10 / 2` возвращает `5.0` без лишних сообщений. При ошибке функция печатает пояснение и возвращает `None` вместо того, чтобы уронить программу.

---

### Пример 4: Один except для нескольких типов

```python
try:
    # data = int("abc")
    data = int("42")
except (ValueError, TypeError) as e:
    print(f"Ошибка преобразования: {e}")
else:
    print(f"Успех: {data}")
```

**Вывод консоли (при int("42")):**

```
Успех: 42
```

**При int("abc"):**

```
Ошибка преобразования: invalid literal for int() with base 10: 'abc'
```

**Разбор:** Один `except` ловит и `ValueError`, и `TypeError` — удобно, когда ошибки похожи по смыслу (сбой преобразования). Блок `else` выполняется только если исключения не было — для `"42"` видим «Успех». Для `"abc"` срабатывает `except`, а `else` пропускается.

---

### Пример 5: `else` — код при успехе

```python
def read_number(text):
    try:
        value = int(text)
    except ValueError:
        print(f"'{text}' — не число")
        return None
    else:
        print(f"Корректное число: {value}")
        return value

read_number("100")
read_number("abc")
```

**Вывод консоли:**

```
Корректное число: 100
'abc' — не число
```

**Разбор:** Блок `else` в `try` срабатывает только после успешного `int(text)`, а не при ошибке. Для `"100"` преобразование проходит — печатаем «Корректное число». Для `"abc"` попадаем в `except` и возвращаем `None` — так разделяют «всё ок» и «ошибка ввода».

---

### Пример 6: `finally` — всегда выполняется

```python
def demo_finally(will_fail):
    try:
        print("  try: начало")
        if will_fail:
            raise ValueError("ошибка!")
        print("  try: успех")
        return "ok"
    except ValueError as e:
        print(f"  except: {e}")
        return "error"
    finally:
        print("  finally: очистка (всегда)")

print("=== С ошибкой ===")
print("Результат:", demo_finally(True))
print("=== Без ошибки ===")
print("Результат:", demo_finally(False))
```

**Вывод консоли:**

```
=== С ошибкой ===
  try: начало
  except: ошибка!
  finally: очистка (всегда)
Результат: error
=== Без ошибки ===
  try: начало
  try: успех
  finally: очистка (всегда)
Результат: ok
```

**Разбор:** Блок `finally` выполняется всегда — и при ошибке, и при успехе, даже если в `try` или `except` есть `return`. При `will_fail=True` срабатывает `except`, но `finally` всё равно печатает «очистку». Это типичный паттерн для закрытия файлов и освобождения ресурсов.

---

### Пример 7: `raise` — валидация

```python
def set_age(age):
    if not isinstance(age, int):
        raise TypeError(f"age должен быть int, получен {type(age).__name__}")
    if age < 0 or age > 150:
        raise ValueError(f"age должен быть 0-150, получен {age}")
    print(f"Возраст установлен: {age}")

set_age(25)

try:
    set_age(-5)
except ValueError as e:
    print(f"Поймали: {e}")

try:
    set_age("25")
except TypeError as e:
    print(f"Поймали: {e}")
```

**Вывод консоли:**

```
Возраст установлен: 25
Поймали: age должен быть 0-150, получен -5
Поймали: age должен быть int, получен str
```

**Разбор:** Оператор `raise` сам создаёт исключение, когда данные не проходят проверку. Сначала проверяем тип (`int`), потом диапазон 0–150 — каждое нарушение даёт своё исключение. Вызов снаружи ловит их отдельными `try/except`, чтобы показать понятное сообщение пользователю.

---

### Пример 8: Свой класс исключения

```python
class NegativeBalanceError(Exception):
    """Попытка снять больше, чем есть на счёте."""
    def __init__(self, balance, amount):
        self.balance = balance
        self.amount = amount
        super().__init__(f"Баланс {balance}, запрошено {amount}")

def withdraw(balance, amount):
    if amount > balance:
        raise NegativeBalanceError(balance, amount)
    return balance - amount

try:
    withdraw(100, 150)
except NegativeBalanceError as e:
    print(f"Ошибка: {e}")
    print(f"Не хватает: {e.amount - e.balance}")
```

**Вывод консоли:**

```
Ошибка: Баланс 100, запрошено 150
Не хватает: 50
```

**Разбор:** Свой класс наследует `Exception` и добавляет поля `balance` и `amount` для деталей ошибки. Сообщение формируется в `super().__init__` — его видно при печати `e`. Попытка снять 150 при балансе 100 бросает исключение, и мы вычисляем, что не хватает 50.

---

### Пример 9: FileNotFoundError при работе с файлами

```python
from pathlib import Path

def read_file_safe(path):
    try:
        return Path(path).read_text(encoding="utf-8")
    except FileNotFoundError:
        print(f"Файл не найден: {path}")
        return None
    except PermissionError:
        print(f"Нет доступа: {path}")
        return None

print(read_file_safe("нет_такого.txt"))
print(read_file_safe("demo_notes.txt")[:20] if Path("demo_notes.txt").exists() else "создай demo_notes.txt из гл.8")
```

**Вывод консоли:**

```
Файл не найден: нет_такого.txt
...
```

**Разбор:** Метод `Path.read_text` бросает `FileNotFoundError`, если файла нет на диске — мы ловим её и возвращаем `None`. Для несуществующего файла программа не падает, а печатает понятное сообщение. Так файловые операции делают безопасными для всего приложения.

---

### Пример 10: JSONDecodeError

```python
import json

def parse_json_safe(text):
    try:
        return json.loads(text)
    except json.JSONDecodeError as e:
        print(f"Битый JSON на позиции {e.pos}: {e.msg}")
        return None

good = '{"name": "Anna", "age": 25}'
bad = '{"name": "Anna",}'   # лишняя запятая

print(parse_json_safe(good))
print(parse_json_safe(bad))
```

**Вывод консоли:**

```
{'name': 'Anna', 'age': 25}
Битый JSON на позиции ...: Expecting property name enclosed in double quotes
None
```

**Разбор:** Корректная JSON-строка парсится в обычный словарь Python. Строка с лишней запятой — невалидный JSON, `JSONDecodeError` сообщает позицию и причину сбоя. Функция возвращает `None` вместо падения — вызывающий код сам решает, что делать дальше.

---

### Пример 11: KeyError и безопасный доступ

```python
user = {"name": "Anna", "age": 25}

# Опасно
try:
    print(user["email"])
except KeyError as e:
    print(f"Ключа нет: {e}")

# Лучше для чтения
print(user.get("email", "не указан"))
```

**Вывод консоли:**

```
Ключа нет: 'email'
не указан
```

**Разбор:** Обращение `user["email"]` падает с `KeyError`, если ключа нет в словаре. Метод `get("email", "не указан")` безопасно возвращает значение по умолчанию без исключения. Для чтения опциональных полей `get` обычно удобнее, чем `try/except`.

---

### Пример 12: IndexError

```python
items = [1, 2, 3]

try:
    print(items[10])
except IndexError as e:
    print(f"Индекс вне диапазона: {e}")

# Безопасно
index = 10
if index < len(items):
    print(items[index])
else:
    print(f"Индекс {index} недопустим, длина {len(items)}")
```

**Вывод консоли:**

```
Индекс вне диапазона: list index out of range
Индекс 10 недопустим, длина 3
```

**Разбор:** Индекс 10 выходит за границы списка из трёх элементов (индексы 0–2) — Python бросает `IndexError`. Проверка `index < len(items)` заранее отсекает недопустимый доступ. Явное сообщение «длина 3» помогает понять, почему обращение невозможно.

---

### Пример 13: Цикл ввода с обработкой ошибок

```python
def get_positive_number():
    """Имитация input — подставляем значения."""
    inputs = ["abc", "-5", "0", "42"]
    for raw in inputs:
        try:
            value = int(raw)
            if value <= 0:
                raise ValueError("Число должно быть положительным")
            print(f"Принято: {value}")
            return value
        except ValueError as e:
            print(f"  '{raw}' — ошибка: {e}")

get_positive_number()
```

**Вывод консоли:**

```
  'abc' — ошибка: invalid literal for int() with base 10: 'abc'
  '-5' — ошибка: Число должно быть положительным
  '0' — ошибка: Число должно быть положительным
Принято: 42
```

---

### Пример 14: EAFP — доступ к dict

```python
config = {"host": "localhost", "port": 5432}

# EAFP
try:
    timeout = config["timeout"]
except KeyError:
    timeout = 30
    print("timeout не задан, используем 30")

# LBYL
timeout2 = config["timeout"] if "timeout" in config else 30

print(timeout, timeout2)
```

**Вывод консоли:**

```
timeout не задан, используем 30
30 30
```

---

### Пример 15: Иерархия — ловим родителя

```python
try:
    int("abc")
except Exception as e:        # ValueError — подкласс Exception
    print(f"Поймали Exception: {type(e).__name__}: {e}")

try:
    int("abc")
except ValueError as e:       # точнее — предпочтительнее
    print(f"Поймали ValueError: {e}")
```

**Вывод консоли:**

```
Поймали Exception: ValueError: invalid literal for int() with base 10: 'abc'
Поймали ValueError: invalid literal for int() with base 10: 'abc'
```

---

### Пример 16: `assert` для отладки

```python
def calculate_discount(price, percent):
    assert price >= 0, "price не может быть отрицательным"
    assert 0 <= percent <= 100, "percent должен быть 0-100"
    return price * (1 - percent / 100)

print(calculate_discount(100, 10))    # 90.0

try:
    calculate_discount(-100, 10)
except AssertionError as e:
    print(f"Assertion failed: {e}")
```

**Вывод консоли:**

```
90.0
Assertion failed: price не может быть отрицательным
```

---

## Теория (дополнение): цепочки, retry, антипаттерны

### Цепочка исключений

```python
try:
    int("abc")
except ValueError as e:
    raise RuntimeError("Не удалось обработать данные") from e
```

`from e` сохраняет **причину** — в traceback видно оба исключения.

---

### Паттерн retry — повтор при ошибке

```python
def fetch_data(attempt=1):
    if attempt < 3:
        raise ConnectionError("Сеть недоступна")
    return "данные"

for i in range(1, 5):
    try:
        result = fetch_data(attempt=i)
        print(f"Успех на попытке {i}: {result}")
        break
    except ConnectionError as e:
        print(f"Попытка {i}: {e}")
else:
    print("Все попытки исчерпаны")
```

---

### Логирование ошибок

```python
import traceback

def risky():
    return 1 / 0

try:
    risky()
except ZeroDivisionError:
    print("Ошибка!")
    traceback.print_exc()    # полный traceback в консоль
```

---

### Когда НЕ использовать try/except

| Ситуация | Лучше |
|----------|-------|
| Проверка `key in dict` | `.get()` или `in` |
| Проверка файла | `Path.exists()` |
| Проверка типа в своём коде | type hints + валидация |
| Ожидаемый поток программы | `if/else` |

`try/except` — для **непредвиденных** или **внешних** сбоев (ввод, файлы, сеть).

---

## Практика — примеры 17–28 (продолжение)

### Пример 17: Несколько except по порядку

```python
def process(data):
    try:
        value = int(data["count"])
        result = 100 / value
        return result
    except KeyError:
        print("Нет ключа 'count'")
    except ValueError:
        print("'count' не число")
    except ZeroDivisionError:
        print("count равен нулю")
    return None

print(process({"count": "10"}))    # 10.0
print(process({"count": "0"}))       # None
print(process({"count": "abc"}))    # None
print(process({}))                  # None
```

**Вывод консоли:**

```
10.0
count равен нулю
'count' не число
Нет ключа 'count'
```

---

### Пример 18: Обёртка функции — всегда возвращает результат или ошибку

```python
def safe_execute(func, *args, default=None, **kwargs):
    try:
        return func(*args, **kwargs), None
    except Exception as e:
        return default, str(e)

def divide(a, b):
    return a / b

result, err = safe_execute(divide, 10, 2)
print(f"10/2 = {result}, err={err}")

result, err = safe_execute(divide, 10, 0)
print(f"10/0 = {result}, err={err}")
```

**Вывод консоли:**

```
10/2 = 5.0, err=None
10/0 = None, err=division by zero
```

---

### Пример 19: ValidationError — своё исключение с полями

```python
class ValidationError(Exception):
    def __init__(self, errors):
        self.errors = errors
        super().__init__(f"Ошибки валидации: {errors}")

def validate_user(data):
    errors = []
    if not data.get("name", "").strip():
        errors.append("name пустой")
    if not isinstance(data.get("age"), int):
        errors.append("age не int")
    elif data["age"] < 0:
        errors.append("age отрицательный")
    if errors:
        raise ValidationError(errors)
    return True

for test in [{"name": "Anna", "age": 25}, {"name": "", "age": "x"}]:
    try:
        validate_user(test)
        print(f"{test} → OK")
    except ValidationError as e:
        print(f"{test} → {e.errors}")
```

**Вывод консоли:**

```
{'name': 'Anna', 'age': 25} → OK
{'name': '', 'age': 'x'} → ['name пустой', 'age не int']
```

---

### Пример 20: try/finally без except — гарантированная очистка

```python
def process_file(path):
    f = None
    try:
        f = open(path, "w", encoding="utf-8")
        f.write("данные\n")
        print("Записано")
    finally:
        if f:
            f.close()
            print("Файл закрыт")

process_file("temp_finally.txt")
```

**Вывод консоли:**

```
Записано
Файл закрыт
```

*(С `with` проще — глава 8)*

---

### Пример 21: Обработка при чтении JSON-файла

```python
import json
from pathlib import Path

def load_config(path):
    try:
        with Path(path).open("r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        print(f"Конфиг {path} не найден — используем defaults")
        return {"theme": "light"}
    except json.JSONDecodeError as e:
        print(f"Битый JSON в {path}: {e}")
        return {"theme": "light"}

Path("good.json").write_text('{"theme":"dark"}', encoding="utf-8")
Path("bad.json").write_text("{broken", encoding="utf-8")

print(load_config("good.json"))
print(load_config("missing.json"))
print(load_config("bad.json"))
```

**Вывод консоли:**

```
{'theme': 'dark'}
Конфиг missing.json не найден — используем defaults
{'theme': 'light'}
Битый JSON в bad.json: ...
{'theme': 'light'}
```

---

### Пример 22: raise из except — преобразование ошибки

```python
def load_age_from_file(path):
    from pathlib import Path
    try:
        text = Path(path).read_text(encoding="utf-8").strip()
        return int(text)
    except FileNotFoundError:
        raise ValueError(f"Файл возраста не найден: {path}")
    except ValueError:
        raise ValueError(f"Файл {path} не содержит целое число")

Path("age.txt").write_text("25", encoding="utf-8")

try:
    print(load_age_from_file("age.txt"))
    load_age_from_file("no_age.txt")
except ValueError as e:
    print(f"Ошибка: {e}")
```

**Вывод консоли:**

```
25
Ошибка: Файл возраста не найден: no_age.txt
```

---

### Пример 23: TypeError при неверных аргументах

```python
def greet(name, age):
    if not isinstance(name, str):
        raise TypeError("name должен быть str")
    if not isinstance(age, int):
        raise TypeError("age должен быть int")
    print(f"{name}, {age} лет")

greet("Anna", 25)

try:
    greet(123, 25)
except TypeError as e:
    print(e)
```

**Вывод консоли:**

```
Anna, 25 лет
name должен быть str
```

---

### Пример 24: Обработка списка операций — не останавливаться на первой ошибке

```python
def process_all(items):
    results = []
    errors = []
    for i, item in enumerate(items):
        try:
            value = int(item)
            results.append(value * 2)
        except ValueError as e:
            errors.append((i, item, str(e)))
    return results, errors

data = ["10", "abc", "20", "3.14", "30"]
results, errors = process_all(data)
print("Результаты:", results)
print("Ошибки:", errors)
```

**Вывод консоли:**

```
Результаты: [20, 40, 60]
Ошибки: [(1, 'abc', "..."), (3, '3.14', "...")]
```

---

### Пример 25: Мини-проект — банкомат с исключениями

```python
class InsufficientFundsError(Exception):
    pass

class InvalidAmountError(Exception):
    pass

class BankAccount:
    def __init__(self, balance=0):
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise InvalidAmountError("Сумма депозита должна быть > 0")
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if amount <= 0:
            raise InvalidAmountError("Сумма снятия должна быть > 0")
        if amount > self.balance:
            raise InsufficientFundsError(
                f"Баланс {self.balance}, запрошено {amount}"
            )
        self.balance -= amount
        return self.balance

account = BankAccount(1000)

operations = [
    ("deposit", 500),
    ("withdraw", 200),
    ("withdraw", 2000),
    ("deposit", -100),
]

for op, amount in operations:
    try:
        if op == "deposit":
            account.deposit(amount)
        else:
            account.withdraw(amount)
        print(f"  {op} {amount}: OK, баланс = {account.balance}")
    except (InsufficientFundsError, InvalidAmountError) as e:
        print(f"  {op} {amount}: ОШИБКА — {e}")
```

**Вывод консоли:**

```
  deposit 500: OK, баланс = 1500
  withdraw 200: OK, баланс = 1300
  withdraw 2000: ОШИБКА — Баланс 1300, запрошено 2000
  deposit -100: ОШИБКА — Сумма депозита должна быть > 0
```

---

### Пример 26: Декоратор-обработчик (идея, глава 14)

```python
def catch_errors(default=None):
    def decorator(func):
        def wrapper(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                print(f"Ошибка в {func.__name__}: {e}")
                return default
        return wrapper
    return decorator

@catch_errors(default=0)
def risky_calc(x, y):
    return x / y

print(risky_calc(10, 2))
print(risky_calc(10, 0))
```

**Вывод консоли:**

```
5.0
Ошибка в risky_calc: division by zero
0
```

---

### Пример 27: traceback — разбор для пользователя

```python
def level3():
    return 1 / 0

def level2():
    return level3()

def level1():
    return level2()

try:
    level1()
except ZeroDivisionError:
    print("Пользователю: произошла ошибка расчёта. Обратитесь в поддержку.")
    import traceback
    print("\n--- Для разработчика ---")
    traceback.print_exc()
```

**Вывод консоли (сокращённо):**

```
Пользователю: произошла ошибка расчёта. Обратитесь в поддержку.

--- Для разработчика ---
Traceback (most recent call last):
  ...
ZeroDivisionError: division by zero
```

---

### Пример 28: Полный пайплайн — ввод → валидация → сохранение

```python
import json
from pathlib import Path

class UserInputError(Exception):
    pass

def parse_user_input(name, age_str):
    if not name.strip():
        raise UserInputError("Имя не может быть пустым")
    try:
        age = int(age_str)
    except ValueError:
        raise UserInputError(f"Возраст '{age_str}' — не число")
    if age < 0 or age > 150:
        raise UserInputError(f"Возраст {age} вне диапазона 0-150")
    return {"name": name.strip(), "age": age}

def save_user(user, path="users.json"):
    users = []
    p = Path(path)
    if p.exists():
        try:
            users = json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            users = []
    users.append(user)
    p.write_text(json.dumps(users, ensure_ascii=False, indent=2), encoding="utf-8")

test_inputs = [
    ("Anna", "25"),
    ("", "30"),
    ("Bob", "abc"),
    ("Vika", "200"),
]

for name, age in test_inputs:
    try:
        user = parse_user_input(name, age)
        save_user(user)
        print(f"  Сохранено: {user}")
    except UserInputError as e:
        print(f"  Отклонено ({name!r}, {age!r}): {e}")

print("\nИтог users.json:")
print(Path("users.json").read_text(encoding="utf-8"))
```

**Вывод консоли:**

```
  Сохранено: {'name': 'Anna', 'age': 25}
  Отклонено ('', '30'): Имя не может быть пустым
  Отклонено ('Bob', 'abc'): Возраст 'abc' — не число
  Отклонено ('Vika', '200'): Возраст 200 вне диапазона 0-150

Итог users.json:
[
  {
    "name": "Anna",
    "age": 25
  }
]
```

---

## Шпаргалка

```python
try:
    risky()
except SpecificError as e:
    handle(e)
except (Error1, Error2):
    ...
else:
    on_success()
finally:
    cleanup()

raise ValueError("сообщение")
raise CustomError("...") from original

class MyError(Exception):
    pass

# Частые типы
# ValueError, TypeError, KeyError, IndexError
# FileNotFoundError, ZeroDivisionError
# json.JSONDecodeError
```

---

## FAQ начинающего

**В: except без типа?**  
`except Exception:` — широко. `except ValueError:` — точечно. Голый `except:` — никогда.

**В: else обязателен?**  
Нет. Используй когда логика «если успех — сделай X».

**В: finally vs with?**  
`with` для файлов. `finally` — любая очистка (закрыть соединение, сбросить флаг).

**В: Свои исключения — когда?**  
Бизнес-логика: недостаточно средств, невалидный заказ, пользователь забанен.

**В: try на весь main?**  
Антипаттерн. Лови локально, где можешь **осмысленно** обработать.

**В: Как пробросить дальше?**  
`raise` без аргумента внутри `except`.

**В: assert vs raise?**  
`assert` — отладка. `raise` — реальные ошибки для пользователя/вызывающего кода.

---

### Частые баги

```python
# БАГ
except:
    pass

# БАГ — слишком широко без логирования
except Exception:
    return None

# FIX
except ValueError as e:
    logger.error(e)
    return None
```

---

## Домашнее задание

**Файл:** `homework_09.py`

### Задача 1 — Лёгкая
Напиши `safe_int(text)` → `int` или `None` при `ValueError`.

---

### Задача 2 — Лёгкая
Напиши `safe_divide(a, b)` — обработай `ZeroDivisionError` и `TypeError`.

---

### Задача 3 — Средняя
Напиши `read_lines_safe(path)` → list строк или `[]` при `FileNotFoundError`.

<details>
<summary>Подсказка</summary>

```python
try:
    with open(path, encoding="utf-8") as f:
        return [line.strip() for line in f]
except FileNotFoundError:
    return []
```

</details>

---

### Задача 4 — Средняя
Напиши `get_dict_value(d, key, default)` — через `try/except KeyError` **и** через `.get()`. Покажи, что результаты одинаковые.

---

### Задача 5 — Средняя
Создай `InvalidEmailError(Exception)`. Функция `validate_email(email)`:
- нет `@` → raise
- нет `.` после `@` → raise
- иначе OK

Протестируй 4 примера.

---

### Задача 6 — Сложная
**Калькулятор с обработкой.** Функция `calculate(expr)` где expr — строка `"10 / 2"`:
- split на 3 части
- обработай `ZeroDivisionError`, `ValueError` (не число), неверный формат
- возвращай `(result, error_message)` — один из них `None`

---

### Задача 7 — Сложная
**Загрузчик пользователей из JSON.** `load_users(path)`:
- файла нет → `[]` + предупреждение
- битый JSON → `[]` + предупреждение
- не list → `[]` + предупреждение
- иначе → list

Создай 4 тестовых файла, протестируй все случаи.

---

### Задача 8 — Сложная
**Банковский перевод.** Классы `InsufficientFundsError`, `AccountNotFoundError`.  
`transfer(accounts, from_id, to_id, amount)` где `accounts` — dict `id → balance`.  
Обработай все ошибки, верни `(success: bool, message: str)`.

---

### Задача 9 — Сложная (бонус) ⏳ ПОСЛЕ ГЛАВЫ 14

> **Не делай сейчас**, если ещё не прошёл **главу 14 (декораторы)**.  
> Декораторы — синтаксис `@retry`, который здесь только намекают (Пример 26).

**Retry-декоратор.** `retry(max_attempts=3)` — повторяет функцию при `ConnectionError` до 3 раз.

**Файл:** `homework_09.py` — блок «ЗАДАЧА 9 — ПОСЛЕ ГЛАВЫ 14».

<details>
<summary>Подсказка (после гл. 14)</summary>

См. главу 14, Пример 10 (retry) + `functools.wraps`.

</details>

---

### Задача 10 — Сложная (бонус)
**Меню с полной обработкой.** Программа читает JSON-базу товаров, меню: добавить / удалить / показать / выход.  
Обработай: битый JSON, неверный ввод, отсутствующий id, `KeyboardInterrupt` (Ctrl+C) — вежливое прощание.

---

### Как сдавать

- `homework_09.py`
- Задачи 5–10 — с тестами и выводом
- Частями: 1–5, 6–10

**Критерии:**
- Конкретные типы в `except`, не голый `except`
- Информативные сообщения в `raise`
- Не глотать ошибки через `pass`
- Свои исключения наследуют `Exception`

---

**Сделай задачи сам и пришли код на проверку. После проверки — Глава 10: *Модули, пакеты, `if __name__`, venv, pip*.**

---
Конец главы.