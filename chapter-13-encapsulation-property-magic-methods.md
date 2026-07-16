# Тема: ООП — инкапсуляция, `@property`, магические методы

> **Если после прошлой версии ничего не понял — читай ЭТУ главу сверху вниз.**  
> Здесь сначала **объяснение**, потом **один пример с разбором каждой строки**.  
> Не надо зубрить 45 примеров. Достаточно **3 частей теории + 12 разобранных примеров**.

---

## Что ты должен вынести из главы (цель)

После главы ты понимаешь **три вещи**:

1. **Инкапсуляция** — прячем «настоящие» данные (`_balance`), наружу даём безопасный доступ.
2. **`@property`** — снаружи пишешь `obj.balance` как атрибут, внутри работает метод с проверками.
3. **Магические методы** (`__str__`, `__eq__`, `__len__`…) — Python сам вызывает их, когда ты пишешь `print(obj)`, `a == b`, `len(obj)`.

Если после прочтения можешь ответить на три вопроса в конце каждой части — глава усвоена.

---

# ЧАСТЬ 1. Инкапсуляция

## 1.1. Проблема — зачем вообще что-то прятать?

В главе 11 ты писал так:

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance    # открытое поле
```

И любой код может сделать:

```python
account.balance = -999999    # баланс сломан, никто не проверил
account.balance = "привет"   # теперь это строка, deposit() упадёт
```

**Проблема:** данные и правила живут отдельно. Кто угодно меняет `balance` в обход твоей логики.

**Инкапсуляция** — идея: «внутренности объекта трогаем только через правила, которые мы сами написали».

---

## 1.2. Аналогия из жизни

Представь банкомат.

- Ты **не лезешь** в сейф руками.
- Ты нажимаешь кнопки: «положить», «снять».
- Банкомат **сам проверяет**: хватает ли денег, корректна ли сумма.

В коде:
- **Сейф** = `self._balance` (внутреннее поле)
- **Кнопки** = методы `deposit()`, `withdraw()` или `@property` с проверкой

---

## 1.3. `_` в начале имени — не замок, а табличка «не трогай»

```python
self.balance = 100    # публичное — используй свободно
self._balance = 100   # «внутреннее» — договорённость для программистов
```

Python **не запрещает** писать `account._balance = 0`. Это не Java с `private`.  
Это **сигнал команде**: «меняй только через методы класса».

| Имя | Смысл |
|-----|-------|
| `name` | Можно читать и писать снаружи |
| `_name` | Внутреннее, снаружи не трогай без причины |
| `__name` | Python переименует в `_ClassName__name` (редко на Junior) |

**Запомни:** инкапсуляция в Python = **дисциплина + методы/property**, не железная блокировка.

---

## 1.4. Первый рабочий вариант — методы вместо прямого доступа

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self._balance = balance    # храним тут

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Сумма должна быть > 0")
        self._balance += amount

    def withdraw(self, amount):
        if amount > self._balance:
            raise ValueError("Недостаточно средств")
        self._balance -= amount

    def get_balance(self):
        return self._balance
```

**Что изменилось:**
- Баланс лежит в `_balance`.
- Изменить его можно **только** через `deposit` / `withdraw` — там проверки.
- Снаружи читаем через `get_balance()`.

**Минус:** `get_balance()` выглядит по-старому, как в Java. В Python для чтения используют `@property` — часть 2.

---

### ✅ Проверь себя — часть 1

1. Зачем `_balance`, а не `balance`? → Чтобы показать: поле внутреннее.
2. Можно ли в Python запретить доступ на 100%? → Нет, только соглашение.
3. Где должна быть проверка «сумма > 0»? → В методах, которые меняют `_balance`.

---

# ЧАСТЬ 2. `@property`

## 2.1. Проблема `get_balance()` — некрасиво

```python
print(account.get_balance())    # работает, но многословно
```

Хочется писать как с обычным полем:

```python
print(account.balance)    # короче, привычнее
```

Но **нельзя** просто сделать `self.balance` открытым — снова обойдут проверки.

**Решение:** `@property` — «атрибут, который на самом деле метод».

---

## 2.2. Как это работает — по шагам

