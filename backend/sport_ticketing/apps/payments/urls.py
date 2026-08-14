from django.urls import path
from apps.payments.views import (
    pay_reservation,
)


urlpatterns = [
    path("", pay_reservation, name="pay-reservation"),
]