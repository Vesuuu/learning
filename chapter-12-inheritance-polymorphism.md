# Тема: ООП — наследование и полиморфизм

## Теория

### Что это такое — простыми словами

В главе 11 ты научился делать **один класс**. В реальности много сущностей **похожи**, но **чуть разные**:

- Собака и кошка — оба животные, но лают/мяукают по-разному
- Обычный счёт и накопительный — оба счета, но у второго есть проценты
- Обычный пользователь и админ — оба пользователи, но админ может банить

**Наследование** — взять готовый класс (родитель) и **расширить** его (потомок), не копируя весь код.

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "..."

class Dog(Animal):    # Dog наследует Animal
    def speak(self):
        return f"{self.name}: Гав!"
```

`Dog` **получает** всё от `Animal` и **переопределяет** `speak`.

**Полиморфизм** — «много форм»: разные классы, **один интерфейс** (одинаковые методы), разное поведение.

```python
animals = [Dog("Rex"), Cat("Мурка")]

for a in animals:
    print(a.speak())    # каждый по-своему — но все имеют .speak()
```

---

### Связь с главой 11

| Глава 11 | Глава 12 |
|----------|----------|
| Один класс | Иерархия классов |
| `isinstance(rex, Dog)` | `isinstance(rex, Animal)` тоже True |
| Композиция (has-a) | Наследование (is-a) |
| `__str__` в одном классе | Переопределение `__str__` в потомке |

**is-a (наследование):** Собака **является** животным → `class Dog(Animal)`  
**has-a (композиция):** Машина **имеет** двигатель → `self.engine = Engine()` (глава 11)

**Правило Junior:** если связь «является» — наследование. Если «содержит» — композиция.

---

### Шпаргалка «на пальцах» — запомни это

```
Родитель (Animal)          Потомок (Dog)
┌─────────────────┐        ┌─────────────────┐
│ name            │   →    │ name            │  ← унаследовано
│ speak() → "..." │   →    │ speak() → "Гав!"│  ← переопределено
└─────────────────┘        │ fetch()         │  ← только у Dog
                           └─────────────────┘
```

| Вопрос | Ответ |
|--------|-------|
| Зачем наследование? | Не копировать один и тот же код |
| Зачем `super()`? | Вызвать логику родителя, не дублируя |
| Зачем полиморфизм? | Один цикл/функция для разных типов |
| `Dog` — это `Animal`? | Да, для Python: `isinstance(dog, Animal)` |
| Когда НЕ наследовать? | «Машина имеет двигатель» → композиция |

**Мини-шаблон** — выучи наизусть:

```python
class Child(Parent):
    def __init__(self, ...):
        super().__init__(...)    # 1. родитель
        self.новое = ...         # 2. своё

    def method(self):
        return super().method()  # опционально: расширить, не заменить
```

---

### Без ООП vs с наследованием — одна задача

**Задача:** вывести звук для собаки, кошки, птицы.

**Без наследования — if/elif на каждый тип:**

```python
def speak_animal(kind, name):
    if kind == "dog":
        return f"{name}: Гав!"
    elif kind == "cat":
        return f"{name}: Мяу!"
    elif kind == "bird":
        return f"{name}: Чирик!"
    # каждое новое животное — ещё один elif...
```

**С наследованием — добавил класс, if не трогаешь:**

```python
class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    def speak(self):
        return f"{self.name}: Гав!"

# новое животное = новый класс, цикл не меняется
for a in [Dog("Rex"), Cat("Мурка")]:
    print(a.speak())
```

**Выигрыш:** код растёт **добавлением классов**, а не раздуванием одной функции.

---

### Синтаксис наследования

```python
class Parent:
    def __init__(self, name):
        self.name = name

class Child(Parent):
    def __init__(self, name, age):
        super().__init__(name)    # вызов __init__ родителя
        self.age = age
```

`Child(Parent)` — **потомок** наследует **родителя** (базовый класс, суперкласс).

| Термин | По-русски |
|--------|-----------|
| Parent / Base | Родительский / базовый класс |
| Child / Subclass | Потомок / подкласс |
| `super()` | Ссылка на родителя для вызова его методов |

---

### `super()` — зачем нужен

Без `super()` пришлось бы дублировать код родителя:

```python
# Плохо — дублирование
class Child(Parent):
    def __init__(self, name, age):
        self.name = name    # копипаста из Parent
        self.age = age

# Хорошо
class Child(Parent):
    def __init__(self, name, age):
        super().__init__(name)
        self.age = age
```

`super().__init__(name)` = «сначала настрой то, что умеет родитель, потом добавь своё».

---

### Переопределение методов (override)

Потомок может **заменить** метод родителя:

```python
class Animal:
    def speak(self):
        return "..."

class Dog(Animal):
    def speak(self):           # override — переопределение
        return "Гав!"
```

Вызов `dog.speak()` — версия из `Dog`, не из `Animal`.

**Расширение, а не только замена** — вызови родителя внутри:

```python
class Dog(Animal):
    def speak(self):
        base = super().speak()
        return base + " Гав!"
```

---

### Полиморфизм — одна функция, разные типы

```python
def announce(animal):
    print(animal.speak())

announce(Dog("Rex"))     # Гав!
announce(Cat("Мурка"))   # Мяу!
```

Функция `announce` не знает, **какой** именно `Animal` — ей нужен только метод `.speak()`. Это **полиморфизм**.

В Python ещё **утиная типизация** (duck typing): «если ходит как утка и крякает как утка — это утка». Наследование не обязательно, главное — **нужные методы есть**.

```python
class Robot:
    def speak(self):
        return "Бип-бип"

announce(Robot())    # работает — есть speak()
```

---

### `isinstance` и `issubclass`

```python
rex = Dog("Rex")

isinstance(rex, Dog)       # True
isinstance(rex, Animal)    # True — Dog является Animal
isinstance(rex, Cat)       # False

issubclass(Dog, Animal)    # True — Dog подкласс Animal
issubclass(Dog, Dog)       # True
```

**Проверка типа** — через `isinstance`, не `type(x) == Dog` (не учитывает наследование).

---

### Многоуровневая иерархия

```python
class Animal: ...
class Mammal(Animal): ...
class Dog(Mammal): ...
```

`Dog` наследует и от `Mammal`, и (транзитивно) от `Animal`.

```
Animal
  └── Mammal
        └── Dog
```

---

### Наследование исключений (связь с главой 9)

```python
class AppError(Exception):
    pass

class ValidationError(AppError):
    pass

class NotFoundError(AppError):
    pass
