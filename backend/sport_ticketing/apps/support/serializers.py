from rest_framework import serializers


class PaginationQuerySerializer(serializers.Serializer):
    limit = serializers.IntegerField(
        required=False,
        default=50,
        min_value=1,
        max_value=100,
    )
    offset = serializers.IntegerField(
        required=False,
        default=0,
        min_value=0,
    )


class ReportListQuerySerializer(PaginationQuerySerializer):
    status = serializers.ChoiceField(
        required=False,
        choices=[
            "pending",
            "in_review",
            "resolved",
            "rejected",
        ],
    )
    issue_type = serializers.CharField(
        required=False,
        max_length=100,
    )


class ReservationListQuerySerializer(PaginationQuerySerializer):
    reservation_status = serializers.ChoiceField(
        required=False,
        choices=[
            "pending",
            "paid",
            "expired",
            "cancelled",
        ],
    )
    support_review_status = serializers.ChoiceField(
        required=False,
        choices=[
            "unreviewed",
            "approved",
            "modified",
            "cancelled",
        ],
    )


class CancelledTicketSerializer(serializers.Serializer):
    ticket_id = serializers.IntegerField()
    serial_number = serializers.IntegerField()
    ticket_status = serializers.CharField()
    issued_at = serializers.DateTimeField(allow_null=True)
    reservation_id = serializers.IntegerField()
    reservation_status = serializers.CharField()
    user_id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField(allow_null=True)
    phone = serializers.CharField(allow_null=True)
    event_id = serializers.IntegerField()
    event_datetime = serializers.DateTimeField()
    home_team_name = serializers.CharField()
    away_team_name = serializers.CharField()
    venue_name = serializers.CharField()
    inventory_id = serializers.IntegerField()
    row_number = serializers.CharField(allow_null=True, allow_blank=True)
    seat_number = serializers.IntegerField(allow_null=True)
    section_name = serializers.CharField()


class SuspiciousPaymentSerializer(serializers.Serializer):
    payment_id = serializers.IntegerField()
    reservation_id = serializers.IntegerField()
    amount = serializers.IntegerField()
    reservation_amount = serializers.IntegerField()
    method = serializers.CharField()
    payment_status = serializers.CharField()
    reservation_status = serializers.CharField()
    created_at = serializers.DateTimeField()
    paid_at = serializers.DateTimeField(allow_null=True)
    refund_amount = serializers.IntegerField(allow_null=True)
    refunded_at = serializers.DateTimeField(allow_null=True)
    transaction_ref = serializers.CharField(allow_null=True, allow_blank=True)
    user_id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField(allow_null=True)
    phone = serializers.CharField(allow_null=True)
    suspicion_reasons = serializers.ListField(child=serializers.CharField())


class SupportReportSerializer(serializers.Serializer):
    report_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField(allow_null=True)
    phone = serializers.CharField(allow_null=True)
    ticket_id = serializers.IntegerField(allow_null=True)
    reservation_id = serializers.IntegerField(allow_null=True)
    issue_type = serializers.CharField()
    message = serializers.CharField()
    status = serializers.CharField()
    support_response = serializers.CharField(allow_null=True, allow_blank=True)
    reviewed_by = serializers.IntegerField(allow_null=True)
    reviewed_at = serializers.DateTimeField(allow_null=True)
    reviewer_first_name = serializers.CharField(allow_null=True, allow_blank=True)
    reviewer_last_name = serializers.CharField(allow_null=True, allow_blank=True)


class UpdateReportSerializer(serializers.Serializer):
    status = serializers.ChoiceField(
        required=False,
        choices=[
            "pending",
            "in_review",
            "resolved",
            "rejected",
        ],
    )
    support_response = serializers.CharField(
        required=False,
        max_length=3000,
        allow_blank=False,
    )

    def validate(self, attrs):
        if not attrs:
            raise serializers.ValidationError(
                "At least one field is required."
            )
        return attrs


class SupportReservationSerializer(serializers.Serializer):
    reservation_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    first_name = serializers.CharField()
    last_name = serializers.CharField()
    email = serializers.EmailField(allow_null=True)
    phone = serializers.CharField(allow_null=True)
    event_id = serializers.IntegerField()
    event_datetime = serializers.DateTimeField()
    home_team_name = serializers.CharField()
    away_team_name = serializers.CharField()
    reservation_status = serializers.CharField()
    support_review_status = serializers.CharField()
    support_note = serializers.CharField(allow_null=True, allow_blank=True)
    reserved_at = serializers.DateTimeField()
    expires_at = serializers.DateTimeField(allow_null=True)
    paid_at = serializers.DateTimeField(allow_null=True)
    total_amount = serializers.IntegerField(
        allow_null=True,
    )

    support_reviewed_by = serializers.IntegerField(
        allow_null=True,
    )

    support_reviewed_at = serializers.DateTimeField(
        allow_null=True,
    )

    inventory_id = serializers.IntegerField(
        allow_null=True,
    )

    row_number = serializers.CharField(
        allow_null=True,
        allow_blank=True,
    )

    seat_number = serializers.IntegerField(
        allow_null=True,
    )

    section_name = serializers.CharField(
        allow_null=True,
        allow_blank=True,
    )

    ticket_id = serializers.IntegerField(
        allow_null=True,
    )

    ticket_status = serializers.CharField(
        allow_null=True,
        allow_blank=True,
    )



class UpdateReservationSerializer(
    serializers.Serializer
):
    action = serializers.ChoiceField(
        choices=[
            "approve",
            "cancel",
            "modify",
        ]
    )

    expires_at = serializers.DateTimeField(
        required=False,
    )

    note = serializers.CharField(
        required=False,
        allow_blank=True,
        max_length=2000,
    )

    def validate(self, attrs):
        action = attrs["action"]

        if (
            action == "modify"
            and attrs.get("expires_at") is None
        ):
            raise serializers.ValidationError({
                "expires_at": (
                    "expires_at is required "
                    "for modify action."
                )
            })

        return attrs


class ReservationActionResponseSerializer(
    serializers.Serializer
):
    reservation_id = serializers.IntegerField()

    reservation_status = serializers.CharField()

    support_review_status = serializers.CharField()

    support_note = serializers.CharField(
        allow_null=True,
        allow_blank=True,
    )

    support_reviewed_by = serializers.IntegerField()

    support_reviewed_at = serializers.DateTimeField()

    expires_at = serializers.DateTimeField(
        required=False,
        allow_null=True,
    )



