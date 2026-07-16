# Тема: SQL — основы запросов к базе данных

> **Формат:** сначала объяснение простыми словами, потом пример с разбором.  
> Не надо зубрить всё сразу — **3 части теории + 12 примеров + 6 задач**.

---

## Цель главы

После прочтения ты понимаешь:

1. **Что такое SQL и таблица** — строки, столбцы, ключи.
2. **SELECT и фильтры** — как достать и отфильтровать данные.
3. **JOIN и изменение данных** — как связать таблицы и делать INSERT/UPDATE/DELETE.

SQL нужен почти каждому Python-разработчику: сайты, API, аналитика, админки — данные почти всегда в базе.

**В этой главе** — язык запросов «на бумаге». В главе 18 подключим **SQLite из Python**.

---

# ЧАСТЬ 1. База данных и таблицы

## 1.1. Зачем база данных

Excel-таблица на 100 строк — удобна. На 10 миллионов — файл тормозит, сложно искать, несколько программ не могут писать одновременно.

**База данных (БД)** — программа, которая:
- хранит данные **структурированно** (таблицы),
- быстро **ищет** по условию,
- безопасно обрабатывает **одновременный доступ**,
- гарантирует **целостность** (например, нельзя удалить заказ, не зная клиента).

**SQL** (Structured Query Language) — язык, на котором мы **просим** БД: «дай строки», «добавь», «обнови», «удали».

---

## 1.2. Аналогия — таблица как Excel

Представь лист Excel «Сотрудники»:

| id | name   | department | salary |
|----|--------|------------|--------|
| 1  | Anna   | IT         | 80000  |
| 2  | Bob    | Sales      | 60000  |
| 3  | Vika   | IT         | 85000  |

В SQL это **таблица** `employees`:
- **столбцы (columns)** — `id`, `name`, `department`, `salary` (поля с типом),
- **строки (rows)** — каждый сотрудник,
- **ячейка** — одно значение в пересечении строки и столбца.

---

## 1.3. Основные понятия

| Термин | Значение |
|--------|----------|
| **Таблица (table)** | Набор строк одного типа сущности |
| **Строка (row / record)** | Один объект (один сотрудник) |
| **Столбец (column / field)** | Одно свойство (имя, зарплата) |
| **Первичный ключ (PRIMARY KEY)** | Уникальный id строки |
| **Внешний ключ (FOREIGN KEY)** | Ссылка на id в другой таблице |
| **Схема (schema)** | Структура: какие таблицы и столбцы есть |

**PRIMARY KEY** — как паспортный номер: у каждой строки свой, повторов нет.

**FOREIGN KEY** — связь: `orders.user_id` указывает на `users.id`.

---

## 1.4. Типы данных (упрощённо)

| Тип SQL | Что хранит | Пример |
|---------|------------|--------|
| `INTEGER` | Целые числа | `42`, `-1` |
| `REAL` / `FLOAT` | Дробные | `3.14` |
| `TEXT` / `VARCHAR` | Строки | `'Anna'` |
| `BOOLEAN` | true/false | `TRUE` |
| `DATE` | Дата | `'2026-07-14'` |
| `TIMESTAMP` | Дата и время | `'2026-07-14 10:30:00'` |

В разных СУБД (PostgreSQL, MySQL, SQLite) названия чуть отличаются — смысл один.

---

## 1.5. CREATE TABLE — создать таблицу

```sql
CREATE TABLE employees (
    id       INTEGER PRIMARY KEY,
    name     TEXT NOT NULL,
    department TEXT,
    salary   INTEGER
);
```

- `PRIMARY KEY` — уникальный идентификатор.
- `NOT NULL` — поле обязательно (нельзя пустое).

---

### ✅ Проверь себя — часть 1

1. Строка в таблице — это что? → **Одна запись (один объект)**.
2. Зачем PRIMARY KEY? → **Уникально идентифицировать строку**.
3. SQL — язык для чего? → **Запросов к реляционной БД**.

---

# ЧАСТЬ 2. SELECT — чтение данных

## 2.1. SELECT — «выбери столбцы»

Самый частый запрос:

```sql
SELECT name, salary FROM employees;
```

Все строки, только столбцы `name` и `salary`.

Все столбцы:

```sql
SELECT * FROM employees;
```

`*` — «все поля». Удобно для просмотра, в проде лучше перечислять нужные столбцы.

