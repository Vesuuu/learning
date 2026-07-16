# Тема: ООП — классы и объекты

> **Файл для кода:** `homework_11.py`  
> **Мостик:** `_поля` и `@property` — **подробно в главе 13**. Символ `@` — это декоратор, механизм в **главе 14**.  
> **Маршрут:** для домашки 1–5 достаточно примеров **1–12**; остальные — углубление.

## Теория

### Что это такое

До сих пор ты описывал данные **отдельно** от логики:

```python
user_name = "Anna"
user_age = 25

def greet_user(name):
    print(f"Привет, {name}!")
```

**ООП (объектно-ориентированное программирование)** объединяет **данные** и **поведение** в одну сущность — **объект**.

**Класс (class)** — чертёж, шаблон.  
**Объект (object)** / **экземпляр (instance)** — конкретная «вещь», созданная по чертежу.

```python
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        print(f"Привет, я {self.name}, мне {self.age}")

anna = User("Anna", 25)    # объект / экземпляр
anna.greet()
```

Аналогия: **класс** = чертёж дома, **объект** = конкретный построенный дом.

---

### Связь с предыдущими главами

| Глава | Без ООП | С ООП |
|-------|---------|-------|
| 4 | `{"name": "Anna", "age": 25}` | `User("Anna", 25)` |
| 5 | Мутабельный dict, ссылки | Атрибуты объекта `self.name` |
| 6 | Функции `deposit(balance, amount)` | Метод `account.deposit(amount)` |
| 9 | `raise ValueError` в функции | `raise ValueError` в `__init__` |
| 10 | `class Book` в `models.py` | Теперь разбираем **как** это устроено |

**Когда ООП уместно:**
- Есть **сущности** с состоянием и действиями (пользователь, заказ, счёт, задача)
- Несколько «штук» одного типа с разными данными
- Код проекта растёт — классы группируют логику

**Когда достаточно функций:**
- Один скрипт на 30 строк
- Чистые преобразования данных без «живых» сущностей

---

### Класс и объект — синтаксис

```python
class Cat:
    pass    # пустой класс — заглушка

fluffy = Cat()    # создание объекта — вызов класса как функции
print(type(fluffy))    # <class '__main__.Cat'>
print(isinstance(fluffy, Cat))    # True
```

**Именование (PEP 8):** классы — `CapWords` (CamelCase): `BankAccount`, `UserProfile`, `TodoItem`.

---

### `__init__` — конструктор (инициализация)

```python
class Dog:
    def __init__(self, name, breed):
        self.name = name
        self.breed = breed

rex = Dog("Rex", "овчарка")
print(rex.name)
```

`__init__` вызывается **автоматически** при создании объекта: `Dog("Rex", "овчарка")`.

**Не путай:** `__init__` **настраивает** объект, но **создание** объекта делает Python внутренне (`__new__` — за рамками Junior).

---

### `self` — ссылка на текущий объект

```python
class Dog:
    def __init__(self, name):
        self.name = name    # атрибут экземпляра

    def bark(self):
        print(f"{self.name}: Гав!")
```

- `self` — **первый параметр** каждого метода экземпляра
- Через `self` метод обращается к **данным этого объекта**
- При вызове `rex.bark()` Python подставляет `rex` как `self` автоматически

```python
rex = Dog("Rex")
rex.bark()           # Rex: Гав!
Dog.bark(rex)        # то же самое — редко так пишут
```

**`self` — соглашение**, можно назвать иначе, но **всегда** пиши `self`.

---

### Атрибуты экземпляра

```python
class User:
    def __init__(self, name):
        self.name = name
        self.is_active = True

user = User("Anna")
user.name = "Ann"           # изменить
user.email = "a@mail.com"   # добавить новый атрибут
print(user.name, user.is_active)
```

Атрибуты — как «переменные, привязанные к объекту». У каждого экземпляра — **свои** значения.

```python
a = User("Anna")
b = User("Bob")
a.is_active = False
print(b.is_active)    # True — b не затронут
```

---

### Методы — функции внутри класса

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Недостаточно средств")
        self.balance -= amount
        return self.balance

    def info(self):
        return f"{self.owner}: {self.balance} руб."
```

**Вызов:** `account.deposit(500)` — метод получает `self` = `account`.

---

### Атрибут класса vs атрибут экземпляра

```python
class Dog:
    species = "Canis familiaris"    # атрибут КЛАССА — общий для всех

    def __init__(self, name):
        self.name = name            # атрибут ЭКЗЕМПЛЯРА — у каждого свой
```

| Тип | Где объявлен | Кому принадлежит |
|-----|--------------|------------------|
| Атрибут класса | В теле класса, до `__init__` | Всем экземплярам |
| Атрибут экземпляра | В `__init__` через `self.` | Одному объекту |

```python
rex = Dog("Rex")
print(rex.species)    # Canis familiaris
print(Dog.species)    # то же — через класс
```

**Ловушка:** изменение **мутабельного** атрибута класса (list, dict) затрагивает всех:

```python
class Team:
    members = []    # ОПАСНО — один list на всех!

# Лучше в __init__:
class Team:
    def __init__(self):
        self.members = []
```

---

### `__str__` и `__repr__` — строковое представление

```python
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def __str__(self):
        return f"User({self.name}, {self.age})"

    def __repr__(self):
        return f"User(name={self.name!r}, age={self.age})"

