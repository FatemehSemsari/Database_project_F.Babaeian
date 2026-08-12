from apps.catalog.repositories import CatalogRepository


class CatalogService:

    @staticmethod
    def get_cities(validated_filters):
        province_id = validated_filters.get("province_id")
        country_id = validated_filters.get("country_id")
        search = validated_filters.get("search")
        cities = CatalogRepository.list_cities(province_id=province_id, country_id=country_id, search=search)
        return cities

    @staticmethod
    def get_venues(validated_filters):
        city_id = validated_filters.get("city_id")
        province_id = validated_filters.get("province_id")
        country_id = validated_filters.get("country_id")
        search = validated_filters.get("search")
        venues = CatalogRepository.list_venues(
            city_id=city_id,
            province_id=province_id,
            country_id=country_id,
            search=search,
        )
        return venues

    @staticmethod
    def get_sports(validated_filters):
        search = validated_filters.get("search")
        return CatalogRepository.list_sports(search=search)

    @staticmethod
    def get_leagues(validated_filters):
        sport_id = validated_filters.get("sport_id")
        season = validated_filters.get("season")
        search = validated_filters.get("search")
        return CatalogRepository.list_leagues(
            sport_id=sport_id,
            season=season,
            search=search,
        )

    @staticmethod
    def get_teams(validated_filters):
        city_id = validated_filters.get("city_id")
        sport_id = validated_filters.get("sport_id")
        league_id = validated_filters.get("league_id")
        search = validated_filters.get("search")
        return CatalogRepository.list_teams(
            city_id=city_id,
            sport_id=sport_id,
            league_id=league_id,
            search=search,
        )