```

Ловить `except AppError` — поймает и `ValidationError`, и `NotFoundError`.

---

### `@classmethod` и `@staticmethod`

**classmethod** — метод привязан к **классу**, первый аргумент `cls`:

```python
class User:
    def __init__(self, name):
        self.name = name

    @classmethod
    def from_email(cls, email):
        name = email.split("@")[0]
        return cls(name)
```

`User.from_email("anna@mail.com")` — альтернативный «конструктор».

**staticmethod** — функция внутри класса, **без** `self` и `cls`:

```python
class MathUtil:
    @staticmethod
    def is_even(n):
        return n % 2 == 0
```

---

### ABC — абстрактный базовый класс (идея)

Иногда родитель — **шаблон**, создавать объекты напрямую нельзя:

```python
from abc import ABC, abstractmethod

class Shape(ABC):
    @abstractmethod
    def area(self):
        pass

class Rectangle(Shape):
    def area(self):
        return self.width * self.height
```

`Shape()` — ошибка. `Rectangle(...)` — OK, если реализован `area`.

---

### Наследование vs композиция — когда что

| Наследование (is-a) | Композиция (has-a) |
|---------------------|-------------------|
| `Dog(Animal)` | `Car` содержит `Engine` |
| Потомок **замена** родителя в полиморфизме | Сборка из частей |
| Опасность: глубокие иерархии | Часто гибче |

**Антипаттерн:** наследовать ради одной переиспользуемой функции — лучше обычная функция или композиция.

---

### Множественное наследование — кратко

```python
class Flyer:
    def fly(self):
        return "Лечу"

class Swimmer:
    def swim(self):
        return "Плыву"

class Duck(Animal, Flyer, Swimmer):
    pass
```

На Junior: **избегай** глубокого множественного наследования. Знай, что `super()` идёт по **MRO** (Method Resolution Order). Детали — Middle+.

---

### Как это работает «под капотом»

1. Поиск атрибута/метода: сначала **экземпляр**, потом **класс потомка**, потом **родитель**, по цепочке вверх
2. `super()` — не «родитель напрямую», а **следующий** класс по MRO
3. `isinstance` проверяет всю цепочку наследования

```python
Dog.__mro__    # порядок поиска методов
```

---

### Где применяется в реальной разработке

| Ситуация | Наследование |
|----------|--------------|
| Django | `class MyModel(models.Model)` |
| Исключения | `class MyError(AppError)` |
| Тесты | `class TestLogin(unittest.TestCase)` |
| Игры | `class Orc(Enemy)` |
| API | Базовый `BaseSerializer` → конкретные |

На собеседовании: разница override/overload (в Python overload через default args), `super()`, полиморфизм, is-a vs has-a.

---

### Микро-моменты, нюансы, частые ошибки новичков

#### 1. Забыли `super().__init__`

Потомок не инициализирует поля родителя → `AttributeError`.

#### 2. Наследование ради копипасты одного поля

Иногда проще композиция или общая функция.

#### 3. Глубокая иерархия 5+ уровней

Сложно поддерживать. Плоская иерархия лучше.

#### 4. Переопределили метод, забыли `super()`

Родительская логика потеряна — иногда это OK, иногда баг.

#### 5. `isinstance` vs `type ==`

Всегда `isinstance` для иерархий.

#### 6. Путаница: потомок — это не «копия» родителя

Один класс `Dog`, объекты `rex` и `bobik` — разные экземпляры.

#### 7. Приватность `_` не наследуется жёстко

`_balance` в родителе доступен потомку (и снаружи по соглашению).

#### 8. Не вызывай переопределённый метод из `__init__` родителя без осторожности

Родительский `__init__` может вызвать метод, который потомок ещё не настроил.

#### 9. `classmethod` наследуется

`Child.from_email()` вернёт экземпляр `Child`, если переопределить правильно.

#### 10. Полиморфизм без наследования — нормально в Python

Главное — одинаковый интерфейс методов.

#### 11. `Exception` — всегда наследуй от `Exception`

Не от `BaseException`.

#### 12. `super()` в Python 3 — без аргументов

`super().__init__()`, не `super(Dog, self).__init__()` (старый стиль).

#### 13. Переопределение `__init__` с разными параметрами — OK

`Child` может требовать больше аргументов, чем `Parent`.

#### 14. List потомков в одной переменной

`animals: list[Animal]` — храни разные подклассы вместе.

#### 15. Liskov (на пальцах)

Потомок должен **не ломать** ожидания родителя: если код работает с `Animal`, подставь `Dog` — должно работать.

#### 16. `type(x) == Dog` — не используй для иерархий

`type(rex) == Animal` → False, хотя `rex` — собака. Только `isinstance`.

#### 17. Родительский метод виден, если не переопределён

Не обязано всё override — только то, что отличается.

#### 18. Потомок может вызывать методы родителя напрямую

`Parent.method(self)` — старый стиль. Предпочитай `super().method()`.

#### 19. Наследование атрибутов класса

Потомок видит атрибуты класса родителя. Осторожно с мутабельными (глава 11).

#### 20. `Exception` → `ValueError` — тоже наследование

Встроенные исключения — иерархия. `except Exception` ловит почти всё.

---

### Как читать эту главу (маршрут для новичка)

| Шаг | Примеры | Что поймёшь |
|-----|---------|-------------|
| 1 | 1–3 | Синтаксис, `super`, `isinstance` |
| 2 | 5–6 | Полиморфизм — главная фишка |
| 3 | 8–9 | `super()` в методах, банковский счёт |
| 4 | 11–12 | Фигуры, зарплата — «один метод, разная логика» |
| 5 | 16–17 | Исключения-наследники |
| 6 | 34, 38 | Мини-проекты целиком |
| 7 | 39–45 | Закрепление + разбор ошибок |

Не зубри все 45 сразу. **1–6 шаг** = достаточно для ДЗ 1–8.

---

## Практика

> Каждый пример: код → вывод → **Разбор** — что произошло и почему.

> **Навигация:** **45 примеров**, шпаргалка, FAQ, домашка.

### Пример 1: Базовое наследование

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return f"{self.name} издаёт звук"

class Dog(Animal):
    def speak(self):
        return f"{self.name}: Гав!"

rex = Dog("Rex")
print(rex.name)
print(rex.speak())
```

**Вывод консоли:**

```
Rex
Rex: Гав!
```

**Разбор:** Класс `Dog` наследует `Animal` — у `rex` есть `name` из родительского `__init__`. Метод `speak` переопределён в потомке, поэтому звук «Гав!», а не общий шаблон родителя. Наследование позволяет переиспользовать код родителя и менять только нужное поведение.

`Dog` **унаследовал** `__init__` и `name`, **переопределил** `speak`.

---

### Пример 2: `super().__init__` — инициализация родителя

