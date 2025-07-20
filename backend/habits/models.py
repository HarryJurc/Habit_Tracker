from django.db import models
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

User = get_user_model()


class Habit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="habits")
    place = models.CharField(max_length=255)
    time = models.TimeField()
    action = models.CharField(max_length=255)
    is_pleasant = models.BooleanField(default=False)
    linked_habit = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)
    periodicity = models.PositiveSmallIntegerField(default=1, help_text="Раз в X дней")
    reward = models.CharField(max_length=255, null=True, blank=True)
    execution_time = models.PositiveSmallIntegerField(help_text="Время в секундах")
    is_public = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        if self.execution_time > 120:
            raise ValidationError("Время выполнения не может превышать 120 секунд.")

        if not (1 <= self.periodicity <= 7):
            raise ValidationError("Периодичность должна быть от 1 до 7 дней.")

        if self.is_pleasant:
            if self.reward or self.linked_habit:
                raise ValidationError("Приятная привычка не может иметь награду или связанную привычку.")
        else:
            if self.reward and self.linked_habit:
                raise ValidationError("Укажите либо награду, либо связанную привычку, но не оба поля.")
            if self.linked_habit and not self.linked_habit.is_pleasant:
                raise ValidationError("Связанной может быть только приятная привычка.")

    def __str__(self):
        return f"{self.action} в {self.place} ({self.time})"
