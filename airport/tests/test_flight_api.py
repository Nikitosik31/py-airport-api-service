import datetime
import tempfile
import os

from PIL import Image
from django.contrib.auth import get_user_model
from django.db.models import Count, F
from django.test import TestCase
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

from airport.models import (
    Country,
    City,
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Flight,
)
from airport.serializers import FlightListSerializer, FlightDetailSerializer
from airport.tests.helpers import (
    sample_city,
    sample_airport,
    sample_route,
    sample_airplane_type,
    sample_airplane,
    sample_flight,
)

AIRPLANE_URL = reverse("airport:airplane-list")
FLIGHT_URL = reverse("airport:flight-list")


def get_flight_queryset():
    return Flight.objects.annotate(
        tickets_available=(
            F("airplane__rows") * F("airplane__seats_in_row")
            - Count("tickets")
        )
    )


def image_upload_url(airplane_id):
    """Return URL for airplane image upload"""
    return reverse("airport:airplane-upload-image", args=[airplane_id])


def detail_url(airplane_id):
    return reverse("airport:flight-detail", args=[airplane_id])


def airplane_detail_url(airplane_id):
    return reverse("airport:airplane-detail", args=[airplane_id])


class UnauthenticatedFlightApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        res = self.client.get(FLIGHT_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthenticatedFlightApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "test@test.com",
            "testpass",
        )
        self.client.force_authenticate(self.user)

    def test_list_flight(self):
        sample_flight(flight_number="PS101")
        sample_flight(flight_number="PS102")

        res = self.client.get(FLIGHT_URL)

        flights = get_flight_queryset().order_by("id")

        serializer = FlightListSerializer(flights, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data["results"], serializer.data)

    def test_filter_flight_by_airplane_id_str(self):
        airplane1 = sample_airplane(name="Airplane1")
        airplane2 = sample_airplane(name="Airplane2")

        flight1 = sample_flight(flight_number="PS101", airplane=airplane1)
        flight2 = sample_flight(flight_number="PS102", airplane=airplane2)

        res = self.client.get(FLIGHT_URL, {"airplane": airplane1.id})

        annotated_flight = get_flight_queryset().get(id=flight1.id)
        annotated_flight2 = get_flight_queryset().get(id=flight2.id)

        serializer1 = FlightListSerializer(annotated_flight)
        serializer2 = FlightListSerializer(annotated_flight2)

        self.assertNotIn(serializer2.data, res.data["results"])
        self.assertIn(serializer1.data, res.data["results"])

    def test_filter_flight_by_date(self):
        flight1 = sample_flight(flight_number="PS102")
        flight2 = sample_flight(
            flight_number="PS103",
            departure_time=datetime.datetime(2021, 5, 5, 10, 0, tzinfo=datetime.timezone.utc),
            arrival_time=datetime.datetime(2021, 5, 5, 14, 0, tzinfo=datetime.timezone.utc),
        )

        res = self.client.get(FLIGHT_URL, {"date": "2020-01-01"})

        annotated_flight = get_flight_queryset().get(id=flight1.id)
        annotated_flight2 = get_flight_queryset().get(id=flight2.id)

        serializer1 = FlightListSerializer(annotated_flight)
        serializer2 = FlightListSerializer(annotated_flight2)

        self.assertNotIn(serializer2.data, res.data["results"])
        self.assertIn(serializer1.data, res.data["results"])

    def test_filter_flight_by_sours(self):
        city1 = sample_city(name="Kyiv")
        city2 = sample_city(name="Barcelona")

        airport1 = sample_airport(name="Boryspil", city=city1)
        airport2 = sample_airport(name="El Prat", city=city2)

        route1 = sample_route(source=airport1)
        route2 = sample_route(source=airport2)

        flight1 = sample_flight(flight_number="PS101", route=route1)
        flight2 = sample_flight(flight_number="PS102", route=route2)

        res = self.client.get(FLIGHT_URL, {"source": "Kyiv"})

        annotated_flight = get_flight_queryset().get(id=flight1.id)
        annotated_flight2 = get_flight_queryset().get(id=flight2.id)

        serializer1 = FlightListSerializer(annotated_flight)
        serializer2 = FlightListSerializer(annotated_flight2)

        self.assertNotIn(serializer2.data, res.data["results"])
        self.assertIn(serializer1.data, res.data["results"])

    def test_filter_flight_by_destination(self):
        city1 = sample_city(name="Kyiv")
        city2 = sample_city(name="Barcelona")

        airport1 = sample_airport(name="Boryspil", city=city1)
        airport2 = sample_airport(name="El Prat", city=city2)

        route1 = sample_route(destination=airport1)
        route2 = sample_route(destination=airport2)

        flight1 = sample_flight(flight_number="PS101", route=route1)
        flight2 = sample_flight(flight_number="PS102", route=route2)

        res = self.client.get(FLIGHT_URL, {"destination": "Kyiv"})

        annotated_flight = get_flight_queryset().get(id=flight1.id)
        annotated_flight2 = get_flight_queryset().get(id=flight2.id)

        serializer1 = FlightListSerializer(annotated_flight)
        serializer2 = FlightListSerializer(annotated_flight2)

        self.assertNotIn(serializer2.data, res.data["results"])
        self.assertIn(serializer1.data, res.data["results"])

    def test_retrieve_flight_detail(self):
        flight = sample_flight(flight_number="PS101")

        url = detail_url(flight.id)
        res = self.client.get(url)

        annotated_flight = get_flight_queryset().get(id=flight.id)

        serializer = FlightDetailSerializer(annotated_flight)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_flight_forbidden(self):
        payload = {}
        res = self.client.post(FLIGHT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)


class AdminFlightApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            "admin@admin.com", "testpass", is_staff=True
        )
        self.client.force_authenticate(self.user)

    def test_create_flight(self):
        route = sample_route()
        airplane = sample_airplane()

        payload = {
            "route": route.id,
            "airplane": airplane.id,
            "departure_time": "2020-01-01T10:00:00",
            "arrival_time": "2020-01-02T13:00:00",
            "flight_number": "PS101",
        }
        res = self.client.post(FLIGHT_URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)


class AirplaneImageUploadTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_superuser(
            "admin@myproject.com", "password"
        )
        self.client.force_authenticate(self.user)
        self.airplane = sample_airplane()

    def tearDown(self):
        self.airplane.image.delete()

    def test_upload_image_to_airplane(self):
        """Test uploading an image to airplane"""
        url = image_upload_url(self.airplane.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            res = self.client.post(url, {"image": ntf}, format="multipart")
        self.airplane.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertIn("image", res.data)
        self.assertTrue(os.path.exists(self.airplane.image.path))

    def test_upload_image_bad_request(self):
        """Test uploading an invalid image"""
        url = image_upload_url(self.airplane.id)
        res = self.client.post(url, {"image": "not image"}, format="multipart")

        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_post_image_to_airplane_list_should_not_work(self):
        url = AIRPLANE_URL
        airplane_type = sample_airplane_type()
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            res = self.client.post(
                url,
                {
                    "name": "Name",
                    "rows": "50",
                    "seats_in_row": 5,
                    "airplane_type": airplane_type.id,
                    "image": ntf,
                },
                format="multipart",
            )

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        airplane = Airplane.objects.get(name="Name")
        self.assertFalse(airplane.image)

    def test_image_url_is_shown_on_airplane_detail(self):
        url = image_upload_url(self.airplane.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            self.client.post(url, {"image": ntf}, format="multipart")
        res = self.client.get(airplane_detail_url(self.airplane.id))

        self.assertIn("image", res.data)

    def test_image_url_is_shown_on_airplane_list(self):
        url = image_upload_url(self.airplane.id)
        with tempfile.NamedTemporaryFile(suffix=".jpg") as ntf:
            img = Image.new("RGB", (10, 10))
            img.save(ntf, format="JPEG")
            ntf.seek(0)
            self.client.post(url, {"image": ntf}, format="multipart")
        res = self.client.get(AIRPLANE_URL)

        self.assertIn("image", res.data["results"][0].keys())

    def test_put_airplane_not_allowed(self):
        airplane_type = sample_airplane_type()

        payload = {
            "name": "Name",
            "rows": "50",
            "seats_in_row": 5,
            "airplane_type": airplane_type.id,
        }

        airplane = sample_airplane()
        url = airplane_detail_url(airplane.id)

        res = self.client.put(url, payload)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_delete_airplane_not_allowed(self):
        airplane = sample_airplane()
        url = airplane_detail_url(airplane.id)

        res = self.client.delete(url)

        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
