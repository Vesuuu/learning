# Курс Junior Python Developer

Путь: **синтаксис → OOP → SQL → API → тесты/Git → production-гигиена → портфолио**.

## С чего начать

1. **Глава 0** — `chapter-00-setup-first-run.md` + `homework_00.py`
2. **Главы 1–21** — ядро курса (до первого capstone)
3. **Главы 22–23** — то, чего ждут на junior: types, logging, env, FastAPI, auth, pagination
4. **Глава 24** — портфолио: мини-проекты + усиленный capstone

## Порядок глав

| # | Тема | Домашка |
|---|------|---------|
| 0 | Установка, первый запуск | homework_00.py |
| 1 | Переменные, типы | homework_01.py |
| 2 | Условия, циклы | homework_02.py |
| 3 | Строки | homework_03.py |
| 4 | Списки, dict, set | homework_04.py |
| 5 | Мутабельность, копии | homework_05.py |
| 6 | Функции | homework_06.py |
| 7 | Comprehensions, zip | homework_07.py |
| 8 | Файлы, JSON | homework_08.py |
| 9 | Исключения | homework_09.py |
| 10 | Модули, venv | homework_10.py |
| 11 | Классы | homework_11.py |
| 12 | Наследование | homework_12.py |
| 13 | Инкапсуляция, property | homework_13.py |
| 14 | Декораторы | homework_14.py |
| 15 | Алгоритмы | homework_15.py |
| 16 | Два указателя, частоты | homework_16.py |
| 17 | SQL + `lab_sql_17.py` | homework_17.py |
| 18 | SQLite | homework_18.py |
| 19 | Flask, HTTP | homework_19.py |
| 20 | Git, pytest | homework_20.py + test_homework_20.py |
| 21 | Финальный проект (Library v1) | homework_21_checklist.md |
| **22** | **Type hints, logging, env** | homework_22.py |
| **23** | **FastAPI, пагинация, API key** | homework_23.py |
| **24** | **Портфолио: 4 mini + capstone** | homework_24_checklist.md |

## Блоки курса

| Блок | Главы | Результат |
|------|-------|-----------|
| Foundations | 0–10 | Пишешь скрипты, файлы, JSON, модули, venv |
| OOP + algorithms | 11–16 | Классы, декораторы, Big-O, типичные задачи |
| Backend base | 17–21 | SQL, SQLite, Flask REST, Git, pytest, Library API |
| Junior+ | 22–23 | Types, logs, env, FastAPI, pagination, auth idea |
| Portfolio | 24 | 3–4 мини + Library v2 / TaskFlow на GitHub |

## Хватит ли для junior?

| После | Уровень |
|-------|---------|
| Только 0–21, эталон library | **Учебный junior** (~5/10 hireability): база есть, портфолио слабое |
| 0–23 + ДЗ | **Junior-ready в учёбе** (~6/10): стек ближе к вакансиям |
| 0–24, трек B, свои репо | **Конкурентный junior / стажировка** (~7/10): есть что показать |

Курс **необходим, но один просмотр глав недостаточен**. Нанимают за **код на GitHub + умение объяснить**, не за галочку «прочитал 24 md».

## Подсказки

- В **шапке каждой главы** — маршрут: какие примеры достаточно для ДЗ.
- Большие главы (4, 10, 12) — не обязательно все 25–45 примеров сразу.
- Задачи с ⏳ — делай **после** указанной главы (retry → гл. 14, try/except превью в гл. 8 → разбор в гл. 9).
- **Гл. 17:** запусти `python lab_sql_17.py` перед гл. 18.
- **Гл. 20:** `demo_db.py` + `test_homework_20.py` — тренировка `monkeypatch` перед финальным проектом.
- **Гл. 21** — первый capstone (можно сверяться с эталоном).
- **Гл. 22–23** — обязательно, если цель — работа, не «просто выучить синтаксис».
- **Гл. 24** — без полного эталона: это уже **твоё** портфолио. Чеклист: `homework_24_checklist.md`.

## Рекомендуемый порядок портфолио (гл. 24)

1. Мини-1 Expense CLI  
2. Мини-2 HTTP client + cache  
3. Мини-3 URL shortener API  
4. Мини-4 CSV ETL  
5. Capstone: **Library v2** или **TaskFlow**

Трек A (быстрее): capstone + мини 1–2.  
Трек B (лучше для найма): всё.
