# 📖 Мини-уроки: что что делает

> Читай **перед** практикой из `LEARNING_PLAN.md`. Здесь не «что учить», а **как это работает** простыми словами + примеры.

---

## Как пользоваться

1. Открыл тему в плане → найди такой же заголовок здесь
2. Прочитал урок → сделай микро-задание
3. Не понял абзац → перечитай пример кода и запусти его в `playground.py`

---

# Модуль 0

## Ошибки Python — что происходит когда код падает

Когда Python встречает проблему, он **останавливается** и печатает **traceback** — цепочку «кто кого вызвал».

```
Traceback (most recent call last):
  File "main.py", line 10, in <module>      ← тут началась проблема
    hero.attack(enemy)
  File "character.py", line 25, in attack   ← внутри этого метода
    target.take_damage(self.power)
  File "character.py", line 18, in take_damage
    self._health -= amount
TypeError: unsupported operand type(s) for -=: 'str' and 'int'
                                              ↑ ПОСЛЕДНЯЯ СТРОКА — главная!
```

**Что делать:** читай **снизу вверх**. Последняя строка = **тип ошибки** + **суть**.

| Ошибка | Что значит | Частая причина |
|--------|------------|----------------|
| `TypeError` | Несовместимые типы | передал `"5"` вместо `5` |
| `AttributeError` | Нет такого атрибута/метода | опечатка в имени или `None.method()` |
| `ValueError` | Тип верный, значение плохое | `int("abc")` |
| `NameError` | Переменная не существует | забыл создать или опечатка |
| `IndentationError` | Кривые отступы | смешал пробелы и табы |

---

## print() для отладки — что делает

`print` показывает **значение в момент выполнения**. Ты вставляешь его **перед** подозрительной строкой:

```python
def take_damage(self, amount: int) -> None:
    print(f"DEBUG: до урона HP={self._health}, урон={amount}")  # смотрим ДО
    self._health -= amount
    print(f"DEBUG: после урона HP={self._health}")               # смотрим ПОСЛЕ
```

**Зачем:** ты видишь, **где** логика пошла не туда. Убери `print` после исправления.

---

## breakpoint() — что делает

```python
def attack(self, target):
    breakpoint()  # программа СТОПнется здесь
    target.take_damage(self.attack_power)
```

Программа **замирает**. В отладчике Cursor/VS Code видишь все переменные: `self`, `target`, их поля. Можешь идти **пошагово** (F10).

**Когда:** когда `print` не хватает и непонятно, **почему** переменная такая.

---

## Типы `name: str` — что делает

```python
def heal(self, amount: int) -> None:
#                   ↑ тип аргумента    ↑ что возвращает (None = ничего)
```

Типы **не меняют** поведение Python при запуске. Это **заметки** для тебя и редактора.

**Что даёт:**
- Cursor подсказывает: у `str` есть `.upper()`, у `int` — нет
- Ты сам видишь: «сюда только число»
- На собеседовании это плюс

```python
fighters: list[Character] = []  # список, внутри только Character
data: dict[str, int] = {"gold": 100}  # ключи str, значения int
```

---

# Модуль 1 — ООП

## Класс — что это и что делает

**Класс** = форма для печенья. **Объект** = конкретное печенье.

```python
class Character:          # ← чертёж (класс)
    pass

hero = Character()        # ← печенье (объект)
enemy = Character()       # ← другое печенье
```

`hero` и `enemy` — **разные** объекты. У каждого свои поля в памяти.

---

## `__init__` — что делает при создании

```python
class Character:
    def __init__(self, name: str, health: int):
        self.name = name       # кладём name В ЭТОТ объект
        self._health = health  # кладём health В ЭТОТ объект

hero = Character("Грок", 100)
# Python автоматически вызывает __init__(hero, "Грок", 100)
#                                              ↑ это и есть self
```

**`__init__`** = «настройка нового объекта при рождении». Без него объект пустой.