```python
class Person:
    def __init__(self, name):
        self.name = name

class Employee(Person):
    def __init__(self, name, salary):
        super().__init__(name)
        self.salary = salary

    def __str__(self):
        return f"{self.name}, зарплата {self.salary}"

emp = Employee("Anna", 80000)
print(emp)
```

**Вывод консоли:**

```
Anna, зарплата 80000
```

**Разбор:** Вызов `super().__init__(name)` сначала инициализирует родителя `Person`, затем добавляется поле `salary`. Без `super` атрибут `name` мог бы не создаться в потомке. Метод `__str__` выводит и имя, и зарплату одной строкой.

---

### Пример 3: `isinstance` — потомок это тоже родитель

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

**Разбор:** `isinstance(rex, Dog)` — объект действительно создан как `Dog`. `isinstance(rex, Animal)` — потомок считается и экземпляром родителя (принцип подстановки). `isinstance(rex, str)` даёт `False`, потому что это собака, а не строка.

---

### Пример 4: `issubclass` — проверка классов

```python
class Animal:
    pass

class Dog(Animal):
    pass

class Cat(Animal):
    pass

print(issubclass(Dog, Animal))
print(issubclass(Cat, Dog))
print(issubclass(Animal, object))
```

**Вывод консоли:**

```
True
False
True
```

**Разбор:** `issubclass(Dog, Animal)` подтверждает, что `Dog` — подкласс `Animal`. `Cat` и `Dog` — «соседи» по иерархии, не родитель и потомок, поэтому между ними `False`. В Python 3 любой класс наследует `object` — отсюда `True` для `Animal` и `object`.

Все классы в Python 3 наследуют `object`.

---

### Пример 5: Полиморфизм — цикл по разным животным

```python
class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    def speak(self):
        return f"{self.name}: Гав!"

class Cat(Animal):
    def speak(self):
        return f"{self.name}: Мяу!"

animals = [Dog("Rex"), Cat("Мурка"), Dog("Бобик")]

for animal in animals:
    print(animal.speak())
```

**Вывод консоли:**

```
Rex: Гав!
Мурка: Мяу!
Бобик: Гав!
```

**Разбор:** Список `animals` содержит и `Dog`, и `Cat`, но у всех вызывается один метод `speak()`. Каждый класс реализует его по-своему — это полиморфизм. Цикл не знает конкретный тип объекта, ему достаточно общего интерфейса.

Один цикл — **разное** поведение. Это полиморфизм.

---

### Пример 6: Функция, принимающая любого «животного»

```python
class Dog:
    def speak(self):
        return "Гав!"

class Cat:
    def speak(self):
        return "Мяу!"

def make_sound(creature):
    print(creature.speak())

make_sound(Dog())
make_sound(Cat())
```

**Вывод консоли:**

```
Гав!
Мяу!
```

**Разбор:** Функция `make_sound` принимает любой объект с методом `speak()` — конкретный класс не важен. `Dog` и `Cat` отвечают по-разному на один и тот же вызов. Это утиная типизация: важно поведение объекта, а не его формальный тип.

Функции не важен **тип** — важен метод `speak()`.

---

### Пример 7: Переопределение `__str__` в потомке

```python
class User:
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return f"User({self.name})"

class Admin(User):
    def __str__(self):
        return f"Admin[{self.name}]"

print(User("Anna"))
print(Admin("Root"))
```

**Вывод консоли:**

```
User(Anna)
Admin[Root]
```

**Разбор:** Класс `Admin` переопределяет `__str__` родителя `User` — формат строки другой. Функция `print` автоматически вызывает `__str__` у объекта. У потомка может быть своё «лицо» для вывода, не затрагивая базовый класс.

---

### Пример 8: Расширение метода через `super()`

```python
class Logger:
    def log(self, message):
        print(f"[LOG] {message}")

class TimestampLogger(Logger):
    def log(self, message):
        from datetime import datetime
        ts = datetime.now().strftime("%H:%M:%S")
        super().log(f"{ts} {message}")

logger = TimestampLogger()
logger.log("Сервер запущен")
```

**Вывод консоли:**

```
[LOG] 15:30:01 Сервер запущен
```

**Разбор:** Метод `TimestampLogger.log` сначала добавляет время к сообщению, затем вызывает родительский `log` через `super()`. Родитель печатает префикс `[LOG]`, потомок дополняет текст временем. Так расширяют поведение, не копируя весь код заново.

---

### Пример 9: Банковский счёт → накопительный

```python
class BankAccount:
    def __init__(self, owner, balance=0):
        self.owner = owner
        self.balance = balance

    def deposit(self, amount):
        self.balance += amount

    def __str__(self):
        return f"{self.owner}: {self.balance} руб."

class SavingsAccount(BankAccount):
    def __init__(self, owner, balance=0, rate=0.05):
        super().__init__(owner, balance)
        self.rate = rate

    def add_interest(self):
        interest = self.balance * self.rate
        self.deposit(interest)
        return interest

account = SavingsAccount("Anna", 10000, rate=0.1)
interest = account.add_interest()
print(account)
print(f"Начислено: {interest}")
```

**Вывод консоли:**

```
Anna: 11000.0 руб.
Начислено: 1000.0
```

**Разбор:** `SavingsAccount` наследует `deposit` и `balance` от `BankAccount`, добавляя процентную ставку. Метод `add_interest` считает 10% от 10000 = 1000 и вызывает унаследованный `deposit`. Баланс становится 11000 — переиспользован готовый код пополнения счёта.

---

### Пример 10: Добавление метода только в потомке

```python
class Vehicle:
    def __init__(self, brand):
        self.brand = brand

    def start(self):
        return f"{self.brand} заведён"

class Car(Vehicle):
    def honk(self):
        return "Би-би!"

car = Car("Toyota")
print(car.start())
print(car.honk())
```

**Вывод консоли:**

```
Toyota заведён
Би-би!
```

**Разбор:** Метод `start` унаследован от `Vehicle` и работает у любой машины. Метод `honk` объявлен только в `Car` — у базового `Vehicle` его нет. Потомок добавляет специфичное поведение, не меняя родительский класс.

`honk` есть только у `Car`, не у `Vehicle`.

---

### Пример 11: Фигуры — полиморфный `area()`

```python
class Shape:
    def area(self):
        raise NotImplementedError("Подкласс должен реализовать area()")

class Rectangle(Shape):
    def __init__(self, width, height):
        self.width = width
        self.height = height

    def area(self):
        return self.width * self.height

class Circle(Shape):
    def __init__(self, radius):
        self.radius = radius

    def area(self):
        return 3.14159 * self.radius ** 2

shapes = [Rectangle(4, 5), Circle(3)]

for s in shapes:
    print(f"{type(s).__name__}: площадь = {s.area():.2f}")
```

