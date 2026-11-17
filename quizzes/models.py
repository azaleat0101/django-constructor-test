"""Модели приложения quizzes: Test и Question."""

from django.db import models


class Test(models.Model):
    """Тест: набор вопросов с названием и описанием."""

    title = models.CharField(
        max_length=200,
        verbose_name="Название теста",
    )
    description = models.TextField(
        blank=True,
        default="",
        verbose_name="Описание",
    )

    class Meta:
        ordering = ["title"]
        verbose_name = "Тест"
        verbose_name_plural = "Тесты"

    def __str__(self) -> str:
        return self.title


class Question(models.Model):
    """Вопрос теста с вариантами ответов и правильным вариантом."""

    test = models.ForeignKey(
        Test,
        on_delete=models.CASCADE,       # вопросы не существуют без теста
        related_name="questions",
        verbose_name="Тест",
    )
    text = models.TextField(verbose_name="Текст вопроса")
    options = models.JSONField(
        default=list,
        verbose_name="Варианты ответов",
    )
    correct_answer = models.CharField(
        max_length=255,
        verbose_name="Правильный ответ",
    )

    class Meta:
        ordering = ["id"]
        verbose_name = "Вопрос"
        verbose_name_plural = "Вопросы"

    def __str__(self) -> str:
        return self.text[:60]