---

## `self` — что это на самом деле

`self` — **ссылка на конкретный объект**, для которого вызвали метод.

```python
hero = Character("Грок", 100)
hero.take_damage(20)
# Python превращает это в:
# Character.take_damage(hero, 20)
#                       ↑ self = hero
```

Когда вызываешь `enemy.take_damage(20)` → `self` = `enemy`. **Разные объекты — разный self.**

---

## Метод — что делает

Метод = функция **привязанная к объекту**. Имеет доступ к `self.name`, `self._health`.

```python
def is_alive(self) -> bool:
    return self._health > 0
# Читать: «этот конкретный персонаж жив?»
```

Вызов `hero.is_alive()` — Python подставляет `hero` как `self`.

---

## `_health` и `__luck` — что реально делает Python

### Один подчёркивание `_`

```python
self._health = 100
```

Python **ничего не блокирует**. `_` — это **договорённость между программистами**: «не трогай снаружи, используй методы».

```python
hero._health = 999  # технически работает! но ты ломаешь правила
```

### Два подчёркивания `__`

```python
self.__luck = 5
```

Python **переименует** внутри: `_Character__luck`. Снаружи `hero.__luck` — ошибка.

**Зачем:** защита от случайного доступа, не от хакера.

---

## `@property` — что делает

Без property:

```python
print(hero._health)  # некрасиво, видим «внутренности»
```

С property:

```python
@property
def health(self) -> int:
    return self._health

print(hero.health)  # выглядит как поле, но это метод!
```

**Что происходит:** `hero.health` → Python вызывает `health(self)` → возвращает `_health`.

**Зачем:** красивый доступ + можешь добавить проверку позже без смены `hero.health`.

### `@health.setter` — что делает

```python
@health.setter
def health(self, value: int) -> None:
    if value < 0:
        raise ValueError("HP не может быть < 0")
    self._health = value

hero.health = 50   # вызовет setter с проверкой
hero.health = -10  # ValueError!
```

---

## Наследование — что делает

```python
class Character:
    def attack(self, target):
        target.take_damage(10)

class Warrior(Character):   # Warrior ПОЛУЧАЕТ все методы Character
    pass

w = Warrior()
w.attack(enemy)  # работает! метод от родителя
```

**Что происходит:** Python ищет метод у `Warrior` → не нашёл → идёт к `Character` → нашёл.

---

## `super()` — что делает (главное для тебя)

```python
class Character:
    def __init__(self, name: str, health: int):
        self.name = name
        self._health = health

class Warrior(Character):
    def __init__(self, name: str, health: int, armor: int):
        super().__init__(name, health)  # ← «вызови __init__ родителя»
        self.armor = armor              # ← потом добавь своё
```

**Пошагово при `Warrior("Рагнар", 120, 5)`:**

1. Создаётся пустой `Warrior`
2. Вызывается `Warrior.__init__`
3. `super().__init__(name, health)` → вызывается `Character.__init__`
4. `Character` ставит `self.name` и `self._health`
5. Возврат в `Warrior` → ставится `self.armor`

**Без super():**

```python
class Warrior(Character):
    def __init__(self, name, health, armor):
        self.armor = armor  # только armor! name и _health НЕТ → баг
```

### super() в переопределённом методе

```python
class Warrior(Character):
    def attack(self, target):
        super().attack(target)   # сначала обычная атака (10 урона)
        target.take_damage(5)    # потом бонус воина (+5)
```

**Итого:** 15 урона. `super()` = «сделай то, что делал родитель, потом добавь своё».

---

## Полиморфизм — что делает

Один вызов — **разное поведение**:

```python
team = [Warrior("А"), Mage("Б"), Archer("В")]

for fighter in team:
    fighter.attack(enemy)  # у каждого СВОЯ версия attack()
```

Python **не спрашивает** «ты Warrior или Mage?». Просто вызывает `attack` у объекта. Каждый делает по-своему.