---

## 2.2. WHERE — фильтр

```sql
SELECT name, salary
FROM employees
WHERE department = 'IT';
```

Только сотрудники IT.

Операторы сравнения: `=`, `<>`, `>`, `<`, `>=`, `<=`.

Логика: `AND`, `OR`, `NOT`.

```sql
SELECT name FROM employees
WHERE department = 'IT' AND salary >= 80000;
```

---

## 2.3. ORDER BY и LIMIT

Сортировка:

```sql
SELECT name, salary FROM employees
ORDER BY salary DESC;
```

`DESC` — по убыванию, `ASC` — по возрастанию (по умолчанию).

Ограничить количество строк:

```sql
SELECT name, salary FROM employees
ORDER BY salary DESC
LIMIT 3;
```

Топ-3 по зарплате.

---

## 2.4. DISTINCT — уникальные значения

```sql
SELECT DISTINCT department FROM employees;
```

Список отделов **без повторов**.

---

## 2.5. Агрегатные функции

Функции над **набором строк**:

| Функция | Смысл |
|---------|-------|
| `COUNT(*)` | Сколько строк |
| `COUNT(column)` | Сколько не-NULL значений |
| `SUM(column)` | Сумма |
| `AVG(column)` | Среднее |
| `MIN(column)` | Минимум |
| `MAX(column)` | Максимум |

```sql
SELECT COUNT(*) FROM employees;
SELECT AVG(salary) FROM employees WHERE department = 'IT';
```

---

## 2.6. GROUP BY и HAVING

**GROUP BY** — сгруппировать строки и посчитать по группам:

```sql
SELECT department, COUNT(*) AS cnt, AVG(salary) AS avg_sal
FROM employees
GROUP BY department;
```

По каждому отделу: сколько человек и средняя зарплата.

**HAVING** — фильтр **после** группировки (как WHERE, но для групп):

```sql
SELECT department, COUNT(*) AS cnt
FROM employees
GROUP BY department
HAVING COUNT(*) > 1;
```

Отделы, где больше одного сотрудника.

**Порядок выполнения (упрощённо):** FROM → WHERE → GROUP BY → HAVING → SELECT → ORDER BY → LIMIT.

---

### ✅ Проверь себя — часть 2

1. `WHERE salary > 50000` — что делает? → **Оставляет строки с зарплатой больше 50000**.
2. `ORDER BY name ASC`? → **Сортировка по имени А→Я**.
3. `HAVING` vs `WHERE`? → **WHERE до группировки, HAVING после GROUP BY**.

---

# ЧАСТЬ 3. JOIN и изменение данных

## 3.1. Зачем несколько таблиц

Одна гигантская таблица «всё обо всём» — дублирование и путаница.

Нормально делят:
- `users` — пользователи,
- `orders` — заказы (с `user_id` на пользователя),
- `products` — товары.

**JOIN** — соединить строки из двух таблиц по условию.

---

## 3.2. INNER JOIN — только совпавшие пары

```sql
SELECT users.name, orders.total
FROM users
INNER JOIN orders ON users.id = orders.user_id;
```

Строка из `users` + строка из `orders`, где `users.id = orders.user_id`.

Если у пользователя нет заказов — он **не попадёт** в результат INNER JOIN.

---

## 3.3. LEFT JOIN — все слева + совпадения справа

```sql
SELECT users.name, orders.total
FROM users
LEFT JOIN orders ON users.id = orders.user_id;
```

**Все** пользователи из `users`. Если заказа нет — `orders.total` будет `NULL`.

Когда нужно: «показать всех клиентов, даже без покупок».

---

## 3.4. INSERT — добавить строку

```sql
INSERT INTO employees (name, department, salary)
VALUES ('Oleg', 'Sales', 55000);
```

Если `id` — AUTOINCREMENT, его не указываем.

Несколько строк:

```sql
INSERT INTO employees (name, department, salary) VALUES
    ('Dina', 'IT', 70000),
    ('Max', 'HR', 50000);
```

---

## 3.5. UPDATE — изменить

```sql
UPDATE employees
SET salary = salary + 5000
WHERE department = 'IT';
```

**Всегда** проверяй `WHERE` — без него обновятся **все** строки.

---

## 3.6. DELETE — удалить

```sql
DELETE FROM employees WHERE id = 2;
```

