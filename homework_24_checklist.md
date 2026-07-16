# Чеклист сдачи — глава 24 (портфолио)

Отметь трек и проекты. Цель — **ссылки на код**, не «прочитал md».

---

## Трек

- [ ] **A** — Быстрый junior (capstone + мини-1 + мини-2)
- [ ] **B** — Конкурентный (4 мини + capstone) — рекомендуется
- [ ] **C** — Стажировка ASAP (capstone full + 2 мини)

Трек: ___________

---

## Мини-проекты

### Мини-1 — Expense Tracker CLI

- [ ] Команды add / list / report / export
- [ ] Данные после перезапуска сохраняются
- [ ] ≥ 5 pytest, все green
- [ ] README + requirements + .gitignore
- [ ] ≥ 3 коммита
- [ ] Ссылка: _______________________________

### Мини-2 — API Client + кэш

- [ ] HTTP timeout
- [ ] Кэш (~10 мин)
- [ ] logging + .env.example
- [ ] Тесты (хотя бы cache / error path)
- [ ] Ссылка: _______________________________

### Мини-3 — URL Shortener

- [ ] POST create + GET redirect (302) или JSON-режим
- [ ] hits++, 400/404
- [ ] Пагинация списка
- [ ] ≥ 8 pytest, isolation DB
- [ ] Ссылка: _______________________________

### Мини-4 — CSV ETL

- [ ] load CSV → SQLite
- [ ] report JSON (paid_revenue, by_product)
- [ ] pytest на агрегаты
- [ ] Ссылка: _______________________________

---

## Capstone

Выбери один:

- [ ] **Library v2** (усиление гл. 21)
- [ ] **TaskFlow API**

### Must (оба варианта)

- [ ] REST + БД + pytest
- [ ] Пагинация списков
- [ ] Auth (API key или token/JWT)
- [ ] 401 / 404 / 409 (где уместно)
- [ ] config из env, секреты не в git
- [ ] logging
- [ ] type hints на публичном слое
- [ ] README: install / run / test / API table / curl
- [ ] ≥ 12 pytest green (TaskFlow ≥ 15)
- [ ] ≥ 5 осмысленных коммитов
- [ ] Ссылка: _______________________________

### Library v2 дополнительно

- [ ] PATCH + DELETE books
- [ ] loan conflict 409 + return endpoint
- [ ] `create_app()` + PRAGMA foreign_keys=ON
- [ ] GET `/api/health`

### TaskFlow дополнительно

- [ ] users + projects + tasks (+ comments желательно)
- [ ] register/login + protected routes
- [ ] password не plaintext

### Бонус

- [ ] FastAPI
- [ ] Dockerfile / compose
- [ ] GitHub Actions pytest
- [ ] Postgres

---

## Самооценка «я junior» (из гл. 24)

Отмечено **___ / 16** пунктов.

- [ ] ≥ 12 — готов слать на стажировки / junior
- [ ] 8–11 — добей capstone и 2 мини
- [ ] < 8 — вернись к гл. 18–23 и доделай практику

---

## Итог для ментора

| Поле | Значение |
|------|----------|
| Трек | |
| Репозитории | |
| Любимый проект (1) | |
| Что было сложнее всего | |
| Скрин/вывод pytest (capstone) | приложить |

**Готово:** все must выбранного трека + ссылки открываются + README запускается с нуля.
