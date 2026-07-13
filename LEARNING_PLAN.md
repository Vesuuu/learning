# 🐍 План обучения Python: от ООП до Junior Developer

> **Персональная версия** — составлена под твои ответы. Обновлено: 13 июля 2026.

---

## 👤 Твой профиль

| Параметр | Значение |
|----------|----------|
| **Уровень** | Базовый синтаксис + начало ООП (`__init__`, классы, методы) |
| **Наследование** | Видел `class Child(Parent)`, но **`super()` путает** |
| **Цель после Junior** | Пока не определился — **универсальная база** |
| **Финальный проект** | Текстовая RPG «Подземелье» |
| **Темп** | **8–12 часов в неделю** (~3–4 месяца) |
| **Стиль обучения** | **Мелкие шаги + много мини-заданий** |

### Зоны роста (твои слова)

- [ ] Наследование и `super()`
- [ ] Инкапсуляция (`_`, `__`, `@property`)
- [ ] Полиморфизм
- [ ] Магические методы
- [ ] `@classmethod` vs `@staticmethod`
- [ ] Логика задач (как разбить на шаги)
- [ ] Отладка кода
- [ ] Структура проекта
- [ ] Файлы, JSON, SQLite
- [ ] Git / GitHub
- [ ] Типы и аннотации
- [ ] Английская документация и ошибки
- [ ] Мотивация / не бросать на полпути

> Это нормально, что список длинный. План **специально замедлен** и разбит на микро-шаги — не пытайся закрыть всё за неделю.

---

## Как пользоваться этим планом

1. Проходи модули **строго по порядку**
2. Каждая тема = **📖 урок → теория → микро-задание → практика → чеклист**
3. **Уроки:** [`EXPLAINED.md`](EXPLAINED.md) — читай **до** практики («что что делает»)
4. Не переходи дальше, пока **все пункты чеклиста** не закрыты
5. На одну тему — **3–5 дней**
6. **Одна папка:** `python-oop-journey/`
7. Застрял > 40 мин — стоп, спроси меня или гугли
8. **Pomodoro:** 25 мин учёба → 5 мин перерыв

### Анти-прокрастинация (коротко)

- Открывай план → делай **только одно микро-задание**, не «весь модуль»
- Каждый вечер: **минимум 1 коммит** или 1 файл с кодом — даже 10 строк считаются
- Веди файл `PROGRESS.md` — 2 строки: что сделал сегодня, что завтра
- Если пропустил 3+ дня — не начинай сначала, просто продолжай с последней галочки

---

# 📊 Общий прогресс

- [ ] Модуль 0: Базовые навыки разработчика (отладка, типы, английский)
- [ ] Модуль 1: Закрепление ООП и «Три Кита»
- [ ] Модуль 2: Продвинутое ООП в Python
- [ ] Модуль 3: Инструменты экосистемы
- [ ] Модуль 4: Работа с данными и файлами
- [ ] Модуль 5: RPG «Подземелье» — финальный проект

---

# Модуль 0: Базовые навыки разработчика

**Срок:** 1 неделя (параллельно с Модулем 1, по 30 мин в день)  
**Цель:** закрыть фоновые дыры — отладка, типы, чтение ошибок — чтобы они не мешали ООП

> Проходи **вместе** с Модулем 1, не вместо него. Каждый день: 1 час ООП + 30 мин Модуль 0.

---

## Тема 0.1: Как читать ошибки Python

