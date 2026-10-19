"""View-функции для работы с попытками (через SQL)."""

from django.shortcuts import render

from db.database import get_connection


_LIST_SQL = """
SELECT
    attempts.id,
    attempts.date,
    attempts.correct,
    attempts.total,
    attempts.percent,
    users.name AS user_name,
    tests.title AS test_title,
    CASE
        WHEN attempts.percent >= 90 THEN 'Отлично'
        WHEN attempts.percent >= 75 THEN 'Хорошо'
        WHEN attempts.percent >= 60 THEN 'Удовлетворительно'
        ELSE 'Неудовлетворительно'
    END AS grade
FROM attempts
JOIN users ON attempts.user_id = users.id
JOIN tests ON attempts.test_id = tests.id
{where}
ORDER BY {order};
"""


def attempts(request):
    """Список попыток: все или только успешные."""
    show_successful = request.GET.get("success") == "1"

    if show_successful:
        sql = _LIST_SQL.format(
            where="WHERE attempts.percent >= ?",
            order="attempts.percent DESC",
        )
        params = (60,)
    else:
        sql = _LIST_SQL.format(where="", order="attempts.date DESC")
        params = ()

    conn = get_connection()
    try:
        attempts_list = conn.execute(sql, params).fetchall()
    finally:
        conn.close()

    return render(
        request,
        "attempts/attempt_list.html",
        {"attempts": attempts_list, "show_successful": show_successful},
    )


def attempt_detail(request, attempt_id):
    """Страница одной попытки."""
    sql = _LIST_SQL.format(
        where="WHERE attempts.id = ?",
        order="attempts.id",
    )
    conn = get_connection()
    try:
        attempt = conn.execute(sql, (attempt_id,)).fetchone()
    finally:
        conn.close()

    status = 200 if attempt is not None else 404
    return render(
        request,
        "attempts/attempt_detail.html",
        {"attempt": attempt},
        status=status,
    )
