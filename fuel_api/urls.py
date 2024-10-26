from django.urls import path
from .views import route_with_fuel_stops

urlpatterns = [
    path('route/', route_with_fuel_stops, name='route_with_fuel_stops')
]
