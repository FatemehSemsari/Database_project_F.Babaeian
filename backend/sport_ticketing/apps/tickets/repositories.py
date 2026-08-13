from django.db import connection
from apps.tickets import sql


def dict_fetchall(cursor):
    columns = [
        column[0]
        for column in cursor.description
    ]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


def dict_fetchone(cursor):
    row = cursor.fetchone()
    if row is None:
        return None
    columns = [
        column[0]
        for column in cursor.description
    ]
    return dict(zip(columns, row))


class TicketRepository:

    @staticmethod
    def search_tickets(filters):
        query = sql.SEARCH_TICKETS_BASE
        parameters = []

        # -------------------------------------------------
        # Sport filter
        # -------------------------------------------------

        sport_id = filters.get("sport_id")
        if sport_id is not None:
            query += """
                AND e.sportid = %s
            """
            parameters.append(sport_id)

        # -------------------------------------------------
        # Team filter
        # -------------------------------------------------

        team_id = filters.get("team_id")
        if team_id is not None:
            query += """
                AND (
                    e.hometeam = %s
                    OR e.awayteam = %s
                )
            """
            parameters.extend([
                team_id,
                team_id,
            ])

        # -------------------------------------------------
        # City filter
        # -------------------------------------------------

        city_id = filters.get("city_id")
        if city_id is not None:
            query += """
                AND v.cityid = %s
            """
            parameters.append(city_id)

        # -------------------------------------------------
        # Venue filter
        # -------------------------------------------------

        venue_id = filters.get("venue_id")
        if venue_id is not None:
            query += """
                AND e.venueid = %s
            """
            parameters.append(venue_id)

        # -------------------------------------------------
        # Ticket category filter
        # -------------------------------------------------

        ticket_category_id = filters.get(
            "ticket_category_id"
        )
        if ticket_category_id is not None:
            query += """
                AND tc.catid = %s
            """
            parameters.append(
                ticket_category_id
            )

        # -------------------------------------------------
        # Date filters
        # -------------------------------------------------

        date_from = filters.get("date_from")
        if date_from is not None:
            query += """
                AND e.eventdate::DATE >= %s
            """
            parameters.append(date_from)
        date_to = filters.get("date_to")
        if date_to is not None:
            query += """
                AND e.eventdate::DATE <= %s
            """
            parameters.append(date_to)

        # -------------------------------------------------
        # Time filters
        # -------------------------------------------------

        time_from = filters.get("time_from")
        if time_from is not None:
            query += """
                AND e.eventdate::TIME >= %s
            """
            parameters.append(time_from)
        time_to = filters.get("time_to")
        if time_to is not None:
            query += """
                AND e.eventdate::TIME <= %s
            """
            parameters.append(time_to)

        # -------------------------------------------------
        # Price filters
        # -------------------------------------------------

        min_price = filters.get("min_price")
        if min_price is not None:
            query += """
                AND tc.price >= %s
            """
            parameters.append(min_price)
        max_price = filters.get("max_price")
        if max_price is not None:
            query += """
                AND tc.price <= %s
            """
            parameters.append(max_price)

        # -------------------------------------------------
        # Pagination
        # -------------------------------------------------

        query += sql.SEARCH_TICKETS_ORDER_AND_PAGINATION
        limit = filters.get(
            "limit",
            20,
        )
        offset = filters.get(
            "offset",
            0,
        )
        parameters.extend([
            limit,
            offset,
        ])

        # -------------------------------------------------
        # Execute
        # -------------------------------------------------

        with connection.cursor() as cursor:
            cursor.execute(
                query,
                parameters,
            )
            return dict_fetchall(cursor)

    # =====================================================
    # Ticket category details
    # =====================================================

    @staticmethod
    def get_ticket_details(
        ticket_category_id,
    ):
        with connection.cursor() as cursor:
            cursor.execute(
                sql.GET_TICKET_DETAILS,
                [
                    ticket_category_id,
                ],
            )
            return dict_fetchone(cursor)