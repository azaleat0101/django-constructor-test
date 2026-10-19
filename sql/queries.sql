-- 1. СПИСОК: все тесты с количеством вопросов
SELECT
    tests.id,
    tests.title,
    tests.description,
    COUNT(questions.id) AS questions_count
FROM tests
LEFT JOIN questions ON questions.test_id = tests.id
GROUP BY tests.id, tests.title, tests.description
ORDER BY tests.title;


-- 2. СПИСОК: все попытки с именем пользователя и названием теста
SELECT
    attempts.id,
    attempts.date,
    attempts.correct,
    attempts.total,
    attempts.percent,
    users.name AS user_name,
    tests.title AS test_title
FROM attempts
JOIN users ON attempts.user_id = users.id
JOIN tests ON attempts.test_id = tests.id
ORDER BY attempts.date DESC;


-- 3. ФИЛЬТРАЦИЯ (WHERE): тесты с числом вопросов не меньше N
SELECT
    tests.id,
    tests.title,
    COUNT(questions.id) AS questions_count
FROM tests
JOIN questions ON questions.test_id = tests.id
GROUP BY tests.id, tests.title
HAVING COUNT(questions.id) >= ?;


-- 4. ФИЛЬТРАЦИЯ (WHERE): поиск тестов по подстроке в названии
SELECT id, title, description
FROM tests
WHERE LOWER(title) LIKE LOWER(?)
ORDER BY title;


-- 5. ФИЛЬТРАЦИЯ (WHERE): успешные попытки (процент >= 60)
SELECT
    attempts.id,
    attempts.percent,
    users.name AS user_name,
    tests.title AS test_title
FROM attempts
JOIN users ON attempts.user_id = users.id
JOIN tests ON attempts.test_id = tests.id
WHERE attempts.percent >= 60
ORDER BY attempts.percent DESC;


-- 6. JOIN: полная информация о попытке по её id
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
WHERE attempts.id = ?;


-- 7. JOIN: вопросы с названием теста
SELECT
    questions.id,
    tests.title AS test_title,
    questions.text,
    questions.options,
    questions.correct_answer
FROM questions
JOIN tests ON questions.test_id = tests.id
WHERE questions.test_id = ?
ORDER BY questions.id;


-- 8. АГРЕГАТ: общее количество тестов
SELECT COUNT(*) AS tests_count
FROM tests;


-- 9. АГРЕГАТ: статистика попыток
SELECT
    COUNT(*) AS attempts_count,
    COALESCE(AVG(percent), 0) AS average_percent,
    COALESCE(MAX(percent), 0) AS best_percent,
    COALESCE(MIN(percent), 0) AS worst_percent
FROM attempts;


-- 10. АГРЕГАТ: количество вопросов в конкретном тесте
SELECT COUNT(*) AS questions_count
FROM questions
WHERE test_id = ?;


-- 11. ГРУППИРОВКА (GROUP BY): попытки и средний балл по тестам
SELECT
    tests.id,
    tests.title,
    COUNT(attempts.id) AS attempts_count,
    AVG(attempts.percent) AS average_percent
FROM tests
LEFT JOIN attempts ON attempts.test_id = tests.id
GROUP BY tests.id, tests.title
ORDER BY attempts_count DESC, tests.title;


-- 12. ГРУППИРОВКА (GROUP BY): активность пользователей
SELECT
    users.id,
    users.name,
    COUNT(attempts.id) AS attempts_count,
    AVG(attempts.percent) AS average_percent
FROM users
LEFT JOIN attempts ON attempts.user_id = users.id
GROUP BY users.id, users.name
ORDER BY attempts_count DESC, users.name;


-- 13. ГРУППИРОВКА + HAVING: тесты, пройденные более одного раза
SELECT
    tests.id,
    tests.title,
    COUNT(attempts.id) AS attempts_count
FROM tests
JOIN attempts ON attempts.test_id = tests.id
GROUP BY tests.id, tests.title
HAVING COUNT(attempts.id) > 1;