**Шаг 1.** Прячем настоящее поле:

```python
self._balance = 1000
```

**Шаг 2.** Делаем «дверь для чтения»:

```python
@property
def balance(self):
    return self._balance
```

Когда пишешь `account.balance` — Python **не ищет поле** `balance`. Он вызывает метод `balance(self)` и возвращает `_balance`.

**Шаг 3 (опционально).** Делаем «дверь для записи» с проверкой:

```python
@balance.setter
def balance(self, value):
    if value < 0:
        raise ValueError("Баланс не может быть отрицательным")
    self._balance = value
```

Когда пишешь `account.balance = 500` — вызывается этот setter.

---

## 2.3. Полный пример с разбором КАЖДОЙ важной строки

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self._balance = balance       # ← РЕАЛЬНОЕ хранилище денег

    @property
    def balance(self):
        # ← вызывается при account.balance (чтение)
        return self._balance

    @balance.setter
    def balance(self, value):
        # ← вызывается при account.balance = value (запись)
        if value < 0:
            raise ValueError("Баланс не может быть отрицательным")
        self._balance = value         # ← пишем в _balance, НЕ в self.balance!

    def deposit(self, amount):
        self._balance += amount       # ← меняем напрямую _balance внутри класса — OK
```

```python
account = BankAccount("Anna", 1000)
print(account.balance)        # → вызов getter → 1000
account.balance = 1500        # → вызов setter → _balance = 1500
# account.balance = -100    # → setter кинет ValueError
```

**Критически важно — не делай так в setter:**

```python
self.balance = value    # ОШИБКА! setter вызовет сам себя → бесконечная рекурсия
self._balance = value   # ПРАВИЛЬНО
```

---

## 2.4. Read-only property — только читать, нельзя присвоить

Иногда значение **считается**, а не хранится:

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def area(self):
        return 3.14159 * self._radius ** 2
```

- `circle.area` — работает (getter есть).
- `circle.area = 100` — **ошибка** `can't set attribute` (setter нет).

**Когда использовать:** `full_name`, `is_adult`, `area`, `total` — всё, что **вычисляется** из других полей.

---

## 2.5. Порядок написания property

Всегда в таком порядке:

```python
@property
def name(self):
    ...

@name.setter
def name(self, value):
    ...
```

Сначала getter (`@property`), потом setter (`@имя.setter`). Имя **одинаковое**.

---

### ✅ Проверь себя — часть 2

1. `account.balance` — это поле или метод? → Метод (getter), просто выглядит как поле.
2. Куда писать в setter — `self.balance` или `self._balance`? → `_balance`.
3. Как сделать свойство только для чтения? → `@property` без `@...setter`.

---

# ЧАСТЬ 3. Магические методы (dunder)

## 3.1. Что это такое — без магии

**Dunder** = **d**ouble **under**score (`__`).

Это методы с именами `__что_то__`. Ты их **не вызываешь напрямую** в обычном коде.  
Python вызывает **сам**, когда видит операцию:

```
Ты написал          Python сделал внутри
──────────          ──────────────────
print(obj)       →  obj.__str__()
a == b           →  a.__eq__(b)
len(obj)         →  obj.__len__()
obj[0]           →  obj.__getitem__(0)
for x in obj     →  obj.__iter__()
a + b            →  a.__add__(b)
```

**Зачем:** чтобы твой класс вёл себя как встроенный тип (list, str), а не как «просто объект в памяти».

---

## 3.2. `__str__` — для людей (print)

**Без `__str__`:**

```python
print(account)
# <__main__.BankAccount object at 0x7f8b3c2d4e50>  ← бесполезно
```

**С `__str__`:**

```python
def __str__(self):
    return f"{self.owner}: {self._balance} руб."

print(account)
# Anna: 1300 руб.
```

**Правило:** у каждого класса, который печатаешь — сделай `__str__`.

---

## 3.3. `__repr__` — для разработчика (отладка)

```python
def __repr__(self):
    return f"BankAccount({self.owner!r}, {self._balance})"
```

- `print(repr(account))` → `BankAccount('Anna', 1300)`
- В списке `[account]` Python показывает `__repr__`, не `__str__`.

