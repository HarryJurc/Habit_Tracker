from celery import shared_task
from django.contrib.auth import get_user_model
from .models import Habit
import datetime
import telegram
import os
from dotenv import load_dotenv

User = get_user_model()

load_dotenv()

TOKEN = os.getenv("TELEGRAM_TOKEN")


@shared_task
def send_telegram_reminder(user_id, habit_id):
    try:
        user = User.objects.get(pk=user_id)
        habit = Habit.objects.get(pk=habit_id)
        chat_id = user.profile.telegram_chat_id

        bot = telegram.Bot(token=TOKEN)
        text = (
            f"Напоминание: пора выполнить привычку '{habit.action}' в {habit.time.strftime('%H:%M')} в {habit.place}."
        )
        bot.send_message(chat_id=chat_id, text=text)
    except Exception as e:
        print(f"Ошибка отправки напоминания: {e}")


@shared_task
def schedule_daily_reminders():
    today = datetime.date.today()
    habits = Habit.objects.filter(is_public=False, is_pleasant=False)
    for habit in habits:
        delta = (today - habit.created_at.date()).days
        if delta % habit.periodicity == 0:
            send_telegram_reminder.delay(habit.user.id, habit.id)