user = User("Anna", 25)
print(user)           # User(Anna, 25) — вызывает __str__
print(repr(user))     # User(name='Anna', age=25)
```

| Метод | Для кого | Цель |
|-------|----------|------|
| `__str__` | `print()`, `str()` | Читаемо для человека |
| `__repr__` | консоль, отладка | Однозначно для разработчика |

На Junior: реализуй хотя бы `__str__` в своих классах.

---

### `isinstance` и `type`

```python
class Cat:
    pass

fluffy = Cat()

print(type(fluffy))              # <class '__main__.Cat'>
print(type(fluffy) == Cat)       # True
print(isinstance(fluffy, Cat))   # True — предпочтительнее
```

`isinstance` учитывает **наследование** (глава 12). Для проверки типа — `isinstance`, не `type(x) == Class`.

---

### Процедурный стиль vs ООП — рефакторинг

**Процедурно:**

```python
def create_user(name, age):
    return {"name": name, "age": age}

def greet(user):
    print(f"Привет, {user['name']}")
```

**ООП:**

```python
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        print(f"Привет, {self.name}")
```

Оба варианта рабочие. ООП удобнее, когда сущностей много и у каждой — свои методы.

---

### «Приватные» атрибуты — соглашение `_`

Python **не** скрывает атрибуты жёстко. Соглашение:

```python
class BankAccount:
    def __init__(self, balance):
        self._balance = balance    # «внутренний» — не трогай снаружи

    def get_balance(self):
        return self._balance
```

Один `_` — «для внутреннего использования». Два `__` (`__balance`) — name mangling (редко на Junior).

---

### `dataclass` — короткая запись класса данных

Для классов, где главное — **хранить поля**:

```python
from dataclasses import dataclass

@dataclass
class Point:
    x: int
    y: int

p = Point(3, 4)
print(p)    # Point(x=3, y=4) — __repr__ автоматически
```

`dataclass` сам генерирует `__init__`, `__repr__`, `__eq__`. Удобно для моделей данных. Логику методов добавляешь как обычно.

---

### Как это работает «под капотом»

1. `class User:` создаёт **объект-класс** в памяти
2. `User("Anna", 25)` — вызов класса:
   - создаёт пустой объект
   - вызывает `User.__init__(obj, "Anna", 25)`
   - `self` = этот новый объект
3. `self.name = name` — в `obj.__dict__` появляется ключ `"name"`
4. `anna.greet()` — Python ищет `greet` в классе, вызывает с `anna` как `self`

```python
class User:
    def __init__(self, name):
        self.name = name

anna = User("Anna")
print(anna.__dict__)    # {'name': 'Anna'}
```

---

### Где применяется в реальной разработке

| Область | Классы |
|---------|--------|
| Django / Flask | `class User(models.Model)` |
| FastAPI | Pydantic `class UserSchema(BaseModel)` |
| Игры | `class Player`, `class Enemy` |
| Боты | `class BotHandler` |
| Тесты | `class TestLogin` (unittest) |
| ORM | `class Order` ↔ таблица в БД |

На собеседовании Junior спрашивают: класс, объект, `__init__`, `self`, разница атрибутов, `__str__`.

---

### Микро-моменты, нюансы, частые ошибки новичков

#### 1. Забыли `self` в методе

```python
def greet(name):       # БАГ — нет self
    print(self.name)
```

#### 2. Вызов `__init__` вручную — редко нужно

Создавай объект: `User("Anna")`, не `User.__init__(...)`.

#### 3. Мутабельный атрибут класса

```python
class ShoppingCart:
    items = []    # БАГ — общая корзина у всех!
```

#### 4. `self` в `__init__` обязателен

```python
def __init__(name):    # БАГ — нет self
```

#### 5. Путаница класса и экземпляра

```python
Dog.name = "Rex"       # атрибут класса, не экземпляра rex
```

#### 6. Изменение объекта через несколько имён

```python
a = User("Anna")
b = a
b.name = "Ann"
print(a.name)    # Ann — один объект, две ссылки (глава 5!)
```

#### 7. `print(class)` vs `print(instance)`

```python
print(User)       # <class '__main__.User'>
print(user)       # User(Anna, 25) — если есть __str__
```

#### 8. Метод без скобок — не вызов

```python
account.deposit    # <bound method> — функция, не результат
account.deposit(100)    # вызов
```

#### 9. Атрибут до `__init__`

Обращение к `self.name` до присвоения в `__init__` → `AttributeError`.

#### 10. Валидация — в `__init__`

```python
if age < 0:
    raise ValueError("Возраст не может быть отрицательным")
```

#### 11. Не всё надо делать классом

`def celsius_to_fahrenheit(c):` — функция достаточна.

#### 12. `type(x) == list` vs `isinstance(x, list)`

Для встроенных типов — `isinstance`. Для своих классов — тоже `isinstance`.

#### 13. `__dict__` только у обычных объектов

У некоторых встроенных (int, str) нет `__dict__`.

#### 14. Класс внутри функции — редко на Junior

Обычно классы на уровне модуля.

#### 15. Документация класса — docstring

```python
class User:
    """Пользователь системы."""
