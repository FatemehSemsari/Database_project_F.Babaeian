from apps.tickets.repositories import TicketRepository
from apps.tickets.search_cache import (
    cache_ticket_search,
    get_cached_ticket_search,
    invalidate_ticket_search_cache
)
from django.db import transaction
from rest_framework.exceptions import (
    APIException,
    NotFound,
)
from apps.tickets.search_api import (
    search_tickets as elastic_search_tickets,
)
from apps.tickets.elastic_sync import (
    safe_sync_by_ticket,
)


class CancellationConflict(APIException):
    status_code = 409
    default_code = "cancellation_conflict"



class TicketService:

    @staticmethod
    def search_tickets(validated_filters):
        cached_results = get_cached_ticket_search(
            validated_filters
        )
        if cached_results is not None:
            return {
                "results": cached_results,
                "cached": True,
            }
        results = TicketRepository.search_tickets(filters=validated_filters)
        cache_ticket_search(filters=validated_filters, results=results)
        return {
            "results": results,
            "cached": False,
        }

    @staticmethod
    def get_ticket_details(ticket_category_id):
        return TicketRepository.get_ticket_details(ticket_category_id=ticket_category_id)


    @staticmethod
    def get_user_bookings(user_id):
        bookings = TicketRepository.get_user_bookings(user_id=user_id)
        grouped = {
            "upcoming": [],
            "cancelled": [],
            "used": [],
            "past": [],
        }
        for booking in bookings:
            state = booking["booking_state"]
            if state in grouped:
                grouped[state].append(booking)
        return grouped

    @staticmethod
    def get_cancellation_info(ticket_id, user_id):
        info = (
            TicketRepository
            .get_ticket_cancellation_info(
                ticket_id=ticket_id,
                user_id=user_id,
            )
        )
        if info is None:
            raise NotFound(
                "Ticket not found."
            )
        ticket_status = (
                info["ticket_status"] or ""
        ).lower()
        reservation_status = (
                info["reservation_status"] or ""
        ).lower()
        can_cancel = True
        reason = None
        refund_percent = info["refund_percent"]
        if ticket_status == "cancelled":
            can_cancel = False
            reason = (
                "Ticket has already been cancelled."
            )
        elif info["is_used"]:
            can_cancel = False
            reason = (
                "A used ticket cannot be cancelled."
            )
        elif reservation_status != "paid":
            can_cancel = False
            reason = (
                "Only paid tickets can be cancelled."
            )
        elif info["event_started"]:
            can_cancel = False
            reason = (
                "The event has already started."
            )
        elif info["rule_id"] is None:
            can_cancel = False
            reason = (
                "No cancellation rule matches "
                "this ticket."
            )
        elif not info["rule_can_cancel"]:
            can_cancel = False
            reason = (
                "Cancellation is not allowed "
                "at this time according to "
                "the organizer policy."
            )
        purchase_price = info["purchase_price"]
        penalty_percent = None
        refund_amount = None
        penalty_amount = None
        if (purchase_price is not None and refund_percent is not None):
            penalty_percent = (
                    100 - refund_percent
            )
            refund_amount = (
                    purchase_price
                    * refund_percent
                    // 100
            )
            penalty_amount = (
                    purchase_price
                    - refund_amount
            )
        return {
            "ticket_id": info["ticket_id"],
            "reservation_id": (
                info["reservation_id"]
            ),
            "event_id": info["event_id"],
            "event_datetime": (
                info["event_datetime"]
            ),
            "organizer_id": (
                info["organizer_id"]
            ),
            "organizer_name": (
                info["organizer_name"]
            ),
            "ticket_category_id": (
                info["ticket_category_id"]
            ),
            "ticket_category_name": (
                info["ticket_category_name"]
            ),
            "ticket_status": (
                info["ticket_status"]
            ),
            "reservation_status": (
                info["reservation_status"]
            ),
            "purchase_price": purchase_price,
            "remaining_hours": (
                info["remaining_hours"]
            ),
            "can_cancel": can_cancel,
            "rule_id": info["rule_id"],
            "min_hours_before_event": (
                info[
                    "min_hours_before_event"
                ]
            ),
            "max_hours_before_event": (
                info[
                    "max_hours_before_event"
                ]
            ),
            "refund_percent": refund_percent,
            "penalty_percent": penalty_percent,
            "refund_amount": refund_amount,
            "penalty_amount": penalty_amount,
            "policy_notes": (
                info["rule_notes"]
            ),
            "reason": reason,
        }

    @staticmethod
    def cancel_user_ticket(ticket_id, user_id):
        with transaction.atomic():
            ticket = (
                TicketRepository
                .get_ticket_for_cancellation(
                    ticket_id=ticket_id,
                    user_id=user_id,
                )
            )
            if ticket is None:
                raise NotFound(
                    "Ticket not found."
                )
            ticket_status = (
                    ticket["ticket_status"] or ""
            ).lower()
            reservation_status = (
                    ticket["reservation_status"] or ""
            ).lower()
            inventory_status = (
                    ticket["inventory_status"] or ""
            ).lower()

            if ticket_status == "cancelled":
                raise CancellationConflict(
                    "Ticket has already been cancelled."
                )
            if ticket_status != "valid":
                raise CancellationConflict(
                    "This ticket cannot be cancelled."
                )
            if ticket["is_used"]:
                raise CancellationConflict(
                    "A used ticket cannot be cancelled."
                )
            if reservation_status != "paid":
                raise CancellationConflict(
                    "Only a paid reservation can "
                    "be cancelled."
                )
            if inventory_status != "sold":
                raise CancellationConflict(
                    "The ticket seat is not in "
                    "sold state."
                )
            if ticket["event_started"]:
                raise CancellationConflict(
                    "The event has already started."
                )


            rule = (
                TicketRepository
                .get_cancellation_rule(
                    event_id=ticket["event_id"]
                )
            )
            if rule is None:
                raise CancellationConflict(
                    "No cancellation rule matches "
                    "this ticket."
                )
            if not rule["can_cancel"]:
                raise CancellationConflict(
                    "Cancellation is not allowed "
                    "at this time according to "
                    "the organizer policy."
                )


            purchase_price = (
                ticket["purchase_price"]
            )
            if purchase_price is None:
                raise CancellationConflict(
                    "Ticket purchase price "
                    "could not be determined."
                )
            refund_percent = int(
                rule["refund_percent"]
            )
            penalty_percent = (
                    100 - refund_percent
            )
            refund_amount = (
                    purchase_price
                    * refund_percent
                    // 100
            )
            penalty_amount = (
                    purchase_price
                    - refund_amount
            )
            payment = (
                TicketRepository
                .get_successful_payment_for_update(
                    reservation_id=(
                        ticket["reservation_id"]
                    )
                )
            )
            if payment is None:
                raise CancellationConflict(
                    "Successful payment was not found."
                )


            TicketRepository.ensure_user_wallet(
                user_id=user_id
            )
            wallet = (
                TicketRepository
                .get_user_wallet_for_update(
                    user_id=user_id
                )
            )
            if wallet is None:
                raise CancellationConflict(
                    "User wallet could not be created."
                )


            wallet_result = (
                TicketRepository.credit_wallet(
                    wallet_id=wallet["wallet_id"],
                    amount=refund_amount,
                )
            )


            cancelled_ticket = (
                TicketRepository.cancel_ticket(
                    ticket_id=ticket_id
                )
            )


            released_inventory = (
                TicketRepository
                .release_cancelled_inventory(
                    inventory_id=(
                        ticket["inventory_id"]
                    )
                )
            )
            if released_inventory is None:
                raise CancellationConflict(
                    "Seat inventory could not "
                    "be released."
                )


            cancelled_reservation = (
                TicketRepository
                .cancel_reservation(
                    reservation_id=(
                        ticket["reservation_id"]
                    )
                )
            )

            refunded_payment = (
                TicketRepository
                .mark_payment_as_refunded(
                    payment_id=(
                        payment["payment_id"]
                    ),
                    refund_amount=refund_amount,
                )
            )

            transaction.on_commit(
                lambda tid=ticket_id:
                safe_sync_by_ticket(
                    tid
                )
            )

            transaction.on_commit(
                invalidate_ticket_search_cache
            )

        return {
            "ticket_id": (
                cancelled_ticket["ticket_id"]
            ),
            "ticket_status": (
                cancelled_ticket["ticket_status"]
            ),
            "reservation_id": (
                cancelled_reservation[
                    "reservation_id"
                ]
            ),
            "reservation_status": (
                cancelled_reservation[
                    "reservation_status"
                ]
            ),
            "payment_id": (
                refunded_payment["payment_id"]
            ),
            "payment_status": (
                refunded_payment["payment_status"]
            ),
            "purchase_price": purchase_price,
            "refund_percent": refund_percent,
            "penalty_percent": penalty_percent,
            "refund_amount": refund_amount,
            "penalty_amount": penalty_amount,
            "wallet_id": (
                wallet_result["wallet_id"]
            ),
            "wallet_balance": (
                wallet_result["wallet_balance"]
            ),
            "refunded_at": (
                refunded_payment["refunded_at"]
            ),
        }


    @staticmethod
    def advanced_search_tickets(validated_filters):
        return elastic_search_tickets(validated_filters)
