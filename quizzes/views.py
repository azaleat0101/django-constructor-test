"""View-функции для работы с тестами (через SQL)."""

import json
import sqlite3
from typing import Any

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

from db.database import get_connection


LIST_TESTS_SQL: str = """
SELECT
    tests.id,
    tests.titel,
    tests.description,
    COUNT(questions.id) AS questions_count
FROM tests
LEFT JOIN questions ON questions.test_id = tests.id
GROUP BY tests.id, tests.title, tests.description
ORDER BY tests.title;
"""

SEARCH_TESTS_SQL: str = """
SELECT id, title, description
FROM tests
WHERE LOWER(title) LIKE LOWER(?)
ORDER BY title;
"""

GET_TEST_SQL: str = "SELECT id, title, description FROM tests WHERE id = ?;"

GET_QUESTIONS_SQL: str = """
SELECT id, text, options, correct_answer
FROM questions
WHERE test_id = ?
ORDER BY id;
"""


def _decode_question(row: sqlite3.Row) -> dict[str, Any]:
    """Преобразовать строку БД в словарь с распакованными options."""
    return {
        "id": row["id"],
        "text": row["text"],
        "options": json.loads(row["options"]),
        "correct_answer": row["correct_answer"],
    }


def quizzes(request: HttpRequest) -> HttpResponse:
    """Список тестов или поиск по названию."""
    query: str = request.GET.get("q", "").strip()
    tests: list[sqlite3.Row]

    conn = get_connection()
    try:
        if query:
            tests = conn.execute(
                SEARCH_TESTS_SQL, (f"%{query}%",)
            ).fetchall()
        else:
            tests = conn.execute(LIST_TESTS_SQL).fetchall()
    finally:
        conn.close()

    return render(
        request,
        "quizzes/quiz_list.html",
        {"tests": tests, "query": query},
    )


def quiz_detail(request: HttpRequest, test_id: int) -> HttpResponse:
    """Страница теста со списком вопросов."""
    conn = get_connection()
    test: sqlite3.Row | None
    questions: list[dict[str, Any]] = []

    try:
        test = conn.execute(GET_TEST_SQL, (test_id,)).fetchone()
        if test is not None:
            rows: list[sqlite3.Row] = conn.execute(
                GET_QUESTIONS_SQL, (test_id,)
            ).fetchall()
            questions = [_decode_question(row) for row in rows]
    finally:
        conn.close()

    context: dict[str, Any] = {"test": test, "questions": questions}
    status: int = 200 if test is not None else 404
    return render(
        request, "quizzes/quiz_detail.html", context, status=status
    )