```

---

## Практика

> Каждый пример: код → вывод → **Разбор** — что произошло и почему.

> **Навигация:** **38 примеров**, шпаргалка, FAQ, домашка.

### Пример 1: Пустой класс и первый объект

```python
class Phone:
    pass

my_phone = Phone()
your_phone = Phone()

print(type(my_phone))
print(my_phone is your_phone)
```

**Вывод консоли:**

```
<class '__main__.Phone'>
False
```

**Разбор:** Вызов `Phone()` создаёт экземпляр класса — объект с типом `Phone`. Два отдельных вызова дают два разных объекта в памяти, поэтому `is` возвращает `False`. Ключевое слово `pass` означает, что в классе пока нет своих методов и атрибутов.

Два вызова `Phone()` — **два разных** объекта.

---

### Пример 2: `__init__` — начальные атрибуты

```python
class Book:
    def __init__(self, title, author, pages):
        self.title = title
        self.author = author
        self.pages = pages

book = Book("1984", "Orwell", 328)
print(book.title, "—", book.author)
print("Страниц:", book.pages)
```

**Вывод консоли:**

```
1984 — Orwell
Страниц: 328
```

**Разбор:** Метод `__init__` вызывается автоматически при создании объекта и записывает данные в `self.title`, `self.author`, `self.pages`. Аргументы `Book("1984", "Orwell", 328)` передаются в конструктор. Атрибуты потом читаются через точку: `book.title`, `book.author`.

---

### Пример 3: Несколько экземпляров — независимые данные

```python
class Cat:
    def __init__(self, name, color):
        self.name = name
        self.color = color

cat1 = Cat("Мурзик", "рыжий")
cat2 = Cat("Барсик", "чёрный")

cat1.name = "Мурка"
print(cat1.name, cat1.color)
print(cat2.name, cat2.color)
```

**Вывод консоли:**

```
Мурка рыжий
Барсик чёрный
```

**Разбор:** У `cat1` и `cat2` свои независимые атрибуты — изменение `cat1.name` не затрагивает `cat2`. Каждый вызов `Cat(...)` создаёт отдельный объект в памяти. Именно поэтому у Мурки и Барсика остаются разные имена и цвета.

---

### Пример 4: Метод экземпляра и `self`

```python
class Greeter:
    def __init__(self, greeting):
        self.greeting = greeting

    def say(self, name):
        print(f"{self.greeting}, {name}!")

en = Greeter("Hello")
ru = Greeter("Привет")

en.say("Anna")
ru.say("Борис")
```

**Вывод консоли:**

```
Hello, Anna!
Привет, Борис!
```

**Разбор:** Метод `say` получает `self` автоматически — через него читает `self.greeting` конкретного объекта. У `en` и `ru` разные приветствия, поэтому вывод разный при одном и том же имени. `self` связывает метод с экземпляром, для которого его вызвали.

---

### Пример 5: Банковский счёт — deposit и withdraw

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Сумма должна быть > 0")
        self.balance += amount

    def withdraw(self, amount):
        if amount > self.balance:
            raise ValueError("Недостаточно средств")
        self.balance -= amount

    def __str__(self):
        return f"Счёт {self.owner}: {self.balance} руб."

account = BankAccount("Anna", 1000)
account.deposit(500)
account.withdraw(200)
print(account)
```

**Вывод консоли:**

```
Счёт Anna: 1300 руб.
```

**Разбор:** Методы `deposit` и `withdraw` меняют `self.balance` внутри одного и того же объекта. Стартовые 1000 + 500 − 200 = 1300 рублей. Метод `__str__` делает `print(account)` читаемым — без него вывелся бы адрес объекта в памяти.

---

### Пример 6: `__str__` — красивый print

```python
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def __str__(self):
        return f"{self.name} — {self.price} руб."

    def __repr__(self):
        return f"Product({self.name!r}, {self.price})"

p = Product("Клавиатура", 3500)
print(p)
print(repr(p))
```

**Вывод консоли:**

```
Клавиатура — 3500 руб.
Product('Клавиатура', 3500)
```

**Разбор:** Метод `__str__` предназначен для пользователя — `print` вызывает его автоматически. `__repr__` даёт однозначное представление для разработчика и срабатывает при `repr(p)`. Оба возвращают строки, но в разном стиле и для разных целей.

---

### Пример 7: Атрибут класса vs экземпляра

```python
class Employee:
    company = "TechCorp"
    count = 0

    def __init__(self, name):
        self.name = name
        Employee.count += 1

e1 = Employee("Anna")
e2 = Employee("Bob")

print(e1.company, e2.company)
print("Сотрудников:", Employee.count)
print("Имя e1:", e1.name)
```

**Вывод консоли:**

```
TechCorp TechCorp
Сотрудников: 2
Имя e1: Anna
```

**Разбор:** Атрибуты `company` и `count` объявлены в теле класса — они общие для всех экземпляров. Каждый новый `Employee(...)` увеличивает `Employee.count`, поэтому в конце их двое. `name` — атрибут экземпляра: у каждого сотрудника своё имя.

---

### Пример 8: Ловушка — мутабельный атрибут класса

```python
class BadTeam:
    members = []

    def add(self, name):
        self.members.append(name)

team_a = BadTeam()
team_b = BadTeam()
team_a.add("Anna")
team_b.add("Bob")

print("team_a:", team_a.members)
print("team_b:", team_b.members)
```

