from rest_framework import serializers


class TicketSearchQuerySerializer(serializers.Serializer):
    sport_id = serializers.IntegerField(
        required=False,
        min_value=1,
    )
    team_id = serializers.IntegerField(
        required=False,
        min_value=1,
    )
    city_id = serializers.IntegerField(
        required=False,
        min_value=1,
    )
    venue_id = serializers.IntegerField(
        required=False,
        min_value=1,
    )
    ticket_category_id = serializers.IntegerField(
        required=False,
        min_value=1,
    )
    date_from = serializers.DateField(
        required=False,
    )
    date_to = serializers.DateField(
        required=False,
    )
    time_from = serializers.TimeField(
        required=False,
    )
    time_to = serializers.TimeField(
        required=False,
    )
    min_price = serializers.IntegerField(
        required=False,
        min_value=0,
    )
    max_price = serializers.IntegerField(
        required=False,
        min_value=0,
    )
    limit = serializers.IntegerField(
        required=False,
        default=20,
        min_value=1,
        max_value=100,
    )
    offset = serializers.IntegerField(
        required=False,
        default=0,
        min_value=0,
    )

    def validate(self, attrs):
        date_from = attrs.get("date_from")
        date_to = attrs.get("date_to")
        if (date_from is not None and date_to is not None and date_from > date_to):
            raise serializers.ValidationError({
                "date_to": (
                    "date_to must be greater than or equal "
                    "to date_from."
                )
            })
        time_from = attrs.get("time_from")
        time_to = attrs.get("time_to")
        if (time_from is not None and time_to is not None and time_from > time_to):
            raise serializers.ValidationError({
                "time_to": (
                    "time_to must be greater than or equal "
                    "to time_from."
                )
            })
        min_price = attrs.get("min_price")
        max_price = attrs.get("max_price")
        if (min_price is not None and max_price is not None and min_price > max_price):
            raise serializers.ValidationError({
                "max_price": (
                    "max_price must be greater than or equal "
                    "to min_price."
                )
            })
        return attrs


class TicketSearchResultSerializer(serializers.Serializer):
    event_id = serializers.IntegerField()
    event_datetime = serializers.DateTimeField()
    event_status = serializers.CharField()
    sport_id = serializers.IntegerField()
    sport_name = serializers.CharField()
    league_id = serializers.IntegerField(allow_null=True)
    league_name = serializers.CharField(allow_null=True, allow_blank=True)
    league_season = serializers.CharField(allow_null=True, allow_blank=True)
    venue_id = serializers.IntegerField()
    venue_name = serializers.CharField()
    venue_address = serializers.CharField(allow_null=True, allow_blank=True)
    venue_capacity = serializers.IntegerField(allow_null=True)
    city_id = serializers.IntegerField(allow_null=True)
    city_name = serializers.CharField(allow_null=True, allow_blank=True)
    province_id = serializers.IntegerField(allow_null=True)
    province_name = serializers.CharField(allow_null=True, allow_blank=True)
    country_id = serializers.IntegerField(allow_null=True)
    country_name = serializers.CharField(allow_null=True, allow_blank=True)
    country_iso_code = serializers.CharField(allow_null=True, allow_blank=True)
    home_team_id = serializers.IntegerField()
    home_team_name = serializers.CharField()
    home_team_logo_url = serializers.CharField(allow_null=True, allow_blank=True)
    away_team_id = serializers.IntegerField()
    away_team_name = serializers.CharField()
    away_team_logo_url = serializers.CharField(allow_null=True, allow_blank=True)
    ticket_category_id = serializers.IntegerField()
    ticket_category_name = serializers.CharField(allow_null=True, allow_blank=True)
    current_price = serializers.IntegerField()
    sales_start_at = serializers.DateTimeField(allow_null=True)
    sales_end_at = serializers.DateTimeField(allow_null=True)
    section_id = serializers.IntegerField()
    section_name = serializers.CharField()
    section_capacity = serializers.IntegerField()
    section_type_id = serializers.IntegerField(allow_null=True)
    section_type_name = serializers.CharField(allow_null=True, allow_blank=True)
    available_count = serializers.IntegerField()


class AmenitySerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class TicketDetailSerializer(serializers.Serializer):
    event_id = serializers.IntegerField()
    event_datetime = serializers.DateTimeField()
    event_status = serializers.CharField(allow_null=True, allow_blank=True)
    event_notes = serializers.CharField(allow_null=True, allow_blank=True)
    home_score = serializers.IntegerField()
    away_score = serializers.IntegerField()
    sport_id = serializers.IntegerField()
    sport_name = serializers.CharField()
    league_id = serializers.IntegerField(allow_null=True)
    league_name = serializers.CharField(allow_null=True, allow_blank=True)
    league_season = serializers.CharField(allow_null=True, allow_blank=True)
    league_start_date = serializers.DateField(allow_null=True)
    league_end_date = serializers.DateField(allow_null=True)
    venue_id = serializers.IntegerField()
    venue_name = serializers.CharField()
    venue_address = serializers.CharField(allow_null=True, allow_blank=True)
    venue_capacity = serializers.IntegerField(allow_null=True)
    city_id = serializers.IntegerField(allow_null=True)
    city_name = serializers.CharField(allow_null=True, allow_blank=True)
    province_id = serializers.IntegerField(allow_null=True)
    province_name = serializers.CharField(allow_null=True, allow_blank=True)
    country_id = serializers.IntegerField(allow_null=True)
    country_name = serializers.CharField(allow_null=True, allow_blank=True)
    country_iso_code = serializers.CharField(allow_null=True, allow_blank=True)
    home_team_id = serializers.IntegerField()
    home_team_name = serializers.CharField()
    home_team_logo_url = serializers.CharField(allow_null=True, allow_blank=True)
    away_team_id = serializers.IntegerField()
    away_team_name = serializers.CharField()
    away_team_logo_url = serializers.CharField(allow_null=True, allow_blank=True)
    ticket_category_id = serializers.IntegerField()
    ticket_category_name = serializers.CharField(allow_null=True, allow_blank=True)
    current_price = serializers.IntegerField()
    sales_start_at = serializers.DateTimeField(allow_null=True)
    sales_end_at = serializers.DateTimeField(allow_null=True)
    section_id = serializers.IntegerField()
    section_name = serializers.CharField()
    section_capacity = serializers.IntegerField()
    section_type_id = serializers.IntegerField(allow_null=True)
    section_type_name = serializers.CharField(allow_null=True, allow_blank=True)
    available_count = serializers.IntegerField()
    cancel_until = serializers.DateTimeField(allow_null=True)
    refund_percent = serializers.IntegerField(allow_null=True)
    policy_notes = serializers.CharField(allow_null=True, allow_blank=True)
    is_sale_open = serializers.BooleanField()
    is_available = serializers.BooleanField()
    amenities = AmenitySerializer(many=True)