**Вывод консоли:**

```
Rectangle: площадь = 20.00
Circle: площадь = 28.27
```

**Разбор:** Базовый `Shape.area` бросает `NotImplementedError` — подкласс обязан реализовать свой расчёт. `Rectangle` и `Circle` считают площадь по разным формулам. Один цикл вызывает `area()` у всех фигур — полиморфизм без проверок `if type(...)`.

---

### Пример 12: Сотрудник → менеджер с бонусом

```python
class Employee:
    def __init__(self, name, base_salary):
        self.name = name
        self.base_salary = base_salary

    def total_pay(self):
        return self.base_salary

class Manager(Employee):
    def __init__(self, name, base_salary, bonus):
        super().__init__(name, base_salary)
        self.bonus = bonus

    def total_pay(self):
        return super().total_pay() + self.bonus

staff = [Employee("Anna", 50000), Manager("Bob", 60000, 15000)]

for person in staff:
    print(f"{person.name}: {person.total_pay()} руб.")
```

**Вывод консоли:**

```
Anna: 50000 руб.
Bob: 75000 руб.
```

**Разбор:** Метод `Manager.total_pay` вызывает `super().total_pay()` и прибавляет бонус к базовой зарплате. Anna — обычный сотрудник: только 50000. Bob — менеджер: 60000 + 15000 = 75000. Один метод `total_pay` в цикле даёт разный результат для разных классов.

---

### Пример 13: Трёхуровневая иерархия

```python
class Animal:
    def __init__(self, name):
        self.name = name

class Mammal(Animal):
    def warm_blooded(self):
        return True

class Dog(Mammal):
    def speak(self):
        return "Гав!"

rex = Dog("Rex")
print(rex.name, rex.warm_blooded(), rex.speak())
print(issubclass(Dog, Animal))
```

**Вывод консоли:**

```
Rex True Гав!
True
```

---

### Пример 14: Пользователь → админ с правами

```python
class User:
    def __init__(self, name):
        self.name = name
        self.role = "user"

    def can_ban(self):
        return False

    def __str__(self):
        return f"{self.name} ({self.role})"

class Admin(User):
    def __init__(self, name):
        super().__init__(name)
        self.role = "admin"

    def can_ban(self):
        return True

users = [User("Anna"), Admin("Root")]

for u in users:
    print(u, "— бан:", u.can_ban())
```

**Вывод консоли:**

```
Anna (user) — бан: False
Root (admin) — бан: True
```

---

### Пример 15: Наследование без переопределения

```python
class Animal:
    def breathe(self):
        return "дышит"

class Fish(Animal):
    pass

nemo = Fish()
print(nemo.breathe())
```

**Вывод консоли:**

```
дышит
```

Потомок **использует** метод родителя как есть.

---

### Пример 16: Исключения — иерархия ошибок

```python
class AppError(Exception):
    """Базовая ошибка приложения."""
    pass

class ValidationError(AppError):
    pass

class NotFoundError(AppError):
    pass

def process(error):
    try:
        raise error
    except AppError as e:
        print(f"Поймали AppError: {type(e).__name__}: {e}")

process(ValidationError("Неверный email"))
process(NotFoundError("Пользователь не найден"))
```

**Вывод консоли:**

```
Поймали AppError: ValidationError: Неверный email
Поймали AppError: NotFoundError: Пользователь не найден
```

---

### Пример 17: Разные `except` — от конкретного к общему

```python
class AppError(Exception):
    pass

class ValidationError(AppError):
    pass

def handle(err):
    try:
        raise err
    except ValidationError as e:
        print("Валидация:", e)
    except AppError as e:
        print("Общая ошибка:", e)

handle(ValidationError("пустое имя"))
handle(AppError("что-то сломалось"))
```

**Вывод консоли:**

```
Валидация: пустое имя
Общая ошибка: что-то сломалось
```

---

### Пример 18: `@classmethod` — фабричный метод

```python
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    @classmethod
    def from_email(cls, email):
        name = email.split("@")[0].capitalize()
        return cls(name, email)

    def __str__(self):
        return f"{self.name} <{self.email}>"

user = User.from_email("anna@mail.com")
print(user)
```

**Вывод консоли:**

```
Anna <anna@mail.com>
```

---

### Пример 19: `@classmethod` наследуется

```python
class User:
    def __init__(self, name):
        self.name = name

    @classmethod
    def create_guest(cls):
        return cls("Guest")

class Admin(User):
    def __str__(self):
        return f"Admin: {self.name}"

admin = Admin.create_guest()
print(admin)
print(type(admin))
```

**Вывод консоли:**

```
Admin: Guest
<class '__main__.Admin'>
```

`create_guest` вернул **Admin**, не User — потому что вызвали `Admin.create_guest()`.

---

### Пример 20: `@staticmethod` — утилита в классе

```python
class StringUtil:
    @staticmethod
    def is_palindrome(text):
        cleaned = text.lower().replace(" ", "")
        return cleaned == cleaned[::-1]

print(StringUtil.is_palindrome("А роза упала на лазор А"))
print(StringUtil.is_palindrome("hello"))
```

**Вывод консоли:**

```
True
False
```

---

### Пример 21: ABC — абстрактный класс

```python
from abc import ABC, abstractmethod

class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, amount):
        pass

class CardPayment(PaymentMethod):
    def pay(self, amount):
        return f"Оплачено картой: {amount} руб."

class CashPayment(PaymentMethod):
    def pay(self, amount):
        return f"Оплачено наличными: {amount} руб."

methods = [CardPayment(), CashPayment()]

for m in methods:
    print(m.pay(1500))
```

**Вывод консоли:**

```
Оплачено картой: 1500 руб.
Оплачено наличными: 1500 руб.
```

---

### Пример 22: Duck typing — без наследования

```python
class Dog:
    def speak(self):
        return "Гав!"

class Speaker:
    def speak(self):
        return "Привет из колонки!"

def announce(obj):
    print(obj.speak())

announce(Dog())
announce(Speaker())
```

**Вывод консоли:**

```
Гав!
Привет из колонки!
```

Нет общего родителя — но оба «крякают» (имеют `speak`).

---

### Пример 23: Композиция vs наследование

```python
# Наследование — is-a
class ElectricCar(Car):
    pass

# Композиция — has-a (правильнее для «двигатель в машине»)
class Engine:
    def __init__(self, power):
        self.power = power

class Car:
    def __init__(self, brand, engine):
        self.brand = brand
        self.engine = engine

    def info(self):
        return f"{self.brand}, {self.engine.power} л.с."

car = Car("Tesla", Engine(300))
print(car.info())
```

