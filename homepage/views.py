"""View-функции главной страницы и страницы статистики."""

from django.shortcuts import render

from db.database import get_connection


TESTS_COUNT_SQL = "SELECT COUNT(*) AS tests_count FROM tests;"

ATTEMPTS_STATS_SQL = """
SELECT
    COUNT(*) AS attempts_count,
    COALESCE(AVG(percent), 0) AS average_percent,
    COALESCE(MAX(percent), 0) AS best_percent,
    COALESCE(MIN(percent), 0) AS worst_percent
FROM attempts;
"""

TESTS_STATS_SQL = """
SELECT
    tests.id,
    tests.title,
    COUNT(attempts.id) AS attempts_count,
    AVG(attempts.percent) AS average_percent
FROM tests
LEFT JOIN attempts ON attempts.test_id = tests.id
GROUP BY tests.id, tests.title
ORDER BY attempts_count DESC, tests.title;
"""

USERS_STATS_SQL = """
SELECT
    users.id,
    users.name,
    COUNT(attempts.id) AS attempts_count,
    AVG(attempts.percent) AS average_percent
FROM users
LEFT JOIN attempts ON attempts.user_id = users.id
GROUP BY users.id, users.name
ORDER BY attempts_count DESC, users.name;
"""


def index(request):
    """Главная страница."""
    return render(request, "homepage/index.html")


def statistics(request):
    """Страница статистики по данным проекта."""
    conn = get_connection()
    try:
        tests_count = conn.execute(TESTS_COUNT_SQL).fetchone()["tests_count"]
        attempts_stats = conn.execute(ATTEMPTS_STATS_SQL).fetchone()
        tests_stats = conn.execute(TESTS_STATS_SQL).fetchall()
        users_stats = conn.execute(USERS_STATS_SQL).fetchall()
    finally:
        conn.close()

    return render(
        request,
        "homepage/statistics.html",
        {
            "tests_count": tests_count,
            "attempts_stats": attempts_stats,
            "tests_stats": tests_stats,
            "users_stats": users_stats,
        },
    )