**Утиная типизация:** если у объекта есть `attack()` — он подходит. Не важно, какой класс.

---

# Модуль 2

## `__str__` — что делает

```python
def __str__(self):
    return f"{self.name} [HP: {self._health}]"

print(hero)       # вызывает __str__ → "Грок [HP: 80]"
str(hero)         # то же самое
```

**Для кого:** человек читает в консоли.

---

## `__repr__` — что делает

```python
def __repr__(self):
    return f"Character(name={self.name!r}, health={self._health})"

repr(hero)  # "Character(name='Грок', health=80)"
```

**Для кого:** разработчик в отладке. Должно быть **точно**, можно скопировать.

**В интерактивной консоли** набрал `hero` → покажет `__repr__`.

---

## `__len__` — что делает

```python
class Inventory:
    def __init__(self):
        self._items = []

    def __len__(self):
        return len(self._items)

inv = Inventory()
len(inv)  # вызывает inv.__len__() → 0
```

**Связывает** твой класс с встроенной функцией `len()`.

---

## `__getitem__` — что делает

```python
def __getitem__(self, index: int):
    return self._items[index]

inv[0]  # то же что inv.__getitem__(0) → первый предмет
```

**Связывает** с синтаксисом `obj[индекс]` как у списка.

---

## `__contains__` — что делает

```python
def __contains__(self, item):
    return item in self._items

"sword" in inv  # вызывает inv.__contains__("sword") → True/False
```

---

## `@staticmethod` — что делает

```python
class Character:
    @staticmethod
    def validate_name(name: str) -> bool:
        return len(name) >= 2

Character.validate_name("Грок")  # True
# Нет self — метод НЕ знает про конкретного героя
# Не знает про класс — просто функция внутри класса
```

**Когда:** логика связана с классом, но **не нужен** ни объект, ни класс.

---

## `@classmethod` — что делает

```python
class Character:
    @classmethod
    def from_dict(cls, data: dict):
        return cls(name=data["name"], health=data["health"])

hero = Character.from_dict({"name": "Грок", "health": 100})
# cls = Character → создаёт Character(...)

warrior = Warrior.from_dict({"name": "Рагнар", "health": 120})
# cls = Warrior → создаёт Warrior(...)  ← вот магия cls!
```

**`cls`** = сам класс, через который вызвали. У `Warrior.from_dict` → `cls` это `Warrior`.

**Когда:** альтернативные способы создать объект (из словаря, из файла, NPC по умолчанию).

### Таблица: три типа методов

| | self | cls | Пример |
|---|------|-----|--------|
| Обычный | ✅ | ❌ | `hero.attack(enemy)` |
| `@classmethod` | ❌ | ✅ | `Character.from_dict(data)` |
| `@staticmethod` | ❌ | ❌ | `Character.validate_name("x")` |

---

# Модуль 3

## venv — что делает

```
python-oop-journey/
  venv/          ← отдельный Python + пакеты ТОЛЬКО для этого проекта
  main.py
```

**Без venv:** ставишь `colorama` глобально → ломаешь другой проект со старой версией.

**С venv:** каждый проект — свои пакеты, изолированно.

```bash
python -m venv venv      # создать коробку
venv\Scripts\activate    # зайти в коробку (Windows)
pip install colorama     # поставить В коробку
deactivate               # выйти из коробки
```

---

## pip — что делает

`pip` скачивает готовый код с **PyPI** (библиотека пакетов Python) и кладёт в `venv`.

```bash
pip install colorama     # скачать и установить
pip uninstall colorama # удалить
pip list               # что установлено
pip freeze             # список с версиями → в requirements.txt
```

---

## Git commit — что делает

```
Рабочая папка  →  git add  →  staging  →  git commit  →  снимок навсегда
(изменения)       (выбрал)    (готово)      (сохранил)
```

