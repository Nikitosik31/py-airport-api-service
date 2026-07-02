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
admin.site.register(Order)
admin.site.register(Airport)
admin.site.register(Crew)
admin.site.register(Airplane)
admin.site.register(Route)
admin.site.register(Flight)
admin.site.register(Ticket)
