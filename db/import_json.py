"""Перенос данных из JSON-файлов в базу данных SQLite."""

import json
import os
import sqlite3

from db.database import get_connection

DATA_DIR = "data"
SCHEMA_FILE = "sql/schema.sql"
TESTS_FILE = os.path.join(DATA_DIR, "tests.json")
USERS_FILE = os.path.join(DATA_DIR, "users.json")
ATTEMPTS_FILE = os.path.join(DATA_DIR, "attempts.json")


def load_json(filename, default):
    """Прочитать JSON-файл, вернуть default, если файла нет."""
    if not os.path.exists(filename):
        return default
    with open(filename, encoding="utf-8") as file:
        return json.load(file)


def apply_schema(conn):
    """Применить схему базы данных."""
    with open(SCHEMA_FILE, encoding="utf-8") as file:
        conn.executescript(file.read())
    conn.commit()


def is_empty(conn):
    """Проверить, пуста ли база (не созданы ли уже данные)."""
    try:
        count = conn.execute("SELECT COUNT(*) FROM tests").fetchone()[0]
        return count == 0
    except sqlite3.OperationalError:
        return True


def import_tests(conn):
    data = load_json(TESTS_FILE, {})
    test_rows = []
    question_rows = []
    question_id = 1

    for test_id_str, test_data in data.items():
        test_id = int(test_id_str)
        test_rows.append(
            (test_id, test_data["title"],
             test_data.get("description", ""))
        )
        for question in test_data.get("questions", []):
            question_rows.append((
                question_id,
                test_id,
                question["text"],
                json.dumps(question["options"], ensure_ascii=False),
                question["correct_answer"],
            ))
            question_id += 1

    conn.executemany(
        "INSERT INTO tests (id, title, description) VALUES (?, ?, ?)",
        test_rows,
    )
    conn.executemany(
        "INSERT INTO questions "
        "(id, test_id, text, options, correct_answer) "
        "VALUES (?, ?, ?, ?, ?)",
        question_rows,
    )


def import_users(conn):
    users = load_json(USERS_FILE, [])
    conn.executemany(
        "INSERT INTO users (id, name) VALUES (?, ?)",
        [(user["id"], user["name"]) for user in users],
    )


def import_attempts(conn):
    attempts = load_json(ATTEMPTS_FILE, [])
    conn.executemany(
        "INSERT INTO attempts "
        "(id, test_id, user_id, date, correct, total, percent) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        [
            (
                a["id"],
                a["test_id"],
                a["user_id"],
                a["date"],
                a["correct"],
                a["total"],
                a["percent"],
            )
            for a in attempts
        ],
    )


def main():
    conn = get_connection()
    try:
        apply_schema(conn)

        if not is_empty(conn):
            print("Данные в базе уже есть, импорт пропущен.")
            return

        import_tests(conn)
        import_users(conn)
        import_attempts(conn)
        conn.commit()
        print("Импорт завершён: данные перенесены из JSON в SQLite.")
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


if __name__ == "__main__":
    main()