На Junior: если лень — хотя бы `__str__`. Лучше оба.

---

## 3.4. `__eq__` — осмысленное сравнение `==`

По умолчанию `==` сравнивает **один ли это объект в памяти** (`is`).  
Обычно нужно сравнивать **содержимое**:

```python
def __eq__(self, other):
    if not isinstance(other, Point):
        return NotImplemented    # «я не знаю, спроси other»
    return self.x == other.x and self.y == other.y
```

```python
a = Point(1, 2)
b = Point(1, 2)
print(a == b)    # True — одинаковые координаты
print(a is b)    # False — разные объекты в памяти
```

---

## 3.5. `__len__`, `__bool__`, `__contains__` — как у коллекций

Если твой класс **хранит список чего-то** (плейлист, корзина, очередь):

```python
def __len__(self):
    return len(self._items)      # len(playlist)

def __bool__(self):
    return len(self._items) > 0    # if playlist:

def __contains__(self, item):
    return item in self._items     # "song" in playlist
```

Без этих методов `len(playlist)` просто **упадёт с ошибкой**.

---

## 3.6. `__getitem__` и `__iter__` — индекс и цикл

```python
def __getitem__(self, index):
    return self._items[index]      # playlist[0]

def __iter__(self):
    return iter(self._items)       # for song in playlist:
```

Твой класс начинает **ощущаться как list** — но с твоей логикой внутри.

---

## 3.7. `__add__` — оператор `+`

```python
def __add__(self, other):
    return Vector(self.x + other.x, self.y + other.y)
```

```python
v3 = v1 + v2    # Python вызывает v1.__add__(v2)
```

Нужен только если «сложение объектов» имеет смысл (векторы, деньги с одной валютой).

---

## 3.8. Какие dunder учить первым — не всё сразу

| Приоритет | Метод | Зачем |
|-----------|-------|-------|
| 1 | `__str__` | Нормальный print |
| 2 | `__eq__` | Сравнение объектов |
| 3 | `__len__`, `__iter__` | Если класс — «контейнер» |
| 4 | `__getitem__` | Если нужен `obj[i]` |
| 5 | `__add__` | Если нужен `a + b` |
| 6 | `__bool__` | Если нужен `if obj:` |

**Не надо** писать все 20 методов в каждый класс. Только те, что реально используешь.

---

### ✅ Проверь себя — часть 3

1. Кто вызывает `__str__`? → Python, когда ты `print(obj)`.
2. `a == b` вызывает какой метод? → `a.__eq__(b)`.
3. Нужен ли `__len__` в классе `Dog`? → Нет, если Dog — не контейнер.

---

# Практика — 12 примеров С РАЗБОРОМ

> Каждый пример: **код → что выведет → что происходит построчно**.

---

## Пример 1. Инкапсуляция через `_` и методы

```python
class Wallet:
    def __init__(self, balance):
        self._balance = balance

    def deposit(self, amount):
        self._balance += amount

    def get_balance(self):
        return self._balance

wallet = Wallet(100)
wallet.deposit(50)
print(wallet.get_balance())
```

**Вывод:** `150`

**Разбор:**
- `__init__` кладёт деньги в `_balance`.
- `deposit` меняет `_balance` только через метод — тут можно добавить проверки.
- Снаружи не пишем `wallet._balance += 50` (хотя технически можно) — пишем `deposit(50)`.

---

## Пример 2. `@property` — чтение без скобок

```python
class Person:
    def __init__(self, first, last):
        self.first = first
        self.last = last

    @property
    def full_name(self):
        return f"{self.first} {self.last}"

p = Person("Anna", "Ivanova")
print(p.full_name)
```

**Вывод:** `Anna Ivanova`

**Разбор:**
- `p.full_name` — **без скобок**, но это вызов метода `full_name(self)`.
- Каждый раз собирается из `first` и `last`. Отдельного поля `full_name` нет.

---

## Пример 3. Setter с валидацией

```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius    # вызовет setter!

    @property
    def celsius(self):
        return self._celsius

    @celsius.setter
    def celsius(self, value):
        if value < -273.15:
            raise ValueError("Ниже абсолютного нуля!")
        self._celsius = value

t = Temperature(25)
print(t.celsius)
t.celsius = 30
print(t.celsius)
```

