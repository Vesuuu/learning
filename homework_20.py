# Домашнее задание — Глава 20
# Git и pytest
#
# Функции здесь, тесты в test_homework_20.py
# Задания текстом — в файле chapter-20-git-pytest.md
# Запуск тестов: pytest test_homework_20.py -v


# ========== ЗАДАЧА 1. reverse_string (без [::-1]) ==========
# reverse_string("abc")  →  "cba"



# ========== ЗАДАЧА 3. unique_sorted ==========
# unique_sorted([1, 1, 2, 3, 3])  →  [1, 2, 3]



# ========== ЗАДАЧА 5. clamp ==========
def clamp(value, min_val, max_val):
    if value < min_val:
        return min_val
    if value > max_val:
        return max_val
    return value



# ========== ЗАДАЧА 6A. Git на практике ==========
# Папка git_practice/, hello.txt, git init, add, commit, switch -c feature/tests
# См. задание 6 в главе


# ========== ЗАДАЧА 6B. test_tmp_path_exists в test_homework_20.py ==========



# ========== ЗАДАЧА 6B. Демо-вывод ==========
if __name__ == "__main__":
    pass  # выведи cba, [1,2,3], 10 после реализации функций