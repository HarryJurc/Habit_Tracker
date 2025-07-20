import datetime
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from habits.models import Habit

User = get_user_model()


class HabitTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        self.user = User.objects.create_user(username="user1", password="pass1234")
        self.other_user = User.objects.create_user(username="user2", password="pass1234")

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
        self.assertEqual(len(response.data["results"]), 5)
        self.assertEqual(response.data["count"], 8)