**Вывод консоли:**

```
Tesla, 300 л.с.
```

---

### Пример 24: Переопределение с сохранением логики родителя

```python
class Discount:
    def apply(self, price):
        return price

class PercentDiscount(Discount):
    def __init__(self, percent):
        self.percent = percent

    def apply(self, price):
        discounted = price * (1 - self.percent / 100)
        return super().apply(discounted)

class FixedDiscount(Discount):
    def __init__(self, amount):
        self.amount = amount

    def apply(self, price):
        return super().apply(max(0, price - self.amount))

print(PercentDiscount(10).apply(1000))
print(FixedDiscount(200).apply(1000))
```

**Вывод консоли:**

```
900.0
800
```

---

### Пример 25: Игра — юниты с общим базовым классом

```python
class Unit:
    def __init__(self, name, hp, attack):
        self.name = name
        self.hp = hp
        self.attack = attack

    def is_alive(self):
        return self.hp > 0

    def strike(self, target):
        target.hp -= self.attack
        return f"{self.name} бьёт {target.name} на {self.attack}"

class Warrior(Unit):
    def __init__(self, name):
        super().__init__(name, hp=100, attack=20)

class Archer(Unit):
    def __init__(self, name):
        super().__init__(name, hp=60, attack=35)

warrior = Warrior("Conan")
archer = Archer("Legolas")
print(warrior.strike(archer))
print(f"{archer.name} HP: {archer.hp}")
```

**Вывод консоли:**

```
Conan бьёт Legolas на 20
Legolas HP: 40
```

---

### Пример 26: Уведомления — полиморфная отправка

```python
class Notifier:
    def send(self, message):
        raise NotImplementedError

class EmailNotifier(Notifier):
    def send(self, message):
        return f"Email: {message}"

class SMSNotifier(Notifier):
    def send(self, message):
        return f"SMS: {message}"

def notify_all(notifiers, message):
    for n in notifiers:
        print(n.send(message))

notify_all([EmailNotifier(), SMSNotifier()], "Заказ доставлен")
```

**Вывод консоли:**

```
Email: Заказ доставлен
SMS: Заказ доставлен
```

---

### Пример 27: `__mro__` — порядок поиска методов

```python
class A:
    def greet(self):
        return "A"

class B(A):
    def greet(self):
        return "B"

class C(A):
    def greet(self):
        return "C"

class D(B, C):
    pass

print(D.__mro__)
print(D().greet())
```

**Вывод консоли (сокращённо):**

```
(<class 'D'>, <class 'B'>, <class 'C'>, <class 'A'>, <class 'object'>)
B
```

`D` ищет метод сначала в `B`, потом `C`, потом `A`.

---

### Пример 28: Рефакторинг дублирования через базовый класс

```python
# Было — дублирование
# class Dog:
#     def __init__(self, name):
#         self.name = name
# class Cat:
#     def __init__(self, name):
#         self.name = name

# Стало
class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    def speak(self):
        return "Гав!"

class Cat(Animal):
    def speak(self):
        return "Мяу!"

for cls in [Dog, Cat]:
    a = cls("Тест")
    print(a.name, a.speak())
```

**Вывод консоли:**

```
Тест Гав!
Тест Мяу!
```

---

### Пример 29: Проверка типа перед действием

```python
class Animal:
    pass

class Dog(Animal):
    pass

class Cat(Animal):
    pass

def describe(pet):
    if isinstance(pet, Dog):
        return "Собака"
    elif isinstance(pet, Cat):
        return "Кошка"
    elif isinstance(pet, Animal):
        return "Животное"
    return "Неизвестно"

print(describe(Dog()))
print(describe(Cat()))
print(describe(Animal()))
```

**Вывод консоли:**

```
Собака
Кошка
Животное
```

Порядок `if` — от **конкретного** к **общему**.

---

### Пример 30: Переопределение `__init__` с валидацией в потомке

```python
class User:
    def __init__(self, name):
        if not name.strip():
            raise ValueError("Имя пустое")
        self.name = name.strip()

class VIPUser(User):
    def __init__(self, name, level):
        super().__init__(name)
        if level < 1:
            raise ValueError("Уровень >= 1")
        self.level = level

    def __str__(self):
        return f"VIP {self.name} (ур. {self.level})"

print(VIPUser("Anna", 3))
```

**Вывод консоли:**

```
VIP Anna (ур. 3)
```

---

### Пример 31: Документы — базовый класс с `open`

```python
class Document:
    def __init__(self, title, content):
        self.title = title
        self.content = content

    def word_count(self):
        return len(self.content.split())

class PDFDocument(Document):
    def __init__(self, title, content, pages):
        super().__init__(title, content)
        self.pages = pages

    def __str__(self):
        return f"PDF '{self.title}', {self.pages} стр., {self.word_count()} слов"

doc = PDFDocument("Отчёт", "Python это круто", pages=10)
print(doc)
```

**Вывод консоли:**

```
PDF 'Отчёт', 10 стр., 3 слов
```

---

### Пример 32: Транспорт — общий метод `move`

```python
class Transport:
    def __init__(self, speed):
        self.speed = speed

    def move(self, hours):
        return self.speed * hours

class Bike(Transport):
    def __init__(self):
        super().__init__(speed=15)

class Train(Transport):
    def __init__(self):
        super().__init__(speed=120)

for vehicle in [Bike(), Train()]:
    print(f"{type(vehicle).__name__}: {vehicle.move(2)} км за 2 ч")
```

**Вывод консоли:**

```
Bike: 30 км за 2 ч
Train: 240 км за 2 ч
```

---

### Пример 33: Исключение с дополнительным полем

```python
class AppError(Exception):
    def __init__(self, message, code):
        super().__init__(message)
        self.code = code

class NotFoundError(AppError):
    pass

try:
    raise NotFoundError("Пользователь не найден", code=404)
except AppError as e:
    print(f"[{e.code}] {e}")
```

**Вывод консоли:**

```
[404] Пользователь не найден
```

---

### Пример 34: Зоопарк — мини-проект

```python
class Animal:
    def __init__(self, name):
        self.name = name

    def speak(self):
        return "..."

    def __str__(self):
        return self.name

class Dog(Animal):
    def speak(self):
        return "Гав!"

class Cat(Animal):
    def speak(self):
        return "Мяу!"

class Zoo:
    def __init__(self):
        self.animals = []

    def add(self, animal):
        self.animals.append(animal)

    def concert(self):
        for a in self.animals:
            print(f"  {a}: {a.speak()}")

zoo = Zoo()
zoo.add(Dog("Rex"))
zoo.add(Cat("Мурка"))
zoo.add(Dog("Бобик"))
print("=== Концерт зоопарка ===")
zoo.concert()
```