Тоже осторожно с `WHERE`:

```sql
DELETE FROM employees;  -- удалит ВСЁ (опасно!)
```

На практике часто делают **мягкое удаление**: поле `is_active = FALSE` вместо физического DELETE.

---

### ✅ Проверь себя — часть 3

1. INNER JOIN: пользователь без заказов виден? → **Нет**.
2. LEFT JOIN: пользователь без заказов виден? → **Да**, с NULL в полях заказа.
3. `UPDATE employees SET salary = 0` без WHERE? → **Обнулит зарплату всем**.

---

# Практика — 12 примеров с разбором

Для примеров 1–8 используем таблицу **employees** (SELECT, WHERE, GROUP BY и т.д.).

**employees**
| id | name | department | salary |
|----|------|------------|--------|
| 1 | Anna | IT | 80000 |
| 2 | Bob | Sales | 60000 |
| 3 | Vika | IT | 85000 |
| 4 | Oleg | HR | 50000 |

Для примеров 9–10 (JOIN) — **отдельные** таблицы **users** и **orders**. Имена Anna и Bob совпадают, но это другая сущность: клиенты магазина, не сотрудники.

**users** — `(id, name)`
| id | name |
|----|------|
| 1 | Anna |
| 2 | Bob |

**orders** — `(id, user_id, product, total)`
| id | user_id | product | total |
|----|---------|---------|-------|
| 1 | 1 | Laptop | 1200 |
| 2 | 1 | Mouse | 25 |
| 3 | 2 | Keyboard | 80 |

Столбец `orders.user_id` — **внешний ключ** на `users.id` (например, `user_id = 1` → Anna в таблице `users`). Это **не** ссылка на `employees.id`.

---

## Пример 1. SELECT всех имён

```sql
SELECT name FROM employees;
```

**Результат:**
```
Anna
Bob
Vika
Oleg
```

**Разбор:** выбрали один столбец `name` из всех строк таблицы `employees`. Без `WHERE` — все 4 строки.

---

## Пример 2. WHERE — фильтр по отделу

```sql
SELECT name, salary
FROM employees
WHERE department = 'IT';
```

**Результат:**
```
Anna    80000
Vika    85000
```

**Разбор:** условие `department = 'IT'` оставляет только IT. Строки сравниваются по точному совпадению строки (регистр зависит от БД).

---

## Пример 3. AND — два условия

```sql
SELECT name, salary
FROM employees
WHERE department = 'IT' AND salary >= 82000;
```

**Результат:**
```
Vika    85000
```

**Разбор:** Anna (80000) не проходит порог 82000. Оба условия должны быть true.

---

## Пример 4. ORDER BY + LIMIT — топ по зарплате

```sql
SELECT name, salary
FROM employees
ORDER BY salary DESC
LIMIT 2;
```

**Результат:**
```
Vika    85000
Anna    80000
```

**Разбор:** сначала сортировка по убыванию зарплаты, потом берём первые 2 строки.

---

## Пример 5. DISTINCT — список отделов

```sql
SELECT DISTINCT department FROM employees;
```

**Результат:**
```
IT
Sales
HR
```

**Разбор:** IT встречается у Anna и Vika, но в результате один раз. DISTINCT убирает дубликаты **в выбранных столбцах**.

---

## Пример 6. Агрегаты COUNT и AVG

```sql
SELECT COUNT(*) AS total_employees,
       AVG(salary) AS avg_salary
FROM employees;
```

**Результат:**
```
total_employees: 4
avg_salary: 68750
```

**Разбор:** `(80000+60000+85000+50000)/4 = 68750`. Агрегат считает по **всем** строкам, попавшим в выборку (здесь без WHERE — все 4).

---

## Пример 7. GROUP BY — статистика по отделам

```sql
SELECT department,
       COUNT(*) AS cnt,
       MAX(salary) AS max_sal
FROM employees
GROUP BY department;
```

**Результат:**
```
IT      2   85000
Sales   1   60000
HR      1   50000
```

**Разбор:** строки разбиты на группы по `department`. В каждой группе свой COUNT и MAX. Столбцы в SELECT должны быть либо в GROUP BY, либо внутри агрегатной функции.

---

## Пример 8. HAVING — отделы с 2+ сотрудниками

```sql
SELECT department, COUNT(*) AS cnt
FROM employees
GROUP BY department
HAVING COUNT(*) >= 2;
```

