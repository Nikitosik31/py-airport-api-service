from django.urls import path, include
from rest_framework import routers

from airport.views import (
    RouteViewSet,
    FlightViewSet,
    CountryViewSet,
    CityViewSet,
    AirplaneTypeViewSet,
    AirportViewSet,
    CrewViewSet,
    OrderViewSet,
    AirplaneViewSet,
)

router = routers.DefaultRouter()
router.register("countries", CountryViewSet)
router.register("cities", CityViewSet)
router.register("airplane-types", AirplaneTypeViewSet)
router.register("flights", FlightViewSet)
router.register("airports", AirportViewSet)
router.register("crews", CrewViewSet)
router.register("airplanes", AirplaneViewSet)
router.register("orders", OrderViewSet, basename="order")
router.register("routes", RouteViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = "airport"
