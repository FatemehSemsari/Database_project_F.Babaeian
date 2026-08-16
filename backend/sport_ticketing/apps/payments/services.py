import uuid
from django.db import transaction
from rest_framework.exceptions import (
    APIException,
    NotFound,
)
from apps.payments.repositories import (
    PaymentRepository,
)
from apps.tickets.search_cache import (
    invalidate_ticket_search_cache,
)


class PaymentConflict(APIException):
    status_code = 409
    default_code = "payment_conflict"


class PaymentService:
    @staticmethod
    def pay_reservation(user_id, validated_data):
        reservation_id = validated_data["reservation_id"]
        method = validated_data["method"]
        transaction_ref = uuid.uuid4().hex
        expired = False
        expired_message = None
        with transaction.atomic():
            reservation = PaymentRepository.get_reservation_for_payment(reservation_id=reservation_id, user_id=user_id)
            if reservation is None:
                raise NotFound(
                    "Reservation not found."
                )
            reservation_status = (reservation["status"] or "").lower()
            if reservation_status == "paid":
                raise PaymentConflict(
                    "This reservation has already been paid."
                )
            if reservation_status == "cancelled":
                raise PaymentConflict(
                    "This reservation has been cancelled."
                )
            if reservation_status == "expired":
                raise PaymentConflict(
                    "This reservation has expired."
                )
            if reservation_status != "pending":
                raise PaymentConflict(
                    "This reservation cannot be paid."
                )
            if reservation["is_expired"]:
                PaymentRepository.expire_reservation(reservation_id)
                (
                    PaymentRepository
                    .release_reservation_inventory(
                        reservation_id
                    )
                )
                transaction.on_commit(
                    invalidate_ticket_search_cache
                )
                expired = True
                expired_message = (
                    "Reservation has expired."
                )
            else:
                inventories = PaymentRepository.get_reservation_inventories_for_update(reservation_id)
                if not inventories:
                    raise PaymentConflict(
                        "No reserved seat was found."
                    )
                for inventory in inventories:
                    if not inventory["valid_hold"]:
                        raise PaymentConflict(
                            "One or more reserved seats "
                            "are no longer available."
                        )
                total_amount = int(
                    reservation["total_amount"]
                )
                if method == "wallet":
                    PaymentRepository.ensure_user_wallet(
                        user_id
                    )
                    wallet = (
                        PaymentRepository
                        .get_user_wallet_for_update(
                            user_id
                        )
                    )
                    if wallet is None:
                        raise PaymentConflict(
                            "User wallet could "
                            "not be found."
                        )
                    wallet_balance = int(
                        wallet["balance"]
                    )
                    if wallet_balance < total_amount:
                        raise PaymentConflict(
                            "Insufficient wallet "
                            "balance."
                        )
                    wallet_result = (
                        PaymentRepository
                        .debit_user_wallet(
                            wallet_id=(
                                wallet["wallet_id"]
                            ),
                            amount=total_amount,
                        )
                    )
                    if wallet_result is None:
                        raise PaymentConflict(
                            "Wallet payment could "
                            "not be completed."
                        )
                payment = (
                    PaymentRepository
                    .create_successful_payment(
                        reservation_id=(
                            reservation_id
                        ),
                        amount=total_amount,
                        method=method,
                        transaction_ref=(
                            transaction_ref
                        ),
                    )
                )
                paid_reservation = PaymentRepository.mark_reservation_as_paid(reservation_id)
                (
                    PaymentRepository
                    .mark_inventory_as_sold(
                        reservation_id
                    )
                )
                tickets = PaymentRepository.issue_tickets(reservation_id)
                transaction.on_commit(invalidate_ticket_search_cache)
        if expired:
            raise PaymentConflict(
                expired_message
            )
        return {
            **payment,
            "reservation_status": (
                paid_reservation[
                    "reservation_status"
                ]
            ),
            "tickets": tickets,
        }