from rest_framework import serializers


class CreateReportSerializer(serializers.Serializer):
    ticket_id = serializers.IntegerField(required=False, min_value=1)
    reservation_id = serializers.IntegerField(required=False, min_value=1)
    issue_type = serializers.ChoiceField(
        choices=[
            "purchase_problem",
            "payment_problem",
            "ticket_information",
            "pricing_problem",
            "seat_problem",
            "venue_problem",
            "event_time_change",
            "unexpected_cancellation",
            "other",
        ]
    )
    message = serializers.CharField(min_length=5, max_length=2000, trim_whitespace=True)


    def validate(self, attrs):
        ticket_id = attrs.get("ticket_id")
        reservation_id = attrs.get("reservation_id")
        if (ticket_id is None and reservation_id is None):
            raise serializers.ValidationError(
                {
                    "detail": (
                        "ticket_id or reservation_id "
                        "is required."
                    )
                }
            )
        return attrs


class ReportResponseSerializer(serializers.Serializer):
    report_id = serializers.IntegerField()
    user_id = serializers.IntegerField()
    ticket_id = serializers.IntegerField(allow_null=True)
    reservation_id = serializers.IntegerField(allow_null=True)
    issue_type = serializers.CharField()
    message = serializers.CharField()
    status = serializers.CharField()