# Домашнее задание — Глава 23
# FastAPI, pagination, API key
# chapter-23-fastapi-auth-pagination.md
# Зависимости: pip install fastapi httpx
# Запуск проверок: python homework_23.py
# (опционально сервер: uvicorn homework_23:app --reload)

from __future__ import annotations

import os
from typing import Any

# Раскомментируй/реализуй после установки fastapi:
#
# from fastapi import FastAPI, HTTPException, Header, Query, Depends, status
# from fastapi.testclient import TestClient
# from pydantic import BaseModel, Field

API_KEY = os.getenv("API_KEY", "dev-secret-key")

# ========== Хранилище in-memory ==========
# _notes: dict[int, dict] = {}
# _next_id = 1

# ========== app = FastAPI(title="HW23") ==========
# app = ...


# ========== ЗАДАЧА 1. GET /ping ==========


# ========== ЗАДАЧА 2–3. Notes: list (paginate + q), post, get, delete ==========


# ========== ЗАДАЧА 4. X-API-Key на POST/DELETE ==========


# ========== ЗАДАЧА 5. POST /api/notes/unique → 409 ==========


# ========== ЗАДАЧА 6. TestClient checks в __main__ ==========

if __name__ == "__main__":
    # После реализации:
    # from fastapi.testclient import TestClient
    # client = TestClient(app)
    # ... asserts из главы 23, задача 6 ...
    print(
        "Implement FastAPI app (see chapter-23), then uncomment TestClient asserts."
    )
    print("pip install fastapi httpx")
    # raise SystemExit(1)  # сними, когда всё готово
