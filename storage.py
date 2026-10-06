"""Сохранение и загрузка данных проекта в JSON-файлах."""

import json
import os
from typing import Any

DATA_DIR = "data"
TESTS_FILE = os.path.join(DATA_DIR, "tests.json")
ATTEMPTS_FILE = os.path.join(DATA_DIR, "attempts.json")


def save_data(file_path: str, data: Any) -> None:
    """Сохранить данные в JSON-файл."""
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def load_data(file_path: str, default: Any) -> Any:
    """Загрузить данные из JSON-файла.

    Если файл отсутствует или повреждён — вернуть default.
    """
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return default
    except json.JSONDecodeError:
        print(f"Предупреждение: файл {file_path} повреждён, данные сброшены.")
        return default


def load_tests(file_path: str) -> dict[int, dict]:
    """Загрузить тесты, преобразовав строковые ключи в int."""
    raw = load_data(file_path, {})
    return {int(key): value for key, value in raw.items()}
