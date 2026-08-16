from datetime import date, datetime

from elasticsearch import Elasticsearch

import logging
from django.db import connection
logger = logging.getLogger(__name__)


es = Elasticsearch(
    "http://localhost:9200"
)

INDEX_NAME = "tickets_search"

SEARCH_DOCUMENT_FIELDS = [
    "event_id",
    "event_datetime",
    "event_status",

    "sport_id",
    "sport_name",

    "league_id",
    "league_name",
    "league_season",

    "venue_id",
    "venue_name",
    "venue_address",
    "venue_capacity",

    "city_id",
    "city_name",

    "province_id",
    "province_name",

    "country_id",
    "country_name",
    "country_iso_code",

    "home_team_id",
    "home_team_name",
    "home_team_logo_url",

    "away_team_id",
    "away_team_name",
    "away_team_logo_url",

    "ticket_category_id",
    "ticket_category_name",

    "current_price",

    "sales_start_at",
    "sales_end_at",

    "section_id",
    "section_name",
    "section_capacity",

    "section_type_id",
    "section_type_name",

    "available_count",
]


def create_index():

    if es.indices.exists(
        index=INDEX_NAME
    ):
        return

    es.indices.create(
        index=INDEX_NAME,
        mappings={
            "properties": {

                "event_id": {
                    "type": "integer"
                },

                "event_datetime": {
                    "type": "date"
                },

                "event_status": {
                    "type": "keyword"
                },

                "sport_id": {
                    "type": "integer"
                },

                "sport_name": {
                    "type": "text"
                },

                "league_id": {
                    "type": "integer"
                },

                "league_name": {
                    "type": "text"
                },

                "league_season": {
                    "type": "keyword"
                },

                "venue_id": {
                    "type": "integer"
                },

                "venue_name": {
                    "type": "text"
                },

                "venue_address": {
                    "type": "text"
                },

                "venue_capacity": {
                    "type": "integer"
                },

                "city_id": {
                    "type": "integer"
                },

                "city_name": {
                    "type": "text"
                },

                "province_id": {
                    "type": "integer"
                },

                "province_name": {
                    "type": "text"
                },

                "country_id": {
                    "type": "integer"
                },

                "country_name": {
                    "type": "text"
                },

                "country_iso_code": {
                    "type": "keyword"
                },

                "home_team_id": {
                    "type": "integer"
                },

                "home_team_name": {
                    "type": "text"
                },

                "home_team_logo_url": {
                    "type": "keyword"
                },

                "away_team_id": {
                    "type": "integer"
                },

                "away_team_name": {
                    "type": "text"
                },

                "away_team_logo_url": {
                    "type": "keyword"
                },

                "ticket_category_id": {
                    "type": "integer"
                },

                "ticket_category_name": {
                    "type": "text"
                },

                "current_price": {
                    "type": "integer"
                },

                "sales_start_at": {
                    "type": "date"
                },

                "sales_end_at": {
                    "type": "date"
                },

                "section_id": {
                    "type": "integer"
                },

                "section_name": {
                    "type": "text"
                },

                "section_capacity": {
                    "type": "integer"
                },

                "section_type_id": {
                    "type": "integer"
                },

                "section_type_name": {
                    "type": "text"
                },

                "available_count": {
                    "type": "integer"
                },
            }
        }
    )


def serialize_value(value):

    if isinstance(
        value,
        (datetime, date),
    ):
        return value.isoformat()

    return value


def build_search_document(data):

    return {
        field: serialize_value(
            data.get(field)
        )
        for field
        in SEARCH_DOCUMENT_FIELDS
    }


def index_ticket_category(
    ticket_data,
    refresh=False,
):

    create_index()

    document = build_search_document(
        ticket_data
    )

    kwargs = {}

    if refresh:
        kwargs["refresh"] = "wait_for"

    return es.index(
        index=INDEX_NAME,

        id=str(
            document[
                "ticket_category_id"
            ]
        ),

        document=document,

        **kwargs,
    )


def delete_ticket_category_from_es(
    ticket_category_id,
):

    if not es.indices.exists(
        index=INDEX_NAME
    ):
        return

    document_id = str(
        ticket_category_id
    )

    if es.exists(
        index=INDEX_NAME,
        id=document_id,
    ):
        es.delete(
            index=INDEX_NAME,
            id=document_id,
            refresh="wait_for",
        )


def sync_ticket_category(
    ticket_category_id,
):

    # Local import avoids import cycle.
    from apps.tickets.repositories import (
        TicketRepository,
    )

    ticket = (
        TicketRepository
        .get_ticket_details(
            ticket_category_id=(
                ticket_category_id
            )
        )
    )

    if ticket is None:
        delete_ticket_category_from_es(
            ticket_category_id
        )
        return

    if (
        not ticket["is_sale_open"]
        or ticket["available_count"] <= 0
    ):
        delete_ticket_category_from_es(
            ticket_category_id
        )
        return

    index_ticket_category(
        ticket,
        refresh=True,
    )


def safe_sync_ticket_category(
    ticket_category_id,
):
    try:
        sync_ticket_category(
            ticket_category_id
        )

    except Exception:
        logger.exception(
            "Failed to sync ticket category "
            "%s with Elasticsearch.",
            ticket_category_id,
        )


def safe_sync_ticket_categories(
    ticket_category_ids,
):
    unique_ids = set(
        ticket_category_ids
    )

    for ticket_category_id in unique_ids:

        if ticket_category_id is None:
            continue

        safe_sync_ticket_category(
            ticket_category_id
        )


def get_expired_category_ids():

    with connection.cursor() as cursor:

        cursor.execute(
            """
            SELECT DISTINCT
                catid

            FROM seatinventory

            WHERE
                LOWER(
                    COALESCE(
                        status,
                        ''
                    )
                ) = 'held'

                AND held_until IS NOT NULL

                AND held_until <= NOW();
            """
        )

        return [
            row[0]
            for row in cursor.fetchall()
        ]


def recreate_index():

    if es.indices.exists(
        index=INDEX_NAME
    ):
        es.indices.delete(
            index=INDEX_NAME
        )

    create_index()


def get_category_ids_by_reservation(
    reservation_id,
):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT DISTINCT
                si.catid
                    AS ticket_category_id

            FROM reservation_seat AS rs

            INNER JOIN seatinventory AS si
                ON si.invid = rs.inventory_id

            WHERE
                rs.reservation_id = %s;
            """,
            [reservation_id],
        )

        return [
            row[0]
            for row in cursor.fetchall()
        ]


def get_category_id_by_inventory(
    inventory_id,
):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                catid

            FROM seatinventory

            WHERE
                invid = %s

            LIMIT 1;
            """,
            [inventory_id],
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return row[0]


def get_category_id_by_ticket(
    ticket_id,
):
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
                si.catid

            FROM ticket AS t

            INNER JOIN seatinventory AS si
                ON si.invid = t.invid

            WHERE
                t.tid = %s

            LIMIT 1;
            """,
            [ticket_id],
        )

        row = cursor.fetchone()

        if row is None:
            return None

        return row[0]


def safe_sync_ticket_category(
    ticket_category_id,
):
    try:
        sync_ticket_category(
            ticket_category_id
        )

    except Exception:
        logger.exception(
            "Elasticsearch sync failed "
            "for ticket category %s.",
            ticket_category_id,
        )


def safe_sync_ticket_categories(
    ticket_category_ids,
):
    unique_ids = set(
        ticket_category_ids
    )

    for ticket_category_id in unique_ids:

        if ticket_category_id is None:
            continue

        safe_sync_ticket_category(
            ticket_category_id
        )


def safe_sync_by_reservation(
    reservation_id,
):
    try:
        category_ids = (
            get_category_ids_by_reservation(
                reservation_id
            )
        )

        safe_sync_ticket_categories(
            category_ids
        )

    except Exception:
        logger.exception(
            "Elasticsearch sync failed "
            "for reservation %s.",
            reservation_id,
        )


def safe_sync_by_inventory(
    inventory_id,
):
    try:
        ticket_category_id = (
            get_category_id_by_inventory(
                inventory_id
            )
        )

        if ticket_category_id is not None:
            safe_sync_ticket_category(
                ticket_category_id
            )

    except Exception:
        logger.exception(
            "Elasticsearch sync failed "
            "for inventory %s.",
            inventory_id,
        )


def safe_sync_by_ticket(
    ticket_id,
):
    try:
        ticket_category_id = (
            get_category_id_by_ticket(
                ticket_id
            )
        )

        if ticket_category_id is not None:
            safe_sync_ticket_category(
                ticket_category_id
            )

    except Exception:
        logger.exception(
            "Elasticsearch sync failed "
            "for ticket %s.",
            ticket_id,
        )


def get_expired_category_ids():
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT DISTINCT
                catid

            FROM seatinventory

            WHERE
                LOWER(
                    COALESCE(
                        status,
                        ''
                    )
                ) = 'held'

                AND held_until IS NOT NULL

                AND held_until <= NOW();
            """
        )

        return [
            row[0]
            for row in cursor.fetchall()
        ]

def safe_sync_expired_categories(
    category_ids,
):
    safe_sync_ticket_categories(
        category_ids
    )