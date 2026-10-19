"""View-функции для работы с тестами (через SQL)."""

import json

from django.shortcuts import render

from db.database import get_connection


LIST_TESTS_SQL = """
SELECT
    tests.id,
    tests.title,
    tests.description,
    COUNT(questions.id) AS questions_count
FROM tests
LEFT JOIN questions ON questions.test_id = tests.id
GROUP BY tests.id, tests.title, tests.description
ORDER BY tests.title;
"""

SEARCH_TESTS_SQL = """
SELECT id, title, description
FROM tests
WHERE LOWER(title) LIKE LOWER(?)
ORDER BY title;
"""

GET_TEST_SQL = "SELECT id, title, description FROM tests WHERE id = ?;"

GET_QUESTIONS_SQL = """
SELECT id, text, options, correct_answer
FROM questions
WHERE test_id = ?
ORDER BY id;
"""


def _decode_question(row):
    return {
        "id": row["id"],
        "text": row["text"],
        "options": json.loads(row["options"]),
        "correct_answer": row["correct_answer"],
    }


def quizzes(request):
    """Список тестов или поиск по названию."""
    query = request.GET.get("q", "").strip()
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


def quiz_detail(request, test_id):
    """Страница теста со списком вопросов."""
    conn = get_connection()
    try:
        test = conn.execute(GET_TEST_SQL, (test_id,)).fetchone()
        questions = []
        if test is not None:
            rows = conn.execute(GET_QUESTIONS_SQL, (test_id,)).fetchall()
            questions = [_decode_question(row) for row in rows]
    finally:
        conn.close()

    context = {"test": test, "questions": questions}
    status = 200 if test is not None else 404
    return render(
        request, "quizzes/quiz_detail.html", context, status=status
    )
