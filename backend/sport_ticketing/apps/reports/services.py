from django.db import transaction
from rest_framework.exceptions import (
    NotFound,
    ValidationError,
)
from apps.reports.repositories import (
    ReportRepository,
)


class ReportService:

    @staticmethod
    def create_report(user_id, validated_data):
        ticket_id = validated_data.get("ticket_id")
        reservation_id = validated_data.get("reservation_id")
        issue_type = validated_data["issue_type"]
        message = validated_data["message"]
        with transaction.atomic():
            ticket = None
            reservation = None
            if ticket_id is not None:
                ticket = ReportRepository.get_user_ticket(ticket_id=ticket_id, user_id=user_id)
                if ticket is None:
                    raise NotFound(
                        "Ticket not found."
                    )
            if reservation_id is not None:
                reservation = ReportRepository.get_user_reservation(reservation_id=reservation_id, user_id=user_id)
                if reservation is None:
                    raise NotFound(
                        "Reservation not found."
                    )
            if (ticket is not None and reservation is not None and ticket["reservation_id"] != reservation["reservation_id"]):
                raise ValidationError(
                    {
                        "reservation_id": (
                            "The reservation does not "
                            "belong to the specified "
                            "ticket."
                        )
                    }
                )
            if (ticket is not None and reservation_id is None):
                reservation_id = ticket["reservation_id"]
            report = (
                ReportRepository.create_report(
                    user_id=user_id,
                    ticket_id=ticket_id,
                    reservation_id=(
                        reservation_id
                    ),
                    issue_type=issue_type,
                    message=message,
                )
            )
        return report

    @staticmethod
    def get_user_reports(user_id):
        return (
            ReportRepository
            .list_user_reports(
                user_id=user_id
            )
        )