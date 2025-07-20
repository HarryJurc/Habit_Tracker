from django.contrib.auth.models import AbstractUser
from django.db import models


class CustomUser(AbstractUser):
    telegram_chat_id = models.CharField(
        max_length=64, blank=True, null=True, help_text="Telegram chat ID для отправки уведомлений"
    )

    def __str__(self):
        return self.username
