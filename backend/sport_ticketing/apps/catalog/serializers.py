from rest_framework import serializers



class CityListQuerySerializer(serializers.Serializer):
    province_id = serializers.IntegerField(required=False, min_value=1)
    country_id = serializers.IntegerField(required=False, min_value=1)
    search = serializers.CharField(required=False, allow_blank=False, max_length=100, trim_whitespace=True)


class CityResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    province_id = serializers.IntegerField(allow_null=True)
    province_name = serializers.CharField(allow_null=True, allow_blank=True)
    country_id = serializers.IntegerField(allow_null=True)
    country_name = serializers.CharField(allow_null=True, allow_blank=True)
    country_iso_code = serializers.CharField(allow_null=True, allow_blank=True)


class VenueListQuerySerializer(serializers.Serializer):
    city_id = serializers.IntegerField(required=False, min_value=1)
    province_id = serializers.IntegerField(required=False, min_value=1)
    country_id = serializers.IntegerField(required=False, min_value=1)
    search = serializers.CharField(required=False, allow_blank=False, max_length=150, trim_whitespace=True)


class VenueResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    address = serializers.CharField(allow_null=True, allow_blank=True)
    capacity = serializers.IntegerField(allow_null=True)
    city_id = serializers.IntegerField(allow_null=True)
    city_name = serializers.CharField(allow_null=True, allow_blank=True)
    province_id = serializers.IntegerField(allow_null=True)
    province_name = serializers.CharField(allow_null=True, allow_blank=True)
    country_id = serializers.IntegerField(allow_null=True)
    country_name = serializers.CharField(allow_null=True, allow_blank=True)
    country_iso_code = serializers.CharField(allow_null=True, allow_blank=True)


class SportListQuerySerializer(serializers.Serializer):
    search = serializers.CharField(required=False, allow_blank=False, max_length=100, trim_whitespace=True)


class SportResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()


class LeagueListQuerySerializer(serializers.Serializer):
    sport_id = serializers.IntegerField(required=False, min_value=1)
    season = serializers.CharField(required=False, allow_blank=False, max_length=30, trim_whitespace=True)
    search = serializers.CharField(required=False, allow_blank=False, max_length=150, trim_whitespace=True)


class LeagueResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    season = serializers.CharField(allow_null=True, allow_blank=True)
    start_date = serializers.DateField(allow_null=True)
    end_date = serializers.DateField(allow_null=True)
    sport_id = serializers.IntegerField(allow_null=True)
    sport_name = serializers.CharField(allow_null=True, allow_blank=True)



class TeamListQuerySerializer(serializers.Serializer):
    city_id = serializers.IntegerField(required=False, min_value=1)
    sport_id = serializers.IntegerField(required=False, min_value=1)
    league_id = serializers.IntegerField(required=False, min_value=1)
    search = serializers.CharField(required=False, allow_blank=False, max_length=150, trim_whitespace=True)


class TeamResponseSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    name = serializers.CharField()
    logo_url = serializers.CharField(allow_null=True, allow_blank=True)
    sport_id = serializers.IntegerField(allow_null=True)
    sport_name = serializers.CharField(allow_null=True, allow_blank=True)
    city_id = serializers.IntegerField(allow_null=True)
    city_name = serializers.CharField(allow_null=True, allow_blank=True)
    province_id = serializers.IntegerField(allow_null=True)
    province_name = serializers.CharField(allow_null=True, allow_blank=True)
    country_id = serializers.IntegerField(allow_null=True)
    country_name = serializers.CharField(allow_null=True, allow_blank=True)
    country_iso_code = serializers.CharField(allow_null=True, allow_blank=True)