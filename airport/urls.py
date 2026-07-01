from django.urls import path, include
from rest_framework import routers

from airport.views import RouteViewSet, FlightViewSet, CountryViewSet, CityViewSet, AirplaneTypeViewSet, AirportViewSet, \
    CrewViewSet, OrderViewSet, AirplaneViewSet

router = routers.DefaultRouter()
router.register("country", CountryViewSet)
router.register("city", CityViewSet)
router.register("airplane_types", AirplaneTypeViewSet)
router.register("flight", FlightViewSet)
router.register("airport", AirportViewSet)
router.register("crew", CrewViewSet)
router.register("airplane", AirplaneViewSet)
router.register("orders", OrderViewSet )
router.register("routes", RouteViewSet)

urlpatterns = [path("", include(router.urls))]

app_name = 'airport'

