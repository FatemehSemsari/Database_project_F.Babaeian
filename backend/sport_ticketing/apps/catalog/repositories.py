from django.db import connection
from apps.catalog import sql


def dict_fetchall(cursor):
    columns = [
        column[0]
        for column in cursor.description
    ]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def normalize_search(search):
    if search is None:
        return None, None
    search = str(search).strip()
    if not search:
        return None, None
    return search, f"%{search}%"


class CatalogRepository:

    @staticmethod
    def list_cities(
        province_id=None,
        country_id=None,
        search=None,
    ):
        search, search_pattern = normalize_search(search)
        parameters = [
            province_id,
            province_id,
            country_id,
            country_id,
            search,
            search_pattern,
        ]
        with connection.cursor() as cursor:
            cursor.execute(
                sql.LIST_CITIES,
                parameters,
            )
            return dict_fetchall(cursor)


    @staticmethod
    def list_venues(
        city_id=None,
        province_id=None,
        country_id=None,
        search=None,
    ):
        search, search_pattern = normalize_search(search)
        parameters = [
            city_id,
            city_id,
            province_id,
            province_id,
            country_id,
            country_id,
            search,
            search_pattern,
            search_pattern,
        ]
        with connection.cursor() as cursor:
            cursor.execute(
                sql.LIST_VENUES,
                parameters,
            )
            return dict_fetchall(cursor)



    @staticmethod
    def list_sports(
        search=None,
    ):
        search, search_pattern = normalize_search(search)
        parameters = [
            search,
            search_pattern,
        ]
        with connection.cursor() as cursor:
            cursor.execute(
                sql.LIST_SPORTS,
                parameters,
            )
            return dict_fetchall(cursor)


    @staticmethod
    def list_leagues(
        sport_id=None,
        season=None,
        search=None,
    ):
        search, search_pattern = normalize_search(search)
        if season is not None:
            season = str(season).strip() or None
        parameters = [
            sport_id,
            sport_id,
            season,
            season,
            search,
            search_pattern,
        ]
        with connection.cursor() as cursor:
            cursor.execute(
                sql.LIST_LEAGUES,
                parameters,
            )
            return dict_fetchall(cursor)


    @staticmethod
    def list_teams(
        city_id=None,
        sport_id=None,
        league_id=None,
        search=None,
    ):
        search, search_pattern = normalize_search(search)
        parameters = [
            city_id,
            city_id,
            sport_id,
            sport_id,
            league_id,
            league_id,
            search,
            search_pattern,
        ]
        with connection.cursor() as cursor:
            cursor.execute(
                sql.LIST_TEAMS,
                parameters,
            )
            return dict_fetchall(cursor)