**Вывод консоли:**

```
team_a: ['Anna', 'Bob']
team_b: ['Anna', 'Bob']
```

**Разбор:** Список `members = []` в теле класса один на все экземпляры — `team_a` и `team_b` ссылаются на один и тот же список. Поэтому `Anna` и `Bob` оказались в обоих «разных» командах. Решение — создавать `self.members = []` отдельно в `__init__` каждого объекта.

**Оба списка общие!** Исправление — `self.members = []` в `__init__`.

---

### Пример 9: Правильно — список в `__init__`

```python
class GoodTeam:
    def __init__(self, name):
        self.name = name
        self.members = []

    def add(self, member):
        self.members.append(member)

    def __str__(self):
        return f"{self.name}: {', '.join(self.members)}"

dev = GoodTeam("Dev")
qa = GoodTeam("QA")
dev.add("Anna")
qa.add("Bob")
print(dev)
print(qa)
```

**Вывод консоли:**

```
Dev: Anna
QA: Bob
```

**Разбор:** Здесь `self.members = []` создаётся при каждом `GoodTeam()` — списки у команд разные. `dev.add` и `qa.add` не мешают друг другу, потому что меняют разные списки. Метод `__str__` собирает имя команды и участников в одну строку для удобного вывода.

---

### Пример 10: Валидация в `__init__`

```python
class User:
    def __init__(self, name, age):
        if not name.strip():
            raise ValueError("Имя не может быть пустым")
        if age < 0 or age > 150:
            raise ValueError(f"Некорректный возраст: {age}")
        self.name = name.strip()
        self.age = age

user = User("Anna", 25)
print(user.name, user.age)

try:
    User("", 30)
except ValueError as e:
    print("Ошибка:", e)
```

**Вывод консоли:**

```
Anna 25
Ошибка: Имя не может быть пустым
```

**Разбор:** Проверки в `__init__` не дают создать объект с пустым именем или неверным возрастом. `User("Anna", 25)` проходит все условия — печатаем имя и возраст. Вызов `User("", 30)` бросает `ValueError`, который мы ловим снаружи и показываем сообщение.

---

### Пример 11: Прямоугольник — метод `area`

```python
class Rectangle:
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

    def perimeter(self):
        return 2 * (self.width + self.height)

rect = Rectangle(5, 3)
print("Площадь:", rect.area())
print("Периметр:", rect.perimeter())
```

**Вывод консоли:**

```
Площадь: 15
Периметр: 16
```

**Разбор:** Методы `area` и `perimeter` используют `self.width` и `self.height` конкретного прямоугольника. Площадь 5×3 = 15, периметр 2×(5+3) = 16. Методы только вычисляют значения и не меняют состояние объекта.

---

### Пример 12: Класс `Counter` — счётчик

```python
class Counter:
    def __init__(self, start=0):
        self.value = start

    def increment(self, step=1):
        self.value += step

    def reset(self):
        self.value = 0

    def __str__(self):
        return f"Counter({self.value})"

c = Counter(10)
c.increment()
c.increment(5)
print(c)
c.reset()
print(c)
```

**Вывод консоли:**

```
Counter(16)
Counter(0)
```

**Разбор:** Метод `increment` увеличивает `self.value` на `step` (по умолчанию 1). Старт 10, затем +1 и +5 дают 16. Метод `reset()` обнуляет счётчик — снова видим `Counter(0)`.

---

### Пример 13: Точка на плоскости — расстояние

```python
import math

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def distance_to(self, other):
        dx = self.x - other.x
        dy = self.y - other.y
        return math.sqrt(dx ** 2 + dy ** 2)

    def __str__(self):
        return f"({self.x}, {self.y})"

a = Point(0, 0)
b = Point(3, 4)
print(a, "→", b, ":", round(a.distance_to(b), 2))
```

**Вывод консоли:**

```
(0, 0) → (3, 4) : 5.0
```

---

### Пример 14: Студент и оценки

```python
class Student:
    def __init__(self, name):
        self.name = name
        self.grades = []

    def add_grade(self, grade):
        if not 1 <= grade <= 5:
            raise ValueError("Оценка 1-5")
        self.grades.append(grade)

    def average(self):
        if not self.grades:
            return 0
        return sum(self.grades) / len(self.grades)

    def __str__(self):
        avg = self.average()
        return f"{self.name}: оценки {self.grades}, средняя {avg:.1f}"

s = Student("Anna")
s.add_grade(5)
s.add_grade(4)
s.add_grade(5)
print(s)
```

**Вывод консоли:**

```
Anna: оценки [5, 4, 5], средняя 4.7
```

---

### Пример 15: `isinstance` — проверка типа

```python
class Animal:
    pass

class Dog(Animal):
    pass

rex = Dog()

print(isinstance(rex, Dog))
print(isinstance(rex, Animal))
print(isinstance(rex, str))
```

**Вывод консоли:**

```
True
True
False
```

*(Наследование — подробно в главе 12)*

---

### Пример 16: Список объектов

