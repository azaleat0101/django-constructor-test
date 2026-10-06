"""Класс Question — вопрос теста с вариантами ответов."""


class Question:
    """Вопрос теста."""

    def __init__(
        self,
        text: str,
        options: list[str],
        correct_answer: str,
    ) -> None:
        cleaned_text = text.strip()
        if not cleaned_text:
            raise ValueError("Текст вопроса не может быть пустым.")
        if len(options) < 2:
            raise ValueError("Нужно минимум 2 варианта ответа.")

        cleaned_correct = correct_answer.strip()
        if cleaned_correct not in options:
            raise ValueError("Правильный ответ должен входить в варианты.")

        self.text = cleaned_text
        self.options = list(options)
        self.correct_answer = cleaned_correct

    def check_answer(self, user_answer: str) -> bool:
        """Проверить ответ без учёта регистра и пробелов."""
        return user_answer.strip().lower() == self.correct_answer.lower()

    def to_data(self) -> dict:
        """Преобразовать объект в словарь для JSON."""
        return {
            "text": self.text,
            "options": self.options,
            "correct_answer": self.correct_answer,
        }

    @classmethod
    def from_data(cls, data: dict) -> "Question":
        """Создать Question из словаря."""
        return cls(
            text=data["text"],
            options=data["options"],
            correct_answer=data["correct_answer"],
        )

    def __str__(self) -> str:
        return f"{self.text} ({' / '.join(self.options)})"