**Результат:**
```
IT    2
```

**Разбор:** только IT имеет 2 сотрудников. Sales и HR по одному — отфильтрованы HAVING.

---

## Пример 9. INNER JOIN — заказы с именами клиентов

```sql
SELECT u.name, o.product, o.total
FROM users u
INNER JOIN orders o ON u.id = o.user_id;
```

**Результат:**
```
Anna    Laptop     1200
Anna    Mouse      25
Bob     Keyboard   80
```

**Разбор:** `u` и `o` — псевдонимы таблиц `users` и `orders`. Условие соединения: `u.id = o.user_id` — то есть `user_id` в заказе указывает на **первичный ключ** `users.id`, а не на `employees.id`. В `users` только Anna (id=1) и Bob (id=2); у обоих есть заказы — в INNER JOIN попадают все 3 строки из `orders`. Пользователь без заказов в эту выборку не попадёт.

---

## Пример 10. LEFT JOIN — все пользователи и их заказы

Добавим в `users` третьего клиента без заказов:

**users** (дополнительная строка)
| id | name |
|----|------|
| 3 | Vika |

```sql
SELECT u.name, o.product, o.total
FROM users u
LEFT JOIN orders o ON u.id = o.user_id;
```

**Результат:**
```
Anna    Laptop     1200
Anna    Mouse      25
Bob     Keyboard   80
Vika    NULL       NULL
```

**Разбор:** LEFT JOIN сохраняет **все** строки из левой таблицы (`users`). Vika в `users` есть, но заказов с `user_id = 3` нет — поля из `orders` будут `NULL`. Снова: связь только `users.id = orders.user_id`, таблица `employees` здесь не участвует. У Anna два заказа — две строки (это нормально для JOIN).

---

## Пример 11. INSERT и SELECT после вставки

```sql
INSERT INTO employees (name, department, salary)
VALUES ('Dina', 'Sales', 62000);

SELECT name, department FROM employees WHERE name = 'Dina';
```

**Результат SELECT:**
```
Dina    Sales
```

**Разбор:** INSERT добавляет строку. SELECT проверяет, что запись появилась. В реальной БД `id` часто назначается автоматически.

---

## Пример 12. UPDATE с WHERE

```sql
-- До: Bob salary = 60000
UPDATE employees
SET salary = 65000
WHERE name = 'Bob';

SELECT name, salary FROM employees WHERE name = 'Bob';
```

**Результат:**
```
Bob    65000
```

**Разбор:** обновили **одну** строку благодаря `WHERE name = 'Bob'`. Без WHERE — подняли бы зарплату всем.

---

# Шпаргалка

| Задача | SQL |
|--------|-----|
| Все столбцы | `SELECT * FROM t` |
| Фильтр | `WHERE условие` |
| Сортировка | `ORDER BY col DESC` |
| Топ N | `LIMIT N` |
| Уникальные | `SELECT DISTINCT col` |
| Сколько строк | `COUNT(*)` |
| По группам | `GROUP BY col` |
| Фильтр групп | `HAVING ...` |
| Связать таблицы | `JOIN ... ON a.id = b.fk` |
| Добавить | `INSERT INTO ... VALUES` |
| Изменить | `UPDATE ... SET ... WHERE` |
| Удалить | `DELETE FROM ... WHERE` |

---

# FAQ

**SQL — это язык программирования?**  
Декларативный язык **запросов**: ты описываешь *что* нужно, БД решает *как*.

**PostgreSQL vs MySQL vs SQLite?**  
Синтаксис похож на 90%. SQLite — файл на диске, удобен для обучения и прототипов. PostgreSQL — мощная продакшен-БД.

**Зачем псевдонимы `e`, `o`?**  
Короче и читабельнее в JOIN: `users u`, `orders o`.

**Можно ли SELECT без FROM?**  
В некоторых БД да (`SELECT 1+1`), но обычно FROM обязателен.

**SQL injection?**  
Никогда не склеивай SQL со строкой пользователя. В Python — **параметризованные запросы** (глава 18).

**`*` в SELECT — плохо?**  
В учебе OK. В API/проде лучше явно перечислять столбцы — меньше лишних данных и проще менять схему.

---

# Домашнее задание

**Файл:** `homework_17.py`

