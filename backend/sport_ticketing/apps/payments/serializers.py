from rest_framework import serializers


class PaymentRequestSerializer(serializers.Serializer):
    reservation_id = serializers.IntegerField(min_value=1)
    method = serializers.ChoiceField(
        choices=[
            "bank_card",
            "wallet",
            "other",
        ]
    )


class IssuedTicketSerializer(serializers.Serializer):
    ticket_id = serializers.IntegerField()
    inventory_id = serializers.IntegerField()
    serial_number = serializers.IntegerField()
    status = serializers.CharField()
    issue_date = serializers.DateTimeField()


class PaymentResponseSerializer(serializers.Serializer):
    payment_id = serializers.IntegerField()
    reservation_id = serializers.IntegerField()
    amount = serializers.IntegerField()
    method = serializers.CharField()
    payment_status = serializers.CharField()
    transaction_ref = serializers.CharField()
    paid_at = serializers.DateTimeField()
    reservation_status = serializers.CharField()
    tickets = IssuedTicketSerializer(many=True)