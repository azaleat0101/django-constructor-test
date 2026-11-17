"""Перенос данных из базы ПР7 (data/constructor.sqlite) в db.sqlite3.

Исходная база открывается на чтение, целевая — та, что в DATABASES['default'].
Повторный запуск безопасен: используется update_or_create(pk=...).
"""

import json
import os
import sqlite3
from datetime import datetime
from pathlib import Path

import django
from django.db import transaction
from django.utils import timezone          # ← добавить

BASE_DIR = Path(__file__).resolve().parent.parent
SOURCE_DB = BASE_DIR / "data" / "constructor.sqlite"

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "constructor.settings")
django.setup()

from attempts.models import Attempt, User  # noqa: E402
from quizzes.models import Question, Test  # noqa: E402


def parse_date(value: str) -> datetime:
    """Разобрать дату из строки ПР7 и вернуть aware-datetime.

    Поддерживаемые форматы:
      - ISO: 2026-10-06T05:12:00 / 2026-10-06 05:12:00 / 2026-10-06
      - RU:  06.10.2026 05:12 / 06.10.2026
    """
    for fmt in (
        None,                       # datetime.fromisoformat
        "%d.%m.%Y %H:%M",
        "%d.%m.%Y",
        "%Y-%m-%d %H:%M:%S",
        "%Y-%m-%dT%H:%M:%S",
    ):
        try:
            parsed = (
                datetime.fromisoformat(value)
                if fmt is None
                else datetime.strptime(value, fmt)
            )
        except ValueError:
            continue

        # Если строка уже содержала пояс (например, +03:00),
        # datetime.fromisoformat вернёт aware — его не трогаем.
        if timezone.is_naive(parsed):
            parsed = timezone.make_aware(
                parsed,
                timezone.get_current_timezone(),
            )
        return parsed

    raise ValueError(f"Не удалось разобрать дату: {value!r}")


def main() -> None:
    if not SOURCE_DB.exists():
        raise FileNotFoundError(
            f"Исходная база не найдена: {SOURCE_DB}. "
            "Сначала выполните ПР7 (python -m db.import_json)."
        )

    with sqlite3.connect(SOURCE_DB) as conn:
        conn.row_factory = sqlite3.Row
        users = conn.execute(
            "SELECT id, name FROM users ORDER BY id"
        ).fetchall()
        tests = conn.execute(
            "SELECT id, title, description FROM tests ORDER BY id"
        ).fetchall()
        questions = conn.execute(
            "SELECT id, test_id, text, options, correct_answer "
            "FROM questions ORDER BY id"
        ).fetchall()
        attempts = conn.execute(
            "SELECT id, test_id, user_id, date, correct, total, percent "
            "FROM attempts ORDER BY id"
        ).fetchall()

    with transaction.atomic():
        # 1. Независимые сущности
        for row in users:
            User.objects.update_or_create(
                pk=row["id"],
                defaults={"name": row["name"]},
            )
        for row in tests:
            Test.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "title": row["title"],
                    "description": row["description"] or "",
                },
            )

        # 2. Зависимые от Test
        for row in questions:
            Question.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "test_id": row["test_id"],
                    "text": row["text"],
                    "options": json.loads(row["options"]),
                    "correct_answer": row["correct_answer"],
                },
            )
        for row in attempts:
            Attempt.objects.update_or_create(
                pk=row["id"],
                defaults={
                    "test_id": row["test_id"],
                    "user_id": row["user_id"],
                    "date": parse_date(row["date"]),
                    "correct": row["correct"],
                    "total": row["total"],
                    "percent": row["percent"],
                },
            )

    print("Перенос завершён.")
    print(f"Пользователей: {User.objects.count()}")
    print(f"Тестов: {Test.objects.count()}")
    print(f"Вопросов: {Question.objects.count()}")
    print(f"Попыток: {Attempt.objects.count()}")


if __name__ == "__main__":
    main()