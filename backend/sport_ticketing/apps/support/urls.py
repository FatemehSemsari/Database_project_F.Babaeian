from django.urls import path

from apps.support.views import (
    cancelled_tickets,
    suspicious_payments,
    reports,
    update_report,
    reservations,
    update_reservation,
)


urlpatterns = [

    path(
        "cancelled-tickets/",
        cancelled_tickets,
        name="support-cancelled-tickets",
    ),

    path(
        "suspicious-payments/",
        suspicious_payments,
        name="support-suspicious-payments",
    ),

    path(
        "reports/",
        reports,
        name="support-reports",
    ),

    path(
        "reports/<int:report_id>/",
        update_report,
        name="support-report-update",
    ),

    path(
        "reservations/",
        reservations,
        name="support-reservations",
    ),

    path(
        "reservations/<int:reservation_id>/",
        update_reservation,
        name="support-reservation-update",
    ),
]