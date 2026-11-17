"""Модели приложения attempts: User и Attempt."""

from django.db import models

from quizzes.models import Test


class User(models.Model):
    """Пользователь, проходящий тесты."""

    name = models.CharField(
        max_length=100,
        verbose_name="Имя пользователя",
    )

    class Meta:
        ordering = ["name"]
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"

    def __str__(self) -> str:
        return self.name


class Attempt(models.Model):
    """Попытка прохождения теста пользователем."""

    test = models.ForeignKey(
        Test,
        on_delete=models.PROTECT,        # сохраняем историю попыток
        related_name="attempts",
        verbose_name="Тест",
    )
    user = models.ForeignKey(
        User,
        on_delete=models.PROTECT,        # сохраняем историю попыток
        related_name="attempts",
        verbose_name="Пользователь",
    )
    date = models.DateTimeField(verbose_name="Дата попытки")
    correct = models.PositiveIntegerField(verbose_name="Правильных ответов")
    total = models.PositiveIntegerField(verbose_name="Всего вопросов")
    percent = models.FloatField(verbose_name="Процент")

    class Meta:
        ordering = ["-date", "pk"]
        verbose_name = "Попытка"
        verbose_name_plural = "Попытки"

    def __str__(self) -> str:
        return f"Попытка #{self.pk} — {self.user.name} — {self.test.title}"

    @property
    def grade(self) -> str:
        """Текстовая оценка по проценту."""
        if self.percent >= 90:
            return "Отлично"
        if self.percent >= 75:
            return "Хорошо"
        if self.percent >= 60:
            return "Удовлетворительно"
        return "Неудовлетворительно"