> 📖 **Урок:** [Ошибки Python — что происходит](EXPLAINED.md#ошибки-python--что-происходит-когда-код-падает)

### 💡 Простыми словами

Когда код ломается, Python не молчит — он показывает **traceback** (цепочку вызовов). **Последняя строка** — самое важное: тип ошибки и суть. `line 25` — номер строки, куда смотреть. Не пугайся длинного текста — читай **снизу**.

### Теория

- **Traceback** — стек вызовов снизу вверх; **последняя строка** = тип ошибки
- Частые ошибки: `TypeError`, `AttributeError`, `ValueError`, `NameError`, `IndentationError`
- `line N` — номер строки, где упало
- Ошибки в терминале почти всегда **на английском** — это норма

### Микро-задания (по 10–15 мин)

- [ ] **М0.1a** — специально сломай код: вызови метод у `None` → прочитай `AttributeError`
- [ ] **М0.1b** — передай `str` вместо `int` → прочитай `TypeError`
- [ ] **М0.1c** — скопируй ошибку в Google **на английском** (первые 2 строки traceback)

### Что гуглить

| Русский | English |
|---------|---------|
| как читать traceback Python | Python traceback explained |
| TypeError AttributeError Python | Python common errors |

---

## Тема 0.2: Отладка без паники

> 📖 **Урок:** [print и breakpoint](EXPLAINED.md#print-для-отладки--что-делает)

### 💡 Простыми словами

**Отладка** = найти, **где** программа делает не то. `print` — «посмотри значение здесь». `breakpoint()` — «замри программу, покажи все переменные». Не переписывай весь код — меняй по одной строке и смотри результат.

### Теория

- **`print()`-отладка** — `print(f"DEBUG: health={self._health}")` перед подозрительной строкой
- **`repr()` vs `str()`** — `repr` показывает «как в коде»
- **Точечная проверка** — не переписывай всё, меняй по одной строке
- **`breakpoint()`** — встроенная отладка (Python 3.7+); в Cursor/VS Code можно ставить красные точки

### Микро-задания

- [ ] **М0.2a** — в классе `Character` добавь `print` в `take_damage` и проследи, как меняется HP
- [ ] **М0.2b** — поставь `breakpoint()` в `attack()` и посмотри переменные в отладчике
- [ ] **М0.2c** — найди баг: `health` уходит в минус — исправь **одной** проверкой

### Что гуглить

| Русский | English |
|---------|---------|
| отладка Python print debug | Python debugging print |
| breakpoint Python | Python breakpoint debugger |

---

## Тема 0.3: Типы и аннотации (минимум для Junior)

### Теория

- **Аннотации** — подсказки типов: `name: str`, `health: int`, `-> bool`
- **`list[str]`** — список строк (Python 3.9+)
- **`dict[str, int]`** — словарь
- **`Optional[str]`** — строка или `None` (нужен `from typing import Optional`)
- Типы **не ломают** код при ошибке — это подсказки для тебя и IDE
- IDE подсказывает автодополнение, если типы указаны

### Микро-задания

- [ ] **М0.3a** — добавь типы во все методы `Character`
- [ ] **М0.3b** — напиши `def get_alive(fighters: list[Character]) -> list[Character]:`
- [ ] **М0.3c** — наведи мышку на переменную в Cursor — посмотри, что подсказывает IDE

### Что гуглить

| Русский | English |
|---------|---------|
| аннотации типов Python | Python type hints tutorial |
| list str typing Python | Python typing list dict |

---

## Тема 0.4: Как читать английскую документацию

### Теория

- Словарь: `method` = метод, `return` = возвращает, `raise` = бросает исключение, `argument` = аргумент
- Читай **сигнатуру** функции первой: `def name(arg: type) -> type`
- Секция **Examples** / **Usage** — самое полезное
- Официальная дока: https://docs.python.org/3/ — закладка в браузер
- Не переводи всё — ищи **пример кода** и повтори его

### Микро-задания

- [ ] **М0.4a** — открой docs.python.org → `json` → найди `dump` и `load`
- [ ] **М0.4b** — прочитай только **первый пример** в доке `pathlib.Path`
- [ ] **М0.4c** — выпиши 10 английских слов из доки с переводом в `PROGRESS.md`

### Чеклист Модуля 0

- [ ] Умею прочитать traceback и найти строку с ошибкой
- [ ] Отлаживаю через `print` и `breakpoint()`
- [ ] Добавил типы хотя бы в один класс
- [ ] Открыл официальную документацию и нашёл пример

---

# Модуль 1: Закрепление ООП и «Три Кита»

**Срок:** 3–4 недели (не торопись — наследование твоя главная цель)  
**Цель:** понять наследование, инкапсуляцию и полиморфизм через **мелкие победы**, а не один большой рывок

**Сквозная линия:** все задания — кусочки будущей RPG. К концу модуля у тебя уже будет мини-бой, не жди Модуль 5.

---

## Тема 1.1: Классы и объекты — повторение с углублением

> 📖 **Уроки:** [Класс](EXPLAINED.md#класс--что-это-и-что-делает) · [`__init__`](EXPLAINED.md#__init__--что-делает-при-создании) · [`self`](EXPLAINED.md#self--что-это-на-самом-деле) · [Метод](EXPLAINED.md#метод--что-делает)

### 💡 Простыми словами

**Класс** — чертёж. **Объект** — экземпляр по чертежу. **`__init__`** — настройка при создании: `hero = Character("Грок", 100)` автоматически вызывает `__init__`. **`self`** — «этот конкретный герой» внутри метода. **Метод** — действие объекта: `hero.attack(enemy)`.

```python
# Запусти и пошагово прочитай комментарии:
class Character:
    def __init__(self, name: str, health: int):
        self.name = name      # поле ЭТОГО героя
        self._health = health

    def is_alive(self) -> bool:
        return self._health > 0  # self = тот, кто вызвал метод

hero = Character("Грок", 100)   # создали объект
hero.is_alive()                 # True — вызвали метод у hero
```

### Теория: что именно нужно понять

- **Класс (class)** — чертёж (шаблон), по которому создаются объекты
- **Объект (object) / экземпляр (instance)** — конкретная «вещь», созданная по чертежу
- **Атрибут (attribute)** — переменная, принадлежащая объекту (`self.name`)
- **Метод (method)** — функция внутри класса, всегда принимает `self` первым аргументом
- **Конструктор `__init__`** — метод, который вызывается автоматически при создании объекта
- **`self`** — ссылка на текущий экземпляр класса
- **Аннотации типов в классах** — `def __init__(self, name: str, age: int)`
- **Атрибуты экземпляра vs атрибуты класса** — `self.x` живёт в объекте, `class_var` живёт в классе и общий для всех

### Микро-задания (делай по порядку, каждое — отдельный файл или коммит)

- [ ] **М1.1a** — создай `character_draft.py`: класс с `__init__` и `name` (5 строк)
- [ ] **М1.1b** — добавь `health` и `attack_power`
- [ ] **М1.1c** — добавь `is_alive() -> bool`
- [ ] **М1.1d** — добавь `take_damage(amount: int) -> None`
- [ ] **М1.1e** — добавь `attack(target: "Character") -> None` (урон = `attack_power`)

### Основная практика

Создай `python-oop-journey/module_01/character.py`:

- Поля: `name`, `health`, `attack_power`
- Методы: `is_alive()`, `take_damage(amount)`, `attack(target)`
- В `main.py` создай 2 персонажей и проведи 3 раунда боя в консоли

### Что гуглить

| Русский | English |
|---------|---------|
| классы и объекты Python | Python classes and objects |
| конструктор __init__ Python | Python __init__ constructor |
| self в Python ООП | Python self in OOP |
| атрибуты экземпляра и класса | instance vs class attributes Python |

### Чеклист

- [ ] Понимаю разницу между классом и объектом
- [ ] Могу создать класс с `__init__` и несколькими методами
- [ ] Понимаю, зачем нужен `self`
- [ ] Выполнил практику с классом `Character`

---

## Тема 1.2: Инкапсуляция — сокрытие данных

> 📖 **Уроки:** [`_` и `__`](EXPLAINED.md#_health-и-__luck--что-реально-делает-python) · [`@property`](EXPLAINED.md#property--что-делает)

### 💡 Простыми словами

**Инкапсуляция** = данные + правила в одном месте. Не даём менять HP как попало — только через `take_damage()` и `heal()`. `_health` — «внутреннее, не трогай». `@property` — читать HP как `hero.health`, но внутри работает метод.

```python
hero._health = -100   # технически можно — но ты обходишь логику
hero.take_damage(20)  # правильно — метод сам не уйдёт ниже 0
print(hero.health)    # property — красиво и безопасно
```

### Теория: что именно нужно понять

- **Инкапсуляция (encapsulation)** — объединение данных и методов в одном классе + контроль доступа к данным
- **Публичный атрибут** — доступен напрямую: `obj.name`
- **Защищённый атрибут `_name`** — соглашение: «не трогай снаружи, это внутреннее»
- **Приватный атрибут `__name`** — name mangling: Python переименует в `_ClassName__name`
- **Почему не стоит менять `obj.health = -100` напрямую** — нарушается логика объекта
- **Геттер (getter)** — метод/свойство для чтения значения
- **Сеттер (setter)** — метод/свойство для записи значения с проверкой
- **`@property`** — превращает метод в «атрибут», доступный как `obj.health`, но с логикой внутри
- **`@имя.setter`** — сеттер для property

### Микро-задания

- [ ] **М1.2a** — переименуй `health` → `_health`, добавь `@property def health(self)`
- [ ] **М1.2b** — попробуй снаружи: `hero._health = 999` — пойми, почему это плохо (работает, но нарушает правило)
- [ ] **М1.2c** — добавь `heal(amount)` с проверкой: нельзя вылечить мёртвого
- [ ] **М1.2d** — в `take_damage`: `self._health = max(0, self._health - amount)`
- [ ] **М1.2e** — добавь `__luck` (приватный) и убедись, что `hero.__luck` снаружи не работает

### Основная практика

Доработай `Character`:

- `_health` + `@property health` (только чтение)
- `heal(amount)` вместо прямого `hero.health = ...`
- `take_damage` не опускает HP ниже 0
- Напиши **в комментарии** своими словами: зачем `@property`, если `_health` и так можно менять

### Что гуглить

| Русский | English |
|---------|---------|
| инкапсуляция Python | Python encapsulation |
| приватные атрибуты _ и __ Python | Python private attributes underscore |
| property геттер сеттер Python | Python @property getter setter |
| name mangling Python | Python name mangling double underscore |

### Чеклист

- [ ] Понимаю разницу между `_attr` и `__attr`
- [ ] Знаю, зачем нужна инкапсуляция
- [ ] Умею использовать `@property` и `@имя.setter`
- [ ] Выполнил практику с защищённым `health`

---

## Тема 1.3: Наследование — повторное использование кода

> 📖 **Уроки:** [Наследование](EXPLAINED.md#наследование--что-делает) · [**super()**](EXPLAINED.md#super--что-делает-главное-для-тебя)

### 💡 Простыми словами

**Наследование** = дочерний класс **получает** методы родителя. `Warrior(Character)` — воин **является** персонажем. **`super().__init__(...)`** = «сначала настрой родительские поля (`name`, `_health`), потом добавь свои (`armor`)». Без `super()` — объект неполный → `AttributeError`.

### Теория: что именно нужно понять

- **Наследование (inheritance)** — один класс берёт поля и методы другого
- **Родительский класс / базовый класс (parent / base class)** — от кого наследуем
- **Дочерний класс / подкласс (child / subclass)** — кто наследует
- **Синтаксис:** `class Warrior(Character):`
- **`super()`** — вызов метода родительского класса
- **Переопределение метода (method overriding)** — дочерний класс пишет свою версию метода
- **`isinstance(obj, Class)`** — проверка типа объекта
- **Цепочка наследования** — `Animal → Mammal → Dog`
- **Когда наследование уместно** — «является» (Warrior **является** Character)
- **Когда наследование плохо** — если связь не «является», а «имеет» (лучше композиция)

### 🔴 Блок «Разбор super()» — пройди ДО основной практики

Ты сказал, что `super()` путает. Вот шпаргалка:

```python
class Character:
    def __init__(self, name: str, health: int):
        self.name = name
        self._health = health

class Warrior(Character):
    def __init__(self, name: str, health: int, armor: int):
        super().__init__(name, health)  # сначала родитель!
        self.armor = armor
```

**`super().__init__(...)`** = «вызови конструктор родителя, чтобы не дублировать код».

### Микро-задания по super() (обязательно все)

- [ ] **М1.3a** — только 2 класса: `Animal` → `Dog`, в `Dog.__init__` вызови `super().__init__("dog")`
- [ ] **М1.3b** — добавь `print` в `Animal.__init__` и `Dog.__init__` — посмотри **порядок** вызова
- [ ] **М1.3c** — `Warrior` наследует `Character`, добавь поле `armor`, `super()` в конструкторе
- [ ] **М1.3d** — переопредели `attack()` в `Warrior` — сначала `super().attack(target)`, потом +5 урона
- [ ] **М1.3e** — нарисуй на бумаге цепочку: `Warrior → Character → object`

### Основная практика

Создай `python-oop-journey/module_01/heroes.py`:

```
Character (базовый)
├── Warrior  — heavy_strike(), бонус к урону
├── Mage     — cast_spell(), урон по области
└── Archer   — критический удар 30%
```

- Общая логика в `Character`
- В каждом `__init__` дочернего класса — **`super().__init__(...)` первой строкой**
- У каждого подкласса — свой уникальный метод атаки

### Типичные ошибки с super()

| Ошибка | Что происходит |
|--------|----------------|
| Забыл `super().__init__()` | У объекта нет полей родителя → `AttributeError` |
| `super()` после своей логики | Родительские поля инициализируются поздно |
| Дублируешь код родителя вместо `super()` | Наследование бессмысленно |

### Что гуглить

| Русский | English |
|---------|---------|
| наследование классов Python | Python class inheritance |
| super() Python пример | Python super() example |
| переопределение методов Python | Python method overriding |
| isinstance Python | Python isinstance check type |

### Чеклист

- [ ] Понимаю, что такое наследование и зачем оно нужно
- [ ] Умею использовать `super()`
- [ ] Могу переопределить метод в дочернем классе
- [ ] Создал иерархию Warrior / Mage / Archer

---

## Тема 1.4: Полиморфизм — один интерфейс, разное поведение

> 📖 **Урок:** [Полиморфизм](EXPLAINED.md#полиморфизм--что-делает)

### 💡 Простыми словами

**Полиморфизм** = один вызов `fighter.attack(enemy)`, но Warrior бьёт иначе, чем Mage. Тебе **не нужно** `if warrior ... elif mage ...` — цикл сам вызывает нужную версию. Python смотрит на **объект**, не на название класса.

```python
for fighter in team:
    fighter.attack(enemy)  # у каждого своя attack() — вот весь полиморфизм
```

### Теория: что именно нужно понять

- **Полиморфизм (polymorphism)** — разные объекты реагируют на один и тот же вызов по-разному
- **Пример:** `character.attack(target)` — у Warrior, Mage и Archer разная реализация
- **Утиная типизация (duck typing)** — «если ходит как утка и крякает как утка — это утка»
- В Python не обязательно наследовать один класс — достаточно иметь нужный метод
- **Полиморфизм через наследование** — переопределённые методы
- **Полиморфизм через общий интерфейс** — все объекты в списке имеют метод `attack()`
- **Функция, принимающая разные типы:**

```python
def battle(fighters: list):
    for fighter in fighters:
        fighter.attack(target)
```

### Микро-задания

- [ ] **М1.4a** — функция `describe(fighter)` вызывает `print(fighter)` — работает для Warrior и Mage
- [ ] **М1.4b** — список `[Warrior(...), Mage(...), Archer(...)]` — цикл `for f in team: f.attack(target)`
- [ ] **М1.4c** — **без** `if type(fighter) == Warrior` — только общий метод `attack`

### Основная практика

Напиши `arena_battle(team_a: list, team_b: list)` в `module_01/battle.py`:

- Принимает два списка персонажей (любых подклассов `Character`)
- Поочерёдные атаки до победы одной команды
- **Запрещено:** `if isinstance(fighter, Warrior)` — только полиморфизм
- Лог боя в консоль

### Что гуглить

| Русский | English |
|---------|---------|
| полиморфизм Python | Python polymorphism |
| утиная типизация Python | Python duck typing |
| полиморфизм и наследование | polymorphism vs inheritance Python |

### Чеклист

- [ ] Понимаю полиморфизм на примере `attack()`
- [ ] Знаю, что такое duck typing
- [ ] Написал `arena_battle` без `if/elif` по типам
- [ ] Модуль 1 завершён — все темы пройдены

---

# Модуль 2: Продвинутое ООП в Python

**Срок:** 2–3 недели  
**Цель:** магические методы и `@classmethod` / `@staticmethod` — через микро-задания, не зубрёжку

> **Фокус недели:** `__str__`/`__repr__` и разница static vs class. Если путаешь — делай М2.3 и М2.4 в один день и сравни в таблице.

---

## Тема 2.1: Магические методы — основы

### Теория: что именно нужно понять

- **Магические методы (magic methods / dunder methods)** — методы с двойным подчёркиванием `__имя__`
- Вызываются **не напрямую**, а Python-ом в определённых ситуациях
- **`__str__(self)`** — красивый вывод для пользователя: `print(obj)`, `str(obj)`
- **`__repr__(self)`** — технический вывод для разработчика: в консоли, в отладке
- **Правило:** `__repr__` должен возвращать строку, по которой можно воссоздать объект
- **Разница `__str__` vs `__repr__`:** `__str__` — для людей, `__repr__` — для машин
- Если `__str__` нет — используется `__repr__`

### Микро-задания

- [ ] **М2.1a** — только `__str__`: `print(hero)` выводит `Грок [HP: 80]`
- [ ] **М2.1b** — добавь `__repr__`: в консоли `hero` показывает техническую строку
- [ ] **М2.1c** — запиши в `PROGRESS.md`: чем `str()` отличается от `repr()` **своими словами**

### Основная практика

```python
def __str__(self):
    return f"{self.name} [HP: {self.health}]"

def __repr__(self):
    return f"Character(name='{self.name}', health={self.health})"
```

- Список героев → `print(heroes)` — каждый через `__str__`
- В REPL: `repr(hero)` vs `str(hero)`

### Что гуглить

| Русский | English |
|---------|---------|
| магические методы Python | Python magic methods dunder |
| __str__ vs __repr__ Python | Python __str__ vs __repr__ |
| dunder methods Python | Python dunder methods guide |

### Чеклист

- [ ] Понимаю, что такое магические методы
- [ ] Знаю разницу `__str__` и `__repr__`
- [ ] Реализовал оба метода в `Character`

---

## Тема 2.2: Магические методы — `__len__` и `__getitem__`

### Теория: что именно нужно понять

- **`__len__(self)`** — вызывается при `len(obj)`; объект должен возвращать целое число
- **`__getitem__(self, key)`** — вызывается при `obj[key]`; позволяет обращаться к объекту как к коллекции
- **`__setitem__(self, key, value)`** — вызывается при `obj[key] = value`
- **`__contains__(self, item)`** — вызывается при `item in obj`
- **Зачем это нужно:** твой класс может вести себя как встроенный `list` или `dict`
- **Пример:** класс `Inventory` — `len(inventory)` возвращает кол-во предметов, `inventory[0]` — первый предмет

### Практика

Создай класс `Inventory`:

- Внутри хранит `list` предметов
- `__len__` — количество предметов
- `__getitem__` — доступ по индексу: `inventory[2]`
- `__contains__` — проверка: `"sword" in inventory`
- Методы: `add(item)`, `remove(item)`, `__str__` — красивый список

### Что гуглить

| Русский | English |
|---------|---------|
| __len__ __getitem__ Python | Python __len__ __getitem__ |
| эмуляция списка в классе Python | Python emulate list in class |
| магические методы коллекций | Python collection magic methods |

### Чеклист

- [ ] Реализовал `__len__` и `__getitem__`
- [ ] Реализовал `__contains__`
- [ ] Класс `Inventory` работает как коллекция

---

## Тема 2.3: `@staticmethod` — метод без доступа к объекту и классу

### Теория: что именно нужно понять

- **Статический метод `@staticmethod`** — функция внутри класса, но **без `self` и `cls`**
- Не имеет доступа к атрибутам объекта или класса
- **Зачем:** логически связан с классом, но не нуждается в его данных
- **Пример:** `Character.validate_name(name)` — проверяет, что имя не пустое
- Вызывается через класс: `Character.validate_name("Grok")` или через объект
- **Когда использовать:** утилитарные функции, валидация, хелперы

### Микро-задания

- [ ] **М2.3a** — `@staticmethod validate_name` — без `self`, без `cls`
- [ ] **М2.3b** — вызови **через класс**: `Character.validate_name("ab")` → `True`
- [ ] **М2.3c** — в `__init__`: если имя невалидно → `raise ValueError("...")`

### Основная практика

```python
@staticmethod
def validate_name(name: str) -> bool:
    return len(name) >= 2 and name.isalpha()
```

- `@staticmethod generate_id()` — случайный ID
- Валидация имени в конструкторе

### Что гуглить

| Русский | English |
|---------|---------|
| staticmethod Python | Python @staticmethod |
| когда использовать staticmethod | when to use staticmethod Python |
| staticmethod vs classmethod | Python staticmethod vs classmethod |

### Чеклист

- [ ] Понимаю, зачем нужен `@staticmethod`
- [ ] Знаю, что у него нет `self` и `cls`
- [ ] Добавил статические методы в `Character`

---

## Тема 2.4: `@classmethod` — метод с доступом к классу

> 📖 **Урок:** [static vs class — таблица](EXPLAINED.md#таблица-три-типа-методов)

### 💡 Простыми словами

- **Обычный метод** — работает с **конкретным** героем (`self`)
- **`@staticmethod`** — просто функция в классе, **без** героя и без класса
- **`@classmethod`** — работает с **классом** (`cls`), создаёт объекты: `from_dict`, `create_npc`

`Warrior.from_dict(data)` → `cls` = `Warrior` → получишь Warrior, не Character.

### Теория: что именно нужно понять

- **Метод класса `@classmethod`** — первый аргумент `cls` (сам класс), не `self`
- Имеет доступ к атрибутам класса, но не к атрибутам конкретного объекта
- **Альтернативные конструкторы (factory methods)** — главное применение
- **Пример:** `Character.from_dict(data)` — создаёт объект из словаря
- **Пример:** `Warrior.create_default()` — создаёт воина с дефолтными параметрами
- **`cls`** — ссылка на класс, через который вызван метод (может быть подкласс!)
- **Разница трёх типов методов:**

| Тип | Первый аргумент | Доступ к |
|-----|----------------|----------|
| Обычный метод | `self` | атрибутам объекта |
| `@classmethod` | `cls` | атрибутам класса |
| `@staticmethod` | нет | ничему |

### Микро-задания

- [ ] **М2.4a** — `from_dict(cls, data)` — создай героя из `{"name": "Grok", "health": 100}`
- [ ] **М2.4b** — вызови `Warrior.from_dict(...)` — убедись, что `cls` = `Warrior`, не `Character`
- [ ] **М2.4c** — таблица в `PROGRESS.md`: static vs class vs обычный метод (3 строки)

### Основная практика

```python
@classmethod
def from_dict(cls, data: dict) -> "Character":
    return cls(name=data["name"], health=data["health"])

@classmethod
def create_npc(cls, name: str) -> "Character":
    return cls(name=name, health=50, attack_power=5)
```

- `Warrior.create_npc("Гоблин")` — NPC слабее игрока
- `Warrior.from_dict(...)` возвращает именно `Warrior`, не `Character`

### Что гуглить

| Русский | English |
|---------|---------|
| classmethod Python | Python @classmethod |
| альтернативный конструктор Python | Python alternative constructor classmethod |
| cls в classmethod Python | Python cls parameter classmethod |

### Чеклист

- [ ] Понимаю разницу `self`, `cls` и отсутствия аргумента
- [ ] Реализовал `from_dict` и `create_npc`
- [ ] Могу объяснить, когда `@classmethod`, а когда `@staticmethod`
- [ ] Модуль 2 завершён

---

# Модуль 3: Инструменты экосистемы

**Срок:** 1–2 недели  
**Цель модуля:** научиться работать как настоящий разработчик — изолированное окружение, пакеты, версионирование кода

---

## Тема 3.1: Виртуальные окружения `venv`

### Теория: что именно нужно понять

- **Виртуальное окружение (virtual environment / venv)** — изолированная среда Python для проекта
- **Зачем:** разные проекты требуют разных версий библиотек
- **Глобальный Python** — тот, что установлен в системе; туда лучше не ставить пакеты проектов
- **Создание:** `python -m venv venv`
- **Активация Windows:** `venv\Scripts\activate`
- **Активация Linux/Mac:** `source venv/bin/activate`
- **Деактивация:** `deactivate`
- **Признак активации:** в начале строки терминала появляется `(venv)`
- **Папка `venv/`** — не коммитить в Git, добавить в `.gitignore`
- **`py` launcher на Windows** — `py -3.12 -m venv venv` для конкретной версии

### Практика

1. Открой папку `python-oop-journey/` (уже создана)
2. Создай venv: `python -m venv venv`
3. Активируй: `venv\Scripts\activate`
4. Проверь: `where python` — путь должен вести в `venv/`
5. Перенеси код из `module_01/` в корень или оставь модули — **одна папка, один Git**
6. Запусти: `python module_01/main.py`

### Что гуглить

| Русский | English |
|---------|---------|
| виртуальное окружение Python venv | Python venv virtual environment |
| как создать venv Windows | create Python venv Windows |
| activate venv Windows PowerShell | activate venv Windows PowerShell |

### Чеклист

- [ ] Создал venv
- [ ] Умею активировать и деактивировать
- [ ] Понимаю, зачем это нужно
- [ ] Запустил проект внутри venv

---

## Тема 3.2: Менеджер пакетов `pip` и `requirements.txt`

### Теория: что именно нужно понять

- **pip** — менеджер пакетов Python, устанавливает библиотеки из PyPI
- **Пакет (package)** — готовая библиотека: `requests`, `pytest`, `colorama`
- **Установка:** `pip install package_name`
- **Установка конкретной версии:** `pip install requests==2.31.0`
- **Список установленных:** `pip list`
- **Удаление:** `pip uninstall package_name`
- **`requirements.txt`** — файл со списком зависимостей проекта
- **Создание:** `pip freeze > requirements.txt`
- **Установка из файла:** `pip install -r requirements.txt`
- **Зачем `requirements.txt`:** другой разработчик (или ты на другом компьютере) воспроизводит окружение
- **`pip` работает только внутри активированного venv** — пакеты ставятся в изоляцию

### Практика

1. Активируй venv
2. Установи `colorama` — цветной вывод в консоли
3. Используй в `main.py`:

```python
from colorama import Fore, init
init()
print(Fore.GREEN + "Победа!" + Fore.RESET)
```

4. Создай `requirements.txt`: `pip freeze > requirements.txt`
5. Удали venv, создай заново, установи зависимости: `pip install -r requirements.txt`

### Что гуглить

| Русский | English |
|---------|---------|
| pip install Python пакеты | Python pip install packages |
| requirements.txt Python | Python requirements.txt tutorial |
| pip freeze Python | Python pip freeze requirements |

### Чеклист

- [ ] Установил пакет через pip
- [ ] Создал `requirements.txt`
- [ ] Воспроизвёл окружение с нуля по `requirements.txt`

---

## Тема 3.3: Git — основы версионирования

### Теория: что именно нужно понять

- **Git** — система контроля версий, хранит историю изменений кода
- **Репозиторий (repository / repo)** — папка проекта с историей Git
- **`git init`** — инициализация репозитория в папке
- **`git status`** — что изменилось
- **`git add файл`** — подготовить файл к коммиту (staging)
- **`git add .`** — добавить все изменения
- **`git commit -m "сообщение"`** — сохранить снимок (коммит)
- **Коммит (commit)** — точка в истории с описанием изменений
- **`.gitignore`** — файлы, которые Git игнорирует (`venv/`, `__pycache__/`, `.env`)
- **`git log`** — история коммитов
- **`git diff`** — что именно изменилось в файлах
- **Хорошее сообщение коммита:** `Add Character class with encapsulation`
- **Плохое сообщение:** `fix`, `update`, `asdf`

### Практика

1. Установи Git: https://git-scm.com/downloads
2. Настрой имя и email:

```bash
git config --global user.name "Твоё Имя"
git config --global user.email "твой@email.com"
```

3. В папке проекта: `git init`
4. Создай `.gitignore`:

```
venv/
__pycache__/
*.pyc
.env
```

5. Сделай 3 коммита:
   - `Initial commit: project structure`
   - `Add Character class with OOP`
   - `Add colorama for colored output`

### Что гуглить

| Русский | English |
|---------|---------|
| Git основы для начинающих | Git basics for beginners |
| git init commit add | git init add commit tutorial |
| gitignore Python | Python gitignore template |

### Чеклист

- [ ] Установил Git
- [ ] Создал репозиторий `git init`
- [ ] Сделал минимум 3 осмысленных коммита
- [ ] Создал `.gitignore`

---

## Тема 3.4: GitHub — публикация кода

### Теория: что именно нужно понять

- **GitHub** — облачный сервис для хранения Git-репозиториев
- **Remote (удалённый репозиторий)** — копия репо на GitHub
- **Создание репо на GitHub** — через сайт github.com → New repository
- **`git remote add origin URL`** — привязка локального репо к GitHub
- **`git push -u origin main`** — отправка коммитов на GitHub
- **`git pull`** — скачать изменения с GitHub
- **`git clone URL`** — скопировать чужой (или свой) репозиторий
- **Ветка (branch)** — параллельная линия разработки
- **`git branch`** — список веток
- **`git checkout -b feature-name`** — создать и перейти на ветку
- **README.md** — описание проекта на главной странице репозитория
- **Публичный vs приватный репозиторий**

### Практика

1. Зарегистрируйся на https://github.com
2. Создай репозиторий `python-oop-journey` (публичный)
3. Привяжи и запушь:

```bash
git remote add origin https://github.com/ТВОЙ_ЛОГИН/python-oop-journey.git
git branch -M main
git push -u origin main
```

4. Создай `README.md`:

```markdown
# Python OOP Journey

Мой путь изучения ООП в Python.

## Что внутри

- Класс Character с наследованием
- Инкапсуляция через @property
- Полиморфизм в arena_battle
```

5. Закоммить и запушь README

### Что гуглить

| Русский | English |
|---------|---------|
| GitHub для начинающих | GitHub tutorial for beginners |
| git push origin main | git push to GitHub |
| как создать README.md | GitHub README.md guide |

### Чеклист

- [ ] Создал аккаунт на GitHub
- [ ] Запушил проект
- [ ] Написал README.md
- [ ] Модуль 3 завершён

---

# Модуль 4: Работа с данными и файлами

**Срок:** 2 недели  
**Цель модуля:** научиться сохранять и загружать данные — без этого нет настоящих проектов

---

## Тема 4.1: Работа с текстовыми файлами

### Теория: что именно нужно понять

- **`open(path, mode)`** — открытие файла; режимы: `"r"` чтение, `"w"` запись, `"a"` дополнение
- **Контекстный менеджер `with`** — автоматически закрывает файл
- **`encoding="utf-8"`** — обязательно для русского текста
- **`file.read()`** — весь файл одной строкой
- **`file.readlines()`** — список строк
- **Итерация:** `for line in file`
- **`file.write(text)`** — запись
- **`pathlib.Path`** — современная работа с путями (лучше, чем `os.path`)
- **`Path.exists()`** — проверка существования файла
- **`Path.read_text()` / `Path.write_text()`** — удобные методы

### Практика

Создай класс `GameLogger`:

- Метод `log_event(message)` — дописывает строку в `game_log.txt` с временной меткой
- Метод `read_log()` — возвращает список всех записей
- Используй `pathlib.Path` и `with open(...)`
- Интегрируй в `arena_battle` — каждая атака пишется в лог

### Что гуглить

| Русский | English |
|---------|---------|
| чтение записи файлов Python | Python read write files |
| with open Python | Python with open context manager |
| pathlib Python примеры | Python pathlib tutorial |

### Чеклист

- [ ] Умею читать и писать TXT через `with open`
- [ ] Использую `pathlib.Path`
- [ ] Создал `GameLogger` и интегрировал в игру

---

## Тема 4.2: Работа с JSON

### Теория: что именно нужно понять

- **JSON (JavaScript Object Notation)** — текстовый формат для хранения структурированных данных
- **Похож на словарь Python:** `{"name": "Grok", "health": 100}`
- **`import json`**
- **`json.dumps(obj)`** — Python-объект → JSON-строка
- **`json.loads(string)`** — JSON-строка → Python-объект
- **`json.dump(obj, file)`** — запись в файл
- **`json.load(file)`** — чтение из файла
- **`ensure_ascii=False`** — чтобы русский текст не превращался в `\u043f`
- **`indent=2`** — красивое форматирование
- **Ограничение:** JSON не знает про Python-классы — нужно конвертировать в `dict`
- **Паттерн сохранения:** `character.to_dict()` → `json.dump()` → `Character.from_dict()` → `json.load()`

### Практика

Добавь в `Character` методы:

```python
def to_dict(self) -> dict:
    return {"name": self.name, "health": self._health, "type": self.__class__.__name__}
```

И класс `SaveManager`:

- `save_characters(characters, filepath)` — сохраняет список в JSON
- `load_characters(filepath)` — загружает и создаёт объекты через `from_dict`
- Сохрани партию персонажей в `party.json`, перезапусти программу, загрузи обратно

### Что гуглить

| Русский | English |
|---------|---------|
| json Python чтение запись | Python json dump load |
| сохранение объектов в JSON Python | Python save class objects to JSON |
| json.dumps json.loads Python | Python json.dumps json.loads |

### Чеклист

- [ ] Умею `json.dump` и `json.load`
- [ ] Реализовал `to_dict` и `from_dict`
- [ ] Персонажи сохраняются и загружаются из JSON

---

## Тема 4.3: SQLite — основы баз данных

### Теория: что именно нужно понять

- **База данных (database)** — структурированное хранилище данных
- **SQLite** — встроенная в Python БД, один файл `.db`, не требует сервера
- **SQL (Structured Query Language)** — язык запросов к базе данных
- **`import sqlite3`**
- **`sqlite3.connect("file.db")`** — подключение (создаёт файл, если нет)
- **Курсор (cursor)** — объект для выполнения запросов: `conn.cursor()`
- **`CREATE TABLE`** — создание таблицы
- **`INSERT INTO`** — добавление записи
- **`SELECT`** — чтение данных
- **`UPDATE`** — обновление
- **`DELETE`** — удаление
- **`conn.commit()`** — сохранить изменения
- **Параметризованные запросы `?`** — защита от SQL-инъекций:

```python
cursor.execute("INSERT INTO chars (name, health) VALUES (?, ?)", (name, health))
```

- **Никогда не используй f-строки в SQL-запросах**

### Практика

Создай класс `DatabaseManager`:

```python
class DatabaseManager:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self._create_tables()

    def _create_tables(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                health INTEGER,
                char_type TEXT
            )
        """)
        self.conn.commit()

    def save_character(self, character) -> int: ...
    def get_all_characters(self) -> list: ...
    def delete_character(self, char_id: int): ...
```

- Сохрани 3 персонажей в БД
- Загрузи всех и выведи
- Удали одного по id

### Что гуглить

| Русский | English |
|---------|---------|
| sqlite3 Python tutorial | Python sqlite3 tutorial |
| SQL CREATE INSERT SELECT Python | Python SQL CRUD sqlite3 |
| SQL injection Python защита | Python SQL injection prevention |

### Чеклист

- [ ] Создал таблицу через `CREATE TABLE`
- [ ] Умею INSERT, SELECT, DELETE
- [ ] Использую `?` вместо f-строк
- [ ] Реализовал `DatabaseManager`
- [ ] Модуль 4 завершён

---

# Модуль 5: Первый серьёзный проект

**Срок:** 3–4 недели  
**Цель модуля:** собрать всё изученное в один законченный проект уровня Junior

---

## Тема 5.1: Выбор проекта и проектирование архитектуры

### Теория: что именно нужно понять

- **Проектирование перед кодом** — сначала классы и связи, потом реализация
- **Принцип единственной ответственности (Single Responsibility)** — один класс = одна задача
- **Разделение на слои:**
  - `models/` — классы данных (Character, Item, Book)
  - `services/` — бизнес-логика (BattleService, LibraryService)
  - `storage/` — работа с файлами/БД (SaveManager, DatabaseManager)
  - `ui/` — взаимодействие с пользователем (меню, ввод)
  - `main.py` — точка входа
- **Диаграмма классов** — нарисуй на бумаге связи между классами до написания кода
- **User Story** — описание функции с точки зрения пользователя: «Как игрок, я хочу атаковать врага»

### Твой проект: Текстовая RPG «Подземелье»

Ты выбрал RPG — это лучший вариант для ООП: много классов, наследование, инвентарь, сохранения.

**Классы:** `Character`, `Enemy`, `Inventory`, `Item`, `Weapon`, `Potion`, `Dungeon`, `BattleSystem`, `LootGenerator`, `DatabaseManager`, `Game`, `Menu`

> К Модулю 5 ты уже напишешь `Character`, `Inventory`, `BattleSystem` в Модулях 1–4. Здесь — **собираешь**, а не начинаешь с нуля.

### Практика

1. Нарисуй диаграмму классов на бумаге (кто кого наследует, кто кого содержит)
2. Опиши 10 User Stories
3. Создай структуру **внутри** `python-oop-journey/`:

```
python-oop-journey/
├── main.py
├── models/
│   ├── __init__.py
│   ├── character.py
│   ├── item.py
│   └── enemy.py
├── services/
│   ├── __init__.py
│   └── battle.py
├── storage/
│   ├── __init__.py
│   └── database.py
├── ui/
│   ├── __init__.py
│   └── menu.py
├── requirements.txt
├── .gitignore
└── README.md
```

### Что гуглить

| Русский | English |
|---------|---------|
| проектирование ООП Python | Python OOP project structure |
| Single Responsibility Principle Python | Python single responsibility principle |
| Python project folder structure | Python project structure best practices |

### Чеклист

- [ ] Выбрал проект
- [ ] Нарисовал диаграмму классов
- [ ] Написал 10 User Stories
- [ ] Создал структуру папок

---

## Тема 5.2: Реализация моделей (models/)

### Теория: что именно нужно понять

- **Модель (model)** — класс, описывающий сущность предметной области
- Модели **не знают** про меню, файлы и базу данных
- Модели содержат: атрибуты, бизнес-логику объекта, `to_dict`, `from_dict`, `__str__`, `__repr__`
- **Композиция:** `Character` **имеет** `Inventory`, а не наследует его
- **`__init__.py`** — делает папку Python-пакетом (может быть пустым)
- **Импорт из пакета:** `from models.character import Character`

### Практика (для RPG)

Реализуй в `models/`:

- `character.py` — `Character` с `@property`, `take_damage`, `attack`, `to_dict`, `from_dict`
- `enemy.py` — `Enemy(Character)` с `@classmethod create_boss()`
- `item.py` — `Item`, `Weapon(Item)`, `Potion(Item)` с `use(target)`
- `inventory.py` — `Inventory` с `__len__`, `__getitem__`, `__contains__`

### Что гуглить

| Русский | English |
|---------|---------|
| Python packages __init__.py | Python packages __init__.py modules |
| композиция vs наследование Python | Python composition vs inheritance |
| Python dataclass vs class | Python dataclass vs regular class |

### Чеклист

- [ ] Все модели в отдельных файлах
- [ ] Модели не зависят от UI и storage
- [ ] Есть `to_dict` / `from_dict` у ключевых классов
- [ ] Использованы `@property`, наследование, композиция

---

## Тема 5.3: Реализация сервисов (services/)

### Теория: что именно нужно понять

- **Сервис (service)** — класс с бизнес-логикой, которая затрагивает несколько моделей
- Сервис **не хранит** данные — получает объекты как аргументы
- **Пример:** `BattleSystem.fight(hero, enemy)` — логика боя
- **Пример:** `LootGenerator.generate(enemy_level)` — генерация добычи
- Сервисы используют **полиморфизм** — работают с базовым классом
- Сервисы могут использовать **статические и классовые методы** для утилит

### Практика (для RPG)

Реализуй в `services/`:

- `battle.py` — `BattleSystem`:
  - `fight(attacker, defender) -> BattleResult`
  - `process_turn(character, enemies: list)`
  - Логирование каждого хода
- `loot.py` — `LootGenerator`:
  - `@staticmethod generate(enemy_type) -> Item`
  - `@classmethod generate_for_dungeon(level) -> list[Item]`

### Что гуглить

| Русский | English |
|---------|---------|
| service layer Python | Python service layer pattern |
| бизнес логика отдельно от UI Python | Python separate business logic from UI |

### Чеклист

- [ ] `BattleSystem` работает с любым `Character` (полиморфизм)
- [ ] Сервисы не содержат `input()` и `print()` напрямую — возвращают результат
- [ ] `LootGenerator` использует `@staticmethod` / `@classmethod`

---

## Тема 5.4: Реализация хранилища (storage/)

### Теория: что именно нужно понять

- **Слой хранения (storage / repository layer)** — единственное место, где код знает про файлы и БД
- **Паттерн Repository** — класс-прослойка между бизнес-логикой и базой данных
- UI и сервисы **не вызывают** `sqlite3` напрямую — только через `DatabaseManager`
- **Методы репозитория:** `save`, `load`, `delete`, `get_all`, `get_by_id`
- **Транзакции** — `conn.commit()` после группы операций
- **Обработка ошибок** — что делать, если файл не найден или БД повреждена

### Практика (для RPG)

Реализуй в `storage/`:

- `database.py` — `DatabaseManager`:
  - Таблицы: `characters`, `inventory_items`, `game_state`
  - `save_game(player, inventory, dungeon_level)`
  - `load_game() -> GameState`
  - `save_character(character) -> int`
- `json_backup.py` — `JsonBackup`:
  - Дублирующее сохранение в JSON (на случай отладки)

### Что гуглить

| Русский | English |
|---------|---------|
| repository pattern Python | Python repository pattern |
| SQLite CRUD Python class | Python SQLite CRUD class |
| Python save load game state | Python save load game state sqlite |

### Чеклист

- [ ] `DatabaseManager` инкапсулирует всю работу с SQLite
- [ ] Сохранение и загрузка игры работают
- [ ] Данные переживают перезапуск программы

---

## Тема 5.5: Реализация интерфейса (ui/) и main.py

### Теория: что именно нужно понять

- **UI-слой** — единственное место с `input()` и `print()`
- **Меню-цикл (menu loop)** — `while True` с выбором действий
- **Обработка неверного ввода** — `try/except ValueError`
- **Делегирование:** меню вызывает сервисы, не реализует логику само
- **`main.py`** — создаёт объекты, запускает игру, обрабатывает `KeyboardInterrupt`
- **Цветной вывод** — `colorama` для HP, урона, победы
- **Чистый выход** — `sys.exit(0)` или `break` из цикла

### Практика (для RPG)

Реализуй в `ui/menu.py`:

```
=== ПОДЗЕМЕЛЬЕ ===
1. Новая игра
2. Продолжить
3. Инвентарь
4. Сохранить
5. Выход
```

- `Game` класс в `main.py` — оркестрирует всё
- Главный игровой цикл: исследование → бой → добыча → сохранение
- Минимум 3 типа врагов, 3 типа предметов, система уровней

### Что гуглить

| Русский | English |
|---------|---------|
| Python CLI menu loop | Python command line menu loop |
| Python text based RPG | Python text based RPG tutorial |
| Python game loop pattern | Python game loop pattern |

### Чеклист

- [ ] Меню работает без падений при неверном вводе
- [ ] Полный игровой цикл: бой → добыча → сохранение
- [ ] UI не содержит бизнес-логики

---

## Тема 5.6: Финализация проекта — уровень Junior

### Теория: что именно нужно понять

- **README.md** — лицо проекта: что это, как запустить, скриншоты/примеры
- **Docstring** — `"""Описание функции."""` у публичных методов
- **Типизация** — аннотации типов везде, где возможно
- **Обработка всех ошибок** — программа не падает при плохом вводе
- **`.gitignore`** — актуальный и полный
- **`requirements.txt`** — все зависимости
- **Коммиты с осмысленными сообщениями** — минимум 10 коммитов в проекте
- **Что смотрит Junior на собеседовании:** структура проекта, ООП, Git, работа с данными

### Практика — финальный чеклист проекта

- [ ] Проект запускается командой `python main.py` из корня
- [ ] README с инструкцией установки и запуска
- [ ] Минимум 8 классов в `models/` и `services/`
- [ ] SQLite сохраняет прогресс
- [ ] Использованы: наследование, инкапсуляция, полиморфизм
- [ ] Использованы: `@property`, `@staticmethod`, `@classmethod`
- [ ] Использованы: `__str__`, `__repr__`, `__len__`, `__getitem__`
- [ ] Код на GitHub с 10+ коммитами
- [ ] `requirements.txt` актуален
- [ ] venv не в репозитории

### Что гуглить

| Русский | English |
|---------|---------|
| Python junior portfolio project | Python junior developer portfolio |
| Python project README example | Python project README example |
| Python junior interview questions | Python junior interview questions OOP |

### Чеклист

- [ ] Проект полностью работает
- [ ] README написан
- [ ] Код на GitHub
- [ ] Могу объяснить архитектуру каждого класса
- [ ] **Модуль 5 завершён — ты на уровне Junior!**

---

# 🗺️ Дорожная карта после Junior (универсальная ветка)

Ты пока не выбрал направление — после Модуля 5 пройди **все три мини-трека по 1 неделе**, потом выбери что ближе:

| Трек | Тема | Мини-проект |
|------|------|-------------|
| A | `pytest` + `requests` | Тесты для RPG + погода через API |
| B | `FastAPI` | REST API поверх твоей RPG (персонажи, инвентарь) |
| C | Telegram-бот (`aiogram`) | Бот, который шлёт статус героя из SQLite |

Общее для всех: `logging` вместо `print`, `.env` для секретов.

---

# 📅 Твой график (8–12 ч/нед)

| Неделя | Что делать | Часов |
|--------|------------|-------|
| 1 | Модуль 0 (фон) + М1.1–1.2: классы, инкапсуляция | 8–10 |
| 2 | М1.3: **super() блок** + Warrior/Mage/Archer | 10–12 |
| 3 | М1.4: полиморфизм + `arena_battle` | 8–10 |
| 4 | Модуль 2: магические методы, static/classmethod | 10–12 |
| 5 | Модуль 3: venv, pip, Git, GitHub | 8–10 |
| 6 | Модуль 4: TXT, JSON, SQLite | 10–12 |
| 7–8 | Модуль 4: `DatabaseManager` + сохранение RPG | 10–12 |
| 9–12 | Модуль 5: сборка RPG «Подземелье» | 10–14 |

**Итого: ~3–4 месяца** — с запасом под твои слабые зоны. Это нормальный темп, не отставание.

### Распределение недели (шаблон)

| День | Время | Задача |
|------|-------|--------|
| Пн | 1.5 ч | Новая теория + 1–2 микро-задания |
| Вт | 1.5 ч | Микро-задания |
| Ср | 1 ч | Основная практика темы |
| Чт | 1.5 ч | Доделать практику + чеклист |
| Пт | 1 ч | Модуль 0 (отладка/типы/англ.) |
| Сб | 2 ч | Повтор слабой темы (сейчас: **super()**) |
| Вс | отдых или 30 мин | `PROGRESS.md` + мелкий коммит |

---

> 💡 **Совет ментора:** у тебя длинный список «слабых мест» — это не приговор, а карта. Каждую неделю выбирай **одну** главную (сейчас: наследование + `super()`). Остальное закрывает Модуль 0 и повтор. Не копируй код вслепую — после каждого микро-задания объясни вслух (или в `PROGRESS.md`), **что делает каждая строка**. Кидай код — разберём вместе.