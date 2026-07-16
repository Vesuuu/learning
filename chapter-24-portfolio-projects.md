# Тема: Портфолио Junior — мини-проекты и capstone

> **Формат:** не «ещё теория», а **задания на GitHub**.  
> **Когда:** после глав 1–23 (минимум после 21 + желательно 22–23).  
> **Файлы:** `homework_24_checklist.md` (сдача), эта глава — ТЗ.  
> **Цель:** доказать рекрутеру/на собесе: «я junior, вот код».

---

## Честный разговор

Одного `library_project` из гл. 21 **мало**, если:

- код почти как эталон главы,
- нет auth / пагинации / env / нормального README,
- на GitHub один репозиторий без истории.

**Что работает на рынке:**

| Артефакт | Зачем |
|----------|--------|
| **3–4 мини-проекта** (по 1–3 дня) | Разные навыки: CLI, HTTP-клиент, API, алгоритмы |
| **1 capstone** (1–2 недели) | Склейка: API + БД + тесты + Git + (бонус) Docker/auth |
| **README + тесты + коммиты** | Смотрят в первые 2 минуты |

Эта глава = твой **выпускной маршрут**.

---

## Маршрут сдачи (выбери трек)

### Трек A — «Быстрый junior» (минимум)

1. Усиленный **Library v2** (capstone ниже)  
2. **Мини-1** (CLI)  
3. **Мини-2** (HTTP client)  

→ 3 репозитория (или 1 monorepo с 3 папками).

### Трек B — «Конкурентный junior» (рекомендуется)

1. Все **4 мини**  
2. Capstone **TaskFlow** или **Library v2 Full**  
3. Главы **22–23** применены (hints, logging, env, FastAPI или Flask+key)

### Трек C — «Стажировка ASAP»

1. Только capstone Library v2 Full  
2. Мини-1 + Мини-2  
3. Выложить, в README — стек и что умеешь  

---

# ЧАСТЬ 0. Правила всех проектов

Для **каждого** репозитория обязательно:

1. **`README.md`**: что это, как установить, как запустить, как тесты, пример запроса/команды.  
2. **`requirements.txt`** (или `pyproject.toml`).  
3. **`.gitignore`**: `venv/`, `__pycache__/`, `.env`, `*.db`, `.pytest_cache/`.  
4. **`.env.example`** если есть секреты (без реальных ключей).  
5. **Минимум 3 осмысленных коммита** (не один «final»).  
6. **Тесты** там, где есть логика API/функций (`pytest`, зелёные).  
7. **Без секретов** в git.

Структура monorepo (если лень 4 репо):

```
portfolio/
├── mini_01_expense_cli/
├── mini_02_api_client/
├── mini_03_url_shortener/
├── mini_04_csv_etl/
├── capstone_taskflow/   # или library_v2/
└── README.md            # оглавление портфолио
```

---

# МИНИ-ПРОЕКТ 1. Expense Tracker CLI

**Срок:** 1–2 дня  
**Стек:** Python, argparse (или `sys.argv`), JSON **или** SQLite, pytest  
**Навык:** чистый Python без веба, файлы, агрегаты, UX CLI

## ТЗ

Консольный учёт расходов.

### Команды

```bash
python -m expense add --amount 150.5 --category food --note "lunch"
python -m expense list
python -m expense list --category food
python -m expense report --month 2026-07
python -m expense export --out expenses.csv
```

### Правила

- `amount` > 0, иначе понятная ошибка (exit code ≠ 0 или сообщение).  
- Категория — непустая строка.  
- Хранение: `data/expenses.json` **или** SQLite.  
- `report --month YYYY-MM` → сумма **всего** и **по категориям**.  
- `export` → CSV с заголовками `id,amount,category,note,date`.

### Тесты (минимум 5)

- add + list  
- amount ≤ 0 → ошибка  
- report считает сумму  
- filter by category  
- export создаёт файл (tmp_path)

### README must

Пример сессии команд + ожидаемый вывод report.

### Критерии «зачёт»

- [ ] 4 команды работают  
- [ ] данные переживают перезапуск  
- [ ] pytest зелёный  
- [ ] git history ≥ 3 commits  