**Вывод консоли:**

```
=== Концерт зоопарка ===
  Rex: Гав!
  Мурка: Мяу!
  Бобик: Гав!
```

---

### Пример 35: Зарплатная ведомость — полиморфный `total_pay`

```python
class Employee:
    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    def total_pay(self):
        return self.salary

class Contractor(Employee):
    def __init__(self, name, salary, project_fee):
        super().__init__(name, salary)
        self.project_fee = project_fee

    def total_pay(self):
        return super().total_pay() + self.project_fee

payroll = [
    Employee("Anna", 50000),
    Contractor("Bob", 30000, project_fee=20000),
    Employee("Vika", 55000),
]

print("=== Зарплата ===")
for e in payroll:
    print(f"  {e.name}: {e.total_pay()} руб.")
print("Итого:", sum(e.total_pay() for e in payroll))
```

**Вывод консоли:**

```
=== Зарплата ===
  Anna: 50000 руб.
  Bob: 50000 руб.
  Vika: 55000 руб.
Итого: 155000
```

---

### Пример 36: Пакет с иерархией — связь с главой 10

**`shapes/base.py`:**

```python
class Shape:
    def area(self):
        raise NotImplementedError
```

**`shapes/rect.py`:**

```python
from shapes.base import Shape

class Rectangle(Shape):
    def __init__(self, w, h):
        self.w, self.h = w, h

    def area(self):
        return self.w * self.h
```

**`main.py`:**

```python
from shapes.rect import Rectangle

shapes = [Rectangle(3, 4), Rectangle(5, 2)]
for s in shapes:
    print(f"Площадь: {s.area()}")
```

**Вывод консоли:**

```
Площадь: 12
Площадь: 10
```

---

### Пример 37: `super()` в цепочке override

```python
class A:
    def process(self, x):
        return x

class B(A):
    def process(self, x):
        return super().process(x) + 10

class C(B):
    def process(self, x):
        return super().process(x) * 2

print(C().process(5))
```

**Вывод консоли:**

```
30
```

Цепочка: `C` → `B` → `A`: `(5 + 10) * 2 = 30`.

---

### Пример 38: Полный пайплайн — магазин с иерархией товаров

```python
class Product:
    def __init__(self, name, price):
        self.name = name
        self.price = price

    def final_price(self):
        return self.price

    def __str__(self):
        return f"{self.name}: {self.final_price()} руб."

class DiscountedProduct(Product):
    def __init__(self, name, price, discount_percent):
        super().__init__(name, price)
        self.discount_percent = discount_percent

    def final_price(self):
        base = super().final_price()
        return base * (1 - self.discount_percent / 100)

class Cart:
    def __init__(self):
        self.items = []

    def add(self, product):
        self.items.append(product)

    def total(self):
        return sum(p.final_price() for p in self.items)

cart = Cart()
cart.add(Product("Книга", 1000))
cart.add(DiscountedProduct("Курс", 5000, discount_percent=20))
cart.add(Product("Ручка", 50))

print("=== Корзина ===")
for item in cart.items:
    print(f"  {item}")
print(f"ИТОГО: {cart.total():.0f} руб.")
```

**Вывод консоли:**

```
=== Корзина ===
  Книга: 1000 руб.
  Курс: 4000.0 руб.
  Ручка: 50 руб.
ИТОГО: 5050 руб.
```

`final_price()` — полиморфный: у `Product` и `DiscountedProduct` разная логика, один интерфейс.

---

### Пример 39: Разбор построчно — что происходит при создании `Dog`

```python
class Animal:
    def __init__(self, name):
        print(f"  Animal.__init__: name={name}")
        self.name = name

class Dog(Animal):
    def __init__(self, name, breed):
        print(f"  Dog.__init__ начало: breed={breed}")
        super().__init__(name)
        self.breed = breed
        print(f"  Dog.__init__ конец")

print("=== Создаём Dog ===")
rex = Dog("Rex", "овчарка")
print(f"Итог: {rex.name}, {rex.breed}")
```

**Вывод консоли:**

```
=== Создаём Dog ===
  Dog.__init__ начало: breed=овчарка
  Animal.__init__: name=Rex
  Dog.__init__ конец
Итог: Rex, овчарка
```

**Порядок:** `Dog.__init__` → `super().__init__` → `Animal.__init__` → обратно в `Dog.__init__`.

---

### Пример 40: Ошибка — забыли `super().__init__`

```python
class Animal:
    def __init__(self, name):
        self.name = name

class Dog(Animal):
    def __init__(self, name, breed):
        # super().__init__(name)  ← ЗАБЫЛИ!
        self.breed = breed

rex = Dog("Rex", "овчарка")
try:
    print(rex.name)
except AttributeError as e:
    print("AttributeError:", e)
    print("Фикс: вызови super().__init__(name)")
```

**Вывод консоли:**

```
AttributeError: 'Dog' object has no attribute 'name'
Фикс: вызови super().__init__(name)
```

---

### Пример 41: `type()` vs `isinstance()` — в чём разница

```python
class Animal:
    pass

class Dog(Animal):
    pass

rex = Dog()

print("type(rex) == Dog:     ", type(rex) == Dog)
print("type(rex) == Animal:  ", type(rex) == Animal)
print("isinstance(rex, Dog): ", isinstance(rex, Dog))
print("isinstance(rex, Animal):", isinstance(rex, Animal))
```

**Вывод консоли:**

```
type(rex) == Dog:      True
type(rex) == Animal:   False
isinstance(rex, Dog):  True
isinstance(rex, Animal): True
```

**Правило:** для иерархий — **только** `isinstance`.

---

### Пример 42: Миксин — добавление «способности» (упрощённо)

```python
class Swimmer:
    def swim(self):
        return f"{self.name} плывёт"

class Animal:
    def __init__(self, name):
        self.name = name

class Duck(Animal, Swimmer):
    def speak(self):
        return "Кря!"

duck = Duck("Дональд")
print(duck.speak())
print(duck.swim())
```

**Вывод консоли:**

```
Кря!
Дональд плывёт
```

`Duck` — животное **и** пловец. Множественное наследование — знай, что есть; не злоупотребляй.

---

### Пример 43: Полиморфная функция `total_area` — как в реальном коде

```python
class Shape:
    def area(self):
        raise NotImplementedError

class Rectangle(Shape):
    def __init__(self, w, h):
        self.w, self.h = w, h

    def area(self):
        return self.w * self.h

class Triangle(Shape):
    def __init__(self, base, height):
        self.base = base
        self.height = height

    def area(self):
        return self.base * self.height / 2

def total_area(shapes):
    return sum(s.area() for s in shapes)

shapes = [Rectangle(4, 5), Triangle(6, 4), Rectangle(2, 3)]
print("Суммарная площадь:", total_area(shapes))
```