```python
class Task:
    def __init__(self, title, done=False):
        self.title = title
        self.done = done

    def __str__(self):
        mark = "✓" if self.done else " "
        return f"[{mark}] {self.title}"

tasks = [
    Task("Изучить классы"),
    Task("Сделать ДЗ", done=True),
    Task("Повторить self"),
]

for task in tasks:
    print(task)
```

**Вывод консоли:**

```
[ ] Изучить классы
[✓] Сделать ДЗ
[ ] Повторить self
```

---

### Пример 17: Фильтрация объектов

```python
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

products = [
    Product("Мышь", 1500),
    Product("Монитор", 25000),
    Product("Коврик", 500),
]

cheap = [p for p in products if p.price < 5000]
for p in cheap:
    print(f"  {p.name}: {p.price}")
```

**Вывод консоли:**

```
  Мышь: 1500
  Коврик: 500
```

---

### Пример 18: Рефакторинг dict → класс

```python
# Было
def show_user(user_dict):
    print(f"{user_dict['name']}, {user_dict['age']} лет")

show_user({"name": "Anna", "age": 25})

# Стало
class User:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def show(self):
        print(f"{self.name}, {self.age} лет")

User("Anna", 25).show()
```

**Вывод консоли:**

```
Anna, 25 лет
Anna, 25 лет
```

---

### Пример 19: Объекты как значения в dict

```python
class User:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return self.name

users = {
    1: User("Anna"),
    2: User("Bob"),
}

print(users[1])
print(users[2].name)
```

**Вывод консоли:**

```
Anna
Bob
```

---

### Пример 20: «Приватный» атрибут `_balance`

```python
class Wallet:
    def __init__(self, balance=0):
        self._balance = balance

    def deposit(self, amount):
        self._balance += amount

    def get_balance(self):
        return self._balance

wallet = Wallet(100)
wallet.deposit(50)
print("Баланс:", wallet.get_balance())
print("Прямой доступ:", wallet._balance)
```

**Вывод консоли:**

```
Баланс: 150
Прямой доступ: 150
```

`_balance` — соглашение «не трогай», но Python **не запрещает** доступ.

---

### Пример 21: `__dict__` — атрибуты объекта

```python
class Car:
    def __init__(self, brand, year):
        self.brand = brand
        self.year = year

car = Car("Toyota", 2020)
print(car.__dict__)

car.color = "белый"
print(car.__dict__)
```

**Вывод консоли:**

```
{'brand': 'Toyota', 'year': 2020}
{'brand': 'Toyota', 'year': 2020, 'color': 'белый'}
```

---

### Пример 22: `dataclass` — компактная модель

```python
from dataclasses import dataclass

@dataclass
class Book:
    title: str
    author: str
    price: float

book = Book("Clean Code", "Robert Martin", 1200)
print(book)
print(book.title, book.price)
```

**Вывод консоли:**

```
Book(title='Clean Code', author='Robert Martin', price=1200)
Clean Code 1200
```

---

### Пример 23: `dataclass` с методом

```python
from dataclasses import dataclass

@dataclass
class Circle:
    radius: float

    def area(self):
        return 3.14159 * self.radius ** 2

c = Circle(5)
print(f"r={c.radius}, площадь={c.area():.2f}")
```

**Вывод консоли:**

```
r=5, площадь=78.54
```

---

### Пример 24: Класс `TodoItem`

```python
class TodoItem:
    def __init__(self, title):
        self.title = title
        self.done = False

    def complete(self):
        self.done = True

    def __str__(self):
        status = "DONE" if self.done else "TODO"
        return f"[{status}] {self.title}"

item = TodoItem("Выучить self")
print(item)
item.complete()
print(item)
```

**Вывод консоли:**

```
[TODO] Выучить self
[DONE] Выучить self
```

---

### Пример 25: Класс `Contact` — телефонная книга

```python
class Contact:
    def __init__(self, name, phone):
        self.name = name
        self.phone = phone

    def __str__(self):
        return f"{self.name}: {self.phone}"

class PhoneBook:
    def __init__(self):
        self.contacts = []

    def add(self, contact):
        self.contacts.append(contact)

    def show_all(self):
        for c in self.contacts:
            print(f"  {c}")

book = PhoneBook()
book.add(Contact("Anna", "+7-111"))
book.add(Contact("Bob", "+7-222"))
book.show_all()
```

**Вывод консоли:**

```
  Anna: +7-111
  Bob: +7-222
```

---

### Пример 26: Композиция — заказ и позиции

```python
class OrderItem:
    def __init__(self, product, quantity, price):
        self.product = product
        self.quantity = quantity
        self.price = price

    def subtotal(self):
        return self.quantity * self.price

class Order:
    def __init__(self, order_id):
        self.order_id = order_id
        self.items = []

    def add_item(self, item):
        self.items.append(item)

    def total(self):
        return sum(item.subtotal() for item in self.items)

order = Order("ORD-001")
order.add_item(OrderItem("Книга", 2, 500))
order.add_item(OrderItem("Ручка", 5, 50))
print(f"Заказ {order.order_id}: {order.total()} руб.")
```

**Вывод консоли:**

```
Заказ ORD-001: 1250 руб.
```

**Композиция** — Order **содержит** OrderItem (has-a). Не путай с наследованием (is-a) — глава 12.

---

### Пример 27: Метод возвращает `self` — цепочка вызовов