---

# МИНИ-ПРОЕКТ 2. API Client + кэш

**Срок:** 1–2 дня  
**Стек:** `requests` или `httpx`, SQLite/JSON cache, `.env`, logging  
**Навык:** интеграции, таймауты, ошибки сети, env

## ТЗ

Клиент к **публичному** API (выбери один):

| API | Идея |
|-----|------|
| https://api.github.com/users/{login} | Профиль GitHub |
| https://httpbin.org/json | Учебный JSON (проще) |
| Open-Meteo weather (без ключа) | Погода по координатам |

### Функции

1. `fetch_user(login: str) -> dict` — HTTP GET, `timeout=5`.  
2. При сетевой ошибке / 404 — своё исключение или `None` + log.  
3. **Кэш 10 минут**: повторный запрос с тем же ключом не бьёт API, а читает кэш (SQLite: `key, json, fetched_at`).  
4. CLI: `python -m ghstats neat-no` → печать name, public_repos, bio (или аналог).  
5. `API` token опционально из env (`GITHUB_TOKEN`) для GitHub — **не** коммитить.

### Тесты

- кэш hit (monkeypatch время или подмена fetch);  
- 404 path;  
- timeout/ошибка обрабатывается (mock).

### Критерии

- [ ] timeout задан  
- [ ] кэш работает  
- [ ] logging (INFO на fetch, DEBUG на cache hit)  
- [ ] `.env.example`  

---

# МИНИ-ПРОЕКТ 3. URL Shortener API

**Срок:** 2–3 дня  
**Стек:** Flask **или** FastAPI + SQLite + pytest  
**Навык:** дизайн API, 302, unique, 409

## ТЗ

| Метод | URL | Действие |
|-------|-----|----------|
| POST | `/api/links` | body `{"url": "https://..."}` → `{"code": "a1b2c3", "url": "..."}` **201** |
| GET | `/api/links` | список (пагинация limit/offset) |
| GET | `/{code}` | **302** redirect на url **или** JSON `{"url"}` если `?format=json` |
| GET | `/api/links/{code}` | статистика: url, hits, created_at |
| DELETE | `/api/links/{code}` | удалить (с API key — бонус must для трека B) |

### Правила

- `code` — 6–8 символов `[a-zA-Z0-9]`, **unique**.  
- Невалидный url → **400**.  
- Неизвестный code → **404**.  
- Коллизия code → retry или **409**.  
- Каждый redirect: `hits += 1`.  
- SQL только с `?` placeholders.

### Тесты (минимум 8)

create, redirect/hits, 404, bad url 400, list pagination, delete optional.

### Критерии

- [ ] 302 или документированный JSON-режим  
- [ ] hits растут  
- [ ] pytest isolation (tmp_path DB)  
- [ ] README с curl-примерами  

---

# МИНИ-ПРОЕКТ 4. CSV → SQLite → отчёт (ETL mini)

**Срок:** 1 день  
**Стек:** csv, sqlite3, pathlib, argparse  
**Навык:** данные, как в «Python для аналитики/автоматизации»

## ТЗ

1. Вход: `sample_orders.csv` (положи в репо):

```csv
order_id,product,qty,price,status
1,Book,2,10.0,paid
2,Pen,5,1.5,paid
3,Book,1,10.0,cancelled
```

2. Команда: `python -m etl load --csv sample_orders.csv --db orders.db`  
   - таблица `orders`  
   - идемпотентность: повторный load не дублирует (DELETE+load или UNIQUE)

3. `python -m etl report --db orders.db` → JSON в stdout:

```json
{
  "orders_total": 3,
  "paid_revenue": 27.5,
  "by_product": {"Book": 20.0, "Pen": 7.5}
}
```

(`paid_revenue` = qty*price только `status=paid`)

4. Тесты на подсчёт revenue и load.

### Критерии

- [ ] CSV + SQL  
- [ ] report сходится с ручным подсчётом  
- [ ] pytest  

---

# CAPSTONE. Вариант L — Library v2 (усиление гл. 21)

