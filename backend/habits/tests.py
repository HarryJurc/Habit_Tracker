import datetime
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.core.exceptions import ValidationError
from habits.models import Habit

User = get_user_model()


class HabitTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(email="user1@example.com", password="pass1234")
        self.other_user = User.objects.create_user(email="user2@example.com", password="pass1234")

        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {refresh.access_token}")

        self.habit = Habit.objects.create(
            user=self.user,
            place="Home",
            time=datetime.time(9, 0),
            action="Read book",
            is_pleasant=False,
            periodicity=1,
            execution_time=30,
            is_public=False,
        )

        self.public_habit = Habit.objects.create(
            user=self.other_user,
            place="Park",
            time=datetime.time(10, 0),
            action="Jogging",
            is_pleasant=True,
            periodicity=1,
            execution_time=60,
            is_public=True,
        )

    def test_create_habit(self):
        url = reverse("habits-list")
        data = {
            "place": "Gym",
            "time": "18:00:00",
            "action": "Workout",
            "is_pleasant": False,
            "periodicity": 3,
            "execution_time": 45,
            "is_public": False,
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.data["place"], "Gym")

    def test_get_own_habits(self):
        url = reverse("habits-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["action"], self.habit.action)

    def test_update_own_habit(self):
        url = reverse("habits-detail", args=[self.habit.id])
        response = self.client.patch(url, {"place": "Office"}, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["place"], "Office")

    def test_delete_own_habit(self):
        url = reverse("habits-detail", args=[self.habit.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 204)
        self.assertFalse(Habit.objects.filter(id=self.habit.id).exists())

    def test_forbid_update_foreign_habit(self):
        url = reverse("habits-detail", args=[self.public_habit.id])
        response = self.client.patch(url, {"place": "Mall"}, format="json")
        self.assertEqual(response.status_code, 403)

    def test_forbid_delete_foreign_habit(self):
        url = reverse("habits-detail", args=[self.public_habit.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 403)

    def test_see_public_habits(self):
        url = reverse("habits-list") + "?public=true"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data["results"]), 1)
        self.assertEqual(response.data["results"][0]["action"], self.public_habit.action)

    def test_pagination(self):
        for i in range(7):
            Habit.objects.create(
                user=self.user,
                place=f"Place {i}",
                time=datetime.time(12, 0),
                action=f"Action {i}",
                is_pleasant=True,
                periodicity=1,
                execution_time=30,
                is_public=False,
            )
        url = reverse("habits-list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn("results", response.data)
        self.assertEqual(len(response.data["results"]), 5)  # Страница по 5 элементов
        self.assertEqual(response.data["count"], 8)

    def test_execution_time_too_long_raises(self):
        habit = Habit(
            user=self.user,
            place="Gym",
            time=datetime.time(10, 0),
            action="Workout",
            execution_time=130,
            periodicity=1,
            is_pleasant=False,
            is_public=False,
        )
        with self.assertRaises(ValidationError) as cm:
            habit.full_clean()
        self.assertIn("Время выполнения не может превышать 120 секунд.", str(cm.exception))

    def test_periodicity_out_of_range_raises(self):
        habit = Habit(
            user=self.user,
            place="Office",
            time=datetime.time(11, 0),
            action="Email checking",
            execution_time=30,
            periodicity=8,
            is_pleasant=False,
            is_public=False,
        )
        with self.assertRaises(ValidationError) as cm:
            habit.full_clean()
        self.assertIn("Периодичность должна быть от 1 до 7 дней.", str(cm.exception))

    def test_pleasant_habit_cannot_have_reward_or_linked(self):
        habit = Habit(
            user=self.user,
            place="Park",
            time=datetime.time(12, 0),
            action="Jogging",
            is_pleasant=True,
            reward="Ice cream",
            execution_time=45,
            periodicity=2,
            is_public=False,
        )
        with self.assertRaises(ValidationError) as cm:
            habit.full_clean()
        self.assertIn("Приятная привычка не может иметь награду или связанную привычку.", str(cm.exception))

        linked = Habit.objects.create(
            user=self.user,
            place="Home",
            time=datetime.time(9, 0),
            action="Reading",
            is_pleasant=True,
            execution_time=30,
            periodicity=1,
            is_public=False,
        )
        habit.reward = None
        habit.linked_habit = linked
        with self.assertRaises(ValidationError) as cm2:
            habit.full_clean()
        self.assertIn("Приятная привычка не может иметь награду или связанную привычку.", str(cm2.exception))

    def test_non_pleasant_habit_cannot_have_both_reward_and_linked(self):
        linked = Habit.objects.create(
            user=self.user,
            place="Home",
            time=datetime.time(9, 0),
            action="Reading",
            is_pleasant=True,
            execution_time=30,
            periodicity=1,
            is_public=False,
        )
        habit = Habit(
            user=self.user,
            place="Office",
            time=datetime.time(13, 0),
            action="Work",
            is_pleasant=False,
            reward="Coffee",
            linked_habit=linked,
            execution_time=50,
            periodicity=3,
            is_public=False,
        )
        with self.assertRaises(ValidationError) as cm:
            habit.full_clean()
        self.assertIn("Укажите либо награду, либо связанную привычку, но не оба поля.", str(cm.exception))

    def test_linked_habit_must_belong_to_same_user(self):
        other_user = User.objects.create_user(email="other@example.com", password="pass1234")
        linked = Habit.objects.create(
            user=other_user,
            place="Cafe",
            time=datetime.time(14, 0),
            action="Coffee break",
            is_pleasant=True,
            execution_time=15,
            periodicity=1,
            is_public=False,
        )
        habit = Habit(
            user=self.user,
            place="Office",
            time=datetime.time(15, 0),
            action="Meeting",
            is_pleasant=False,
            linked_habit=linked,
            execution_time=40,
            periodicity=1,
            is_public=False,
        )
        with self.assertRaises(ValidationError) as cm:
            habit.full_clean()
        self.assertIn("Нельзя ссылаться на чужую привычку.", str(cm.exception))

    def test_str_method(self):
        habit = Habit.objects.create(
            user=self.user,
            place="Library",
            time=datetime.time(15, 30),
            action="Read",
            is_pleasant=False,
            periodicity=1,
            execution_time=20,
            is_public=False,
        )
        self.assertEqual(str(habit), "Read в Library (15:30:00)")

    def test_non_pleasant_habit_without_reward_and_linked(self):
        habit = Habit(
            user=self.user,
            place="Test place",
            time=datetime.time(12, 0),
            action="Test action",
            is_pleasant=False,
            periodicity=3,
            execution_time=30,
            is_public=False,
            reward=None,
            linked_habit=None,
        )
        habit.full_clean()

    def test_pleasant_habit_without_reward_and_linked(self):
        habit = Habit(
            user=self.user,
            place="Test place",
            time=datetime.time(12, 0),
            action="Test action",
            is_pleasant=True,
            periodicity=1,
            execution_time=30,
            is_public=False,
            reward=None,
            linked_habit=None,
        )
        habit.full_clean()

    def test_non_pleasant_with_linked_same_user(self):
        linked = Habit.objects.create(
            user=self.user,
            place="Linked place",
            time=datetime.time(10, 0),
            action="Linked action",
            is_pleasant=True,
            execution_time=30,
            periodicity=1,
            is_public=False,
        )
        habit = Habit(
            user=self.user,
            place="Test place",
            time=datetime.time(13, 0),
            action="Test action",
            is_pleasant=False,
            periodicity=2,
            execution_time=40,
            is_public=False,
            reward=None,
            linked_habit=linked,
        )
        habit.full_clean()

    def test_periodicity_lower_bound(self):
        habit = Habit(
            user=self.user,
            place="Test place",
            time=datetime.time(14, 0),
            action="Test action",
            is_pleasant=False,
            periodicity=1,
            execution_time=30,
            is_public=False,
        )
        habit.full_clean()

    def test_periodicity_upper_bound(self):
        habit = Habit(
            user=self.user,
            place="Test place",
            time=datetime.time(14, 0),
            action="Test action",
            is_pleasant=False,
            periodicity=7,
            execution_time=30,
            is_public=False,
        )
        habit.full_clean()