```python
class Builder:
    def __init__(self):
        self.parts = []

    def add(self, part):
        self.parts.append(part)
        return self

    def build(self):
        return ", ".join(self.parts)

result = Builder().add("A").add("B").add("C").build()
print(result)
```

**Вывод консоли:**

```
A, B, C
```

---

### Пример 28: Класс с `__bool__` — проверка в if

```python
class Account:
    def __init__(self, balance):
        self.balance = balance

    def __bool__(self):
        return self.balance > 0

    def __str__(self):
        return f"Баланс: {self.balance}"

accounts = [Account(0), Account(100), Account(-50)]

for acc in accounts:
    if acc:
        print(f"  Активен: {acc}")
    else:
        print(f"  Пустой/нулевой: {acc}")
```

**Вывод консоли:**

```
  Пустой/нулевой: Баланс: 0
  Активен: Баланс: 100
  Пустой/нулевой: Баланс: -50
```

---

### Пример 29: Сравнение двух объектов — `__eq__`

```python
class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, other):
        if not isinstance(other, Point):
            return False
        return self.x == other.x and self.y == other.y

    def __str__(self):
        return f"({self.x}, {self.y})"

a = Point(1, 2)
b = Point(1, 2)
c = Point(3, 4)

print(a == b)
print(a == c)
print(a is b)
```

**Вывод консоли:**

```
True
False
False
```

`==` сравнивает **значения** (через `__eq__`). `is` — **один объект** в памяти.

---

### Пример 30: Класс `User` + модуль — связь с главой 10

**`models.py`:**

```python
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __str__(self):
        return f"User({self.name})"
```

**`main.py`:**

```python
from models import User

users = [User("Anna", "a@mail.com"), User("Bob", "b@mail.com")]
for u in users:
    print(u)
```

**Вывод консоли:**

```
User(Anna)
User(Bob)
```

---

### Пример 31: Класс `Temperature` — конвертация

```python
class Temperature:
    def __init__(self, celsius):
        self.celsius = celsius

    @property
    def fahrenheit(self):
        return self.celsius * 9 / 5 + 32

    def __str__(self):
        return f"{self.celsius}°C = {self.fahrenheit:.1f}°F"

t = Temperature(0)
print(t)
t.celsius = 100
print(t)
```

**Вывод консоли:**

```
0°C = 32.0°F
100°C = 212.0°F
```

*`@property` — атрибут, который вычисляется. Подробнее в главе 13.*

---

### Пример 32: Обработка ошибок в методах

```python
class BankAccount:
    def __init__(self, balance=0):
        self._balance = balance

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Сумма > 0")
        if amount > self._balance:
            raise ValueError(f"Баланс {self._balance}, нужно {amount}")
        self._balance -= amount

account = BankAccount(500)
try:
    account.withdraw(600)
except ValueError as e:
    print("Ошибка:", e)
print("Баланс:", account._balance)
```

**Вывод консоли:**

```
Ошибка: Баланс 500, нужно 600
Баланс: 500
```

---

### Пример 33: Класс `ShoppingCart` — полный мини-класс

```python
class ShoppingCart:
    def __init__(self, owner):
        self.owner = owner
        self.items = []

    def add(self, name, price):
        self.items.append({"name": name, "price": price})

    def remove(self, name):
        self.items = [i for i in self.items if i["name"] != name]

    def total(self):
        return sum(i["price"] for i in self.items)

    def __str__(self):
        lines = [f"  {i['name']}: {i['price']}" for i in self.items]
        return f"Корзина {self.owner}:\n" + "\n".join(lines) + f"\n  ИТОГО: {self.total()}"

cart = ShoppingCart("Anna")
cart.add("Книга", 800)
cart.add("Чай", 300)
print(cart)
cart.remove("Чай")
print("После удаления:", cart.total())
```

**Вывод консоли:**

```
Корзина Anna:
  Книга: 800
  Чай: 300
  ИТОГО: 1100
После удаления: 800
```

---

### Пример 34: Несколько классов в одном модуле

```python
class Engine:
    def __init__(self, power):
        self.power = power

class Car:
    def __init__(self, brand, engine):
        self.brand = brand
        self.engine = engine

    def info(self):
        return f"{self.brand}, {self.engine.power} л.с."

engine = Engine(150)
car = Car("Toyota", engine)
print(car.info())
```

**Вывод консоли:**

```
Toyota, 150 л.с.
```

---

### Пример 35: Класс `Timer` — накопление времени

```python
class Timer:
    def __init__(self):
        self.elapsed = 0

    def tick(self, seconds):
        if seconds < 0:
            raise ValueError("Время не может быть отрицательным")
        self.elapsed += seconds

    def reset(self):
        self.elapsed = 0

    def __str__(self):
        return f"{self.elapsed} сек."

timer = Timer()
timer.tick(30)
timer.tick(45)
print(timer)
timer.reset()
print("Сброс:", timer)
```

**Вывод консоли:**

```
75 сек.
Сброс: 0 сек.
```

---

### Пример 36: Класс `Note` — заметки

```python
from datetime import datetime

class Note:
    def __init__(self, text):
        self.text = text
        self.created_at = datetime.now()

    def __str__(self):
        ts = self.created_at.strftime("%H:%M")
        return f"[{ts}] {self.text}"

notes = [Note("Купить молоко"), Note("Сделать ДЗ гл. 11")]
for note in notes:
    print(note)
```