**Вывод:**
```
25
30
```

**Разбор:**
- В `__init__` пишем `self.celsius = celsius` — это **не** прямое поле, а вызов **setter**.
- Setter проверяет значение **до** записи в `_celsius`.
- Читаем через `t.celsius` — вызывается **getter**.

---

## Пример 4. Ошибка — рекурсия в setter (ОБЯЗАТЕЛЬНО ПРОЧИТАЙ)

```python
class Bad:
    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, v):
        self.value = v    # БАГ!
```

**Что произойдёт:** `RecursionError: maximum recursion depth exceeded`

**Почему:**
1. Пишешь `self.value = v`
2. Python вызывает setter
3. Setter снова пишет `self.value = v`
4. Снова setter → бесконечность

**Фикс:** `self._value = v`

---

## Пример 5. Read-only `area`

```python
class Circle:
    def __init__(self, radius):
        self._radius = radius

    @property
    def area(self):
        return 3.14159 * self._radius ** 2

c = Circle(5)
print(f"{c.area:.2f}")
```

**Вывод:** `78.54`

**Разбор:**
- `area` нет в `__init__` — оно **вычисляется** при каждом обращении.
- Setter для `area` не определён → присвоить нельзя.

---

## Пример 6. `__str__` — человекочитаемый print

```python
class Book:
    def __init__(self, title, price):
        self.title = title
        self.price = price

    def __str__(self):
        return f"{self.title} — {self.price} руб."

book = Book("1984", 500)
print(book)
```

**Вывод:** `1984 — 500 руб.`

**Разбор:**
- `print(book)` не печатает адрес в памяти.
- Python ищет `book.__str__()` и печатает результат.

---

## Пример 7. `__eq__` — сравнение по смыслу

```python
class Point:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __eq__(self, other):
        if not isinstance(other, Point):
            return NotImplemented
        return self.x == other.x and self.y == other.y

a = Point(1, 2)
b = Point(1, 2)
print(a == b)
print(a is b)
```

**Вывод:**
```
True
False
```

**Разбор:**
- `==` сравнивает координаты (логика в `__eq__`).
- `is` проверяет, один ли объект в памяти — тут разные объекты.

---

## Пример 8. `__lt__` — сортировка

```python
class Student:
    def __init__(self, name, grade):
        self.name = name
        self.grade = grade

    def __lt__(self, other):
        return self.grade < other.grade

    def __str__(self):
        return f"{self.name} ({self.grade})"

students = [Student("Bob", 4), Student("Anna", 5)]
for s in sorted(students):
    print(s)
```

**Вывод:**
```
Bob (4)
Anna (5)
```

**Разбор:**
- `sorted()` сравнивает пары через `<` → вызывает `__lt__`.
- Anna с оценкой 5 идёт после Bob с 4 — подождите, 4 < 5, Bob первый. Верно.

---

## Пример 9. Контейнер — `__len__`, `__contains__`, `__iter__`

```python
class Playlist:
    def __init__(self):
        self._tracks = []

    def add(self, track):
        self._tracks.append(track)

    def __len__(self):
        return len(self._tracks)

    def __contains__(self, track):
        return track in self._tracks

    def __iter__(self):
        return iter(self._tracks)

pl = Playlist()
pl.add("Song A")
pl.add("Song B")
print(len(pl))
print("Song A" in pl)
for t in pl:
    print(t)
```

**Вывод:**
```
2
True
Song A
Song B
```

**Разбор:**
- `len(pl)` → `__len__`
- `"Song A" in pl` → `__contains__`
- `for t in pl` → `__iter__`
- Внутри всё равно обычный list `_tracks`.

---

## Пример 10. `__getitem__` — доступ по индексу

```python
class SimpleList:
    def __init__(self):
        self._data = []

    def append(self, x):
        self._data.append(x)

    def __getitem__(self, index):
        return self._data[index]

    def __len__(self):
        return len(self._data)

lst = SimpleList()
lst.append(10)
lst.append(20)
print(lst[1])
print(len(lst))
```