**Срок:** 3–7 дней  
**База:** `library_project` из гл. 21  
**Для кого:** уже сделал гл. 21, хочешь «допилить до junior»

## Обязательный scope (must)

### API

| Метод | URL | Поведение |
|-------|-----|-----------|
| GET | `/api/health` | `{"status": "ok"}` |
| GET | `/api/books` | пагинация + опционально `?q=` |
| POST | `/api/books` | 201, валидация |
| GET | `/api/books/<id>` | 200/404 |
| PATCH | `/api/books/<id>` | частичное обновление |
| DELETE | `/api/books/<id>` | 204/404 |
| GET/POST | `/api/readers` | как раньше |
| GET/POST | `/api/loans` | выдача |
| POST | `/api/loans/<id>/return` | возврат книги |

### Бизнес-правила

1. Нельзя выдать книгу, если есть **активная** выдача (нет `returned_at`) → **409**.  
2. `PRAGMA foreign_keys = ON` в каждом connect.  
3. В таблице `loans`: `returned_at TEXT NULL` (NULL = на руках).

### Инженерия

1. **`create_app()`** factory + отдельный `DB_PATH` для тестов.  
2. **`config`** из env (`DB_PATH`, `API_KEY`, `LOG_LEVEL`).  
3. **logging** на старте и на 4xx/5xx (без секретов).  
4. **API Key** на POST/PATCH/DELETE (GET можно открыть).  
5. Type hints на публичных функциях `database.py`.  
6. **≥ 12 pytest**: health, 201, 400, 404, 401, 409 loan, return, pagination, isolation.  
7. README: architecture (2 абзаца), таблица API, curl, pytest, env.  
8. ≥ 5 осмысленных коммитов.

### Структура (рекомендуется)

```
library_v2/
├── app/
│   ├── __init__.py      # create_app
│   ├── config.py
│   ├── database.py
│   └── routes.py
├── tests/
│   ├── conftest.py
│   ├── test_books.py
│   └── test_loans.py
├── requirements.txt
├── .env.example
├── .gitignore
└── README.md
```

### Бонус (сильный junior)

- [ ] FastAPI вместо Flask (или второй сервис)  
- [ ] `Dockerfile` + `docker compose up`  
- [ ] GitHub Actions: `pytest` на push  
- [ ] Pydantic / TypedDict схемы  

---

# CAPSTONE. Вариант T — TaskFlow API (с нуля)

**Срок:** 1–2 недели  
**Для кого:** хочешь один «вау»-репозиторий вместо library

## Домен

Трекер задач для маленькой команды.

### Таблицы

**users:** id, email UNIQUE, password_hash, name  
**projects:** id, name, owner_id → users  
**tasks:** id, project_id, title, status (`todo`/`doing`/`done`), assignee_id NULL, created_at  
**comments:** id, task_id, author_id, body, created_at  

### API (минимум)

| Метод | URL | Auth |
|-------|-----|------|
| POST | `/api/auth/register` | нет |
| POST | `/api/auth/login` | нет → token или api-session |
| GET/POST | `/api/projects` | да |
| GET/POST | `/api/projects/{id}/tasks` | да |
| PATCH | `/api/tasks/{id}` | да (status, assignee) |
| GET | `/api/tasks?status=&page=&limit=` | да |
| POST | `/api/tasks/{id}/comments` | да |

### Must

- Пароль: **не** plaintext (хотя бы `hashlib.pbkdf2_hmac` + salt, лучше `bcrypt`).  
- Защищённые маршруты: API token после login **или** JWT (гл. 23).  
- Пагинация tasks.  
- SQLite OK; Postgres + Docker — бонус.  
- ≥ 15 pytest.  
- README уровня «возьми в портфолио».

### Если JWT сложно

Упрощение, всё ещё засчитывается:

- `POST /login` → `{"token": "<random>"}` сохраняешь в таблице `tokens`.  
- Заголовок `Authorization: Bearer <token>`.  
- Это **session token**, не JWT — на junior OK, если честно описано в README.

---

# ЧАСТЬ. Порядок работы (как не сгореть)

## Неделя 1