**Коммит** = фотография проекта в момент времени. Можно откатиться.

```bash
git status          # что изменилось
git add character.py  # выбрать файл
git commit -m "Add Character class"  # сохранить с описанием
git log             # история снимков
```

---

# Модуль 4

## `with open(...)` — что делает

```python
with open("log.txt", "a", encoding="utf-8") as f:
    f.write("Бой начался\n")
# файл автоматически ЗАКРЫТ здесь, даже если была ошибка
```

**Без `with`:** забыл `f.close()` → утечка, файл заблокирован.

| Режим | Что делает |
|-------|------------|
| `"r"` | читать (файл должен существовать) |
| `"w"` | писать (перезаписывает всё!) |
| `"a"` | дописать в конец |

---

## JSON — что делает

**Превращает** Python-данные в текст и обратно:

```python
import json

data = {"name": "Грок", "health": 100}   # dict в Python

text = json.dumps(data)                   # → строка '{"name": "Грок", ...}'
back = json.loads(text)                   # → снова dict

with open("hero.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)  # dict → файл

with open("hero.json", "r", encoding="utf-8") as f:
    loaded = json.load(f)  # файл → dict
```

**Почему не просто `str(data)`:** JSON — **стандарт**. Любая программа на любом языке прочитает.

**Классы напрямую не сохраняются** → сначала `to_dict()`, потом `json.dump()`.

---

## SQLite — что делает

Файл `game.db` — это **база данных** (таблицы как Excel, но мощнее).

```python
import sqlite3

conn = sqlite3.connect("game.db")  # создаст файл, если нет
conn.execute("""
    CREATE TABLE IF NOT EXISTS heroes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        health INTEGER
    )
""")
conn.execute("INSERT INTO heroes (name, health) VALUES (?, ?)", ("Грок", 100))
conn.commit()  # ОБЯЗАТЕЛЬНО — иначе данные не сохранятся!

rows = conn.execute("SELECT name, health FROM heroes").fetchall()
# [('Грок', 100)]
```

**`?`** — «сюда подставь значение безопасно». Защита от SQL-инъекций.

**`commit()`** — «запиши на диск по-настоящему». Без него — данные в воздухе.

---

# Модуль 5 — как думать про структуру

## Зачем папки models / services / ui

```
Пользователь вводит "1"     →  ui/menu.py        (только ввод/вывод)
Меню вызывает бой           →  services/battle.py (логика боя)
Бой меняет HP героя         →  models/character.py (данные + методы героя)
Сохранить после боя         →  storage/database.py (только SQLite)
```

**Правило:** если файл делает **две разные работы** — раздели.

| Слой | Знает про | Не знает про |
|------|-----------|--------------|
| `models/` | свои поля и методы | меню, SQLite |
| `services/` | модели | `input()`, SQL |
| `storage/` | SQL, файлы | правила боя |
| `ui/` | `input`, `print` | SQL напрямую |

---

## Как разбить задачу на шаги (логика)

**Задача:** «Сделай бой в RPG»

Разбей:

1. Кто участники? → `Character`, `Enemy`
2. Что происходит за ход? → `attack()` → `take_damage()`
3. Когда бой кончен? → `is_alive()` → False
4. Кто ходит первым? → цикл `while` по очереди
5. Что показать игроку? → `print` в `ui/`, не в `Character`

**Одна подзадача = одно микро-задание = один коммит.**

---

# Шпаргалка «Три кита» ООП

| Кит | Одной фразой | В RPG |
|-----|--------------|-------|
| **Инкапсуляция** | Скрывай внутренности, давай методы | `_health` + `take_damage()` |
| **Наследование** | Общее — в родителя, особенное — в детях | `Warrior(Character)` |
| **Полиморфизм** | Один вызов — разное поведение | `fighter.attack()` для всех |

---

> Вопросы по уроку — кидай в чат с номером темы (например «не понял super в 1.3»).