**Вывод:**
```
20
2
```

**Разбор:**
- `lst[1]` выглядит как list, но это твой класс.
- Python вызывает `lst.__getitem__(1)`.

---

## Пример 11. `__add__` — сложение векторов

```python
class Vector:
    def __init__(self, x, y):
        self.x, self.y = x, y

    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y)

    def __str__(self):
        return f"({self.x}, {self.y})"

v = Vector(1, 2) + Vector(3, 4)
print(v)
```

**Вывод:** `(4, 6)`

**Разбор:**
- `Vector(1,2) + Vector(3,4)` → первый вектор вызывает `__add__(второй)`.
- Возвращается **новый** Vector, исходные не меняются.

---

## Пример 12. Всё вместе — банковский счёт

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self._balance = balance

    @property
    def balance(self):
        return self._balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Сумма > 0")
        self._balance += amount

    def withdraw(self, amount):
        if amount > self._balance:
            raise ValueError("Недостаточно средств")
        self._balance -= amount

    def __str__(self):
        return f"{self.owner}: {self.balance} руб."

    def __eq__(self, other):
        if not isinstance(other, BankAccount):
            return NotImplemented
        return self.owner == other.owner

    def __bool__(self):
        return self.balance > 0

account = BankAccount("Anna", 1000)
account.deposit(500)
account.withdraw(200)
print(account)
print("Активен:", bool(account))
```

**Вывод:**
```
Anna: 1300 руб.
Активен: True
```

**Разбор по частям:**
- `_balance` + `deposit`/`withdraw` — инкапсуляция, нельзя накрутить баланс с минусом через методы.
- `@property balance` — читаем баланс красиво, setter **не даём** (менять только через методы).
- `__str__` — нормальный print.
- `__bool__` — `if account:` True, если деньги есть.

**Это образец** того, как должен выглядеть «взрослый» класс на Junior.

---

# Шпаргалка на одну страницу

```python
# Инкапсуляция
self._balance = 0           # внутреннее поле

# Property
@property
def balance(self):
    return self._balance

@balance.setter
def balance(self, value):
    self._balance = value   # НЕ self.balance!