| День | Дело |
|------|------|
| 1–2 | Мини-1 Expense CLI + git push |
| 3–4 | Мини-2 API client |
| 5–7 | Мини-3 URL shortener |

## Неделя 2

| День | Дело |
|------|------|
| 1 | Мини-4 ETL (быстро) |
| 2–6 | Capstone Library v2 **или** TaskFlow |
| 7 | README, скрин pytest, ссылки в одном PORTFOLIO.md |

## Ежедневно

1. Сначала **тест или ручной сценарий** «что должно работать».  
2. Потом код.  
3. Коммит: `Add loan conflict 409` — не `fix`.  
4. Не копируй эталон гл. 21 целиком — **перепиши** слои.

---

# Чеклист «я реально junior» (самооценка)

Отметь честно. **12+ из 16** → можно слать резюме на стажировки/junior.

### Код

- [ ] Пишу функции с type hints  
- [ ] SQL только с placeholders  
- [ ] Обрабатываю 400/401/404/409, не ловлю голый Exception везде  
- [ ] Умею объяснить O(n) vs O(n²) на своём коде  
- [ ] Понимаю mutable default и `==` vs `is`  

### Backend

- [ ] REST: GET/POST/PATCH/DELETE  
- [ ] JSON API + статусы  
- [ ] SQLite (или Postgres) CRUD + JOIN  
- [ ] Пагинация list endpoints  
- [ ] Простая auth (API key или token)  

### Инженерия

- [ ] venv + requirements.txt  
- [ ] pytest с фикстурами / tmp_path  
- [ ] Git: ветки, осмысленные коммиты, GitHub  
- [ ] logging + env, секреты не в git  
- [ ] README, по которому незнакомый человек запустит проект  

### Портфолио

- [ ] ≥ 3 публичных проекта с README  
- [ ] Один проект = API + БД + тесты  

---

# Как описывать в резюме / LinkedIn

**Плохо:** «Прошёл курс Python».  

**Хорошо:**

> Pet-projects: REST API библиотеки (Flask/FastAPI, SQLite, pytest, API key); CLI expense tracker; URL shortener с redirect и hit counter.  
> Стек: Python 3.12, FastAPI/Flask, SQLite, pytest, Git.

В сопроводительном: **ссылка на GitHub** + 2 буллета «что сделал сам».

---

# FAQ

**Q: Один большой или много маленьких?**  
A: **Оба.** Маленькие показывают ширину, capstone — глубину. См. треки A/B.

**Q: Можно всё на Flask без FastAPI?**  
A: Да. FastAPI — плюс, не блокер, если Library v2 + auth + tests сильные.

**Q: Нужен Docker?**  
A: Для оффера «сразу middle» — да. Для первого junior — бонус. Добавь, когда capstone стабилен.

**Q: Эталонный код этой главы?**  
A: **Нет полного эталона.** В гл. 21 был учебный каркас. Здесь ты **автор** портфолио. Подсказки — в гл. 18–23.

**Q: Сколько времени до «готов»?**  
A: При 10–15 ч/нед: курс 1–21 ≈ 2–3 мес; гл. 22–24 + портфолио ≈ +3–5 недель. Быстрее = поверхностно.

---

# Связь с курсом

| Главы | Что даёт портфолио |
|-------|-------------------|
| 1–10 | CLI, файлы, JSON, модули |
| 11–14 | Модели, аккуратный код (по желанию классы) |
| 15–16 | Чистые функции, сложность |
| 17–18 | SQL, sqlite3 |
| 19–20 | HTTP, Flask, git, pytest |
| 21 | Первый capstone-скелет |
| 22 | hints, logging, env |
| 23 | FastAPI, pagination, API key |
| **24** | **Собрать доказательства для найма** |

---

# Сдача главы 24

Отметь в `homework_24_checklist.md`:

1. Какой **трек** (A/B/C).  
2. Ссылки на GitHub (или путь к папкам).  
3. Скрин/вывод `pytest` по каждому проекту с тестами.  
4. Самооценка чеклиста «я junior» (сколько из 16).

**Ментору / себе:** не «прочитал главу», а «вот репозитории».