**Вывод консоли (время зависит от запуска):**

```
[15:30] Купить молоко
[15:30] Сделать ДЗ гл. 11
```

---

### Пример 37: Мини-проект — `TodoList`

```python
class TodoItem:
    def __init__(self, title):
        self.title = title
        self.done = False

    def __str__(self):
        mark = "x" if self.done else " "
        return f"[{mark}] {self.title}"

class TodoList:
    def __init__(self, name):
        self.name = name
        self.items = []

    def add(self, title):
        self.items.append(TodoItem(title))

    def complete(self, index):
        if 0 <= index < len(self.items):
            self.items[index].done = True

    def pending_count(self):
        return sum(1 for i in self.items if not i.done)

    def show(self):
        print(f"=== {self.name} ({self.pending_count()} активных) ===")
        for i, item in enumerate(self.items):
            print(f"  {i}. {item}")

todo = TodoList("Учёба")
todo.add("Прочитать гл. 11")
todo.add("Написать класс User")
todo.add("Сдать ДЗ")
todo.complete(0)
todo.show()
```

**Вывод консоли:**

```
=== Учёба (2 активных) ===
  0. [x] Прочитать гл. 11
  1. [ ] Написать класс User
  2. [ ] Сдать ДЗ
```

---

### Пример 38: Полный пайплайн — регистрация пользователей

```python
class User:
    def __init__(self, name, email):
        if "@" not in email:
            raise ValueError(f"Некорректный email: {email}")
        self.name = name.strip()
        self.email = email.lower()
        self.is_active = True

    def deactivate(self):
        self.is_active = False

    def __str__(self):
        status = "active" if self.is_active else "inactive"
        return f"{self.name} <{self.email}> [{status}]"

class UserRegistry:
    def __init__(self):
        self.users = []

    def register(self, name, email):
        user = User(name, email)
        self.users.append(user)
        return user

    def active_users(self):
        return [u for u in self.users if u.is_active]

registry = UserRegistry()

test_data = [
    ("Anna", "anna@mail.com"),
    ("Bob", "invalid-email"),
    ("Vika", "vika@test.org"),
]

for name, email in test_data:
    try:
        user = registry.register(name, email)
        print(f"  OK: {user}")
    except ValueError as e:
        print(f"  FAIL: {name} — {e}")

print("\nАктивных:", len(registry.active_users()))
for u in registry.active_users():
    print(f"  {u}")
```

**Вывод консоли:**

```
  OK: Anna <anna@mail.com> [active]
  FAIL: Bob — Некорректный email: invalid-email
  OK: Vika <vika@test.org> [active]

Активных: 2
  Anna <anna@mail.com> [active]
  Vika <vika@test.org> [active]
```

---

## Шпаргалка

```python
class User:
    species = "human"           # атрибут класса

    def __init__(self, name):   # конструктор
        self.name = name        # атрибут экземпляра

    def greet(self):            # метод — self первый
        print(self.name)

    def __str__(self):
        return f"User({self.name})"

user = User("Anna")             # создание объекта
user.greet()                    # вызов метода
isinstance(user, User)            # True
```

| Термин | Значение |
|--------|----------|
| Класс | Шаблон / чертёж |
| Объект / экземпляр | Конкретная «вещь» по шаблону |
| `__init__` | Инициализация при создании |
| `self` | Ссылка на текущий объект |
| Атрибут | Данные объекта (`self.name`) |
| Метод | Функция внутри класса |
| `__str__` | Строка для `print()` |
| `__repr__` | Строка для отладки |
| `__eq__` | Сравнение `==` |
| `_name` | «Приватный» по соглашению |

### Таблица: когда что использовать

| Задача | Решение |
|--------|---------|
| Хранить поля + немного логики | Обычный класс |
| Только данные, мало методов | `@dataclass` |
| Общая константа для всех | Атрибут класса |
| Список/словарь у каждого | В `__init__`: `self.items = []` |
| Красивый print | `__str__` |
| Сравнение объектов | `__eq__` |

---

## FAQ начинающего

**В: Класс и объект — в чём разница?**  
Класс — один. Объектов по этому классу — сколько угодно.

**В: Зачем `self`?**  
Чтобы метод знал, **с каким** объектом работать. `anna.greet()` → `self` = `anna`.

**В: `__init__` — это создание объекта?**  
Инициализация. Создание делает Python, потом вызывает `__init__`.

**В: Можно ли без `__init__`?**  
Да. Объект будет без начальных атрибутов (или только с атрибутами класса).

**В: `__str__` обязателен?**  
Нет, но без него `print(obj)` даст `<__main__.User object at 0x...>`.

**В: Чем класс отличается от dict?**  
Dict — просто данные. Класс — данные + методы + валидация + структура.

**В: Всё ли писать классами?**  
Нет. Функции проще для разовых операций. Классы — для сущностей.

**В: `self` внутри класса — это переменная?**  
Параметр метода. При вызове `obj.method()` Python передаёт `obj` как `self`.

**В: Что такое `dataclass`?**  
Синтаксический сахар для классов-данных. Меньше boilerplate.

**В: `_balance` — реально скрыт?**  
Нет. Это **соглашение** «внутреннее». Python не блокирует доступ.

