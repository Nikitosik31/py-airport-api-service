import datetime
from django.utils import timezone

from airport.models import (
    Country,
    City,
    Airport,
    Route,
    AirplaneType,
    Airplane,
    Flight,
)


def sample_country(**params):
    defaults = {
        "name": "Sample country",
    }
    defaults.update(params)
    return Country.objects.create(**defaults)


def sample_city(**params):
    defaults = {
        "name": "Sample city",
        "country": sample_country(),
    }
    defaults.update(params)
    return City.objects.create(**defaults)


def sample_airport(**params):
    defaults = {
        "name": "Sample airport",
        "city": sample_city(),
    }
    defaults.update(params)
    return Airport.objects.create(**defaults)


def sample_route(**params):
    defaults = {
        "source": sample_airport(),
        "destination": sample_airport(),
        "distance": 10,
    }
    defaults.update(params)
    return Route.objects.create(**defaults)


def sample_airplane_type(**params):
    defaults = {
        "name": "Sample airplane type",
    }
    defaults.update(params)
    return AirplaneType.objects.create(**defaults)


def sample_airplane(**params):
    defaults = {
        "name": "Sample airplane",
        "rows": 40,
        "seats_in_row": 10,
        "airplane_type": sample_airplane_type(),
    }
    defaults.update(params)
    return Airplane.objects.create(**defaults)


def sample_flight(**params):
    defaults = {
        "route": sample_route(),
        "airplane": sample_airplane(),
        "departure_time": datetime.datetime(2020, 1, 1, 10, 0, tzinfo=datetime.timezone.utc),
        "arrival_time": datetime.datetime(2020, 1, 2, 13, 0, tzinfo=datetime.timezone.utc),
        "flight_number": 10,
    }
    defaults.update(params)
    return Flight.objects.create(**defaults)