В каждой задаче напиши SQL-запрос в **многострочной строке** (тройные кавычки) и выведи её через `print()`.  
Проверять в БД пока не обязательно — важно **правильно сформулировать** запрос. В главе 18 выполним в SQLite.

---

## Задача 1. Простой SELECT

Таблица `products`: столбцы `id`, `name`, `price`.

Напиши запрос: выбрать `name` и `price` для всех товаров.

**Ожидаемый запрос (смысл):** `SELECT name, price FROM products`

---

## Задача 2. WHERE

Та же таблица `products`.

Напиши запрос: товары дороже 1000 (`price > 1000`), вывести `name`, `price`, отсортировать по цене по убыванию.

**Должно содержать:** `WHERE`, `ORDER BY price DESC`

---

## Задача 3. Агрегат

Таблица `orders`: `id`, `amount`.

Напиши запрос: общее количество заказов и сумма всех `amount`.  
Используй псевдонимы: `total_count`, `total_sum`.

**Должно содержать:** `COUNT(*)`, `SUM(amount)`

---

## Задача 4. GROUP BY

Таблица `sales`: `id`, `city`, `amount`.

Напиши запрос: по каждому `city` — количество продаж и сумма `amount`.  
Только города, где продаж **больше 5** (HAVING).

**Должно содержать:** `GROUP BY city`, `HAVING COUNT(*) > 5`

---

## Задача 5. INNER JOIN

Таблицы: `users (id, name)`, `orders (id, user_id, total)`.

Напиши INNER JOIN: имя пользователя и сумма заказа.

**Должно содержать:** `INNER JOIN orders ON users.id = orders.user_id`

---

## Задача 6. Мини-сценарий текстом

В `homework_17.py` создай список `queries` из **трёх** строк-SQL для сценария:

1. `INSERT` — добавить пользователя `'Test User'` в таблицу `users (name)` (без id).
2. `UPDATE` — поднять `price` на 10% для всех товаров в категории `'books'` (таблица `products`, столбцы `price`, `category`).
3. `DELETE` — удалить заказы старше `'2020-01-01'` (таблица `orders`, столбец `created_at`).

Выведи все три запроса с подписями `print("1:", ...)`, `print("2:", ...)`, `print("3:", ...)`.

**Проверь:** у UPDATE и DELETE есть `WHERE` — иначе затронешь все строки.

---

## Как сдать

- Файл `homework_17.py` с запросами в строках
- Сдавай задачи 1–3, потом 4–6
- **Лаборатория ниже** — проверь 2–3 запроса в SQLite до главы 18

---

# Лаборатория — первый SQL в Python (мост к гл. 18)

> **Не пропускай:** 10 минут здесь снимают обрыв «SQL на бумаге → глава 18».

Скопируй в `lab_sql_17.py` и запусти:

```python
import sqlite3

with sqlite3.connect(":memory:") as conn:
    cur = conn.cursor()
    cur.executescript("""
        CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT);
        CREATE TABLE orders (id INTEGER PRIMARY KEY, user_id INTEGER, total REAL);
    """)
    cur.execute("INSERT INTO users (name) VALUES (?)", ("Anna",))
    cur.execute("INSERT INTO orders (user_id, total) VALUES (?, ?)", (1, 120.0))
    conn.commit()

    cur.execute("""
        SELECT u.name, o.total
        FROM users u
        INNER JOIN orders o ON u.id = o.user_id
    """)
    print("JOIN:", cur.fetchall())

    cur.execute("SELECT COUNT(*) FROM users")
    print("COUNT:", cur.fetchone()[0])
```

**Должно вывести:**
```
JOIN: [('Anna', 120.0)]
COUNT: 1
```

**Разбор:** тот же SQL из примеров 9–10, но уже **живой** SQLite. `:memory:` — БД в RAM, файл не нужен. В гл. 18 разберём `commit`, `?`, файлы `.db`.

---

# Итог

1. Данные в **таблицах**: строки, столбцы, PRIMARY KEY.
2. **SELECT + WHERE + ORDER BY + LIMIT** — чтение и фильтрация.
3. **GROUP BY / HAVING** — статистика по группам.
4. **JOIN** — связь таблиц; **INSERT/UPDATE/DELETE** — изменение данных.

**Следующая глава 18:** SQLite из Python — `sqlite3`, параметризованные запросы, основы ORM.

---
Конец главы.