**В: `==` vs `is` для объектов?**  
`==` — одинаковые **данные** (`__eq__`). `is` — **один** объект в памяти.

**В: Композиция vs наследование?**  
«Has-a» (заказ содержит позиции) vs «is-a» (собака — животное). Наследование — глава 12.

**В: Сколько классов в одном файле?**  
Допустимо несколько, если они связаны. Крупные классы — отдельные файлы (глава 10).

---

### Частые баги

```python
# БАГ — забыли self
class User:
    def set_name(name):
        self.name = name

# БАГ — мутабельный атрибут класса
class Cart:
    items = []

# БАГ — вызов метода без ()
result = account.deposit

# БАГ — AttributeError
user = User("Anna")
print(user.email)    # не задали в __init__

# FIX
class User:
    def __init__(self, name, email=""):
        self.name = name
        self.email = email
```

### Типичные ошибки

| Ошибка | Причина | Решение |
|--------|---------|---------|
| `TypeError: missing 1 required positional argument: 'self'` | Вызов метода на классе без self | `User("Anna")` или `User.greet(obj)` |
| `AttributeError: 'User' object has no attribute 'x'` | Атрибут не создан | Добавь в `__init__` |
| Все экземпляры делят один list | `items = []` в классе | `self.items = []` в `__init__` |
| `print(obj)` → `<object at 0x...>` | Нет `__str__` | Добавь `__str__` |

---

## Домашнее задание

**Файл:** `homework_11.py`

> У каждой задачи ниже — **что должно получиться** при правильном решении (как в главе 13).

### Задача 1 — Лёгкая
Создай класс `Dog` с `__init__(name, breed)` и методом `bark()`, выводящим `"{name}: Гав!"`.  
Создай 2 собаки, вызови `bark()`.

**Должно получиться (пример вывода):**
```
Рекс: Гав!
Бобик: Гав!
```

---

### Задача 2 — Лёгкая
Создай класс `Rectangle(width, height)` с методом `area()`.  
Проверь для прямоугольника 4×5.

**Должно получиться:** `20`

---

### Задача 3 — Средняя
Создай класс `BankAccount(owner, balance=0)` с `deposit`, `withdraw`, `__str__`.  
`withdraw` при недостатке средств — `raise ValueError`. Протестируй 3 сценария.

**Должно получиться:** после `deposit(100)` и `withdraw(30)` баланс `70`; при `withdraw(1000)` — `ValueError`.

<details>
<summary>Подсказка</summary>

См. Пример 5 и 32.

</details>

---

### Задача 4 — Средняя
Создай класс `Student(name)` с методами `add_grade(grade)` и `average()`.  
Оценки 1–5, иначе `ValueError`. Добавь `__str__`.

---

### Задача 5 — Средняя
Создай `@dataclass` `Point(x, y)` с методом `distance_to(other)`.  
Проверь расстояние от (0,0) до (3,4) = 5.0.

---

### Задача 6 — Сложная
Класс `TodoItem` + класс `TodoList` (как Пример 37):
- `add(title)`, `complete(index)`, `show()`, `pending_count()`
- Не используй мутабельный атрибут класса для списка

---

### Задача 7 — Сложная
Класс `Product(name, price)` и класс `Shop`:
- `add_product`, `find_by_name(name)` → Product или None
- `total_value()` — сумма цен всех товаров
- `__str__` у обоих классов

---

### Задача 8 — Сложная
Класс `User(name, email)` с валидацией в `__init__` и класс `UserRegistry`:
- `register(name, email)` → User или raise
- `count()`, `list_active()`
- Протестируй 5 пар (name, email), включая невалидный email

---

### Задача 9 — Сложная (бонус)
Класс `Order` и `OrderItem` (композиция, Пример 26):
- Добавление позиций, `total()`, `remove_item(product_name)`
- `__str__` выводит все позиции и итог

---

### Задача 10 — Сложная (бонус)
Вынеси классы в модуль `models.py`, логику запуска в `main.py` (глава 10):
- Минимум 2 класса
- `if __name__ == "__main__"` в `main.py`
- Демо с 3+ объектами

---

### Задача 11 — Сложная (бонус)
Добавь `__eq__` и `__repr__` в класс `Point` из задачи 5.  
Покажи: два Point(1,2) равны через `==`, но `is` — False.

---

### Задача 12 — Сложная (бонус)
**Мини-библиотека:** пакет `library/` с `book.py` (класс `Book`) и `catalog.py` (класс `Catalog` с `add_book`, `find_by_title`, `list_all`).  
`main.py` — демо. Структура как в главе 10.

---

### Как сдавать

- Папка `homework_11/` или файл `homework_11.py` (задачи 1–5)
- Задачи 6–12 — отдельные файлы/пакеты
- Частями: 1–5, 6–10, 11–12
- Вывод `print` для каждой задачи

**Критерии:**
- У всех методов экземпляра первый аргумент — `self`
- Списки/словари — в `__init__`, не как атрибуты класса
- Есть `__str__` хотя бы у основных классов
- Валидация в `__init__` или методах через `raise ValueError`
- Имена классов — `CapWords`

---

**Сделай задачи сам и пришли код на проверку. После проверки — Глава 12: *ООП — наследование и полиморфизм*.**

---
Конец главы.