**Вывод консоли:**

```
Суммарная площадь: 32.0
```

Функция `total_area` **не знает** про Rectangle/Triangle — только про `.area()`.

---

### Пример 44: Переопределение с условием — `Manager` одобряет больше

```python
class Approver:
    def __init__(self, name, limit):
        self.name = name
        self.limit = limit

    def can_approve(self, amount):
        return amount <= self.limit

    def __str__(self):
        return f"{self.name} (лимит {self.limit})"

class SeniorApprover(Approver):
    def __init__(self, name):
        super().__init__(name, limit=10000)

    def can_approve(self, amount):
        if amount <= 50000:
            return True
        return super().can_approve(amount)

staff = [Approver("Anna", 5000), SeniorApprover("Director")]

for person in staff:
    for amount in [3000, 8000, 30000]:
        ok = person.can_approve(amount)
        print(f"  {person}: {amount} руб. → {'OK' if ok else 'нет'}")
```

**Вывод консоли:**

```
  Anna (лимит 5000): 3000 руб. → OK
  Anna (лимит 5000): 8000 руб. → нет
  Anna (лимит 5000): 30000 руб. → нет
  Director (лимит 10000): 3000 руб. → OK
  Director (лимит 10000): 8000 руб. → OK
  Director (лимит 10000): 30000 руб. → OK
```

---

### Пример 45: Полный пайплайн — система пользователей с ролями

```python
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email

    def permissions(self):
        return ["read"]

    def __str__(self):
        return f"{self.name} ({', '.join(self.permissions())})"

class Editor(User):
    def permissions(self):
        base = super().permissions()
        return base + ["write"]

class Admin(User):
    def permissions(self):
        base = super().permissions()
        return base + ["write", "delete", "ban"]

def show_access(user):
    print(f"  {user}")
    for action in ["read", "write", "delete", "ban"]:
        allowed = action in user.permissions()
        print(f"    {action}: {'✓' if allowed else '✗'}")

users = [User("Guest", "g@mail.com"), Editor("Anna", "a@mail.com"), Admin("Root", "r@admin.com")]

print("=== Права доступа ===")
for u in users:
    show_access(u)
```

**Вывод консоли:**

```
=== Права доступа ===
  Guest (read)
    read: ✓
    write: ✗
    delete: ✗
    ban: ✗
  Anna (read, write)
    read: ✓
    write: ✓
    delete: ✗
    ban: ✗
  Root (read, write, delete, ban)
    read: ✓
    write: ✓
    delete: ✓
    ban: ✓
```

`permissions()` — полиморфный. `show_access` работает с **любым** `User`.

---

## Шпаргалка

```python
class Parent:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return "Привет"

class Child(Parent):
    def __init__(self, name, age):
        super().__init__(name)
        self.age = age

    def greet(self):              # override
        return super().greet() + f", мне {self.age}"

isinstance(child, Parent)         # True
issubclass(Child, Parent)         # True
```

| Термин | Значение |
|--------|----------|
| Наследование | Потомок получает код родителя |
| `super()` | Вызов метода родителя |
| Override | Переопределение метода в потомке |
| Полиморфизм | Один интерфейс — разное поведение |
| is-a | «Является» → наследование |
| has-a | «Содержит» → композиция |
| Duck typing | Важны методы, не иерархия |
| ABC | Абстрактный класс-шаблон |

### Таблица: когда наследовать, когда нет

| Ситуация | Решение |
|----------|---------|
| Собака — животное | `class Dog(Animal)` |
| Машина имеет двигатель | Композиция |
| Общий `__init__` у 3 классов | Базовый класс |
| Разное `speak()` у животных | Override + полиморфизм |
| Альтернативный конструктор | `@classmethod` |
| Утилита без `self` | `@staticmethod` |

### Таблица: override vs не трогать

| Метод в родителе | Что делать в потомке |
|------------------|----------------------|
| `__init__` | Почти всегда `super().__init__` + свои поля |
| `speak()` — разное поведение | Override полностью |
| `breathe()` — то же | Не трогать — наследуется |
| `log()` — дополнить | Override + `super().log()` |
| `area()` — обязателен | Реализовать (или ABC) |

### Схема: цепочка вызова `super()`

```
C.__init__
  └→ super() → B.__init__
                  └→ super() → A.__init__
                                  └→ object
```

---

## FAQ начинающего

**В: Наследование — это копирование кода?**  
Нет. Потомок **ссылается** на родителя. Один `Animal`, много `Dog`.

**В: Зачем `super()`?**  
Чтобы не дублировать логику родителя и правильно расширять методы.

**В: Чем полиморфизм отличается от наследования?**  
Наследование — **механизм**. Полиморфизм — **результат**: один вызов — разное поведение.

**В: `Dog` — это `Animal`?**  
Для кода — да: `isinstance(dog, Animal)` → True. Для здравого смысла — собака **вид** животного.

**В: Обязательно ли наследовать для полиморфизма?**  
В Python нет. Достаточно одинаковых методов (duck typing).

**В: Когда не наследовать?**  
Если связь не is-a. Не делай `class Car(Engine)`.

**В: Что переопределять?**  
То, что должно работать **по-другому** в потомке. Остальное наследуется.

**В: `classmethod` vs обычный метод?**  
`classmethod` — для фабрик: `User.from_email(...)`. Обычный — работа с `self`.

**В: `staticmethod` — зачем, если есть функция?**  
Группировка: утилита логически принадлежит классу.

**В: ABC — обязателен?**  
Нет. Удобен, когда хотите **заставить** потомков реализовать метод.

**В: Множественное наследование на Junior?**  
Знай, что бывает. Не усложняй без нужды.

**В: Исключения — как наследовать?**  
От `Exception` → свои типы → ловить родителя `except AppError`.

**В: Наследование = копия объекта?**  
Нет. Потомок — **новый класс**. `rex = Dog()` — новый объект.

**В: Можно ли наследовать от двух классов?**  
Да: `class Duck(Animal, Swimmer)`. Осторожно — сложнее MRO.

**В: Что такое MRO?**  
Порядок поиска методов: `Class.__mro__`. Слева направо в объявлении.

**В: `super()` без аргументов — куда идёт?**  
К **следующему** классу по MRO, не обязательно к прямому родителю.

**В: Переопределил `__init__` — родительский вызовется сам?**  
**Нет.** Только если **ты** вызовешь `super().__init__()`.

