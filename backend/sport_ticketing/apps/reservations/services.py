import uuid
from datetime import timedelta
from django.conf import settings
from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import (
    APIException,
    NotFound,
    ValidationError,
)
from apps.reservations.repositories import (
    ReservationRepository,
)
from apps.tickets.search_cache import (
    invalidate_ticket_search_cache,
)


class ReservationService:
    @staticmethod
    def get_available_seats(ticket_category_id):
        return ReservationRepository.get_available_seats(ticket_category_id=ticket_category_id)

    @staticmethod
    def create_reservation(user_id, validated_data):
        ticket_category_id = validated_data["ticket_category_id"]
        inventory_id = validated_data["inventory_id"]
        ttl_minutes = getattr(settings, "RESERVATION_TTL_MINUTES", 10)
        expires_at = (timezone.now() + timedelta(minutes=ttl_minutes))
        reserve_key = uuid.uuid4().hex
        with transaction.atomic():
            ReservationRepository.cleanup_expired_reservations()
            inventory = ReservationRepository.get_inventory_for_reservation(inventory_id=inventory_id, ticket_category_id=ticket_category_id)
            if inventory is None:
                raise NotFound(
                    "Selected seat or ticket category "
                    "was not found."
                )
            if not inventory["seat_is_active"]:
                raise ValidationError({
                    "inventory_id": (
                        "This seat is inactive."
                    )
                })
            if not inventory["sale_open"]:
                raise ValidationError({
                    "ticket_category_id": (
                        "Ticket sale is not currently open."
                    )
                })
            if not inventory["inventory_available"]:
                raise ReservationConflict()
            reservation = (
                ReservationRepository
                .create_reservation(
                    user_id=user_id,
                    event_id=inventory["event_id"],
                    total_amount=inventory["price"],
                    expires_at=expires_at,
                )
            )
            ReservationRepository.create_reservation_item(
                reservation_id=(
                    reservation["reservation_id"]
                ),
                ticket_category_id=(
                    ticket_category_id
                ),
                price=inventory["price"],
            )
            ReservationRepository.create_reservation_seat(
                reservation_id=(
                    reservation["reservation_id"]
                ),
                inventory_id=inventory_id,
            )
            ReservationRepository.hold_inventory(
                reservation_id=(
                    reservation["reservation_id"]
                ),
                reserve_key=reserve_key,
                held_until=expires_at,
                inventory_id=inventory_id,
            )
            transaction.on_commit(
                invalidate_ticket_search_cache
            )

        return {
            "reservation_id": (
                reservation["reservation_id"]
            ),
            "event_id": inventory["event_id"],

            "ticket_category_id": (
                inventory["ticket_category_id"]
            ),
            "ticket_category_name": (
                inventory["ticket_category_name"]
            ),
            "inventory_id": (
                inventory["inventory_id"]
            ),
            "seat_id": inventory["seat_id"],
            "row_number": inventory["row_number"],
            "seat_number": inventory["seat_number"],
            "status": reservation["status"],
            "price": inventory["price"],
            "reserved_at": (
                reservation["reserved_at"]
            ),
            "expires_at": (
                reservation["expires_at"]
            ),
        }

    @staticmethod
    def get_my_reservations(user_id):
        with transaction.atomic():
            ReservationRepository.cleanup_expired_reservations()
        active_reservations = ReservationRepository.get_active_user_reservations(user_id=user_id)
        history = ReservationRepository.get_user_reservation_history(user_id=user_id)
        return {
            "active": active_reservations,
            "history": history,
        }


class ReservationConflict(APIException):
    status_code = 409
    default_detail = (
        "The selected seat is no longer available."
    )
    default_code = "reservation_conflict"


