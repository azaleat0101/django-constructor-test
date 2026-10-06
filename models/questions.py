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

    def update(
        self,
        text: str | None = None,
        options: list[str] | None = None,
        correct_answer: str | None = None,
    ) -> None:
        """Обновить поля вопроса.

        Параметр None означает «не менять соответствующее поле».
        Валидация выполняется как в конструкторе.
        """
        new_text = self.text if text is None else text.strip()
        if not new_text:
            raise ValueError("Текст вопроса не может быть пустым.")

        new_options = self.options if options is None else list(options)
        if len(new_options) < 2:
            raise ValueError("Нужно минимум 2 варианта ответа.")

        new_correct = (
            self.correct_answer
            if correct_answer is None
            else correct_answer.strip()
        )
        if new_correct not in new_options:
            raise ValueError("Правильный ответ должен входить в варианты.")

        self.text = new_text
        self.options = new_options
        self.correct_answer = new_correct

    def check_answer(self, user_answer: str) -> bool:
        """Проверить ответ без учёта регистра и пробелов."""
        return user_answer.strip().lower() == self.correct_answer.lower()

    def to_data(self) -> dict:
        return {
            "text": self.text,
            "options": self.options,
            "correct_answer": self.correct_answer,
        }

    @classmethod
    def from_data(cls, data: dict) -> "Question":
        return cls(
            text=data["text"],
            options=data["options"],
            correct_answer=data["correct_answer"],
        )

    def __str__(self) -> str:
        return f"{self.text} ({' / '.join(self.options)})"
