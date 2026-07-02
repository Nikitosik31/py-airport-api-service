from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from rest_framework import status

from airport.tests.helpers import sample_flight

ORDER_URL = reverse("airport:order-list")

class OrderApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test",
            password="testtest"
        )
        self.user2 = get_user_model().objects.create_user(
            email="test@test2",
            password="testtest2"
        )
        self.client.force_authenticate(user=self.user)
        self.flight = sample_flight()

    def test_order_create(self):
        payload = {
            "tickets": [
                {"row": 5, "seat": 5, "flight": self.flight.id}
            ]
        }

        res = self.client.post(ORDER_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)

    def test_user_sees_only_own_orders(self):
        payload1 = {
            "tickets": [
                {"row": 5, "seat": 5, "flight": self.flight.id}
            ]
        }
        payload2 = {
            "tickets": [
                {"row": 5, "seat": 6, "flight": self.flight.id}
            ]
        }
        self.client.post(ORDER_URL, payload1, format="json")

        self.client.force_authenticate(user=self.user2)
        self.client.post(ORDER_URL, payload2, format="json")

        self.client.force_authenticate(user=self.user)
        res = self.client.get(ORDER_URL)
        self.assertEqual(len(res.data["results"]), 1)


    def test_auth_required(self):
        self.client.force_authenticate(user=None)
        res = self.client.get(ORDER_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)