"""Загрузка и сохранение данных в JSON.

Здесь выполняется преобразование:
- JSON → объекты Python;
- объекты Python → JSON.
"""

import json
import os
from typing import Any

from models import Attempt, Test, User
from models.attempts import Attempt as _Attempt  # для type hints
from models.tests import Test as _Test
from models.users import User as _User

DATA_DIR = "data"
TESTS_FILE = os.path.join(DATA_DIR, "tests.json")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
ATTEMPTS_FILE = os.path.join(DATA_DIR, "attempts.json")


def _save(file_path: str, data: Any) -> None:
    os.makedirs(os.path.dirname(file_path), exist_ok=True)
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=2)


def _load(file_path: str, default: Any) -> Any:
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        return default
    except json.JSONDecodeError:
        print(f"Предупреждение: файл {file_path} повреждён.")
        return default


def load_tests() -> list[Test]:
    """Загрузить тесты из JSON и создать объекты Test."""
    raw = _load(TESTS_FILE, {})
    return [
        Test.from_data(int(test_id), data)
        for test_id, data in raw.items()
    ]


def save_tests(tests: list[Test]) -> None:
    """Сохранить объекты Test в JSON."""
    data = {str(test.id): test.to_data() for test in tests}
    _save(TESTS_FILE, data)


def load_users() -> list[User]:
    """Загрузить пользователей из JSON."""
    raw = _load(USERS_FILE, [])
    return [User.from_data(item) for item in raw]


def save_users(users: list[User]) -> None:
    """Сохранить пользователей в JSON."""
    _save(USERS_FILE, [user.to_data() for user in users])


def load_attempts(
    tests: list[Test],
    users: list[User],
) -> list[Attempt]:
    """Загрузить попытки, восстановив связи с Test и User."""
    raw = _load(ATTEMPTS_FILE, [])
    result: list[Attempt] = []
    for item in raw:
        attempt = Attempt.from_data(item, tests, users)
        if attempt is not None:
            result.append(attempt)
    return result


def save_attempts(attempts: list[Attempt]) -> None:
    """Сохранить попытки в JSON (хранятся id, а не объекты)."""
    _save(ATTEMPTS_FILE, [a.to_data() for a in attempts])