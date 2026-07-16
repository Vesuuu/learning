# Домашнее задание — Глава 22
# Type hints, logging, env
# chapter-22-typing-logging-env.md
# Запуск: python homework_22.py

from __future__ import annotations

import logging
import os
from typing import TypedDict

# ========== ЗАДАЧА 1. clamp + word_count ==========


def clamp(value: float, low: float, high: float) -> float:
    """Ограничить value диапазоном [low, high]."""
    ...


def word_count(text: str) -> dict[str, int]:
    """Счётчик слов (нижний регистр, split по пробелам)."""
    ...


# ========== ЗАДАЧА 2. TypedDict User ==========


class User(TypedDict):
    id: int
    name: str
    active: bool


def active_names(users: list[User]) -> list[str]:
    """Имена пользователей с active=True (порядок сохранить)."""
    ...


# ========== ЗАДАЧА 3. safe_divide + logging ==========

logger = logging.getLogger("homework_22")


def safe_divide(a: float, b: float) -> float | None:
    """a/b или None при b==0; пиши в logger."""
    ...


# ========== ЗАДАЧА 4. get_settings из env ==========


def get_settings() -> dict[str, str | bool]:
    """
    app_name из APP_NAME (default homework22),
    debug из DEBUG ('1' -> True, иначе False).
    """
    ...


# ========== ЗАДАЧА 5. env_example_text ==========


def env_example_text() -> str:
    """Вернуть шаблон .env.example (см. главу)."""
    ...


# ========== ЗАДАЧА 6. create_note + API key ==========


class Config:
    API_KEY: str = os.getenv("API_KEY", "dev")


def create_note(text: str, api_key: str) -> dict[str, str | int]:
    """
    Неверный key -> PermissionError + logger.warning
    Пустой text -> ValueError
    Иначе logger.info и {"id": 1, "text": text}
    """
    ...


# ========== ПРОВЕРКИ ==========

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)

    assert clamp(15, 0, 10) == 10
    assert clamp(-1, 0, 10) == 0
    assert clamp(5, 0, 10) == 5
    assert word_count("A a b") == {"a": 2, "b": 1}

    users: list[User] = [
        {"id": 1, "name": "Ann", "active": True},
        {"id": 2, "name": "Bob", "active": False},
        {"id": 3, "name": "Cat", "active": True},
    ]
    assert active_names(users) == ["Ann", "Cat"]

    assert safe_divide(10, 2) == 5.0
    assert safe_divide(1, 0) is None

    os.environ["APP_NAME"] = "testapp"
    os.environ["DEBUG"] = "1"
    s = get_settings()
    assert s["app_name"] == "testapp"
    assert s["debug"] is True

    text = env_example_text()
    assert "APP_NAME=" in text
    assert "API_KEY=" in text
    assert "LOG_LEVEL=" in text

    note = create_note("hello", Config.API_KEY)
    assert note == {"id": 1, "text": "hello"}

    try:
        create_note("x", "wrong-key")
        raise AssertionError("expected PermissionError")
    except PermissionError:
        pass

    try:
        create_note("", Config.API_KEY)
        raise AssertionError("expected ValueError")
    except ValueError:
        pass

    print("homework_22: all asserts passed")