# Dunder
def __str__(self): ...      # print(obj)
def __eq__(self, other): ...# obj == other
def __len__(self): ...      # len(obj)
def __iter__(self): ...     # for x in obj
def __getitem__(self, i): ...# obj[i]
def __add__(self, other): ...# obj + other
```

---

# FAQ — короткие ответы

**Инкапсуляция в Python = private в Java?**  
Нет. Это соглашение `_` + контроль через методы/property.

**Зачем property, если есть метод?**  
`obj.balance` читается проще, чем `obj.get_balance()`.

**setter обязателен?**  
Нет. Без setter — только чтение.

**Все dunder обязательны?**  
Нет. Только нужные. Минимум — `__str__`.

**`==` и `is`?**  
`==` → `__eq__` (значение). `is` → один объект в памяти.

---

# Домашнее задание

**Тема:** инкапсуляция, `@property`, магические методы.

**Файл для сдачи:** `homework_13.py` (создай сам или допиши свой).

**Как делать:** одна задача = один блок в файле. В конце каждой задачи — `print`, чтобы я видел результат. Сдавай можно частями: 1–3, потом 4–6.

---

## Задача 1. Прямоугольник и площадь (`@property`)

**Тема:** read-only property — свойство только для чтения.

Напиши класс `Rectangle`. Ширина и высота хранятся в `self._width` и `self._height`. Сделай свойство `area` через `@property`: при обращении `rect.area` возвращается площадь (ширина × высота). Setter для `area` не нужен.

В конце создай `Rectangle(4, 5)` и выведи площадь.

**Должно получиться:**
```
20
```

**Подсказка:** смотри Пример 5 в главе.

---

## Задача 2. Человек и полное имя (`@property`)

**Тема:** вычисляемое свойство.

Напиши класс `Person` с полями `first` и `last`. Добавь `@property full_name`, который возвращает имя и фамилию через пробел.

Создай `Person("Anna", "Ivanova")` и выведи `full_name` (без скобок — это свойство, не метод).

**Должно получиться:**
```
Anna Ivanova
```

**Подсказка:** смотри Пример 2 в главе.

---

## Задача 3. Температура (`@property` + setter)

**Тема:** чтение и запись с проверкой.

Напиши класс `Temperature`:
- внутри храни градусы в `self._celsius`;
- `celsius` — property с getter и setter; в setter если значение меньше -273.15, выбрось `ValueError`;
- `fahrenheit` — property только для чтения, формула: `celsius * 9/5 + 32`.

Проверь в коде:
1. `Temperature(0)` — выведи celsius и fahrenheit;
2. поставь `celsius = 100`, выведи снова;
3. попробуй `celsius = -300` в `try/except` и выведи текст ошибки.

**Должно получиться (примерно):**
```
0 32.0
100 212.0
Ошибка: ...
```

**Важно:** в setter пиши `self._celsius = value`, не `self.celsius = value`.

**Подсказка:** смотри Пример 3 в главе.

---

## Задача 4. Банковский счёт (инкапсуляция + `__str__`)

**Тема:** прячем баланс, меняем только через методы.

Напиши класс `BankAccount`:
- `owner` — имя владельца;
- деньги в `self._balance`, снаружи не трогаем;
- `balance` — `@property` только для чтения (без setter);
- `deposit(amount)` — прибавляет к балансу;
- `withdraw(amount)` — если денег не хватает, `raise ValueError("Недостаточно средств")`, иначе вычитает;
- `__str__` — строка вида `Anna: 1300 руб.`

Проверь: счёт Anna с 1000, положи 500, сними 200, выведи `print(account)`.

**Должно получиться:**
```
Anna: 1300 руб.
```

**Подсказка:** смотри Пример 12 в главе.

---

## Задача 5. Точка и сравнение (`__eq__` + `__str__`)

**Тема:** магические методы для `print` и `==`.

Напиши класс `Point` с координатами `x` и `y`:
- `__str__` возвращает строку вида `(1, 2)`;
- `__eq__` сравнивает две точки по координатам; если сравниваешь не с `Point`, верни `NotImplemented`.

Создай `a = Point(1, 2)`, `b = Point(1, 2)`, `c = Point(3, 4)`. Выведи `a == b`, `a == c`, `a is b`.

**Должно получиться:**
```
True
False
False
```

**Подсказка:** смотри Пример 7 в главе.

---

## Задача 6. Плейлист (`__len__`, `__iter__`, `__str__`)

**Тема:** класс ведёт себя как список треков.

Напиши класс `Playlist`:
- при создании принимает `name` и пустой список `self._tracks`;
- метод `add(track)` добавляет название трека;
- `__len__` — сколько треков;
- `__iter__` — чтобы работал `for track in playlist`;
- `__str__` — например `Мои (2 трека)`.

Добавь два трека, выведи `len(playlist)`, затем `print(playlist)`, затем в цикле каждый трек.

**Должно получиться:**
```
2
Мои (2 трека)
Song A
Song B
```

**Подсказка:** смотри Пример 9 в главе.

---

## Бонус (не обязательно)

**Задача 7.** `Vector` с `__add__` и `__str__`: сложи `(1,2)` и `(3,4)`, выведи `(4, 6)`.

**Задача 8.** `User(email)` — setter проверяет наличие `@`, `domain` — read-only property с частью после `@`.

---

## Как сдать

1. Файл `homework_13.py`.
2. Запускается командой `python homework_13.py` без ошибок.
3. Пришли код сюда — проверю и напишу, что исправить.

Если непонятна **конкретная** задача — напиши номер, разберём.

---

# Итог — три предложения

1. **Прячь данные** в `_поле`, меняй через методы или setter с проверкой.
2. **`@property`** — чтобы читать (и иногда писать) как атрибут, а не `get_*()`.
3. **Dunder-методы** — чтобы `print`, `==`, `len`, `for` работали с твоим классом как с нормальным типом.

---

**Сделай задачи 1–3 и пришли `homework_13.py` — проверю.**

---

> **Мостик в гл. 14:** `@property` — это **встроенный декоратор**. Символ `@` и обёртки функций — разбираем в **следующей главе**.

---
Конец главы.