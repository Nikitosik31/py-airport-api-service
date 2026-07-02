import datetime

from django.contrib.auth import get_user_model
from django.db.models import Model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from airport.models import Ticket
from airport.tests.helpers import (
    sample_airplane,
    sample_flight, sample_route,
)
from django.urls import reverse



ORDER_URL = reverse("airport:order-list")

class TicketValidationTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email="test@test",
            password="testtest"
        )
        self.client.force_authenticate(user=self.user)
        self.airplane = sample_airplane()
        self.flight = sample_flight(airplane=self.airplane, flight_number="PS101")

    def test_ticket_validation_row(self):
        payload = {
            "tickets": [
            {"row": 50, "seat": 1, "flight": self.flight.id}
            ]
        }

        res = self.client.post(ORDER_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_ticket_validation_seat(self):
        payload = {
            "tickets": [
                {"row": 32, "seat": 11, "flight": self.flight.id}
            ]
        }

        res = self.client.post(ORDER_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)


    def test_ticket_validation_seat_and_row(self):
        payload = {
            "tickets": [
                {"row": 50, "seat": 15, "flight": self.flight.id}
            ]
        }

        res = self.client.post(ORDER_URL, payload, format="json")
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_dublicate_tickets_validation(self):
        payload1 = {
            "tickets": [
                {"row": 5, "seat": 5, "flight": self.flight.id}
            ]
        }

        payload2 = {
            "tickets": [
                {"row": 5, "seat": 5, "flight": self.flight.id}
            ]
        }

        res1 = self.client.post(ORDER_URL, payload1, format="json")
        res2 = self.client.post(ORDER_URL, payload2, format="json")
        self.assertEqual(res1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(res2.status_code, status.HTTP_400_BAD_REQUEST)
