from rest_framework import serializers


class AvailableSeatsQuerySerializer(serializers.Serializer):
    ticket_category_id = serializers.IntegerField(required=True, min_value=1)


class AvailableSeatSerializer(serializers.Serializer):
    inventory_id = serializers.IntegerField()
    seat_id = serializers.IntegerField()
    row_number = serializers.CharField(allow_null=True, allow_blank=True)
    seat_number = serializers.IntegerField(allow_null=True)
    section_id = serializers.IntegerField()
    section_name = serializers.CharField()
    ticket_category_id = serializers.IntegerField()
    ticket_category_name = serializers.CharField(allow_null=True, allow_blank=True)
    price = serializers.IntegerField()


class CreateReservationSerializer(serializers.Serializer):
    ticket_category_id = serializers.IntegerField(min_value=1)
    inventory_id = serializers.IntegerField(min_value=1)


class ReservationResponseSerializer(serializers.Serializer):
    reservation_id = serializers.IntegerField()
    event_id = serializers.IntegerField()
    ticket_category_id = serializers.IntegerField()
    ticket_category_name = serializers.CharField(allow_null=True, allow_blank=True)
    inventory_id = serializers.IntegerField()
    seat_id = serializers.IntegerField()
    row_number = serializers.CharField(allow_null=True, allow_blank=True)
    seat_number = serializers.IntegerField(allow_null=True)
    status = serializers.CharField()
    price = serializers.IntegerField()
    reserved_at = serializers.DateTimeField()
    expires_at = serializers.DateTimeField()


class ReservationSeatSerializer(serializers.Serializer):
    inventory_id = serializers.IntegerField()
    seat_id = serializers.IntegerField()

    row_number = serializers.CharField(
        allow_null=True,
        allow_blank=True,
    )
    seat_number = serializers.IntegerField(
        allow_null=True,
    )

    section_id = serializers.IntegerField()
    section_name = serializers.CharField()


class UserReservationSerializer(serializers.Serializer):
    reservation_id = serializers.IntegerField()
    event_id = serializers.IntegerField()
    event_datetime = serializers.DateTimeField()
    home_team_name = serializers.CharField()
    away_team_name = serializers.CharField()
    venue_name = serializers.CharField()
    city_name = serializers.CharField(allow_null=True, allow_blank=True)
    ticket_category_id = serializers.IntegerField()
    ticket_category_name = serializers.CharField(allow_null=True, allow_blank=True)
    status = serializers.CharField()
    quantity = serializers.IntegerField()
    price = serializers.IntegerField()
    total_amount = serializers.IntegerField(allow_null=True)
    reserved_at = serializers.DateTimeField()
    expires_at = serializers.DateTimeField(allow_null=True)
    paid_at = serializers.DateTimeField(allow_null=True)
    remaining_seconds = serializers.IntegerField(allow_null=True)
    seats = ReservationSeatSerializer(many=True)


