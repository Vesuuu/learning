# Тесты к homework_20.py — Глава 20
# pip install pytest
# Запуск: pytest test_homework_20.py -v

# from homework_20 import reverse_string, unique_sorted, clamp
# import demo_db


# ========== ЗАДАЧА 2. Тесты reverse_string ==========
# "hello" → "olleh", "" → ""


# ========== ЗАДАЧА 4. parametrize unique_sorted ==========


# ========== ЗАДАЧА 5. Тесты clamp ==========


# ========== ЗАДАЧА 6B. monkeypatch — ОБЯЗАТЕЛЬНО перед гл. 21 ==========
# def test_monkeypatch_sets_path(tmp_path, monkeypatch):
#     import demo_db
#     fake = str(tmp_path / "test.db")
#     monkeypatch.setattr(demo_db, "DB_PATH", fake)
#     assert demo_db.DB_PATH == fake