from __future__ import annotations

from django.core.validators import MinLengthValidator
from django.db import models


class MailingMessage(models.Model):
    external_id = models.CharField(
        max_length=255,
        unique=True,
        validators=[MinLengthValidator(1)],
        verbose_name="Внешний идентификатор",
    )
    user_id = models.CharField(max_length=255, verbose_name="Идентификатор пользователя")
    email = models.EmailField(verbose_name="Email получателя")
    subject = models.CharField(max_length=255, verbose_name="Тема письма")
    message = models.TextField(verbose_name="Текст письма")

    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Создано")
    sent_at = models.DateTimeField(null=True, blank=True, verbose_name="Отправлено")

    class Meta:
        verbose_name = "Письмо рассылки"
        verbose_name_plural = "Письма рассылки"
        indexes = [models.Index(fields=["external_id"])]

    def __str__(self) -> str:
        return f"{self.external_id} -> {self.email}"

