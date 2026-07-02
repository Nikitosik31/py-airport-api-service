from django.contrib import admin

from airport.models import (
    Order,
    AirplaneType,
    Country,
    City,
    Airport,
    Crew,
    Airplane,
    Route,
    Flight,
    Ticket,
)

admin.site.register(AirplaneType)
admin.site.register(Country)
admin.site.register(Airport)
admin.site.register(Crew)
admin.site.register(City)

@admin.register(Flight)
class FlightAdmin(admin.ModelAdmin):
    list_display = (
        "flight_number",
        "route",
        "departure_time",
        "arrival_time",
        "airplane",
    )

    list_filter = ("departure_time", "airplane",)

    search_fields = ("flight_number",)

@admin.register(Airplane)
class AirplaneAdmin(admin.ModelAdmin):
    list_display = ("name", "rows", "seats_in_row", "airplane_type")

    list_filter = ("airplane_type",)
    search_fields = ("name",)


@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ("source", "destination", "distance",)

    list_filter = ("source", "destination", )
    search_fields = ("source__name", "destination__name", "distance",)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("created_at", "user",)
    list_filter = ("created_at",)
    search_fields = ("user__email",)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ("row", "seat", "flight", "order")
    list_filter = ("flight", "order",)
    search_fields = ("flight__flight_number", "order__created_at",)
