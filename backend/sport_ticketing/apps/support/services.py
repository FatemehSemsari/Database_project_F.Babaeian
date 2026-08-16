from django.db import transaction
from django.utils import timezone

from rest_framework.exceptions import (
    APIException,
    NotFound,
)

from apps.support.repositories import (
    SupportRepository,
)

from apps.tickets.search_cache import (
    invalidate_ticket_search_cache,
)
from apps.tickets.elastic_sync import (
    safe_sync_by_reservation,
)


class SupportConflict(APIException):
    status_code = 409
    default_code = "support_conflict"


class SupportService:

    @staticmethod
    def get_cancelled_tickets(
        validated_filters,
    ):
        return (
            SupportRepository
            .list_cancelled_tickets(
                limit=validated_filters["limit"],
                offset=validated_filters["offset"],
            )
        )

    @staticmethod
    def get_suspicious_payments(
        validated_filters,
    ):
        return (
            SupportRepository
            .list_suspicious_payments(
                limit=validated_filters["limit"],
                offset=validated_filters["offset"],
            )
        )

    @staticmethod
    def get_reports(
        validated_filters,
    ):
        return SupportRepository.list_reports(
            status=validated_filters.get(
                "status"
            ),
            issue_type=validated_filters.get(
                "issue_type"
            ),
            limit=validated_filters["limit"],
            offset=validated_filters["offset"],
        )

    @staticmethod
    def update_report(
        report_id,
        support_user_id,
        validated_data,
    ):
        report = (
            SupportRepository.update_report(
                report_id=report_id,

                support_user_id=(
                    support_user_id
                ),

                status=validated_data.get(
                    "status"
                ),

                support_response=(
                    validated_data.get(
                        "support_response"
                    )
                ),
            )
        )

        if report is None:
            raise NotFound(
                "Report not found."
            )

        return report

    @staticmethod
    def get_reservations(
        validated_filters,
    ):
        return (
            SupportRepository
            .list_reservations(
                reservation_status=(
                    validated_filters.get(
                        "reservation_status"
                    )
                ),

                support_review_status=(
                    validated_filters.get(
                        "support_review_status"
                    )
                ),

                limit=validated_filters["limit"],

                offset=validated_filters["offset"],
            )
        )

    @staticmethod
    def update_reservation(
        reservation_id,
        support_user_id,
        validated_data,
    ):
        action = validated_data["action"]

        note = validated_data.get(
            "note"
        )

        with transaction.atomic():

            reservation = (
                SupportRepository
                .get_reservation_for_update(
                    reservation_id
                )
            )

            if reservation is None:
                raise NotFound(
                    "Reservation not found."
                )



            reserved_at = reservation.get(
                "reserved_at"
            )

            expires_at = reservation.get(
                "expires_at"
            )



            if (
                reserved_at is not None
                and timezone.is_naive(
                    reserved_at
                )
            ):
                reserved_at = (
                    timezone.make_aware(
                        reserved_at,
                        timezone.get_current_timezone(),
                    )
                )

            if (
                expires_at is not None
                and timezone.is_naive(
                    expires_at
                )
            ):
                expires_at = (
                    timezone.make_aware(
                        expires_at,
                        timezone.get_current_timezone(),
                    )
                )

            current_status = (
                reservation[
                    "reservation_status"
                ] or ""
            ).lower()

            # =====================================
            # APPROVE
            # =====================================

            if action == "approve":

                if current_status != "pending":
                    raise SupportConflict(
                        "Only pending reservations "
                        "can be approved by support."
                    )

                if (
                    expires_at is not None
                    and expires_at
                    <= timezone.now()
                ):
                    raise SupportConflict(
                        "Expired reservation "
                        "cannot be approved."
                    )

                result = (
                    SupportRepository
                    .approve_reservation(
                        reservation_id=(
                            reservation_id
                        ),
                        support_user_id=(
                            support_user_id
                        ),
                        note=note,
                    )
                )

                return result

            # =====================================
            # MODIFY
            # =====================================

            if action == "modify":

                if current_status != "pending":
                    raise SupportConflict(
                        "Only pending reservations "
                        "can be modified."
                    )

                new_expires_at = (
                    validated_data[
                        "expires_at"
                    ]
                )


                if timezone.is_naive(
                    new_expires_at
                ):
                    new_expires_at = (
                        timezone.make_aware(
                            new_expires_at,
                            timezone.get_current_timezone(),
                        )
                    )

                if (
                    new_expires_at
                    <= timezone.now()
                ):
                    raise SupportConflict(
                        "New expiration time must "
                        "be in the future."
                    )

                if (
                    reserved_at is not None
                    and new_expires_at
                    < reserved_at
                ):
                    raise SupportConflict(
                        "Expiration time cannot "
                        "be before reserved_at."
                    )

                result = (
                    SupportRepository
                    .modify_reservation_expiry(
                        reservation_id=(
                            reservation_id
                        ),

                        expires_at=(
                            new_expires_at
                        ),

                        support_user_id=(
                            support_user_id
                        ),

                        note=note,
                    )
                )

                (
                    SupportRepository
                    .sync_inventory_expiry(
                        reservation_id=(
                            reservation_id
                        ),
                        expires_at=(
                            new_expires_at
                        ),
                    )
                )

                transaction.on_commit(
                    invalidate_ticket_search_cache
                )

                return result

            # =====================================
            # CANCEL
            # =====================================

            if action == "cancel":

                if current_status != "pending":
                    raise SupportConflict(
                        "Support can directly "
                        "cancel only pending "
                        "reservations."
                    )

                result = (
                    SupportRepository
                    .cancel_reservation(
                        reservation_id=(
                            reservation_id
                        ),

                        support_user_id=(
                            support_user_id
                        ),

                        note=note,
                    )
                )

                (
                    SupportRepository
                    .release_cancelled_reservation(
                        reservation_id
                    )
                )
                transaction.on_commit(
                    lambda rid=reservation_id:
                    safe_sync_by_reservation(
                        rid
                    )
                )

                transaction.on_commit(
                    invalidate_ticket_search_cache
                )

                return result

        raise SupportConflict(
            "Invalid support action."
        )