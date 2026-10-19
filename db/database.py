import sqlite3

DB_PATH = "data/constructor.sqlite"


def get_connection() -> sqlite3.Connection:
    """Создать соединение с БД с доступом к полям по именам."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn
