from django.urls import path
from apps.reservations.views import available_seats, create_reservation, my_reservations


urlpatterns = [
    path("seats/", available_seats, name="available-seats"),
    path("", create_reservation, name="create-reservation"),
    path("mine/", my_reservations, name="my-reservations"),
]