**В: Полиморфизм в одном предложении?**  
Одна функция вызывает `.method()`, а результат зависит от **реального** типа объекта.

**В: Зачем ABC, если есть `NotImplementedError`?**  
ABC **запрещает** создать объект без реализации. Жёстче.

**В: Django `models.Model` — это наследование?**  
Да. Твоя модель — потомок, получает ORM-магию от родителя.

**В: Как тренироваться?**  
Возьми 3 похожих класса с дублированием → вынеси в родителя → override одного метода → цикл полиморфизма.

---

### Частые баги

```python
# БАГ — забыли super().__init__
class Child(Parent):
    def __init__(self, name, age):
        self.age = age    # self.name нет!

# БАГ — isinstance в неправильном порядке
if isinstance(x, Animal):
    ...
elif isinstance(x, Dog):    # до Dog никогда не дойдёт!
    ...

# БАГ — наследование вместо композиции
class Car(Engine):    # машина НЕ является двигателем
    pass

# FIX
class Child(Parent):
    def __init__(self, name, age):
        super().__init__(name)
        self.age = age
```

### Типичные ошибки

| Ошибка | Причина | Решение |
|--------|---------|---------|
| `AttributeError` на поле родителя | Нет `super().__init__` | Вызови `super().__init__(...)` |
| Потомок не тот в `isinstance` | Проверяешь родителя раньше потомка | Сначала конкретный тип |
| `NotImplementedError` | Не реализован abstract метод | Реализуй в потомке |
| Родительский метод не вызывается | Override без `super()` | Добавь `super().method()` |

### Антипаттерны — не делай так

```python
# 1. Глубокая иерархия без нужды
class A: pass
class B(A): pass
class C(B): pass
class D(C): pass
class E(D): pass    # плохо читать

# 2. Наследование ради одной функции
class Utils(Helper):    # лучше просто функция helper()

# 3. if type(x) == Dog вместо isinstance
if type(pet) == Dog:    # не учитывает подклассы

# 4. Пустой потомок «на будущее»
class Dog(Animal):
    pass    # OK если реально будет расширение; иначе — YAGNI
```

---

## Домашнее задание

**Файл:** `homework_12.py`

> Ниже — **ожидаемый результат** для самопроверки (как в главах 13–16).  
> **Мостик:** `@classmethod` / `@staticmethod` — декораторы, разбор в **главе 14**.  
> **Маршрут:** для ДЗ 1–5 хватит примеров **1–12**, **11**, **39–40**; 45 примеров — не обязательно все.

### Задача 1 — Лёгкая
`Animal(name)` и `Dog(Animal)` с переопределённым `speak()`.  
Создай 2 собаки, выведи `speak()` и `isinstance(dog, Animal)`.

**Должно получиться:** `Гав!` (или свой звук), `True` для `isinstance`.

---

### Задача 2 — Лёгкая
`Person(name)` и `Student(Person)` с полем `grade`.  
`super().__init__`, `__str__` у обоих.

**Должно получиться:** `Student(name='Anna', grade=5)` или похожий `__str__`.

---

### Задача 3 — Средняя
`Shape` с методом `area()` (заглушка `NotImplementedError`).  
`Rectangle` и `Circle` — реализуй `area()`.  
Цикл по списку фигур, выведи площади.

**Должно получиться:** для `Rectangle(4, 5)` → `20`, для `Circle(r=1)` → около `3.14`.

<details>
<summary>Подсказка</summary>

См. Пример 11.

</details>

---

### Задача 4 — Средняя
`BankAccount` и `SavingsAccount` с `add_interest()`.  
Протестируй депозит + начисление процентов.

---

### Задача 5 — Средняя
`User` с `can_edit() → False` и `Admin(User)` с `can_edit() → True`.  
Список из 3 пользователей (смешанных), цикл с выводом прав.

---

### Задача 6 — Сложная
**Зоопарк** (Пример 34): классы `Animal`, `Dog`, `Cat`, `Zoo` с `add`, `concert`.  
Добавь `Bird` с `speak() → "Чирик!"`.

---

### Задача 7 — Сложная
Иерархия исключений: `AppError`, `ValidationError`, `AuthError`.  
Функция `handle(action)` симулирует 3 ошибки через `try/except AppError`.

---

### Задача 8 — Сложная
`Employee`, `Manager` (бонус), `Contractor` (project_fee) — полиморфный `total_pay()`.  
Зарплатная ведомость из 5 человек + итог.

---

### Задача 9 — Сложная (бонус)
`PaymentMethod` (ABC) + `CardPayment` + `CashPayment`.  
Функция `checkout(methods, amount)` вызывает `pay()` у каждого (демо).

---

### Задача 10 — Сложная (бонус)
`Product` и `DiscountedProduct` с `final_price()` + `Cart` (Пример 38).  
Добавь `PremiumProduct` с наценкой +10%.

---

### Задача 11 — Сложная (бонус)
`@classmethod User.from_email` и `Admin(User)` с `from_email`, возвращающим `Admin`.  
Покажи `type(Admin.from_email("root@admin.com"))`.

---

### Задача 12 — Сложная (бонус)
Пакет `employees/` с `base.py`, `staff.py`, `main.py`.  
Минимум 2 уровня наследования. Демо + `README.txt`.

---

### Задача 13 — Средняя (доп.)
Напиши `speak_animal(kind, name)` с if/elif (как в теории).  
Потом перепиши на классы `Dog`, `Cat`, `Bird` + цикл.  
Покажи, что второй вариант проще расширять.

---

### Задача 14 — Сложная (доп.)
Система ролей как Пример 45: `User`, `Editor`, `Admin` с `permissions()`.  
Функция `can(user, action)` → bool. Таблица прав для 3 пользователей.

<details>
<summary>Подсказка</summary>

`return action in user.permissions()` — полиморфизм сделает остальное.

</details>

---

### Задача 15 — Сложная (доп., бонус)
**Фигуры + отчёт:** `Shape`, `Rectangle`, `Triangle`, `Circle` + `total_area(shapes)`.  
Выведи каждую площадь и сумму. Минимум 4 фигуры в списке.

---

### Как сдавать

- `homework_12.py` или папка `homework_12/`
- Частями: 1–5, 6–10, 11–15
- Вывод `print` / тестов для каждой задачи

**Критерии:**
- `super().__init__` в потомках с расширенным `__init__`
- Полиморфизм — хотя бы один цикл по списку разных подклассов
- `isinstance` / `issubclass` — где уместно
- Не путай наследование и композицию
- Имена классов — `CapWords`

---

**Сделай задачи сам и пришли код на проверку. После проверки — Глава 13: *ООП — инкапсуляция, property, магические методы*.**

---
Конец главы.